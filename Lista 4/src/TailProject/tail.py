import sys
import argparse
import time
from collections import deque


def read_last_lines(source, n):
    if n <= 0:
        for _ in source:
            pass
        return deque()
    return deque(source, maxlen=n)


def seek_to_end_efficiently(f, n):
    # Rozmiar bloku do czytania wstecz (w bajtach)
    BLOCK_SIZE = 8192
    f.seek(0, 2)  # skocz na koniec pliku
    file_size = f.tell()

    if file_size == 0:
        return []

    lines_found = []
    buffer = b""
    pos = file_size

    while pos > 0 and len(lines_found) <= n:
        # Czytaj blok wstecz
        read_size = min(BLOCK_SIZE, pos)
        pos -= read_size
        f.seek(pos)
        chunk = f.read(read_size)
        buffer = chunk + buffer

        # Podziel bufor na linie
        lines_in_buffer = buffer.split(b"\n")

        # Ostatni element może być niekompletny — zostaw go w buforze
        buffer = lines_in_buffer[0]
        lines_found = lines_in_buffer[1:] + lines_found

    # Zostałość bufora to pierwsza (być może niepełna) linia
    if buffer:
        lines_found = [buffer] + lines_found

    # Weź ostatnie n linii i zdekoduj
    result = lines_found[-n:]
    return [line.decode("utf-8", errors="replace") + "\n"
            for line in result if line]


def main():
    parser = argparse.ArgumentParser(
        description="Uproszczona wersja programu tail",
    )
    parser.add_argument(
        '--lines', type=int, default=10, metavar='n',
        help='Liczba linii do wyświetlenia (domyślnie: 10)'
    )
    parser.add_argument(
        '--follow', action='store_true',
        help='Śledź plik i wypisuj nowe linie (tylko dla pliku, nie stdin)'
    )
    parser.add_argument(
        'file', nargs='?', default=None,
        help='Ścieżka do pliku (opcjonalne; bez argumentu czyta ze stdin)'
    )
    args = parser.parse_args()

    if args.lines < 0:
        print("Błąd: liczba linii musi być nieujemna", file=sys.stderr)
        sys.exit(1)

    use_file = args.file is not None
    stdin_is_pipe = not sys.stdin.isatty()

    if not use_file and not stdin_is_pipe:
        parser.print_usage(sys.stderr)
        print("Błąd: podaj plik lub przekaż dane przez potok (stdin)", file=sys.stderr)
        sys.exit(1)

    if args.follow and not use_file:
        print("Błąd: --follow działa tylko z argumentem pliku, nie ze stdin", file=sys.stderr)
        sys.exit(1)

    try:
        f = None

        if use_file:
            # Tryb binarny dla seek_to_end_efficiently; dla małych plików fallback do deque
            f = open(args.file, 'rb')
            file_size = f.seek(0, 2)

            # Heurystyka: jeśli plik > 10 MB i n jest małe → szukaj od końca
            # Próg można dostosować do potrzeb
            TEN_MB = 10 * 1024 * 1024
            if file_size > TEN_MB:
                last_lines = seek_to_end_efficiently(f, args.lines)
            else:
                # Mały plik — wróć na początek i użyj deque
                f.seek(0)
                text_f = (line.decode('utf-8', errors='replace') for line in f)
                last_lines = read_last_lines(text_f, args.lines)

        else:
            # stdin — musi być deque, nie można seekować
            last_lines = read_last_lines(sys.stdin, args.lines)

        # Wypisz ostatnie n linii
        for line in last_lines:
            print(line, end='')

        # Tryb --follow
        if args.follow and f:
            # Ustaw wskaźnik na koniec pliku (gdzie skończyliśmy czytać)
            f.seek(0, 2)
            print(f"\n=== Śledzenie '{args.file}' (Ctrl+C aby zakończyć) ===",
                  file=sys.stderr)
            while True:
                raw_line = f.readline()
                if raw_line:
                    print(raw_line.decode('utf-8', errors='replace'), end='', flush=True)
                else:
                    time.sleep(0.1)

    except FileNotFoundError:
        print(f"Błąd: plik '{args.file}' nie istnieje", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print(f"Błąd: brak uprawnień do odczytu pliku '{args.file}'", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print()
        sys.exit(0)
    finally:
        if f:
            f.close()


if __name__ == "__main__":
    main()
