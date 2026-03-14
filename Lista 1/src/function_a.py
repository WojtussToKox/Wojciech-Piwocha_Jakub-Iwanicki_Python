import sys

def count_paragraphs():
    try:
        paragraphs = 0
        in_paragraph = False

        line = sys.stdin.readline()
        while line:
            if not line.isspace() and line != "":
                if not in_paragraph:
                    paragraphs += 1
                    in_paragraph = True
            else:
                in_paragraph = False

            line = sys.stdin.readline()

        return paragraphs
    except Exception as e:
        raise RuntimeError(f"Błąd podczas zliczania akapitów: {e}")


def main():
    try:
        sys.stdin.reconfigure(encoding='utf-8')
        sys.stdout.reconfigure(encoding='utf-8')

        result = count_paragraphs()
        sys.stdout.write(str(result) + '\n')
    except Exception as e:
        sys.stderr.write(f"Krytyczny błąd programu a: {e}\n")


if __name__ == "__main__":
    main()