# ZAD 2
import argparse
import os

# Sprawdzenie czy plik jest wykonwyalny zgodnie z systemem
def isExecutable(full_path):
    if not os.path.isfile(full_path):
        return False

    # Logika dla Windows(nt)
    if os.name == 'nt':
        return full_path.lower().endswith(('.exe', '.bat', '.cmd'))

    # Logika dla reszty
    return os.access(full_path, os.X_OK)

# Pobiera PATH i dzieli na osobne ścieżki
def getPathDirs():
    path_var = os.environ.get("PATH", "")
    if not path_var:
        return []
    return path_var.split(os.pathsep)

# Wypisuje każdy katalog w osobnej lini
def listDirs():
    dirs = getPathDirs()

    for d in dirs:
        print(d)

# Wypisuje katalogi z PATH wraz z plikami wykonwyalnymi
def listExecutables():
    dirs = getPathDirs()

    for d in dirs:
        if not d:
            continue
        print(f"\nKatalog: {d}")

        if not os.path.isdir(d):
            print(" (katalog nie istnieje lub brak dostępu)")
            continue

        try:
            files = os.listdir(d)
            # Filtrujemy tylko wykonywalne i sortujemy dla porządku
            executables = [f for f in sorted(files) if isExecutable(os.path.join(d, f))]

            if executables:
                for exe in executables:
                    print(f" [EXE] {exe}")
            else:
                print(" (brak plików wykonywalnych)")
        except PermissionError:
            print(" (brak uprawnień do odczytu katalogu)")
        except Exception as e:
            print(f" (błąd: {e})")

def main():
    parser = argparse.ArgumentParser(
        description="Operacje na zmiennej PATH"
    )

    # Tworzymy grupe która wymusza wybór tylko jednej opcji naraz
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--dirs",
        action="store_true",
        help="Wypisuje katalogi z PATH"
    )

    group.add_argument(
        "--executables",
        action="store_true",
        help="Wypisuje katalogi z PATH + pliki wykonywalne"
    )

    args = parser.parse_args()

    if args.dirs:
        listDirs()
    elif args.executables:
        listExecutables()

if __name__ == "__main__":
    main()
