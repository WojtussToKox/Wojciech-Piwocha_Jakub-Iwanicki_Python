# ZAD4 PART2
import argparse
import os
import sys
import json
import subprocess
from collections import Counter

# Zwraca posortowaną liste ścieżek do plikow txt w danym katalogu
def getTextFiles(directory):
    text_files = []
    for entry in os.scandir(directory):
        if entry.is_file() and entry.name.endswith(".txt"):
            text_files.append(entry.path)
    return sorted(text_files)

def runAnalyzer(filepath):
    # Odpala analyzer jako osobny proces
    result = subprocess.run(
        [sys.executable, os.path.join(os.path.dirname(__file__), "analyzer.py")],
        input=filepath,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )

    if result.returncode != 0:
        print(f"Błąd analizy pliku {filepath}: {result.stderr.strip()}", file=sys.stderr)
        return None

    try:
        return json.loads(result.stdout.strip()) # Zamienia JSON na słownik
    except json.JSONDecodeError as e:
        print(f"Błąd parsowania JSON dla {filepath}: {e}", file=sys.stderr)
        return None

def main():
    parser = argparse.ArgumentParser(
        description="Uruchamia analyze.py dla każdego pliku txt w katalogu i wypisuje statystyki"
    )
    parser.add_argument(
        "directory",
        help="Ścieżka do katalogu z plikami txt"
    )
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"Błąd: '{args.directory}' nie jest katalogiem")
        sys.exit(1)

    files = getTextFiles(args.directory)

    if not files:
        print("Brak plików .txt w podanym katalogu")
        sys.exit(0)

    # Uruchamiamy analyze dla kazdego pliku i zbieramy wyniki do listy słowników
    results = []
    for filepath in files:
        data = runAnalyzer(filepath)
        if data:
            results.append(data)

    if not results:
        print("Nie udało się przeanalizować żadnego pliku.")
        sys.exit(1)

    # Obliczanie statystyk
    total_files = len(results)
    total_chars = sum(r["total_chars"] for r in results)
    total_words = sum(r["total_words"] for r in results)
    total_lines = sum(r["total_lines"] for r in results)

    all_chars = Counter()
    all_words = Counter()

    for r in results:
        all_chars[r["most_common_char"]] += r["most_common_char_count"]
        all_words[r["most_common_word"]] += r["most_common_word_count"]

    most_common_char = all_chars.most_common(1)[0][0] if all_chars else ""
    most_common_word = all_words.most_common(1)[0][0] if all_words else ""

    print(f"Liczba przeczytanych plików: {total_files}")
    print(f"Sumaryczna liczba znaków:    {total_chars}")
    print(f"Sumaryczna liczba słów:      {total_words}")
    print(f"Sumaryczna liczba wierszy:   {total_lines}")
    print(f"Najczęstszy znak:            {repr(most_common_char)}")
    print(f"Najczęstsze słowo:           {most_common_word}")

if __name__ == "__main__":
    main()

