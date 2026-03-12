import sys

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')


def isLetter(char):
    if type(char) is not str or len(char) != 1:
        raise ValueError("Funkcja oczekuje pojedynczego znaku (str).")
    return char.isalpha()


def isSentenceEnder(char):
    if type(char) is not str or len(char) != 1:
        raise ValueError("Funkcja oczekuje pojedynczego znaku (str).")
    sentence_enders = ".!?"
    return char in sentence_enders


def isWordSeparator(char):
    if type(char) is not str or len(char) != 1:
        raise ValueError("Funkcja oczekuje pojedynczego znaku (str).")
    word_separators = " \n\t\r.,;:!?(){}[]/"
    return char in word_separators


def isWhiteSpace(char):
    if type(char) is not str or len(char) != 1:
        raise ValueError("Funkcja oczekuje pojedynczego znaku (str).")
    return char.isspace()


def readNextSentence():
    try:
        sentence_buffer = ""
        newline_count = 0
        c = sys.stdin.read(1)

        while c:
            # Sprawdzenie konca akapitu
            if c == "\n":
                newline_count += 1
            elif not isWhiteSpace(c):
                newline_count = 0

            # Dodanie do bufora
            sentence_buffer += c

            # Sprawdzenie czy koniec zdania
            if isSentenceEnder(c) or newline_count >= 2:
                clean_sentence = sentence_buffer.strip()

                # Jeśli po oczyszczeniu zdanie ma treść, zwracamy je
                if len(clean_sentence) > 0:
                    return clean_sentence
                else:
                    # Koniec akapitu ->  bufor jest pusty
                    # Czyścimy bufor -> szukamy dalej
                    sentence_buffer = ""
                    newline_count = 0

            c = sys.stdin.read(1)

        # Koniec pliku -> buffor pełny -> zwróć to co jest w nim
        if sentence_buffer.strip():
            return sentence_buffer.strip()

        return ""

    except Exception as e:
        raise RuntimeError(f"Błąd podczas czytania zdania ze strumienia: {e}")


def getNextWord(sentence):
    # TO_DO
    return 0


def countWords(sentence):
    # TO_DO
    return 0

