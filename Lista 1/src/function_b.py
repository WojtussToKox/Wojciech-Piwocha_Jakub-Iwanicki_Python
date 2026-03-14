import sys
import helper_functions as helpFun


def countNonWhiteChars():
    char_count = 0
    c = sys.stdin.read(1)

    while c:
        try:
            if not helpFun.isWhiteSpace(c):
                char_count += 1
        except Exception as e:
            # Ewentualne błędy z funkcji pomocniczych
            sys.stderr.write(f"Błąd przetwarzania znaku: {e}\n")

        c = sys.stdin.read(1)

    return char_count


def main():
    try:
        # 1. Obliczenie
        result = countNonWhiteChars()

        # 2. Wypisanie
        sys.stdout.write(str(result) + '\n')

    except Exception as e:
        sys.stderr.write(f"Krytyczny błąd programu b: {e}\n")


if __name__  == "__main__":
    main()