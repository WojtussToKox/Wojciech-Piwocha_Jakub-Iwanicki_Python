import sys
import argparse
import time

parser = argparse.ArgumentParser(
        description="Uproszczona wersja tail"
)

parser.add_argument('-l', '--lines', type=int, default=10, help='Liczba linii do wyświetlenia')
parser.add_argument('-f', '--follow', action="store_true", help='Śledź plik')
parser.add_argument('file', nargs='?', default=None, help='Ścieżka do pliku')


args = parser.parse_args()

try:
    f = None
    # 1. Odczyt danych z pliku lub stdin
    if args.file:
        f = open(args.file, 'r', encoding='utf-8')
        text = f.readlines()
    else:
        text = sys.stdin.readlines()

    # 2. Wypisanie zadanej liczby ostatnich linii
    n = args.lines
    last_lines = text[-n:]

    for line in last_lines:
        print(line, end='')
        
    # 3. Śledzenie pliku (tryb --follow)
    if args.follow and f:
        # Wskaźnik odczytu (pointer) w 'f' po wykonaniu readlines() znajduje się już na samym końcu pliku.
        # Wystarczy tylko nasłuchiwać nowych danych.
        while True:
            line = f.readline()
            if line:
                print(line, end='')
            else:
                time.sleep(0.1)

    if f:
        f.close()
        
except FileNotFoundError:
    print(f"Błąd: Plik '{args.file}' nie istnieje", file=sys.stderr)
    sys.exit(1)
except KeyboardInterrupt:
    # Dla --follow - pozwól zakończyć Ctrl+C
    sys.exit(0)