import streamlit as st
import torch
import re
import time
import torch.nn.functional as F
from transformers import BertTokenizer, BertForSequenceClassification
from transformers_interpret import SequenceClassificationExplainer
from pathlib import Path

# --- 1. KONFIGURACJA STRONY ---
st.set_page_config(
    page_title="System Weryfikacji Treści",
    page_icon="📄",
    layout="wide" # Szeroki układ dla lepszej czytelności wykresów
)

# Style CSS (usunięcie zbędnych odstępów, czytelna czcionka)
st.markdown("""
    <style>
        .block-container { padding-top: 2rem; }
        h1 { font-size: 2.2rem; }
        .stAlert { padding: 0.5rem; }
        .highlight-text { line-height: 1.6; font-family: monospace; font-size: 14px; }
    </style>
""", unsafe_allow_html=True)

st.title("System Klasyfikacji Wiarygodności Artykułów")
st.markdown("Narzędzie wykorzystuje architekturę **BERT** do oceny wiarygodności tekstu oraz **Explainable AI** do analizy wpływu poszczególnych tokenów na decyzję modelu.")
st.divider()

# --- 2. LOGIKA BACKENDU ---

def clean_text_standard(text):
    """Standardyzacja tekstu wejściowego (zgodna z treningiem)."""
    if not isinstance(text, str): return ""
    text = text.lower()
    text = re.sub(r'http\S+|www\.\S+', '', text)
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Mapowanie klas (0=Real, 1=Fake)
LABELS = {0: "WIARYGODNY (REAL)", 1: "FAŁSZYWY (FAKE)"}

@st.cache_resource
def load_inference_engine():
    model_path = Path(__file__).resolve().parent.parent / "model"
    model_path_str = str(model_path)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    try:
        if not model_path.exists():
            raise FileNotFoundError(f"Model directory not found: {model_path_str}")

        tokenizer = BertTokenizer.from_pretrained(model_path_str)
        model = BertForSequenceClassification.from_pretrained(model_path_str)
        model.to(device)
        model.eval()
        
        # Inicjalizacja explainera
        explainer = SequenceClassificationExplainer(model, tokenizer)
        return tokenizer, model, device, explainer
    except Exception as e:
        st.error(f"Błąd inicjalizacji modelu: {e}")
        return None, None, None, None

tokenizer, model, device, cls_explainer = load_inference_engine()

# --- 3. FUNKCJA WIZUALIZACJI ---
def visualize_attributions(attributions, prediction_label):
    """
    Ręczne generowanie HTML dla atrybucji, aby uniknąć błędów biblioteki.
    Słowa wpływające na predykcję są podświetlane.
    """
    html_content = '<div class="highlight-text">'
    
    # Normalizacja kolorów
    # Jeśli wynik to FAKE (1), to tokeny popychające do FAKE są czerwone.
    # Jeśli wynik to REAL (0), to tokeny popychające do REAL są zielone.
    
    for word, score in attributions:
        # Pomiń tokeny specjalne
        if word in ['[CLS]', '[SEP]']:
            continue
            
        clean_word = word.replace('##', '') # Usunięcie artefaktów tokenizacji BERTa
        
        # Ustalenie koloru tła na podstawie wagi (score)
        # Score > 0 oznacza, że słowo wspiera wybraną klasę
        alpha = min(abs(score) * 5, 1.0) # Wzmocnienie koloru dla widoczności
        
        if prediction_label == 1: # FAKE
            if score > 0:
                color = f"rgba(255, 0, 0, {alpha})" # Czerwony (Wspiera Fake)
            else:
                color = f"rgba(0, 255, 0, {alpha})" # Zielony (Przeczy Fake)
        else: # REAL
            if score > 0:
                color = f"rgba(0, 255, 0, {alpha})" # Zielony (Wspiera Real)
            else:
                color = f"rgba(255, 0, 0, {alpha})" # Czerwony (Przeczy Real)

        # Jeśli waga jest znikoma, brak tła
        if abs(score) < 0.05:
            html_content += f'<span>{clean_word} </span>'
        else:
            html_content += f'<span style="background-color: {color}; border-radius: 3px; padding: 0 2px;">{clean_word}</span> '
            
    html_content += '</div>'
    return html_content

# --- 4. INTERFEJS UŻYTKOWNIKA ---

col_input, col_stats = st.columns([2, 1])

with col_input:
    user_text = st.text_area("Wprowadź tekst artykułu (język angielski):", height=250)
    analyze_btn = st.button("Uruchom analizę", type="primary")

# Kontener na wyniki
if analyze_btn and user_text and model:
    start_time = time.time()
    
    with st.spinner("Przetwarzanie..."):
        # 1. Preprocessing
        cleaned_text = clean_text_standard(user_text)
        
        # 2. Tokenizacja i Predykcja
        inputs = tokenizer(cleaned_text, return_tensors="pt", truncation=True, padding=True, max_length=512).to(device)
        
        with torch.no_grad():
            outputs = model(**inputs)
            probs = F.softmax(outputs.logits, dim=1)
            pred_idx = torch.argmax(probs, dim=1).item()
            confidence = probs[0][pred_idx].item()
            
            # Pobranie prawdopodobieństw dla obu klas
            prob_real = probs[0][0].item()
            prob_fake = probs[0][1].item()

        # 3. Explainability (Obliczanie wag)
        attributions = cls_explainer(cleaned_text)
        
    end_time = time.time()
    inference_time = (end_time - start_time) * 1000

    # --- PREZENTACJA WYNIKÓW ---
    
    # Prawa kolumna - Metryki techniczne
    with col_stats:
        st.subheader("Metryki Modelu")
        st.info(f"Czas inferencji: {inference_time:.1f} ms")
        st.text(f"Liczba tokenów: {len(tokenizer.encode(cleaned_text))}")
        st.text(f"Urządzenie: {str(device).upper()}")
        
        st.write("Rozkład prawdopodobieństwa:")
        st.progress(prob_real, text=f"REAL: {prob_real:.2%}")
        st.progress(prob_fake, text=f"FAKE: {prob_fake:.2%}")

    # Lewa kolumna - Główny wynik i Wyjaśnienie
    with col_input:
        st.subheader("Wynik Klasyfikacji")
        
        if pred_idx == 1:
            st.error(f"**{LABELS[1]}** (Pewność: {confidence:.2%})")
        else:
            st.success(f"**{LABELS[0]}** (Pewność: {confidence:.2%})")

        st.divider()
        st.subheader("Analiza Atrybucji Tokenów")
        st.caption("Poniższy tekst wizualizuje wpływ poszczególnych słów na decyzję modelu. Kolor intensywny oznacza silny wpływ na wybraną klasę.")
        
        # Generowanie i wyświetlanie wizualizacji (Manual HTML)
        html_viz = visualize_attributions(attributions, pred_idx)
        st.markdown(html_viz, unsafe_allow_html=True)
