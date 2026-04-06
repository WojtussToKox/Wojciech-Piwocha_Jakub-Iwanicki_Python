"""
Glowny skrypt - konwersja plikow multimedialnych za pomoca ffmpeg/ImageMagick
"""
import sys
import os
import subprocess
import argparse
from pathlib import Path
from datetime import datetime

from utils import (
    findMediaFiles,
    getOutputDir,
    generateOutputFilename,
    saveHistoryJson,
    saveHistoryCsv,
    getFileType
)


# FUNKCJA POMOCNICZA: Konwersja przez ffmpeg

def convertWithFfmpeg(input_file, output_file, timeout=300):
    try:
        command = ['ffmpeg',
                   '-i', input_file, 
                   '-y',         # nadpisz
                   output_file]
        
        # Uruchom konwersje
        
        result = subprocess.run(
            command,
            capture_output = True,
            text = True,
            timeout = timeout
        )
        
        if result.returncode == 0:
            print(f" Sukces: {Path(input_file).name} -> {Path(output_file).name}")
            return True
        else:
            print(f" Blad konwersji: {Path(input_file).name}")
            if result.stderr:
                print(f" {result.stderr[:100]}")
            return False
        
    except subprocess.TimeoutExpired:
        print(f" Timeout dla pliku: {Path(input_file).name}")
        return False
    except FileNotFoundError:
        print(f" ffmpeg nie jest zainstalowany bądź nie dodany do PATH")
        return False
    except Exception as e:
        print(f" Nieoczekiwany błąd: {e}")
        return False

# FUNKCJA POMOCNICZA: Konwersja przez ImageMagick (opcjonalnie)

def convertWithImagemagick(input_file, output_file, timeout=300):
    
    try:
        command = ['magick',
                   input_file,
                   output_file]
        
        # Uruchom konwersje
        
        result = subprocess.run(
            command,
            capture_output = True,
            text = True,
            timeout = timeout
        )
        
        if result.returncode == 0:
            print(f" Sukces: {Path(input_file).name} -> {Path(output_file).name}")
            return True
        else:
            print(f" Blad konwersji: {Path(input_file).name}")
            if result.stderr:
                print(f" {result.stderr[:100]}")
            return False
        
    except subprocess.TimeoutExpired:
        print(f" Timeout dla pliku: {Path(input_file).name}")
        return False
    except FileNotFoundError:
        print(f" ImageMagick nie jest zainstalowny")
        return False
    except Exception as e:
        print(f" Nieoczekiwany błąd: {e}")
        return False


# GLOWNA FUNKCJA

def main():
    
    # Parsowanie argumentow
    
    parser = argparse.ArgumentParser(
        description="Konwerter formatow plikow media za pomoca ffmpeg/ImageMagick"
    )
    
    parser.add_argument('directory', help='Sciezka do katalogu z plikami dla konwertera')
    
    parser.add_argument('--format', '-f', default='mp4', help='Format wyjsciowy (domyslnie: mp4)')
    
    args = parser.parse_args()
    
    # Walidacja katalogu
    
    directory = args.directory
    
    if not Path(directory).exists():
        print(f"Podany plik nie istnieje {directory}")
        sys.exit(1)
    if not Path(directory).is_dir():
        print(f"Podany plik nie jest katalogiem {directory}")
        sys.exit(1)
        
    
    
    # Utworzenie katalogu wyjsciowego
    output_dir = getOutputDir()
    os.makedirs(output_dir, exist_ok=True)
    print(f"Katalog wyjsciowy: {output_dir}")
    

    # Znalezienie plikow multimedialnych
    
    media_files = findMediaFiles(directory)
    
    if not media_files:
        print(f'Nie znaleziono żadnych plików do konwersji')
        sys.exit(1)
    
    print(f'Znaleziono: {len(media_files)} plikow')
    
    
    # Glowna petla konwersji
    converted_count = 0
    failed_count = 0
    
    for i, file in enumerate(media_files, 1):
        print(f'[{i}/{len(media_files)}] Konwersja pliku -> {Path(file).name}')
        try: 
            output_name = generateOutputFilename(file, args.format)
            output_file = os.path.join(output_dir, output_name)
            
            file_type = getFileType(file)
            
            if file_type == "image":
                success = convertWithImagemagick(file, output_file, 300)
            else:
                success = convertWithFfmpeg(file, output_file, 300)
                
            if success:
                tool_used = "magick" if file_type == "image" else "ffmpeg"
                
                history_entry = {
                        'data': datetime.now().isoformat(),
                        'plik_oryginalny': file,
                        'format_wyjsciowy': args.format,
                        'plik_wynikowy': output_file,
                        'uzyty_program': tool_used
                    }
                history_path = os.path.join(output_dir, 'history.json')
                saveHistoryJson(history_entry, history_path)
                
                history_path = os.path.join(output_dir, 'history.csv')
                saveHistoryCsv(history_entry, history_path)
                
                converted_count += 1
            else:
                failed_count += 1
                
        except KeyboardInterrupt:
            print("\n Przerwano przez uzytkownika")
            sys.exit(0)
        except Exception as e:
            print(f" Nieoczekiwany blad: {e}")
            failed_count += 1
    
    
    # Podsumowanie
    print(f"\n{'='*50}")
    print(f"    Konwersja zakonczona!")
    print(f"    Skonwertowano: {converted_count}")
    print(f"    Niepowodzenia: {failed_count}")
    print(f"    Katalog wynikowy: {output_dir}")
    print(f"{'='*50}")


# PUNKT WEJSCIA

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Przerwano przez uzytkownika")
        sys.exit(0)
    except Exception as e:
        print(f"[!] Nieoczekiwany blad: {e}", file=sys.stderr)
        sys.exit(1)