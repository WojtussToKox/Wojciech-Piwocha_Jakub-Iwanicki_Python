import argparse
import random
import statistics
import sys
from datetime import datetime
from pathlib import Path
from Parser.parser import parse_measurements, parse_stations

# Stałe
DATA_DIR = Path('Lista 5/data')

VALID_INDICATORS = {
    'PM2.5', 'PM10', 'NO', 'NO2', 'NOX', 'SO2', 'CO', 'O3',
    'C6H6', 'BaA(PM10)', 'BaP(PM10)', 'As(PM10)', 'Cd(PM10)',
    'Ni(PM10)', 'Pb(PM10)',
}

VALID_FREQUENCES = {'1g', '24g'}

# Walidatory argumentów
def parse_date(value: str) -> datetime:
    try:
        return datetime.strptime(value, '%Y-%m-%d')
    except ValueError:
        raise argparse.ArgumentTypeError(
            f'Nieprawdiłowa data: "{value}". Wymagany format: RRRR-MM-DD'
        )

def validate_indicator(value: str) -> str:
    if value not in VALID_INDICATORS:
        raise argparse.ArgumentTypeError(
            f'Nienznan wielkość: "{value}".\n'
            f'Dozwolone: {", ".join(sorted(VALID_INDICATORS))}'
        )
    return value

def validate_frequency(value: str) -> str:
    if value not in VALID_FREQUENCES:
        raise argparse.ArgumentTypeError(
            f'Nieznana częstotliwość: "{value}.\n'
            f'Dozwolone: {", ".join(VALID_FREQUENCES)}'
        )
    return value

# Logika pomocnicza
# Szukanie pliku pomiarowego CSV pasująxcego do wzorca
def find_measurement_file(indicator:str, frequency: str) -> Path:
    meas_dir = DATA_DIR / 'measurements'
    if not meas_dir.exists():
        print(f'Błąd: katalog z pomiarami nie istnieje: {meas_dir}', file=sys.stderr)
        sys.exit(1)

    candidates = list(meas_dir.glob(f'*{indicator}_{frequency}.csv'))
    if not candidates:
        print(
            f'Błąd: brak pliku pomiarowego dla wielkości "{indicator}" '
            f'i częstotliwości "{frequency}"', file=sys.stderr
        )
        sys.exit(1)

    return candidates[0]

# Wczytuje plik pomiarowy i filtruje dane do zadanego przedziału czasowego
def load_filtered_measurements(
        indicator:str,
        frequency:str,
        start: datetime,
        end: datetime,
) -> dict[str, list[float]]:
    path = find_measurement_file(indicator, frequency)
    mf = parse_measurements(path)

    result: dict[str, list[float]] = {}
    for code, measurements in mf.data.items():
        values = [
            m.value
            for m in measurements
            if start <= m.timestamp <= end and m.value is not None
        ]
        if values:
            result[code] = values

    return result

# Wypisuje nazwe i adres losowej stacji mierzącej podaną wartość
def cmd_random_station(args: argparse.Namespace) -> None:
    data = load_filtered_measurements(
        args.indicator, args.frequency, args.start, args.end
    )

    if not data:
        print('Brak pomiarów dla podanych argumentów')
        return

    stations_path = DATA_DIR / 'stacje.csv'
    if not stations_path.exists():
        print(f'Błąd: plik stacji nie istnieje: {stations_path}', file=sys.stderr)
        sys.exit(1)

    stations = parse_stations(stations_path)
    available_codes = set(data.keys())
    matched = [st for st in stations if st.station_code in available_codes]

    if not matched:
        print(f'Nie znaleziono żadnej stacji mierzącej "{args.indicator}"')
        return

    chosen = random.choice(matched)
    print(f'\nLosowa stacja mierząca {args.indicator} ({args.frequency}):')
    print(f'  Nazwa:     {chosen.name}')
    print(f'  Kod:       {chosen.station_code}')
    print(f'  Miasto:    {chosen.city}')
    print(f'  Adres:     {chosen.address}')
    print(f'  Województwo: {chosen.province}')

# Podkomenda stats
def cmd_stats(args: argparse.Namespace) -> None:
    data = load_filtered_measurements(
        args.indicator, args.frequency, args.start, args.end
    )

    if args.station_code not in data:
        print(
            f'Brak pomiarów dla stacji "{args.station_code}" przy podanych parametrach',
            file=sys.stderr
        )
        sys.exit(1)

    values = data[args.station_code]
    mean = statistics.mean(values)
    stdev = statistics.stdev(values) if len(values) > 1 else 0.0

    print(f'\nStatystyki dla stacji: {args.station_code}')
    print(f'  Wskaźnik:            {args.indicator}')
    print(f'  Częstotliwość:       {args.frequency}')
    print(f'  Przedział:           {args.start.date()} – {args.end.date()}')
    print(f'  Liczba pomiarów:     {len(values)}')
    print(f'  Średnia:             {mean:.4f}')
    print(f'  Odch. standardowe:   {stdev:.4f}')


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='air_quality',
        description='Analiza pomiarów zanieczyszczeń powietrza (dane GIOŚ)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        )

    parser.add_argument(  # Zad. 5a-i – mierzona wielkość (PM2.5, PM10, NO, …)
        '-i', '--indicator',
        required=True,
        type=validate_indicator,  # Zad. 5c-i – walidacja wielkości wywoływana przez argparse
        metavar='WSKAŹNIK',
        help=(
            'Mierzona wielkość, np. PM10, PM2.5, NO2. '
            f'Dozwolone wartości: {", ".join(sorted(VALID_INDICATORS))}'
        )
    )
    parser.add_argument(  # częstotliwość (1g / 24g)
        '-f', '--frequency',
        required=True,
        type=validate_frequency,  # walidacja częstotliwości
        metavar='CZĘSTOTLIWOŚĆ',
        help='Częstotliwość uśredniania: 1g lub 24g.'
    )
    parser.add_argument(  # przedział czasowy: początek (rrrr-mm-dd)
        '-s', '--start',
        required=True,
        type=parse_date,  # walidacja formatu daty
        metavar='RRRR-MM-DD',
        help='Początek przedziału czasowego (włącznie).'
    )
    parser.add_argument(  # przedział czasowy: koniec (rrrr-mm-dd)
        '-e', '--end',
        required=True,
        type=parse_date,  # walidacja formatu daty
        metavar='RRRR-MM-DD',
        help='Koniec przedziału czasowego (włącznie).'
    )


    subparsers = parser.add_subparsers(
        title='podkomendy',
        dest='command',
        metavar='PODKOMENDA',
    )
    subparsers.required = True

    subparsers.add_parser(  # Zad. 5b-i – podkomenda: losowa stacja
        'random-station',
        help='Wypisuje nazwę i adres losowej stacji mierzącej podaną wielkość.',
    ).set_defaults(func=cmd_random_station)

    sp_stats = subparsers.add_parser(  # Zad. 5b-ii – podkomenda: statystyki
        'stats',
        help='Oblicza średnią i odchylenie standardowe dla podanej stacji.',
    )
    sp_stats.add_argument(  # Zad. 5b-ii – kod stacji jako argument podkomendy
        'station_code',
        metavar='KOD_STACJI',
        help='Kod stacji pomiarowej, np. MzKatowiceROŚKatowice.',
    )
    sp_stats.set_defaults(func=cmd_stats)

    return parser

def main():
    parser = build_parser()
    args = parser.parse_args()
    if args.start > args.end:
        parser.error('Data początkowa nie może być późniejsza niż data końcowa.')

    args.func(args)

if __name__ == '__main__':
    main()