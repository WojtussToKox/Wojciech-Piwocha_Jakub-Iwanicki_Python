import sys
import helper_functions as helpFun

def filterShortSentences():
    try:
        sentence = helpFun.readNextSentence()
        while sentence != "":
            if helpFun.countWords(sentence) <= 4:
                sys.stdout.write(sentence + "\n")
            sentence = helpFun.readNextSentence()
    except Exception as e:
        raise RuntimeError(f"Błąd podczas filtrowania krótkich zdań: {e}")

def main():
    try:
        sys.stdin.reconfigure(encoding='utf-8')
        sys.stdout.reconfigure(encoding='utf-8')

        filterShortSentences()
    except Exception as e:
        sys.stderr.write(f"Krytyczny błąd funkcji G: {e}\n")

if __name__ == "__main__":
    main()