import os
import sys


# Wypisywanie każdego katalogu w osobnej lini
def listDirs():
    path_var = os.environ.get("PATH", "")

    dirs = path_var.split(os.pathsep)

    for d in dirs:
        print(d)

# Sprawdzenie czy plik jest wykonwyalny zgodnie z systemem
def isExecutable(full_path):
    if not(os.path.isfile(full_path)):
        return False

    # Logika dla Windows(nt)
    if os.name == 'nt':
        extensions = ('.exe', '.bat', '.cmd')
        return full_path.lower().endswith(extensions)
    # Logika dla reszty
    else:
        return os.access(full_path, os.X_OK)

# Wypisywanie katalogów z PATH wraz z plikami wykonwyalnymi
def listExecutables():
    path_var = os.environ.get("PATH", "")
    dirs = path_var.split(os.pathsep)

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


def printHelp():
    print("Błąd: Nie podano poprawnej opcji.")
    print("Użycie:")
    print("  python zad2.py --dirs         -> Wypisuje katalogi z PATH")
    print("  python zad2.py --executables  -> Wypisuje katalogi + pliki wykonywalne")

def main():
    if len(sys.argv) < 2:
        printHelp()
        sys.exit(1)

    option = sys.argv[1]

    if option == "--dirs":
        listDirs()
    elif option == "--executables":
        listExecutables()
    else:
        print(f"Nieznana opcja: {option}")
        printHelp()
        sys.exit(1)

if __name__ == "__main__":
    main()
