import os
import time
import json
import pandas as pd
import argparse
import logging
import hashlib
import re
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from datetime import datetime

# Sabitler
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB
LOG_FILE = "tracewords_log.txt"
SUPPORTED_FORMATS = (".txt", ".json", ".csv", ".log", ".xml", ".html", ".py", ".js", ".php", ".sql", ".conf", ".ini")

# Günlük kaydı yapılandırması
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

def calculate_file_hash(filepath):
    """Dosyanın MD5 hash'ini hesaplar (dijital kanıt bütünlüğü için)."""
    try:
        hash_md5 = hashlib.md5()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception as e:
        logging.error(f"Hash hesaplanamadı {os.path.basename(filepath)}: {e}")
        return "N/A"

def read_file_content(filepath):
    """
    Dosya içeriğini okur ve küçük harfe dönüştürür.
    Büyük dosyalar için akış okuma kullanılır.
    """
    try:
        if os.path.getsize(filepath) > MAX_FILE_SIZE:
            logging.warning(f"{os.path.basename(filepath)} çok büyük, atlanıyor.")
            return ""
        
        # Dosya uzantısına göre okuma stratejisi
        if filepath.endswith((".txt", ".log", ".py", ".js", ".php", ".html", ".xml", ".sql", ".conf", ".ini")):
            content = ""
            with open(filepath, "r", encoding="utf-8", errors="ignore") as file:
                content = file.read().lower()
            return content
        elif filepath.endswith(".json"):
            with open(filepath, "r", encoding="utf-8", errors="ignore") as file:
                data = json.load(file)
                return json.dumps(data, indent=2).lower()
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

def extract_context(content, keyword, context_lines=2):
    """Anahtar kelimenin etrafındaki bağlamı çıkarır (dijital kanıt analizi için)."""
    lines = content.split('\n')
    contexts = []
    
    for i, line in enumerate(lines):
        if keyword.lower() in line.lower():
            start = max(0, i - context_lines)
            end = min(len(lines), i + context_lines + 1)
            context = {
                'line_number': i + 1,
                'context': '\n'.join(lines[start:end]),
                'matched_line': line.strip()
            }
            contexts.append(context)
    
    return contexts

def process_file(filepath, keywords, exact_match, regex_mode=False):
    """Tek bir dosyayı tarar ve dijital kanıtları döndürür."""
    logging.info(f"Dijital kanıt analizi: {os.path.basename(filepath)}")
    content = read_file_content(filepath)
    
    if not content:
        return os.path.basename(filepath), {}, [], ""
    
    matches = {}
    all_contexts = []
    file_hash = calculate_file_hash(filepath)
    
    # Dosya meta verileri (dijital kanıt için)
    stat = os.stat(filepath)
    file_info = {
        'size': stat.st_size,
        'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
        'created': datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
        'hash': file_hash
    }
    
    for keyword in keywords:
        keyword = keyword.strip()
        count = 0
        
        if regex_mode:
            # Regex arama (gelişmiş siber analiz için)
            try:
                pattern = re.compile(keyword, re.IGNORECASE)
                matches_found = pattern.findall(content)
                count = len(matches_found)
                if count > 0:
                    contexts = extract_context(content, keyword)
                    all_contexts.extend(contexts)
            except re.error as e:
                logging.error(f"Geçersiz regex pattern '{keyword}': {e}")
                continue
        else:
            keyword_lower = keyword.lower()
            if exact_match:
                # Tam kelime eşleşmesi
                word_pattern = r'\b' + re.escape(keyword_lower) + r'\b'
                matches_found = re.findall(word_pattern, content, re.IGNORECASE)
                count = len(matches_found)
            else:
                # Kısmi eşleşme
                count = content.count(keyword_lower)
            
            if count > 0:
                contexts = extract_context(content, keyword)
                all_contexts.extend(contexts)
        
        if count > 0:
            matches[keyword] = count
    
    return os.path.basename(filepath), matches, all_contexts, file_info

