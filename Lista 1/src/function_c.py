import sys
import helper_functions as helpFun

def hasProperNoun(sentence):
    in_word = False
    word_count = 0
    current_word = ""

    for char in sentence:
        if helpFun.isLetter(char):
            if not in_word:
                in_word = True
                word_count += 1
            current_word += char
        elif helpFun.isWordSeparator(char) or helpFun.isWhiteSpace(char):
            if in_word:
                if word_count > 1 and len(current_word) > 0 and current_word[0].isupper():
                    return True
                current_word = ""
                in_word = False
    if in_word and word_count > 1 and len(current_word) > 0 and current_word[0].isupper():
        return True

    return False

def calculateProperNounsPercentage():
    try:
        total_sentences = 0
        proper_noun_sentences = 0

        sentence = helpFun.readNextSentence()
        while sentence != "":
            total_sentences += 1
            if hasProperNoun(sentence):
                proper_noun_sentences += 1
            sentence = helpFun.readNextSentence()

        if total_sentences > 0:
            percentage = (proper_noun_sentences / total_sentences)*100
            return percentage
        else:
            return 0.0
    except Exception as e:
        raise RuntimeError(f"Błąd podczas obliczania procentu zdań, które zawierają przynajmniej jedną nazwę własną: {e}")

def main():
    try:
        sys.stdin.reconfigure(encoding='utf-8')
        sys.stdout.reconfigure(encoding='utf-8')

        percentage = calculateProperNounsPercentage()
        sys.stdout.write(f"{percentage:.2f}%\n")

    except Exception as e:
        sys.stderr.write(f"Błąd krytyczny funkcji C: {e}\n")

if __name__ == "__main__":
    main()