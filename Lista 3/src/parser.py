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
import datetime


def process_record(record, all_tuples):
    my_tuple = record.split("\t")

    if len(my_tuple) >= 15:
        try:
            # Obsługa brakujących wartości reprezentowanych jako '-'
            status_code = int(my_tuple[14]) if my_tuple[14] != '-' else 0
            port_orig = int(my_tuple[3]) if my_tuple[3] != '-' else 0
            port_resp = int(my_tuple[5]) if my_tuple[5] != '-' else 0

            all_tuples.append((
                datetime.datetime.fromtimestamp(float(my_tuple[0])),    # [0] ts (dateTime)
                my_tuple[1],                                            # [1] uid (str)
                my_tuple[2],                                            # [2] host_orig (str)
                port_orig,                                              # [3] port_orig (int)
                my_tuple[4],                                            # [4] host_resp (str)
                port_resp,                                              # [5] port_resp (int)
                my_tuple[7],                                            # [6] method (str)
                my_tuple[8],                                            # [7] host (str)
                my_tuple[9],                                            # [8] uri (str)
                status_code                                             # [9] status_code (int)
            ))
        except ValueError as e:
            sys.stdout.write(f"Uwaga: Błąd konwersji typów dla rekordu ({e}), pomijam...\n")
    else:
        sys.stdout.write(f"Uwaga: Rekord za krótki (liczba kolumn: {len(my_tuple)}), pomijam.\n")

def readLog():
    all_tuples = []
    bufor = ""

    for line in sys.stdin:
        # Usuwamy tylko znaki końca linii, żeby nie zepsuć zawartości
        clean_line = line.strip("\r\n")

        if not clean_line:
            continue

        pierwszy_element = clean_line.split("\t")[0]

        try:
            float(pierwszy_element) # Jeśli to timestamp, rzutowanie na float się uda
            is_new_record = True
        except ValueError:
            is_new_record = False   # Jeśli wywali błąd, to znaczy, że to urwana linia

        if is_new_record:
            # Trafiliśmy na nowy rekord. Jeśli coś jest w buforze, to znaczy,że to koniec poprzedniego rekordu - przetwarzamy go.
            if bufor:
                process_record(bufor, all_tuples)

            # Zaczynamy budowę nowego bufora na podstawie aktualnej linii
            bufor = clean_line
        else:
            # Jeśli to urwana linia, dopisujemy ją do aktualnego bufora
            bufor += clean_line

    # Przetworzenie ostatniego rekordu
    if bufor:
        process_record(bufor, all_tuples)

    return all_tuples


def main():
    try:
        for my_tuple in readLog():
            print(my_tuple)
    except Exception as e:
        raise RuntimeError(f"Błąd podczas parsowania pliku: {e}")


if __name__ == "__main__":
    main()