def search_keywords(directory, keywords, exact_match=False, regex_mode=False, recursive=False):
    """
    TraceWords: Klasördeki dosyaları paralel tarar ve dijital kanıtları döndürür.
    """
    found = {}
    start_time = time.time()
    logging.info(f"TraceWords analizi başlatıldı: {directory}")
    print(f"🔍 TraceWords dijital anahtar kelime analizi: {directory}")
    
    if not os.path.exists(directory):
        logging.error("Hedef dizin bulunamadı!")
        print("❌ Hedef dizin bulunamadı!")
        return found, 0
    
    # Dosya listesi oluştur
    files = []
    if recursive:
        for root, dirs, filenames in os.walk(directory):
            for filename in filenames:
                if filename.endswith(SUPPORTED_FORMATS):
                    files.append(os.path.join(root, filename))
    else:
        files = [
            os.path.join(directory, f) for f in os.listdir(directory)
            if f.endswith(SUPPORTED_FORMATS)
        ]
    
    file_count = len(files)
    
    if not files:
        print(f"⚠️  Desteklenen formatlarda dosya bulunamadı: {', '.join(SUPPORTED_FORMATS)}")
        logging.warning("Analiz edilecek dosya bulunamadı.")
        return found, 0
    
    print(f"📁 Desteklenen formatlar: {', '.join(SUPPORTED_FORMATS)}")
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(process_file, filepath, keywords, exact_match, regex_mode)
            for filepath in files
        ]
        
        for future in tqdm(futures, desc="Dijital kanıt analizi", unit="dosya"):
            filepath, matches, contexts, file_info = future.result()
            if matches:
                found[filepath] = {
                    "matches": matches, 
                    "contexts": contexts,
                    "file_info": file_info
                }
    
    print(f"📊 Analiz edilen dosya sayısı: {file_count}")
    print(f"⏱️  Analiz süresi: {time.time() - start_time:.2f} saniye")
    logging.info(f"TraceWords analizi tamamlandı. Dosya sayısı: {file_count}, Süre: {time.time() - start_time:.2f} saniye")
    return found, file_count

