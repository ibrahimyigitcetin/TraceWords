import os
import time
import json
import pandas as pd
import argparse
import logging
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

# Sabitler
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB
LOG_FILE = "forensic.log"

# Günlük kaydı yapılandırması
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

def read_file_content(filepath):
    """
    Dosya içeriğini okur ve küçük harfe dönüştürür.
    Büyük .txt dosyaları için akış okuma kullanılır.
    """
    try:
        if os.path.getsize(filepath) > MAX_FILE_SIZE:
            logging.warning(f"{os.path.basename(filepath)} çok büyük, atlanıyor.")
            return ""
        
        if filepath.endswith(".txt"):
            content = ""
            with open(filepath, "r", encoding="utf-8", errors="ignore") as file:
                for chunk in file:
                    content += chunk.lower()
            return content
        elif filepath.endswith(".json"):
            with open(filepath, "r", encoding="utf-8", errors="ignore") as file:
                data = json.load(file)
                return json.dumps(data).lower()
        elif filepath.endswith(".csv"):
            df = pd.read_csv(filepath, encoding="utf-8")
            return df.to_string().lower()
    except FileNotFoundError:
        logging.error(f"{os.path.basename(filepath)} bulunamadı.")
    except UnicodeDecodeError:
        logging.error(f"{os.path.basename(filepath)} okunamadı: Kodlama hatası.")
    except json.JSONDecodeError:
        logging.error(f"{os.path.basename(filepath)} geçersiz JSON formatında.")
    except pd.errors.ParserError:
        logging.error(f"{os.path.basename(filepath)} geçersiz CSV formatında.")
    except PermissionError:
        logging.error(f"{os.path.basename(filepath)} erişim izni yok.")
    except Exception as e:
        logging.error(f"{os.path.basename(filepath)} okunamadı: {e}")
    return ""

def process_file(filepath, keywords, exact_match):
    """Tek bir dosyayı tarar ve eşleşmeleri döndürür."""
    logging.info(f"Tarama: {os.path.basename(filepath)}")
    content = read_file_content(filepath)
    matches = {}
    for keyword in keywords:
        keyword = keyword.lower().strip()
        if exact_match:
            if keyword in content.split():
                matches[keyword] = content.count(keyword)
        else:
            if keyword in content:
                matches[keyword] = content.count(keyword)
    return os.path.basename(filepath), matches

def search_keywords(directory, keywords, exact_match=False):
    """
    Klasördeki dosyaları paralel tarar ve eşleşmeleri döndürür.
    """
    found = {}
    start_time = time.time()
    logging.info(f"Taranan klasör: {directory}")
    print(f"Taranan klasör: {directory}")
    
    if not os.path.exists(directory):
        logging.error("Klasör bulunamadı!")
        print("Klasör bulunamadı!")
        return found, 0
    
    files = [
        os.path.join(directory, f) for f in os.listdir(directory)
        if f.endswith((".txt", ".json", ".csv"))
    ]
    file_count = len(files)
    
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(process_file, filepath, keywords, exact_match)
            for filepath in files
        ]
        for future in tqdm(futures, desc="Dosyalar taranıyor", unit="dosya"):
            filename, matches = future.result()
            if matches:
                found[filename] = matches
    
    print(f"Taranan dosya sayısı: {file_count}")
    print(f"Tarama süresi: {time.time() - start_time:.2f} saniye")
    logging.info(f"Tarama tamamlandı. Dosya sayısı: {file_count}, Süre: {time.time() - start_time:.2f} saniye")
    return found, file_count

def save_report(results, output_file, directory):
    """Tarama sonuçlarını bir rapora kaydeder."""
    full_path = os.path.join(directory, output_file)
    
    if os.path.exists(full_path):
        print(f"{output_file} zaten mevcut. Üzerine yazılsın mı? (e/h): ", end="")
        overwrite = input().lower()
        if overwrite != "e":
            print("Rapor kaydedilmedi.")
            logging.info(f"Rapor kaydedilmedi: {full_path}")
            return
    
    try:
        with open(full_path, "w", encoding="utf-8") as report:
            report.write("Dijital Anahtar Kelime Adli Taraması Aracı Raporu\n")
            report.write(f"Tarih: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            if results:
                for file, matches in results.items():
                    report.write(f"Dosya: {file} (Son değiştirilme: {time.ctime(os.path.getmtime(os.path.join(directory, file)))})\n")
                    for keyword, count in matches.items():
                        report.write(f"  - {keyword}: {count} eşleşme\n")
                    report.write("\n")
            else:
                report.write("Hiçbir eşleşme bulunamadı.\n")
        print(f"Rapor kaydedildi: {os.path.abspath(full_path)}")
        logging.info(f"Rapor kaydedildi: {full_path}")
    except Exception as e:
        print(f"Rapor kaydedilemedi: {e}")
        logging.error(f"Rapor kaydedilemedi: {e}")

def parse_args():
    """Komut satırı argümanlarını ayrıştırır."""
    parser = argparse.ArgumentParser(
        description="Dijital Anahtar Kelime Adli Taraması Aracı",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "directory",
        help="Taranacak klasör yolu"
    )
    parser.add_argument(
        "-k", "--keywords",
        required=True,
        help="Virgülle ayrılmış anahtar kelimeler (örn: hata,şifre)"
    )
    parser.add_argument(
        "-e", "--exact",
        action="store_true",
        help="Tam kelime eşleşmesi"
    )
    parser.add_argument(
        "-o", "--output",
        default="forensic_report.txt",
        help="Rapor dosya adı (varsayılan: forensic_report.txt)"
    )
    return parser.parse_args()

def main():
    """Ana program akışı."""
    args = parse_args()
    
    if not os.path.exists(args.directory):
        print("Klasör bulunamadı!")
        logging.error(f"Klasör bulunamadı: {args.directory}")
        return
    
    keywords = [kw.strip() for kw in args.keywords.split(",") if kw.strip()]
    if not keywords:
        print("En az bir kelime gir!")
        logging.error("Anahtar kelime girilmedi.")
        return
    
    print("\nTarama yapılıyor...")
    results, file_count = search_keywords(args.directory, keywords, args.exact)
    save_report(results, args.output, args.directory)

if __name__ == "__main__":
    print("Dijital Anahtar Kelime Adli Taraması Aracı")
    print(f"Başlangıç saati: {time.strftime('%H:%M:%S', time.localtime())}")
    logging.info("Program başlatıldı.")
    try:
        main()
    except KeyboardInterrupt:
        print("\nTarama iptal edildi.")
        logging.warning("Tarama kullanıcı tarafından iptal edildi.")
    except Exception as e:
        print(f"Hata oluştu: {e}")
        logging.error(f"Hata oluştu: {e}")
    finally:
        print("Program sona erdi.")
        logging.info("Program sona erdi.")
