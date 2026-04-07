import argparse
import os
import sys

# ZAD 1
def main():
    parser = argparse.ArgumentParser(
        description="Wyświetla zmienne środowiskowe, opcjonalnie filtrując po nazwie."
    )

    parser.add_argument(
        "filters",
        nargs="*",
        help="Filtry nazw zmiennych (case-insensitive)."
    )
    args = parser.parse_args()

    env_vars = sorted(os.environ.items())

    if args.filters:
        filters = [f.lower() for f in args.filters]
        result = []
        for name, value in env_vars:
            if any(f in name.lower() for f in filters):
                result.append((name, value))
    else:
        # Brak filtrów - bierzemy wszystkie zmienne
        result = env_vars

    if not result and args.filters:
        print(f"Brak zmienny pasujących do filtrów: {', '.join(args.filters)}")
    else:
        for name, value in result:
            print(f"{name}: {value}")


if __name__ == '__main__':
    main()