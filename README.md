# Klasyfikator Fake News

Aplikacja webowa wykrywający fake news.

Instalacja

```bash
python -m venv .venv
source .venv/bin/activate
```

- Zainstaluj pakiet i zależności:

```bash
pip install .
```

Pobranie modelu
- Pobierz model zgodnie z instrukcją zawartą w `model/README.md`.

Pobieranie datasetu (OPCJONALNIE)
- Pobierz dataset zgodnie z instrukcją zawartą w `data/README.md`, (niepotrzebny do działania aplikacji)

Uruchomienie aplikacji (Streamlit)

```bash
streamlit run src/app.py
```

W konsoli wyswietli się adres, na którym pracuje aplikacja. Zazwyczaj:
```bash
http://localhost:8501
```




Uwaga o strukturze
- `src/app.py` zakłada, że model znajduje się w `../model/` (ścieżka względna od `src`).
- Notatniki w `notebooks/` oczekują datasetu w `../data/` (ścieżka względna od `notebooks`).
