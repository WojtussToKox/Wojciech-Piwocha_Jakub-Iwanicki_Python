import sys
import helper_functions as helpFun

def findLongestSentence():
    try:
        longest = ""
        max_len = -1

        sentence = helpFun.readNextSentence()

        while sentence != "":
            if len(sentence) > max_len:
                longest = sentence
                max_len = len(sentence)
            sentence = helpFun.readNextSentence()
        return longest
    except Exception as e:
        raise RuntimeError(f"Błąd podczas wyszukiwania najdłuższego zdania: {e}")

def main():
    try:
        sys.stdin.reconfigure(encoding='utf-8')
        sys.stdout.reconfigure(encoding='utf-8')

        result = findLongestSentence()

        if result != "":
            sys.stdout.write(result+"\n")
    except Exception as e:
        sys.stderr.write(f"Krytyczny błąd funkcji D: {e}\n")

if __name__ == "__main__":
    main()