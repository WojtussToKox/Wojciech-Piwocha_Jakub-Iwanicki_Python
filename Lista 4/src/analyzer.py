# ZAD4 PART1
import argparse
import sys
import json
from collections import Counter

# Wczytuje plik i zwraca słownik ze stat.
def analyzeFile(filepath):
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
    total_chars = len(content)

    # splitlines obsługuje różne zak. linii
    lines = content.splitlines()
    total_lines = len(lines)

    words = content.split()
    total_words = len(words)

    # Counter zlicza wystąpienia każdego znaku
    # most_common(1) zwraca listę [(znak, count)]
    if content:
        char_counter = Counter(content)
        most_common_char, most_common_char_count = char_counter.most_common(1)[0]
    else:
        most_common_char = ""
        most_common_char_count = 0

    if words:
        word_counter = Counter(w.lower() for w in words)
        most_common_word, most_common_word_count = word_counter.most_common(1)[0]
    else:
        most_common_word = ""
        most_common_word_count = 0

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
        description="Analizuje statystycznie plik tekstowy. Czyta ścieżkę do pliku z stdin"
    )
    parser.parse_args()

    filepath = input().strip()
    result = analyzeFile(filepath)

    # ensure_ascii=False by polskie znaki nie były zamieniane
    print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main()