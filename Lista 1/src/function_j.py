import sys
import helper_functions as helpFun

def countTargetWords(sentence):
    in_word = False
    current_word = ""
    target_word_count = 0
    target_words = "|i|oraz|ale|że|lub|"

    for char in sentence:
        if helpFun.isLetter(char):
            if not in_word:
                in_word = True
            current_word += char.lower()
        elif helpFun.isWordSeparator(char) or helpFun.isWhiteSpace(char):
            if in_word:
                if "|" + current_word + "|" in target_words:
                    target_word_count += 1
                current_word = ""
                in_word = False
    if in_word:
        if "|" + current_word + "|" in target_words:
            target_word_count += 1
    return target_word_count

def filterConjunctionSentences():
    try:
        sentence = helpFun.readNextSentence()
        while sentence != "":
            if countTargetWords(sentence) >= 2:
                sys.stdout.write(sentence + "\n")
            sentence = helpFun.readNextSentence()
    except Exception as e:
        raise RuntimeError(f"Błąd podczas filtrowania zdań ze spójnikami: {e}")

def main():
    try:
        sys.stdin.reconfigure(encoding='utf-8')
        sys.stdout.reconfigure(encoding='utf-8')

        filterConjunctionSentences()
    except Exception as e:
        sys.stderr.write(f"Krytyczny błąd funkcji J: {e}\n")

if __name__ == "__main__":
    main()