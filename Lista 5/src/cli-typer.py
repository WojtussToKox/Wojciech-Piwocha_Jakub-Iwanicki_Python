import random
import statistics
from datetime import datetime
from pathlib import Path
from typing import Annotated
import typer
from Parser.parser import parse_measurements, parse_stations
from enum import Enum

app = typer.Typer(
    name='air_quality',
    help='Analiza pomiarów zanieczyszczeń powietrza (dane GIOŚ)',
    add_completion=False,
)

DATA_DIR = Path('Lista 5/data')

class Indicator(str, Enum):
    PM2_5 = 'PM2.5'
    PM10 = 'PM10'
    NO = 'NO'
    NO2 = 'NO2'
    NOX = 'NOX'
    SO2 = 'SO2'
    CO = 'CO'
    O3 = 'O3'
    C6H6 = 'C6H6'
    BaA = 'BaA(PM10)'
    BaP = 'BaP(PM10)'
    As = 'As(PM10)'
    Cd = 'Cd(PM10)'
    Ni = 'Ni(PM10)'
    Pb = 'Pb(PM10)'

class Frequency(str, Enum):
    g1 = '1g'
    g24 = '24g'

# Logika pomocnicza
def find_measurement_file(indicator: str, frequency: str) -> Path:
    """Szuka pliku CSV pasującego do wzorca *_<indicator>_<frequency>.csv."""
    meas_dir = DATA_DIR / 'measurements'
    if not meas_dir.exists():
        raise typer.BadParameter(
            f'Katalog z pomiarami nie istnieje: {meas_dir}',
            param_hint="'--indicator' / '--frequency'"
        )

    candidates = list(meas_dir.glob(f'*_{indicator}_{frequency}.csv'))
    if not candidates:
        raise typer.BadParameter(
            f'Brak pliku pomiarowego dla wielkości "{indicator}" i częstotliwości "{frequency}".',
            param_hint="'--indicator' / '--frequency'"
        )

    return candidates[0]


def load_filtered_measurements(
        indicator: str,
        frequency: str,
        start: datetime,
        end: datetime,
) -> dict[str, list[float]]:
    """Wczytuje pomiary z pliku i filtruje je do zadanego przedziału czasowego.

        Zwraca słownik kod_stacji → lista wartości liczbowych (bez None).
        """
    path = find_measurement_file(indicator, frequency)
    mf = parse_measurements(path)

    result: dict[str, list[float]] = {}
    for code, measurements in mf.data.items():
        values = [
            m.value for m in measurements
            if start <= m.timestamp <= end and m.value is not None
        ]
        if values:
            result[code] = values
    return result

# Wspólna walidacja parametrów
def validate_params(start: datetime, end: datetime) -> None:
    """Sprawdza, czy data początkowa nie jest późniejsza niż końcowa."""
    if start > end:
        raise typer.BadParameter(
            'Data początkowa nie może być późniejsza niż końcowa.',
            param_hint="'--start' / '--end'"
        )


@app.command('random-station')
def cmd_random_station(
        indicator: Annotated[Indicator, typer.Option('-i', '--indicator', help='Mierzona wielkość.')],
        frequency: Annotated[Frequency, typer.Option('-f', '--frequency', help='Częstotliwość.')],
        start: Annotated[datetime, typer.Option('-s', '--start', formats=['%Y-%m-%d'])],
        end: Annotated[datetime, typer.Option('-e', '--end', formats=['%Y-%m-%d'])],
) -> None:
    """Wypisuje nazwę i adres losowej stacji mierzącej podaną wielkość w zadanym przedziale."""
    validate_params(start, end)

    data = load_filtered_measurements(indicator.value, frequency.value, start, end)

    if not data:
        typer.echo('Brak pomiarów dla podanych parametrów.')
        return

    stations_path = DATA_DIR / 'stacje.csv'
    if not stations_path.exists():
        raise typer.BadParameter(
            f'Plik stacji nie istnieje: {stations_path}',
            param_hint="DATA_DIR"
        )

    stations = parse_stations(stations_path)
    matched = [st for st in stations if st.station_code in data]

    if not matched:
        typer.echo(f'Nie znaleziono stacji mierzących "{indicator}".')
        return

    chosen = random.choice(matched)

    typer.echo(f'\nLosowa stacja mierząca {indicator.value} ({frequency.value}):')
    typer.echo(f'  Nazwa:       {chosen.name}')
    typer.echo(f'  Kod:         {chosen.station_code}')
    typer.echo(f'  Miasto:      {chosen.city}')
    typer.echo(f'  Adres:       {chosen.address}')
    typer.echo(f'  Województwo: {chosen.province}')


@app.command('stats')
def cmd_stats(
        station_code: Annotated[str, typer.Argument(help='Kod stacji pomiarowej, np. MzKatowiceROŚKatowice.')],
        indicator: Annotated[Indicator, typer.Option('-i', '--indicator', help='Mierzona wielkość.')],
        frequency: Annotated[Frequency, typer.Option('-f', '--frequency', help='Częstotliwość.')],
        start: Annotated[datetime, typer.Option('-s', '--start', formats=['%Y-%m-%d'], help='Początek przedziału.')],
        end: Annotated[datetime, typer.Option('-e', '--end', formats=['%Y-%m-%d'], help='Koniec przedziału.')],
) -> None:
    """Oblicza średnią i odchylenie standardowe dla wybranej stacji."""

    validate_params(start, end)

    data = load_filtered_measurements(indicator.value, frequency.value, start, end)

    if station_code not in data:
        raise typer.BadParameter(
            f'Brak pomiarów dla stacji "{station_code}" przy podanych parametrach.',
            param_hint="'STATION_CODE'"
        )

    values = data[station_code]
    mean = statistics.mean(values)
    stdev = statistics.stdev(values) if len(values) > 1 else 0.0

    typer.echo(f'\nStatystyki dla stacji: {station_code}')
    typer.echo(f'  Wskaźnik:            {indicator.value}')
    typer.echo(f'  Częstotliwość:       {frequency.value}')
    typer.echo(f'  Przedział:           {start.date()} – {end.date()}')
    typer.echo(f'  Liczba pomiarów:     {len(values)}')
    typer.echo(f'  Średnia:             {mean:.4f}')
    typer.echo(f'  Odch. standardowe:   {stdev:.4f}')

if __name__ == '__main__':
    app()