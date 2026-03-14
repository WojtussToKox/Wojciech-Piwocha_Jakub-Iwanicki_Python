import sys
import helper_functions as helpFun


def isQuestionOrExclamation(sentence):
    return "?" in sentence or "!" in sentence


def processText():
    try:
        sentence = helpFun.readNextSentence()

        while sentence != "":
            if isQuestionOrExclamation(sentence):
                sys.stdout.write(sentence + '\n')

            sentence = helpFun.readNextSentence()

    except Exception as e:
        raise RuntimeError(f"Błąd podczas szukania zdania: {e}")


def main():
    try:
        processText()

    except Exception as e:
        sys.stderr.write(f"Krytyczny błąd programu h: {e}\n")


if __name__ == "__main__":
    main()