def save_report(results, output_file, directory, keywords):
    """TraceWords analiz sonuçlarını detaylı bir rapora kaydeder."""
    full_path = os.path.join(directory, output_file)
    
    if os.path.exists(full_path):
        print(f"⚠️  {output_file} zaten mevcut. Üzerine yazılsın mı? (e/h): ", end="")
        overwrite = input().lower()
        if overwrite != "e":
            print("📄 Rapor kaydedilmedi.")
            logging.info(f"Rapor kaydedilmedi: {full_path}")
            return
    
    try:
        with open(full_path, "w", encoding="utf-8") as report:
            # Rapor başlığı
            report.write("=" * 70 + "\n")
            report.write("TRACEWORDS — DİJİTAL ANAHTAR KELİME ADLİ TARAMASI RAPORU\n")
            report.write("=" * 70 + "\n")
            report.write("TraceWords v3.0 - Dijital Anahtar Kelime Adli Taraması Aracı\n")
            report.write(f"Analiz Tarihi: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            report.write(f"Aranan Terimler: {', '.join(keywords)}\n")
            report.write(f"Bulunan Dijital Kanıt Dosyası: {len(results)}\n")
            report.write(f"Analiz Edilen Dizin: {directory}\n\n")
            
            if results:
                total_matches = 0
                
                for file, data in results.items():
                    matches = data["matches"]
                    contexts = data["contexts"]
                    file_info = data["file_info"]
                    
                    report.write("-" * 60 + "\n")
                    report.write(f"DİJİTAL KANIT DOSYASI: {file}\n")
                    report.write("-" * 60 + "\n")
                    report.write(f"Dosya Boyutu: {file_info['size']:,} bytes\n")
                    report.write(f"Son Değiştirilme: {file_info['modified']}\n")
                    report.write(f"Oluşturulma Tarihi: {file_info['created']}\n")
                    report.write(f"MD5 Hash (Bütünlük): {file_info['hash']}\n\n")
                    
                    report.write("BULUNAN DİJİTAL KANITLAR:\n")
                    for keyword, count in matches.items():
                        report.write(f"  🔍 {keyword}: {count} eşleşme\n")
                        total_matches += count
                    
                    if contexts:
                        report.write("\nKANIT BAĞLAMLARI:\n")
                        for i, context in enumerate(contexts[:5], 1):  # İlk 5 bağlam
                            report.write(f"\n  [{i}] Satır {context['line_number']}:\n")
                            report.write(f"      Eşleşen: {context['matched_line']}\n")
                            report.write(f"  Bağlam:\n")
                            for line in context['context'].split('\n'):
                                report.write(f"      {line}\n")
                    
                    report.write("\n" + "=" * 60 + "\n\n")
                
                # Rapor özeti
                report.write("TRACEWORDS ANALİZ ÖZETİ\n")
                report.write("=" * 35 + "\n")
                report.write(f"Toplam Dijital Kanıt: {total_matches}\n")
                report.write(f"Kanıt İçeren Dosya Sayısı: {len(results)}\n")
                
                # En çok kanıt bulunan dosyalar
                sorted_files = sorted(results.items(), 
                                    key=lambda x: sum(x[1]["matches"].values()), 
                                    reverse=True)
                
                report.write(f"\nEn Çok Dijital Kanıt İçeren Dosyalar:\n")
                for file, data in sorted_files[:5]:
                    total_file_matches = sum(data["matches"].values())
                    report.write(f"  📁 {file}: {total_file_matches} kanıt\n")
                
            else:
                report.write("❌ HİÇBİR DİJİTAL KANIT BULUNAMADI.\n")
            
            report.write(f"\nRapor Oluşturulma: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            report.write("Bu rapor TraceWords tarafından dijital adli bilişim standartlarına uygun olarak hazırlanmıştır.\n")
        
        print(f"📋 TraceWords raporu kaydedildi: {os.path.abspath(full_path)}")
        logging.info(f"Siber adli bilişim raporu kaydedildi: {full_path}")
    except Exception as e:
        print(f"❌ Rapor kaydedilemedi: {e}")
        logging.error(f"Rapor kaydedilemedi: {e}")

def parse_args():
    """Komut satırı argümanlarını ayrıştırır."""
    parser = argparse.ArgumentParser(
        description="TraceWords — Dijital Anahtar Kelime Adli Taraması Aracı v3.0",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "directory",
        help="Analiz edilecek dizin yolu"
    )
    parser.add_argument(
        "-k", "--keywords",
        required=True,
        help="Virgülle ayrılmış arama terimleri (örn: password,admin,hack)"
    )
    parser.add_argument(
        "-e", "--exact",
        action="store_true",
        help="Tam kelime eşleşmesi (varsayılan: False)"
    )
    parser.add_argument(
        "-r", "--regex",
        action="store_true",
        help="Regex pattern arama modu"
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Alt dizinleri de analiz et"
    )
    parser.add_argument(
        "-o", "--output",
        default="tracewords_report.txt",
        help="Rapor dosya adı (varsayılan: tracewords_report.txt)"
    )
    return parser.parse_args()

def main():
    """Ana program akışı."""
    args = parse_args()
    
    if not os.path.exists(args.directory):
        print("❌ Hedef dizin bulunamadı!")
        logging.error(f"Hedef dizin bulunamadı: {args.directory}")
        return
    
    keywords = [kw.strip() for kw in args.keywords.split(",") if kw.strip()]
    if not keywords:
        print("⚠️  En az bir arama terimi girin!")
        logging.error("Arama terimi girilmedi.")
        return
    
    # Arama modunu belirle
    exact_match = args.exact
    regex_mode = args.regex
    recursive = args.recursive
    
    if not args.exact and not args.regex:
        print("🔍 TraceWords arama modu seçin:")
        print("1. Kısmi eşleşme (varsayılan)")
        print("2. Tam kelime eşleşmesi")
        print("3. Regex pattern arama")
        choice = input("Seçiminiz (1-3): ").strip()
        
        if choice == "2":
            exact_match = True
        elif choice == "3":
            regex_mode = True
    
    print(f"\n🔧 TraceWords Analiz Parametreleri:")
    print(f"  📂 Hedef Dizin: {args.directory}")
    print(f"  🔍 Arama Terimleri: {', '.join(keywords)}")
    print(f"  ✅ Tam Eşleşme: {'Evet' if exact_match else 'Hayır'}")
    print(f"  🔄 Regex Modu: {'Evet' if regex_mode else 'Hayır'}")
    print(f"  📁 Recursive: {'Evet' if recursive else 'Hayır'}")
    print(f"  📋 Desteklenen Formatlar: {', '.join(SUPPORTED_FORMATS)}")
    
    print("\n🚀 TraceWords dijital anahtar kelime analizi başlatılıyor...")
    results, file_count = search_keywords(args.directory, keywords, exact_match, regex_mode, recursive)
    
    if results:
        print(f"\n✅ {len(results)} dosyada dijital kanıt bulundu!")
        save_report(results, args.output, args.directory, keywords)
    else:
        print("\n❌ Hiçbir dijital kanıt bulunamadı.")

if __name__ == "__main__":
    print("🔍 TRACEWORDS — DİJİTAL ANAHTAR KELİME ADLİ TARAMASI ARACI v3.0")
    print("=" * 65)
    print(f"🕐 Başlangıç zamanı: {datetime.now().strftime('%H:%M:%S')}")
    logging.info("TraceWords programı başlatıldı.")
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  TraceWords analizi kullanıcı tarafından iptal edildi.")
        logging.warning("TraceWords analizi kullanıcı tarafından iptal edildi.")
    except Exception as e:
        print(f"\n❌ Beklenmeyen hata: {e}")
        logging.error(f"Beklenmeyen hata: {e}")
    finally:
        print(f"\n🏁 TraceWords analizi sona erdi - {datetime.now().strftime('%H:%M:%S')}")
        logging.info("TraceWords programı sona erdi.")
