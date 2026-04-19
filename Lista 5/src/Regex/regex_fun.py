import re
from pathlib import Path

from Parser.parser import parse_stations

pattern = re.compile(r'^(\d{4})_(.*)_(.*)\.csv$')
address_pattern = re.compile(r"^((?:ul\.|al\.|pl\.)\s*)?([\w\s.,'/\-]+?)(?:\s+(\d+\S*))?$")


def group_measurement_files_by_key(path: Path) -> dict[tuple[str, str, str], Path]:
    grouped_files = {}

    for file_path in path.iterdir():
        if file_path.is_file():
            match = pattern.match(file_path.name)

            if match:
                year, indicator, frequency = match.groups()
                key = (year, indicator, frequency)
                grouped_files[key] = file_path

    return grouped_files


def get_addresses(path: Path, city: str) -> list[tuple[str, str, str, str]]:
    stations = parse_stations(path)

    addresses = []

    for st in stations:
        # 2. Filtrujemy po mieście (case-insensitive, aby uniknąć błędów wielkości liter)
        if st.city.lower() == city.lower():
            ulica = ""
            numer = ""

            adres_raw = st.address.strip()

            if adres_raw:
                match = address_pattern.match(adres_raw)
                if match:
                    # Wyciągamy przedrostek (jeśli istnieje, np. "ul. ")
                    przedrostek = match.group(1) if match.group(1) else ""

                    # Wyciągamy nazwę ulicy
                    nazwa = match.group(2).strip()

                    # Łączymy przedrostek z nazwą, aby otrzymać pełną ulicę
                    ulica = (przedrostek + nazwa).strip()

                    # Wyciągamy numer (jeśli istnieje)
                    numer = match.group(3) if match.group(3) else ""
                else:
                    # Jeśli z jakiegoś powodu regex nie dopasuje (np. adres to "Brak"),
                    # traktujemy całość jako ulicę
                    ulica = adres_raw

            addresses.append((st.province, st.city, ulica, numer))

    return addresses


def main():
    print("\n--- Test Zadania 2: Grupowanie plików ---")

    katalog_z_pomiarami = Path('../../data/measurements')

    grupy = group_measurement_files_by_key(katalog_z_pomiarami)

    print(f"Znaleziono {len(grupy)} plików pasujących do wzorca.")

    for klucz, sciezka in grupy.items():
        print(f"Klucz: {klucz}  --->  Plik: {sciezka.name}")

    print("\n--- Test Zadania 3 ---")
    sciezka_do_stacji = Path('../../data/stacje.csv')

    miasto_testowe = "Wrocław"
    adresy = get_addresses(sciezka_do_stacji, miasto_testowe)

    print(f"Znaleziono {len(adresy)} stacji w miejscowości {miasto_testowe}:")
    for adres in adresy:
        print(adres)


if __name__ == "__main__":
    main()
