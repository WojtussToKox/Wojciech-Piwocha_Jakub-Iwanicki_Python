from typing import NamedTuple
from datetime import datetime
from pathlib import Path
import csv
import logging

logger = logging.getLogger('AirQuality')
MEASUREMENT_DATE_FORMAT = '%d/%m/%y %H:%M'
MIN_HEADER_ROWS = 6


class Station(NamedTuple):
    number: int                     # liczba porządkowa
    station_code: str
    international_code: str
    name: str
    old_code: str | None
    start_date: str                 # 'RRRR-MM-DD' lub ''
    close_date: str
    station_type: str               # Typ
    area_type: str
    station_sort: str               # Rodzaj
    province: str
    city: str
    address: str
    latitude: float | None
    longitude: float | None


# Jeden pomiar dla jednej stacji w jednej chwili czasu
class Measurement(NamedTuple):
    timestamp: datetime
    value: float | None


class MeasurementFile(NamedTuple):
    indicator: str        # np. 'BaA(PM10)'
    averaging_time: str   # np. '24g'
    unit: str             # np. 'ng/m3'
    # Kod stacji to klucz w słowniku
    data: dict[str, list[Measurement]]


def safe_float(value: str) -> float | None:
    value = value.strip()

    if not value:
        return None
    try:
        return float(value.replace(',','.'))
    except ValueError:
        return None


def parse_stations(path: Path) -> list[Station]:
    stations: list[Station] = []

    logger.info(f"Otwarto plik: {path}")

    with open(path, newline='', encoding='utf-8-sig') as f:

        lines = f.readlines()
        for line in lines:
            logger.debug(f"Przeczytano {len(line.encode('utf-8'))} bajtów")  # Zadanie 6a

        reader = csv.DictReader(f)
        for row in reader:
            # Klucze mogą zawierać białe znaki
            clean_row = {k.replace('\n', '').strip(): v.strip() for k, v in row.items()}

            station = Station(
                number = int(clean_row.get('Nr', 0) or 0),
                station_code = clean_row.get('Kod stacji', ''),
                international_code = clean_row.get('Kod międzynarodowy', ''),
                name = clean_row.get('Nazwa stacji', ''),
                # Szukamy klucza zawierającego "Stary Kod stacji"
                old_code = clean_row.get('Stary Kod stacji (o ile inny od aktualnego)', None) or None,
                start_date = clean_row.get('Data uruchomienia', ''),
                close_date = clean_row.get('Data zamknięcia', ''),
                station_type = clean_row.get('Typ stacji', ''),
                area_type = clean_row.get('Typ obszaru', ''),
                station_sort = clean_row.get('Rodzaj stacji', ''),
                province = clean_row.get('Województwo', ''),
                city = clean_row.get('Miejscowość', ''),
                address = clean_row.get('Adres', ''),
                latitude = safe_float(clean_row.get('WGS84 φ N', '')),
                longitude = safe_float(clean_row.get('WGS84 λ E', ''))
            )
            stations.append(station)
            
    logger.info(f"Zamknięto plik: {path}")
    return stations


def parse_measurements(path: Path) -> MeasurementFile:
    logger.info(f"Otwarto plik: {path}") # Zadanie 6b
    with open(path, newline='', encoding='utf-8-sig') as f:
        # Zadanie 6a: logowanie liczby bajtów wiersza
        for line in f:
            logger.debug(f"Przeczytano {len(line.encode('utf-8'))} bajtów")
        reader = list(csv.reader(f))

    station_codes = [c.strip() for c in reader[1][1:] if c.strip()]
    indicator = reader[2][1].strip() if len(reader) > 2 else ''
    averaging_time = reader[3][1].strip() if len(reader) > 3 else ''
    unit = reader[4][1].strip() if len(reader) > 4 else ''

    measurements_data: dict[str, list[Measurement]] = {code: [] for code in station_codes}

    for row in reader[6:]:
        if not row or not row[0].strip():
            continue

        try:
            timestamp = datetime.strptime(row[0].strip(), '%d/%m/%y %H:%M')
        except ValueError:
            continue

        values = row[1:]
        for i, station_code in enumerate(station_codes):
            val = values[i].strip() if i < len(values) else ''
            measurements_data[station_code].append(
                Measurement(timestamp=timestamp, value=safe_float(val))
            )
    logger.info(f"Zamknięto plik: {path}")  # Zadanie 6b
    return MeasurementFile(indicator, averaging_time, unit, measurements_data)


def main():
    stations = parse_stations(Path('../../data/stacje.csv'))
    print(f'Wczytano {len(stations)} stacji.')
    print('Pierwsza stacja:', stations[0])

    # Parsowanie pliku pomiarowego
    mf = parse_measurements(Path('../../data/measurements/2023_BaA(PM10)_24g.csv'))
    print(f'\nWskaźnik: {mf.indicator}, Czas: {mf.averaging_time}, Jednostka: {mf.unit}')
    print(f'Liczba stacji: {len(mf.data)}')

    total = sum(len(v) for v in mf.data.values())
    print(f'Liczba pomiarów: {total}')

    first_station = next(iter(mf.data))
    print('Przykładowy pomiar:', mf.data[first_station][0])


if __name__ == "__main__":
    main()
