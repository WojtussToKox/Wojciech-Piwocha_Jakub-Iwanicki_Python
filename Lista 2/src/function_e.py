import sys
import helper_functions as helpFun

def isValidSentence(sentence):
    in_word = False
    prev_first_char = ""
    current_first_char = ""

    for char in sentence:
        if helpFun.isLetter(char):
            if not in_word:
                in_word = True
                current_first_char = char.lower()
                if prev_first_char == current_first_char:
                    return False
        elif helpFun.isWordSeparator(char) or helpFun.isWhiteSpace(char):
            if in_word:
                prev_first_char = current_first_char
                in_word = False
    return True

def findSpecialLongestSentence():
    try:
        longest = ""
        max_len = -1

        sentence = helpFun.readNextSentence()
        while sentence != "":
            if isValidSentence(sentence) and len(sentence) > max_len:
                longest = sentence
                max_len = len(sentence)

            sentence = helpFun.readNextSentence()
        return longest
    except Exception as e:
        raise RuntimeError(f"Błąd podczas wyszukiwania specjanlnego najdłuższego zdania: {e}")

def main():
    try:
        sys.stdin.reconfigure(encoding='utf-8')
        sys.stdout.reconfigure(encoding='utf-8')

        result = findSpecialLongestSentence()

        if result != "":
            sys.stdout.write(result + "\n")

    except Exception as e:
        sys.stderr.write(f"Krytyczny błąd funkcji E: {e}\n")

if __name__ == "__main__":
    main()