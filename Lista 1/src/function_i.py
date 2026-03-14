import sys
import helper_functions as helpFun


def processText():
    try:
        sentence = helpFun.readNextSentence()
        sentence_counter = 1

        while sentence_counter <= 20 and sentence != "":
            sentence_counter += 1

            sys.stdout.write(sentence + '\n')

            sentence = helpFun.readNextSentence()

    except Exception as e:
        raise RuntimeError(f"Błąd podczas szukania zdania: {e}")


def main():
    try:
        processText()

    except Exception as e:
        sys.stderr.write(f"Krytyczny błąd programu i: {e}\n")


if __name__ == "__main__":
    main()