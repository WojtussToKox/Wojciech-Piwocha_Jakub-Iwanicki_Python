import os
import sys

# ZAD 1
def main():
    # sys.argv[0] to nazwa skryptu, dlatego filtry zaczynają się od 1
    filters = sys.argv[1:]
    # Pobieramy pary (nazwa, wartość) zmiennych środowiskowych
    env_vars = os.environ.items()

    if filters:
        result = []
        for name, value in env_vars:
            for f in filters:
                # Porównujemy obustronnie małymi literami
                if f.lower() in name.lower():
                    result.append((name, value))
                    # Wystarczy że jeden filtr pasuje, nie sprawdzamy dalej
                    break
    else:
        # Brak filtrów - bierzemy wszystkie zmienne
        result = list(env_vars)

    # Sortujemy alfabetycznie po nazwie zmiennej
    for name, value in sorted(result, key=lambda x: x[0].lower()):
        print(f'{name}: {value}')


if __name__ == '__main__':
    main()