# Analizator Tekstu w Pythonie (Strumienie i Potoki)

## Informacje o zespole
* **Grupa:** Grupa t
* **Skład zespołu:**
  * Wojciech Piwocha
  * Jakub Iwanicki

## Cel projektu
Celem projektu jest stworzenie zestawu narzędzi do strumieniowego przetwarzania i analizy tekstu (książek w formacie TXT, np. z serwisu WolneLektury.pl). Program działa w architekturze potokowej (pipeline), odczytując dane ze standardowego wejścia (`stdin`) i wypisując wynik na wyjście (`stdout`). Głównym wyzwaniem projektu jest całkowity zakaz używania typów nieskalarnych (list, słowników, zbiorów) oraz wyrażeń regularnych – cała analiza opiera się wyłącznie na iteracji znak po znaku za pomocą typu `str`.

## Struktura projektu
* `src/` - kody źródłowe (główny parser, skrypty funkcji, funkcje pomocnicze)
* `tests/` - teksty testujące poszczególne funkcje
* `docs/` - dokumentacja projektu oraz treści zadań
* `data/` - pliki tekstowe służące jako wejście do analizy

## Instrukcja uruchomienia
Wymagane jest środowisko Python 3.x.

**1. Uruchomienie programu podstawowego (witającego):**
Z poziomu głównego katalogu repozytorium wpisz w terminalu:
```bash
type data\calineczka.txt | python src\parser.py | python src\function_b.py
