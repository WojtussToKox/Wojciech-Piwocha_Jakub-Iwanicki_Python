from collections import Counter
from collections import defaultdict

LOG_KEYS = ["ts", "uid", "host_orig", "port_orig", "host_resp", "port_resp", "method", "host", "uri", "status_code"]

# Zadanie 7
def getTopIps(log, n=10):
    # 1. Wyciągamy same adresy IP (indeks 2) ze wszystkich krotek w logu
    all_ip = [entry[2] for entry in log]

    # 2. Counter automatycznie zlicza wystąpienia każdego IP
    counted_ip = Counter(all_ip)

    # 3. Metoda most_common(n) zwraca posortowaną listę krotek [(ip1, ilosc1), (ip2, ilosc2), ...]
    return counted_ip.most_common(n)

# Zadanie 11
def getTopUris(log, n=10):
    # 1. Wyciągamy same adresy URI (indeks 8) ze wszystkich krotek w logu
    all_uri = [entry[8] for entry in log]

    # 2. Counter automatycznie zlicza wystąpienia każdego IP
    counted_uri = Counter(all_uri)


    # 3. Z listy krotek [(uri1, ilosc1), (uri2, ilosc2), ...] wyciągamy tylko Uri
    return [uri for uri, count in counted_uri.most_common(n)]

# Zadanie 13
def entryToDict(entry):
    # zip(keys, entry) tworzy iterator, który łączy elementy w pary (krotki).
    # Np. ('ts', entry[0]), ('uid', entry[1]) itd. Zatrzymuje się na najkrótszej liście.
    # dict() przyjmuje te pary i konwertuje je na gotowy słownik {klucz: wartość}.
    return dict(zip(LOG_KEYS, entry))

# Zadanie 14
def logToDict(log):
    # Dziedziczący po Dictionary defaultdict przy braku klucza w słowniku tworzy parę klucz:pusta lista, do której możemy dopisać jakiś element
    sessions = defaultdict(list)

    for entry in log:
        entry_dict = entryToDict(entry)

        sessions[entry[1]].append(entry_dict)

    # Ewentualne rzutowanie na zwyły słownik
    return sessions

# Zadanie 15
def printDictEntryDates(log_dict):
    # Przechodzimy przez słownik
    for (uid, entries) in log_dict.items():

        request_count = len(entries)

        # Adresy IP (wyciągamy unikalne i pozbywamy się ewentualnych braków '-')
        host_orig_set = {entry['host_orig'] for entry in entries if entry.get('host_orig') and entry['host_orig'] != "-"}
        host_resp_set = {entry['host_resp'] for entry in entries if entry.get('host_resp') and entry['host_resp'] != "-"}

        # Daty pierwszego i ostatniego żadania

        timestamps = {entry['ts'] for entry in entries if 'ts' in entry}

        if timestamps:
            first_req = min(timestamps).strftime('%d-%m-%Y %H:%M:%S')
            last_req = max(timestamps).strftime('%d-%m-%Y %H:%M:%S')
        else:
            first_req, last_req = "Brak danych", "Brak danych"


        methods_counter = Counter([entry['method'] for entry in entries])

        codes_2xx_count = sum(1 for entry in entries if 200 <= entry.get("method") < 300)
        codes_2xx_percent = (codes_2xx_count/request_count) * 100 if request_count > 0 else 0

        # --- FORMATOWANIE WYJŚCIA ---
        print(f"=== Sesja UID: {uid} ===")
        print(f"Adresy IP klienta (orig): {', '.join(host_orig_set) or 'Brak'}")
        print(f"Adresy IP serwera (resp): {', '.join(host_resp_set) or 'Brak'}")
        print(f"Liczba żądań:             {request_count}")
        print(f"Pierwsze żądanie:         {first_req}")
        print(f"Ostatnie żądanie:         {last_req}")
        print("Udział metod HTTP:")
        for method, count in methods_counter.items():
            percent = (count / request_count) * 100
            print(f"   - {method}: {percent:.2f}% ({count} szt.)")

        print(f"Kody 2xx: {codes_2xx_count}/{request_count} ({codes_2xx_percent:.2f}%)")
        print("-" * 50)

# Zadanie 16a
def getMostActiveSessionFromDict(log_dict):
    if not log_dict:
        return None, 0

    winner_uid, winner_logs = max(log_dict.items(), key=lambda item: len(item[1]))

    return winner_uid, len(winner_logs)

# Zadanie 16b
def getMostActiveSessionFromLog(log):
    counts = Counter(entry[1] for entry in log)
    return counts.most_common(1)[0]