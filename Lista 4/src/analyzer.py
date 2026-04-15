# ZAD4 PART1
import argparse
import sys
import json
from collections import Counter

# Wczytuje plik i zwraca słownik ze stat.
def analyzeFile(filepath):
    total_chars = 0
    total_words = 0
    total_lines = 0
    char_counter = Counter()
    word_counter = Counter()

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:  # Czytanie strumieniowe
                total_lines += 1
                total_chars += len(line)

                # Podział na słowa dla bieżącej linii
                words = line.split()
                total_words += len(words)

                # Zliczanie znaków w linii (bez białych znaków)
                char_counter.update(ch for ch in line if not ch.isspace())

                # Zliczanie słów w linii (z małych liter)
                word_counter.update(w.lower() for w in words)
    except FileNotFoundError:
        print(f"Błąd: plik {filepath} nie istnieje", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Błąd odczytu pliku: {e}", file=sys.stderr)
        sys.exit(1)

    # Pobieranie najczęstszych wyników
    if char_counter:
        most_common_char, most_common_char_count = char_counter.most_common(1)[0]
    else:
        most_common_char, most_common_char_count = "", 0

    if word_counter:
        most_common_word, most_common_word_count = word_counter.most_common(1)[0]
    else:
        most_common_word, most_common_word_count = "", 0

    return {
        "filepath": filepath,
        "total_chars": total_chars,
        "total_words": total_words,
        "total_lines": total_lines,
        "most_common_char": most_common_char,
        "most_common_char_count": most_common_char_count,
        "most_common_word": most_common_word,
        "most_common_word_count": most_common_word_count,
    }

def main():
    parser = argparse.ArgumentParser(
        description="Analizuje statystycznie plik tekstowy. Czyta ścieżkę do pliku z stdin."
    )
    parser.parse_args()

    # Wczytywanie ścieżki z wejścia standardowego (stdin)
    try:
        filepath = input().strip()
        if not filepath:
            print("Błąd: Oczekiwano ścieżki do pliku, ale wejście jest puste.", file=sys.stderr)
            sys.exit(1)
    except EOFError:
        print("Błąd: Nie podano ścieżki do pliku z wejścia standardowego.", file=sys.stderr)
        sys.exit(1)

    result = analyzeFile(filepath)

    # Zwrócenie wyniku jako JSON (ensure_ascii=False chroni polskie znaki)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()