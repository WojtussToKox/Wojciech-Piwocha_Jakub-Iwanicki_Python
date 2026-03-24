import os
from urllib.parse import urlparse

# Zadanie 3
def getEntriesByCode(log, code):
    if not isinstance(code, int):
        print("Błąd! Kod statusu musi być liczbą całkowitą!")
        return []
    # Filtrujemy tylko te rekordy, gdzie status_code == code
    return [entry for entry in log if entry[9] == code]

# Zadanie 4
def getEntriesByAddr(log, addr):
    # Sprawdzamy format IP, gdy zawiera kropki
    if "." in addr:
        parts = addr.split(".")

        # Adres IP musi składać się z 4 części
        if len(parts) == 4:
            # Sprawdzamy czy każda część jest liczbą z zakresu 0-255
            is_valid_ip = all(p.isdigit() and 0<=int(p)<=255 for p in parts)
            if not is_valid_ip:
                print(f"Warning! {addr} nie jest poprawnym adresem IP!")
                return []
        # Jeśli są kropki, ale liczba części różna od 4
        else:
            print(f"Warning! {addr} ma błędną liczbę segmentów!")
            return []
    # Filtrujemy po adresie klienta/hosta serwera
    return [entry for entry in log if entry[2] == addr or entry[7] == addr]

# Zadanie 5
def getFailedReads(log, merge=False):
    # Filtrujemy rekordy według zakresów kodów statusu
    err_4xx = [entry for entry in log if 400<=entry[9] < 500]
    err_5xx = [entry for entry in log if 500<=entry[9] < 600]

    # Decydujemy o formacie wyniku na podstawie merge
    if merge:
        return err_4xx + err_5xx
    return err_4xx, err_5xx

# Zadanie 6
def getEntriesByExtension(log, ext):
    results = []
    # Ujednolicamy rozszerzenie(zacyna sie od kropki i jest małymi literami)
    ext = ext.lower() if ext.startswith('.') else f".{ext.lower()}"

    for entry in log:
        uri = entry[8]

        # Odcinamy parametry (wszystko co znajduje sie po ?/#)
        clean_path = urlparse(uri).path

        # splitext wyciąga samo rozszerzenie
        _, file_ext = os.path.splitext(clean_path)

        # Sprawdzamy dopasowanie rozszerzenia, ignorując wielkość liter w nazwie pliku
        if file_ext.lower() == ext:
            results.append(entry)

    return results

# Zadanie 9
def getEntriesInTimeRange(log, start, end):
    return [entry for entry in log if start <= entry[0] < end]