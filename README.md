# Języki Skryptowe: Python - Repozytorium Zespołowe

## 👥 Informacje o zespole
* **Nazwa grupy:** Grupa 5
* **Skład zespołu:**
  * Wojciech Piwocha
  * Jakub Iwanicki

## 🎯 Cel projektu
Niniejsze repozytorium zawiera zbiór rozwiązań zadań realizowanych w ramach przedmiotu *Języki Skryptowe*. Projekt ma na celu praktyczne opanowanie programowania w języku Python oraz naukę współpracy przy użyciu systemu kontroli wersji Git i platformy GitHub.

## 📁 Struktura Repozytorium

Projekt został podzielony na katalogi odpowiadające poszczególnym listom zadań. Każda z list zawiera kod źródłowy (`src/`), dane testowe (`data/`, `tests/`) oraz dokumentację/treść zadań (`docs/`).

### [Lista 2](./Lista%202) - Podstawy Pythona i przetwarzanie tekstu
Katalog zawiera zestaw podstawowych funkcji implementujących różne zadania algorytmiczne oraz operacje na plikach.
* **Pliki źródłowe:** `function_a.py` – `function_j.py`, `helper_functions.py`
* Zaimplementowano m.in. parser plików i narzędzia pomocnicze.

### [Lista 3](./Lista%203) - Analiza i filtrowanie danych
Zestaw narzędzi służących do przetwarzania, analizy i filtrowania danych.
* **Główne moduły:**
  * `analytics.py` – moduł odpowiedzialny za statystyki i analizę.
  * `filters.py` – funkcje filtrujące zestawy danych.
  * `parser.py` – przetwarzanie i formatowanie danych wejściowych.
  * `main.py` – główny skrypt spinający funkcjonalności.

### [Lista 4](./Lista%204) - Narzędzia systemowe i konsolowe
Zadania skupiające się na integracji z systemem operacyjnym, operacjach na plikach i tworzeniu własnych narzędzi CLI (Command Line Interface).
* **TailProject (`TailProject/tail.py`)** – własna, zoptymalizowana implementacja uniksowego narzędzia `tail` z obsługą flagi `--lines` oraz trybem śledzenia pliku `--follow`.
* **MediaConverter (`MediaConverter/`)** – program do konwersji plików multimedialnych (`mediaconvert.py` oraz `utils.py`).
* **Narzędzia systemowe:**
  * `env_viewer.py` – przeglądarka i analizator zmiennych środowiskowych (w tym `PATH`).
  * `file_stats.py` – program generujący zaawansowane statystyki plików tekstowych (liczba znaków, słów, wierszy, najczęstsze znaki i słowa).
  * `path_explorer.py` – eksplorator i analizator ścieżek systemowych.
  * `analyzer.py` – skrypt narzędziowy do analizy logów/danych.

---

## 🚀 Jak uruchomić

Wszystkie skrypty zostały napisane w języku Python. Aby je uruchomić, przejdź do katalogu wybranej listy i uruchom odpowiedni plik z poziomu konsoli.

Przykład uruchomienia narzędzia `tail` z Listy 4:
```bash
cd "Lista 4/src/TailProject"
python tail.py --lines 15 sciezka_do_pliku.txt
