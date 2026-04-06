# ZAD4 PART2

import os
import sys
import json
import subprocess
from collections import Counter

# Zwraca posortowaną liste ścieżek do plikow txt w danym katalogu
def get_text_files(directory):
    textFiles = []
    for entry in os.scandir(directory):
        if entry.is_file() and entry.name.endswith(".txt"):
            textFiles.append(entry.path)
    return sorted(textFiles)

def run_analyzer(filepath):
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
        return json.loads(result.stdout.strip())
    except json.JSONDecodeError as e:
        print(f"Błąd parsowania JSON dla {filepath}: {e}", file=sys.stderr)
        return None

def main():
    if len(sys.argv) < 2:
        print("Użycie: python file_stats.py path/to/file")
        sys.exit(1)

    directory = sys.argv[1]

    if not os.path.isdir(directory):
        print(f"Błąd: '{directory}' nie jest katalogiem")
        sys.exit(1)

    files = get_text_files(directory)

    if not files:
        print("Brak plików .txt w podanym katalogu")
        sys.exit(0)

    # Uruchamiamy analyze dla kazdego pliku i zbieramy wyniki do listy słowników
    results = []
    for filepath in files:
        data = run_analyzer(filepath)
        if data:
            results.append(data)

    if not results:
        print("Nie udało się przeanalizować żadnego pliku.")
        sys.exit(1)

    # Obliczanie statystyk
    totalFiles = len(results)
    totalChars = sum(r["totalChars"] for r in results)
    totalWords = sum(r["totalWords"] for r in results)
    totalLines = sum(r["totalLines"] for r in results)

    # By wybrac najcżestsze słowo/znak globalnie, ważymy wyniki per rozmiar
    allChars = Counter()
    allWords = Counter()

    for r in results:
        allChars[r["mostCommonChar"]] += r["totalChars"]
        allWords[r["mostCommonWord"]] += r["totalWords"]

    mostCommonChar = allChars.most_common(1)[0][0] if allChars else ""
    mostCommonWord = allWords.most_common(1)[0][0] if allWords else ""

    print(f"Liczba przeczytanych plików: {totalFiles}")
    print(f"Sumaryczna liczba znaków:    {totalChars}")
    print(f"Sumaryczna liczba słów:      {totalWords}")
    print(f"Sumaryczna liczba wierszy:   {totalLines}")
    print(f"Najczęstszy znak:            {repr(mostCommonChar)}")
    print(f"Najczęstsze słowo:           {mostCommonWord}")

if __name__ == "__main__":
    main()

