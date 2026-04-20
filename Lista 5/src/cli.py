import argparse
import random
import statistics
import sys
import logging
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


# Filtr przepuszczający tylko logi niższe niż ERROR
class StdOutFilter(logging.Filter):
    def filter(self, record):
        return record.levelno < logging.ERROR


def setup_logger():
    logger = logging.getLogger('AirQuality')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)s: %(message)s')

    # Handler dla stdout (DEBUG, INFO, WARNING)
    stdout_h = logging.StreamHandler(sys.stdout)
    stdout_h.setLevel(logging.DEBUG)
    stdout_h.addFilter(StdOutFilter())
    stdout_h.setFormatter(formatter)

    # Handler dla stderr (ERROR, CRITICAL)
    stderr_h = logging.StreamHandler(sys.stderr)
    stderr_h.setLevel(logging.ERROR)
    stderr_h.setFormatter(formatter)

    logger.addHandler(stdout_h)
    logger.addHandler(stderr_h)
    return logger


logger = setup_logger()


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
def find_measurement_file(indicator: str, frequency: str) -> Path:
    meas_dir = DATA_DIR / 'measurements'
    if not meas_dir.exists():
        logger.error(f'Błąd krytyczny: katalog z pomiarami nie istnieje: {meas_dir}')
        sys.exit(1)

    candidates = list(meas_dir.glob(f'*{indicator}_{frequency}.csv'))
    if not candidates:
        logger.error(
            f'Błąd: brak pliku pomiarowego dla wielkości "{indicator}" '
            f'i częstotliwości "{frequency}"'
        )
        sys.exit(1)

    return candidates[0]


# Wczytuje plik pomiarowy i filtruje dane do zadanego przedziału czasowego
def load_filtered_measurements(
        indicator: str,
        frequency: str,
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


# Ładowanie surowych danych (zostawiamy daty i puste wartości None)
def load_raw_measurements(
        indicator: str,
        frequency: str,
        start: datetime,
        end: datetime,
) -> dict:
    path = find_measurement_file(indicator, frequency)
    mf = parse_measurements(path)

    result = {}
    for code, measurements in mf.data.items():
        # Wypakowujemy pomiary, które mieszczą się w zadanym czasie.
        # W odróżnieniu od zwykłego filtra, NIE usuwamy tu wartości 'None', bo brak prądu to też anomalia!
        valid_time_measurements = [
            m for m in measurements
            if start <= m.timestamp <= end
        ]
        if valid_time_measurements:
            result[code] = valid_time_measurements
    return result


# Funkcja z regułami analizującymi anomalie
def detect_anomalies(measurements: list, indicator: str) -> list[str]:
    anomalies = []
    total_count = len(measurements)

    if total_count == 0:
        return ["Brak danych do analizy w podanym przedziale."]

    none_count = 0
    zero_count = 0
    valid_m = []

    # Progi alarmowe zależne od wielkości zanieczyszczenia
    thresholds = {'PM10': 150, 'PM2.5': 100, 'NO2': 200, 'SO2': 350, 'O3': 180}
    alarm_threshold = thresholds.get(indicator, 400) # Domyślny próg
    max_delta = alarm_threshold * 0.6 # Skok o 60% progu w jednym odczycie to anomalia

    for m in measurements:
        if m.value is None:
            none_count += 1
            continue

        # Reguła 1: Wartości ujemne (brak sensu fizycznego)
        if m.value < 0:
            anomalies.append(f"[{m.timestamp.date()} {m.timestamp.time()}] Ujemna wartość pomiaru: {m.value}")
        elif m.value == 0:
            zero_count += 1

        # Reguła 2: Przekroczenie ekstremalnych progów
        if m.value > alarm_threshold:
            anomalies.append(f"[{m.timestamp.date()} {m.timestamp.time()}] Krytyczny alarm smogowy! Skrajna wartość: {m.value} (próg: {alarm_threshold})")

        valid_m.append(m)

    # Reguła 3: Zbyt wiele braków lub zer
    if none_count / total_count > 0.2:
        anomalies.append(f"Zbyt wiele braków danych: {(none_count/total_count)*100:.1f}% odczytów to puste wartości.")

    if total_count > 0 and zero_count / total_count > 0.3:
        anomalies.append(f"Podejrzanie dużo wartości idealnie zerowych ({(zero_count/total_count)*100:.1f}%).")

    # Reguła 4: Podejrzane nagłe skoki (delta)
    valid_m.sort(key=lambda x: x.timestamp)
    for i in range(1, len(valid_m)):
        prev = valid_m[i-1]
        curr = valid_m[i]

        delta = abs(curr.value - prev.value)
        if delta > max_delta:
            anomalies.append(f"[{curr.timestamp.date()} {curr.timestamp.time()}] Nagły, podejrzany skok wartości o {delta:.1f} względem poprzedniego odczytu.")

    return anomalies


# Krok 3: Podkomenda działająca z CLI
def cmd_anomalies(args: argparse.Namespace) -> None:
    data = load_raw_measurements(
        args.indicator, args.frequency, args.start, args.end
    )

    if args.station_code not in data:
        logger.warning(f'Brak pomiarów dla stacji "{args.station_code}" przy podanych parametrach')
        sys.exit(1)

    measurements = data[args.station_code]
    print(f"\n--- Diagnostyka anomalii dla stacji: {args.station_code} ---")
    print(f"Badany wskaźnik: {args.indicator} | Analizowany przedział: {args.start.date()} do {args.end.date()}")

    anomalies = detect_anomalies(measurements, args.indicator)

    if not anomalies:
        print(" Nie wykryto żadnych anomalii. Dane z czujnika wydają się być wiarygodne i stabilne.")
    else:
        print(f"️ Wykryto potencjalne błędy i anomalie ({len(anomalies)}):")
        for a in anomalies:
            print(f"  - {a}")


# Wypisuje nazwe i adres losowej stacji mierzącej podaną wartość
def cmd_random_station(args: argparse.Namespace) -> None:
    data = load_filtered_measurements(
        args.indicator, args.frequency, args.start, args.end
    )

    if not data:
        logger.warning('Brak pomiarów dla podanych argumentów')
        return

    stations_path = DATA_DIR / 'stacje.csv'
    if not stations_path.exists():
        logger.error(f'Błąd: plik stacji nie istnieje: {stations_path}')
        sys.exit(1)

    stations = parse_stations(stations_path)
    available_codes = set(data.keys())
    matched = [st for st in stations if st.station_code in available_codes]

    if not matched:
        logger.warning(f'Nie znaleziono żadnej stacji mierzącej "{args.indicator}"')
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
        logger.warning(f'Brak pomiarów dla stacji "{args.station_code}" przy podanych parametrach')
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

    # Zadanie na max pkt - podkomenda: anomalie
    sp_anomalies = subparsers.add_parser(
        'anomalies',
        help='Analizuje dane stacji w poszukiwaniu błędów czujnika i nagłych skoków smogu.',
    )
    sp_anomalies.add_argument(
        'station_code',
        metavar='KOD_STACJI',
        help='Kod stacji pomiarowej do zdiagnozowania.',
    )
    sp_anomalies.set_defaults(func=cmd_anomalies)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
