import os
import json
import csv
from datetime import datetime
from pathlib import Path

# KONFIGURACJA - ROZSZERZENIA PLIKOW

VIDEO_EXTENSIONS = {'.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm'}
AUDIO_EXTENSIONS = {'.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a'}
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}
CSV_FIELD_NAMES = ['data', 'plik_oryginalny', 'format_wyjsciowy', 'plik_wynikowy', 'uzyty_program']


# FUNKCJA 1: Znalezienie plikow multimedialnych

def findMediaFiles(directory):
    files = []
    
    searching_dir = Path(directory)
    
    if not searching_dir.exists() or not searching_dir.is_dir():
        print("Podany katalog nie istnieje lub nie jest folderem.")
        return []
    
    # rglob - pliki i podkatalogi
    # iterdir - tylko pliki w katalogu
    try:
        for file in searching_dir.rglob('*'):
            if file.is_file():
                extension = file.suffix.lower()
                
                full_path = str(file.resolve())
                
                if extension in VIDEO_EXTENSIONS or extension in AUDIO_EXTENSIONS or extension in IMAGE_EXTENSIONS:
                    files.append(full_path)
        return files
    except PermissionError:
        print(f"[!] Brak uprawnien do odczytu katalogu: {directory}")
        return []


# FUNKCJA 2: Pobranie katalogu wyjsciowego

def getOutputDir():
    return os.environ.get('CONVERTED_DIR', 'converted')


# FUNKCJA 3: Generowanie nazwy pliku wyjsciowego - RRRRMMDD-nazwa_pliku.rozszerzenie

def generateOutputFilename(input_file, output_format):
    
    timestamp = datetime.now().strftime("%Y%m%d")
    original_name = Path(input_file).stem
    
    return f"{timestamp}-{original_name}.{output_format}"


# FUNKCJA 4: Zapisywanie historii do JSON (wersja podstawowa)

def saveHistoryJson(history_entry, history_file='history.json'):
    history_data = []
    
    if os.path.exists(history_file) and os.path.getsize(history_file) > 0:
        try:
            with open(history_file, 'r', encoding='utf-8') as f:
                history_data = json.load(f)
                
        except (json.JSONDecodeError, IOError) as e:
            print(f"[!] Blad odczytu historii: {e}")   
    
    history_data.append(history_entry)
    
    try:
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history_data, f, indent=2, ensure_ascii=False)
    except IOError as e:
        print(f"[!] Blad zapisu historii: {e}")


# FUNKCJA 5: Zapisywanie historii do CSV (wersja rozszerzona)

def saveHistoryCsv(history_entry, history_file='history.csv'):
    
    required_fields = set(CSV_FIELD_NAMES)
    if not required_fields.issubset(history_entry.keys()):
        print("[!] Brak wymaganych pol w history_entry")
        return
    
    
    file_exists = os.path.exists(history_file) and os.path.getsize(history_file) > 0
    try:
        with open(history_file, 'a' if file_exists else 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELD_NAMES)
                
            if not file_exists:
                writer.writeheader()
            
            writer.writerow(history_entry)
    except IOError as e:
        print(f"[!] Blad zapisu historii CSV: {e}")


# FUNKCJA 6: Okrelenie typu pliku (dla ImageMagick)

def getFileType(filepath):
    extension = Path(filepath).suffix.lower()
    
    if extension in VIDEO_EXTENSIONS or extension in AUDIO_EXTENSIONS:
        return "media"
    elif extension in IMAGE_EXTENSIONS:
        return "image"
    
    return None