import re
from pathlib import Path
from Parser.parser import parse_stations

# Wzorce
DATE_PATTERN = re.compile(r'(\d{4}-\d{2}-\d{2})')
COORD_PATTERN        = re.compile(r'\d+\.\d{6}')
TWO_PART_NAME        = re.compile(r'^[^-]+-[^-]+$')
THREE_PART_LOCATION  = re.compile(r'^[^-]+-[^-]+-[^-]+$')
COMMA_STREET_PATTERN = re.compile(r',.*\b(?:ul\.|al\.)')

DIACRITICS_MAP = str.maketrans(
    'ąćęłńóśźżĄĆĘŁŃÓŚŹŻ',
    'acelnoszzACELNOSZZ'
)

# 4a - wyodrębnia daty w formacie RRRR-MM-DD z kolumn start/end
def extract_dates(path: Path) -> list[str]:
    stations = parse_stations(path)
    dates: list[str] = []
    for station in stations:
        dates += DATE_PATTERN.findall(station.start_date)
        dates += DATE_PATTERN.findall(station.close_date)
    return dates

# 4b - zwraca liste par (szer., dł.) jako napisy z 6 cyframi po kropce
def extract_coordinates(path: Path) -> list[tuple[str, str]]:
    stations = parse_stations(path)
    coords: list[tuple[str, str]] = []
    for station in stations:
        lat_str = f'{station.latitude:.6f}' if station.latitude is not None else ''
        lon_str = f'{station.longitude:.6f}' if station.longitude is not None else ''
        if COORD_PATTERN.fullmatch(lat_str) and COORD_PATTERN.fullmatch(lon_str):
            coords.append((lat_str, lon_str))
    return coords

# 4c - zwraca nazwy stajci składające się z dwóch części (1x '-')
def find_two_part_names(path: Path) -> list[str]:
    stations = parse_stations(path)
    return [
        station.name for station in stations
        if TWO_PART_NAME.match(station.name.strip())
    ]

# 4d - zastepuje spacje podkreślnikami i polskie znaki odpowiednikami
def normalize_name(name: str) -> str:
    name = name.replace(' ', '_')
    name = name.translate(DIACRITICS_MAP)
    return name

# 4e - weryfikacja spacji
def verify_mobile_stations(path: Path) -> dict[str, bool]:
    stations = parse_stations(path)
    result: dict[str, bool] = {}
    for station in stations:
        if station.station_code.endswith('MOB'):
            is_mobile = station.station_sort.strip().lower() == 'mobilna'
            result[station.station_code] = is_mobile
    return result

# 4f - znajduje 3-członowe stacje
def find_three_part_locations(path: Path) -> list[str]:
    stations = parse_stations(path)
    return [
        station.name for station in stations
        if THREE_PART_LOCATION.match(station.name.strip())
    ]

# 4g - lokalizacje z przecinkiem i ul./al.
def find_comma_street_locations(path: Path) -> list[str]:
    stations = parse_stations(path)
    return [
        station.address for station in stations
        if COMMA_STREET_PATTERN.search(station.address)
    ]

