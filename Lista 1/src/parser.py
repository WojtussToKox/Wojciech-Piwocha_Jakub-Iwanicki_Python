import sys


def cleanLine(text):
    # Usunięcie białych znaków
    text = text.strip()

    # Zastąpienie podwójnej spacji przez pojedynczą
    while "  " in text:
        text = text.replace("  ", " ")

    return text


def main():
    sys.stdin.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')

    lines_read = 0
    empty_lines_in_row = 0
    is_checking_preamble = True
    has_preamble = False

    # Na wypadek braku preambuły w tekscie
    buffer = ""

    while True:
        line = sys.stdin.readline()

        # 1. Koniec tekstu -> brak preambuły oraz brak info o wydaniu
        if not line:
            if is_checking_preamble and not has_preamble:
                sys.stdout.write(buffer)
            break

        cleaned = cleanLine(line)

        # 2. info o wydaniu -> brak preambuły
        if cleaned == "-----":
            if is_checking_preamble and not has_preamble:
                sys.stdout.write(buffer)
            break

        # 3. Nadal szukamy preambuły
        if is_checking_preamble:
            lines_read += 1

            if cleaned == "":
                empty_lines_in_row += 1
            else:
                empty_lines_in_row = 0

            # Zebranie do buforu na wypadek braku preambuły
            buffer += cleaned + "\n"

            # Znaleziono koniec preambuły
            if empty_lines_in_row == 2:
                has_preamble = True
                is_checking_preamble = False
                buffer = ""
                empty_lines_in_row = 0
                continue

            # Pierwsze 10 wierszy pustych -> brak preambuły -> wypisanie 10 wierszy
            if lines_read == 10 and not has_preamble:
                is_checking_preamble = False
                sys.stdout.write(buffer)
                buffer = ""

        # 4. Treść właściwa
        else:
            sys.stdout.write(cleaned + "\n")


if __name__ == "__main__":
    main()

