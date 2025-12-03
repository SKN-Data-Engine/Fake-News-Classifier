# Fake-News-Classifier

Repozytorium zawiera webową aplikację (Streamlit) do klasyfikacji tekstów jako wiarygodne / fałszywe (fake news).

## Najważniejsze cechy
- Fine-tuned BERT (model do klasyfikacji tekstu)
- Explainable AI: wizualizacje wpływu tokenów na decyzję modelu (przy użyciu transformers_interpret)
- Prosty interfejs Streamlit do testowania i analizowania wyników

## Wymagania
- Python >= 3.10
- Git i Git LFS

## Quick start
Poniżej kroki, które pozwolą uruchomić aplikację od zera na czystym systemie.

Krok 1 - sklonuj repo (przykład):

```bash
# z katalogu w którym chcesz umieścić projekt
git clone https://github.com/SKN-Data-Engine/Fake-News-Classifier.git
cd Fake-News-Classifier
```

Krok 2 - pobierz model (Hugging Face)

```bash
# z katalogu projektu
# 1) zainstaluj/configuruj git-lfs (jeśli nie masz)
git lfs install

# 2) sklonuj repo modelu bezpośrednio do katalogu `model`
git clone https://huggingface.co/mgud29/Fake-News-BERT model

# 3) pobierz rzeczywiste obiekty LFS (safetensors/pytorch_model.bin)
cd model
git lfs pull origin main
cd ..

# Weryfikacja:
ls -la model
file model/model.safetensors  # powinien byc bitowym plikiem a nie tekstowym
```

Krok 3 - środowisko i zależności

```bash
# utwórz virtualenv i aktywuj (macOS / Linux)
python3.10 -m venv .venv
source .venv/bin/activate

# zainstaluj wymagane pakiety
pip install -r requirements.txt
```

Krok 4 - uruchom aplikację

```bash
streamlit run src/app.py
```

Otwórz w przeglądarce adres wyświetlony przez Streamlit (zazwyczaj http://localhost:8501).


## Struktura repo
- `src/app.py` - aplikacja Streamlit (UI + ładowanie modelu)
- `model/` - lokalne pliki modelu/tokenizera (nie śledź dużych wag w zwykłym commicie; używaj Git LFS)
- `data/` - opcjonalne pliki danych / datasety
- `notebooks/` - notatniki eksploracyjne i treningowe
