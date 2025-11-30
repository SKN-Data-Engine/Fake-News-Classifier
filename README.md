# Klasyfikator Fake News

Aplikacja webowa wykrywający fake news.

## Instalacja

```bash
python -m venv .venv
source .venv/bin/activate
```

## Zainstaluj pakiet i zależności:

```bash
pip install .
```

## Pobierz model

Repo modelu: `mgud29/Fake-News-BERT`.

Proste kroki (uruchom w katalogu głównym projektu):

1) Zainstaluj i włącz Git LFS (jeśli jeszcze nie):

```bash
git lfs install
```

2) Sklonuj repo modelu i skopiuj pliki do `model/`:

```bash
git clone https://huggingface.co/mgud29/Fake-News-BERT tmp_model_repo
mkdir -p model
cp -r tmp_model_repo/* model/
rm -rf tmp_model_repo
```

3) Szybka weryfikacja - sprawdź, że w `model/` masz wymagane pliki:

```bash
ls -la model/
# powinny być m.in.: config.json, model.safetensors (lub pytorch_model.bin), tokenizer_config.json, special_tokens_map.json, vocab.txt
```

To wszystko - skopiuj i wklej powyższe komendy, a model znajdzie się w `model/`


Pobieranie datasetu (OPCJONALNIE)
- Pobierz dataset zgodnie z instrukcją zawartą w `data/README.md`, (niepotrzebny do działania aplikacji)

## Uruchomienie aplikacji (Streamlit)

```bash
streamlit run src/app.py
```

W konsoli wyswietli się adres, na którym pracuje aplikacja. Zazwyczaj:
```bash
http://localhost:8501
```




## Uwaga o strukturze
- `src/app.py` zakłada, że model znajduje się w `../model/` (ścieżka względna od `src`).
- Notatniki w `notebooks/` oczekują datasetu w `../data/` (ścieżka względna od `notebooks`).
