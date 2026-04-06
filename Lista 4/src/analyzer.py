# ZAD4 PART1
import sys
import json
from collections import Counter

# Wczytuje plik i zwraca słownik ze stat.
def analyze_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Błąd: plik {filepath} nie istnieje", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Błąd odczytu pliku: {e}", file=sys.stderr)
        sys.exit(1)

    # len na stringu liczy znaki Unicode
    totalChars = len(content)

    # splitlines obsługuje różne zak. linii
    lines = content.splitlines()
    totalLines = len(lines)

    words = content.split()
    totalWords = len(words)

    # Counter zlicza wystąpienia każdego znaku
    # most_common(1) zwraca listę [(znak, count)]
    if content:
        charCounter = Counter(content)
        mostCommonChar, _ = charCounter.most_common(1)[0]
    else:
        mostCommonChar = ""

    if words:
        wordCounter = Counter(w.lower() for w in words)
        mostCommonWord, _ = wordCounter.most_common(1)[0]
    else:
        mostCommonWord = ""

    return {
        "filepath": filepath,
        "totalChars": totalChars,
        "totalWords": totalWords,
        "totalLines": totalLines,
        "mostCommonChar": mostCommonChar,
        "mostCommonWord": mostCommonWord,
    }

def main():
    filepath = input().strip()
    result = analyze_file(filepath)

    # ensure_ascii=False by polskie znaki nie były zamieniane
    print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main()