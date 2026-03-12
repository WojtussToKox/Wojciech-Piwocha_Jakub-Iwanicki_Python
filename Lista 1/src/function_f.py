import sys
import helper_functions as helpFun


def findFirstComplexSentence():
    try:
        sentence = helpFun.readNextSentence()

        while sentence != "":
            comma_count = 0

            for char in sentence:
                if char == ",":
                    comma_count += 1

            if comma_count >= 2:
                return sentence

            sentence = helpFun.readNextSentence()

        return ""

    except Exception as e:
        raise RuntimeError(f"Błąd podczas szukania zdania: {e}")


def main():
    try:
        result_sentence = findFirstComplexSentence()

        if result_sentence != "":
            sys.stdout.write(result_sentence + '\n')

    except Exception as e:
        sys.stderr.write(f"Krytyczny błąd programu f: {e}\n")


if __name__  == "__main__":
    main()