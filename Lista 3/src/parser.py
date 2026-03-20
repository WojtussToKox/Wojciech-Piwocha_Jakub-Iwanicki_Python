#  ts (dateTime) – Znacznik czasu żądania w formacie UNIX timestamp (sekundy od 1970-01-01).
#  uid (str) – Unikalny identyfikator sesji (np. dla konkretnego połączenia).
#  id.orig_h (str) – Adres IP hosta wysyłającego żądanie (klienta).
#  id.orig_p (int) – Port źródłowy hosta wysyłającego żądanie.
#  id.resp_h (str) – Adres IP serwera, do którego skierowano żądanie.
#  id.resp_p (int) – Port docelowy serwera, zwykle 80 (HTTP) lub 443 (HTTPS).
#  method (str) – Metoda HTTP (GET, POST, HEAD, PUT, DELETE, OPTIONS, itp.).
#  host (str) – Nazwa domenowa hosta serwera, do którego wysyłane jest żądanie.
#  uri (str) – Ścieżka URI zasobu, który jest żądany (np. /index.html).
import sys
from datetime import datetime


def safeInt(val, default=0):
    try:
        return int(val)
    except (ValueError, TypeError):
        return default


def processEntry(entry):
    return (
            datetime.fromtimestamp(float(entry[0])),             # [0] ts (dateTime)
            entry[1],                                            # [1] uid (str)
            entry[2],                                            # [2] host_orig (str)
            safeInt(entry[3]),                                   # [3] port_orig (int)
            entry[4],                                            # [4] host_resp (str)
            safeInt(entry[5]),                                   # [5] port_resp (int)
            entry[7],                                            # [6] method (str)
            entry[8],                                            # [7] host (str)
            entry[9],                                            # [8] uri (str)
            safeInt(entry[14])                                   # [9] status_code (int)
        )


def readLog():
    sep ="\t"
    return [
        processEntry(line.strip().split(sep))
        for line in sys.stdin
        if line.strip() and len(line.split(sep)) >= 15
    ]


def main():
    try:
        logs = readLog()
        print(f"Wczytano rekordów: {len(logs)}")
        for r in logs[:3]:  # pokaż 3 pierwsze dla testu
            print(r)
    except Exception as e:
        raise RuntimeError(f"Błąd podczas parsowania pliku: {e}")


if __name__ == "__main__":
    main()
