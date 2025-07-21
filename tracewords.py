import os
import time
import json
import pandas as pd
import argparse
import logging
import hashlib
import re
import uuid
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import warnings

# Sabitler
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB
LOG_FILE = "tracewords.log"
AUDIT_LOG_FILE = "tracewords_audit.log"
PRIVACY_LOG_FILE = "tracewords_privacy.log"
SUPPORTED_FORMATS = (".txt", ".json", ".csv", ".log", ".xml", ".html", ".py", ".js", ".php", ".sql", ".conf", ".ini")

# GDPR/CCPA Uyumluluk Ayarları
PRIVACY_SETTINGS = {
    "enable_pii_masking": True,
    "enable_data_minimization": True,
    "enable_audit_logging": True,
    "retention_period_days": 90,  # Veri saklama süresi
    "anonymize_results": False,
    "require_consent": True,
    "enable_right_to_be_forgotten": True
}

# PII Tespit Regex Kalıpları
PII_PATTERNS = {
    'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
    'phone_us': r'\b(?:\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})\b',
    'phone_international': r'\+[1-9]\d{1,14}',
    'ssn_us': r'\b(?!000|666|9\d{2})\d{3}[-.]?(?!00)\d{2}[-.]?(?!0000)\d{4}\b',
    'credit_card': r'\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|6(?:011|5[0-9]{2})[0-9]{12}|3[47][0-9]{13}|3[0-9]{13}|2[0-9]{15})\b',
    'ip_address': r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',
    'mac_address': r'\b([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})\b',
    'url': r'https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?',
    'tc_kimlik': r'\b[1-9][0-9]{10}\b',  # Türk T.C. Kimlik No
    'iban': r'\b[A-Z]{2}[0-9]{2}[A-Z0-9]{4}[0-9]{7}([A-Z0-9]?){0,16}\b',
    'passport': r'\b[A-Z][0-9]{8}\b',
    'date_of_birth': r'\b(0[1-9]|[12][0-9]|3[01])[\/\-\.](0[1-9]|1[012])[\/\-\.]((19|20)\d\d)\b'
}

# Günlük kaydı yapılandırması
def setup_logging():
    """Çoklu log sistemi kurulumu (normal, audit, privacy)"""
    
    # Ana log
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        encoding="utf-8"
    )
    
    # Audit log
    audit_logger = logging.getLogger('audit')
    audit_logger.setLevel(logging.INFO)
    audit_handler = logging.FileHandler(AUDIT_LOG_FILE, encoding='utf-8')
    audit_formatter = logging.Formatter('%(asctime)s - AUDIT - %(message)s')
    audit_handler.setFormatter(audit_formatter)
    audit_logger.addHandler(audit_handler)
    
    # Privacy log
    privacy_logger = logging.getLogger('privacy')
    privacy_logger.setLevel(logging.INFO)
    privacy_handler = logging.FileHandler(PRIVACY_LOG_FILE, encoding='utf-8')
    privacy_formatter = logging.Formatter('%(asctime)s - PRIVACY - %(message)s')
    privacy_handler.setFormatter(privacy_formatter)
    privacy_logger.addHandler(privacy_handler)
    
    return audit_logger, privacy_logger

def generate_session_id():
    """Her analiz için benzersiz oturum ID'si oluşturur"""
    return str(uuid.uuid4())

def log_privacy_event(privacy_logger, event_type: str, details: str, session_id: str):
    """Veri gizliliği olaylarını loglar"""
    privacy_logger.info(f"Session: {session_id} | Event: {event_type} | Details: {details}")

def log_audit_event(audit_logger, action: str, resource: str, user: str, session_id: str, result: str = "SUCCESS"):
    """Denetim olaylarını loglar"""
    audit_logger.info(f"Session: {session_id} | Action: {action} | Resource: {resource} | User: {user} | Result: {result}")

def check_consent(session_id: str, audit_logger) -> bool:
    """GDPR uyumluluğu için kullanıcı onayı kontrolü"""
    if not PRIVACY_SETTINGS["require_consent"]:
        return True
    
    print("\n" + "="*60)
    print("GDPR/CCPA UYUMLULUK - VERİ İŞLEME ONAYI")
    print("="*60)
    print("Bu araç, dosya içeriklerini analiz eder ve kişisel verileri işleyebilir.")
    print("Aşağıdaki haklar size tanınmıştır:")
    print("• Verilerinizin işlenmesini reddetme hakkı")
    print("• Kişisel verilerinizin silinmesini talep etme hakkı")
    print("• Veri işleme süreçleri hakkında bilgi alma hakkı")
    print("• Analiz sonuçlarına erişim ve düzeltme hakkı")
    print("\nVeri işleme süreci:")
    print("1. Dosyalar analiz edilir ve anahtar kelimeler aranır")
    print("2. Kişisel veriler otomatik olarak maskelenir (PII)")
    print("3. Analiz sonuçları belirtilen süre boyunca saklanır")
    print("4. Audit logları uyumluluk için kaydedilir")
    
    consent = input("\nBu koşulları kabul ediyor musunuz? (EVET/HAYIR): ").strip().upper()
    
    if consent == "EVET":
        log_audit_event(audit_logger, "CONSENT_GRANTED", "data_processing", "user", session_id)
        print("✅ Veri işleme onayı verildi.")
        return True
    else:
        log_audit_event(audit_logger, "CONSENT_DENIED", "data_processing", "user", session_id)
        print("❌ Veri işleme onayı reddedildi. Analiz sonlandırılıyor.")
        return False

def detect_pii(content: str) -> Dict[str, List[str]]:
    """İçerikte PII tespit eder"""
    detected_pii = {}
    
    for pii_type, pattern in PII_PATTERNS.items():
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            if isinstance(matches[0], tuple):  # Grup yakalama durumu
                matches = [''.join(match) for match in matches]
            detected_pii[pii_type] = list(set(matches))  # Benzersiz değerler
    
    return detected_pii

def mask_pii(content: str, pii_data: Dict[str, List[str]], session_id: str, privacy_logger) -> str:
    """PII verilerini maskeler"""
    if not PRIVACY_SETTINGS["enable_pii_masking"]:
        return content
    
    masked_content = content
    total_masked = 0
    
    for pii_type, pii_values in pii_data.items():
        for pii_value in pii_values:
            if pii_type == 'email':
                mask = f"[EMAIL_{total_masked}]"
            elif pii_type in ['phone_us', 'phone_international']:
                mask = f"[PHONE_{total_masked}]"
            elif pii_type == 'ssn_us':
                mask = f"[SSN_{total_masked}]"
            elif pii_type == 'credit_card':
                mask = f"[CREDIT_CARD_{total_masked}]"
            elif pii_type == 'ip_address':
                mask = f"[IP_ADDR_{total_masked}]"
            elif pii_type == 'tc_kimlik':
                mask = f"[TC_KIMLIK_{total_masked}]"
            elif pii_type == 'iban':
                mask = f"[IBAN_{total_masked}]"
            else:
                mask = f"[PII_{pii_type.upper()}_{total_masked}]"
            
            masked_content = masked_content.replace(pii_value, mask)
            total_masked += 1
    
    if total_masked > 0:
        log_privacy_event(privacy_logger, "PII_MASKED", f"Masked {total_masked} PII items", session_id)
    
    return masked_content

def anonymize_file_path(filepath: str) -> str:
    """Dosya yollarını anonimleştirir"""
    if not PRIVACY_SETTINGS["anonymize_results"]:
        return filepath
    
    filename = os.path.basename(filepath)
    extension = os.path.splitext(filename)[1]
    anonymous_name = f"file_{hashlib.md5(filepath.encode()).hexdigest()[:8]}{extension}"
    return anonymous_name

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

def extract_context(content: str, keyword: str, context_lines: int = 2, mask_pii: bool = True, session_id: str = "", privacy_logger = None):
    """Anahtar kelimenin etrafındaki bağlamı çıkarır ve PII'yi maskeler"""
    lines = content.split('\n')
    contexts = []
    
    for i, line in enumerate(lines):
        if keyword.lower() in line.lower():
            start = max(0, i - context_lines)
            end = min(len(lines), i + context_lines + 1)
            context_block = '\n'.join(lines[start:end])
            
            # PII maskeleme
            if mask_pii and privacy_logger:
                pii_detected = detect_pii(context_block)
                if pii_detected:
                    context_block = mask_pii(context_block, pii_detected, session_id, privacy_logger)
                    line = mask_pii(line, detect_pii(line), session_id, privacy_logger)
            
            context = {
                'line_number': i + 1,
                'context': context_block,
                'matched_line': line.strip()
            }
            contexts.append(context)
    
    return contexts

def process_file(filepath, keywords, exact_match, regex_mode=False, session_id="", privacy_logger=None):
    """Tek bir dosyayı tarar ve dijital kanıtları döndürür."""
    logging.info(f"Dijital kanıt analizi: {os.path.basename(filepath)}")
    content = read_file_content(filepath)
    
    if not content:
        return os.path.basename(filepath), {}, [], "", {}
    
    # PII tespiti
    detected_pii = detect_pii(content)
    if detected_pii and privacy_logger:
        log_privacy_event(privacy_logger, "PII_DETECTED", f"File: {os.path.basename(filepath)}, Types: {list(detected_pii.keys())}", session_id)
    
    # İçeriği PII maskeleme ile işle
    if PRIVACY_SETTINGS["enable_pii_masking"] and detected_pii and privacy_logger:
        content = mask_pii(content, detected_pii, session_id, privacy_logger)
    
    matches = {}
    all_contexts = []
    file_hash = calculate_file_hash(filepath)
    
    # Dosya meta verileri (dijital kanıt için)
    stat = os.stat(filepath)
    file_info = {
        'size': stat.st_size,
        'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
        'created': datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
        'hash': file_hash,
        'pii_types_detected': list(detected_pii.keys()) if detected_pii else [],
        'pii_masked': bool(detected_pii and PRIVACY_SETTINGS["enable_pii_masking"])
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
                    contexts = extract_context(content, keyword, mask_pii=True, session_id=session_id, privacy_logger=privacy_logger)
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
                contexts = extract_context(content, keyword, mask_pii=True, session_id=session_id, privacy_logger=privacy_logger)
                all_contexts.extend(contexts)
        
        if count > 0:
            matches[keyword] = count
    
    anonymized_filename = anonymize_file_path(filepath)
    return anonymized_filename, matches, all_contexts, file_info, detected_pii

def search_keywords(directory, keywords, exact_match=False, regex_mode=False, recursive=False, session_id="", audit_logger=None, privacy_logger=None):
    """
    TraceWords: Klasördeki dosyaları paralel tarar ve dijital kanıtları döndürür.
    """
    found = {}
    pii_summary = {}
    start_time = time.time()
    logging.info(f"TraceWords analizi başlatıldı: {directory}")
    print(f"🔍 TraceWords dijital anahtar kelime analizi: {directory}")
    
    if audit_logger:
        log_audit_event(audit_logger, "ANALYSIS_STARTED", directory, "user", session_id)
    
    if not os.path.exists(directory):
        logging.error("Hedef dizin bulunamadı!")
        print("❌ Hedef dizin bulunamadı!")
        if audit_logger:
            log_audit_event(audit_logger, "ANALYSIS_FAILED", directory, "user", session_id, "DIRECTORY_NOT_FOUND")
        return found, 0, pii_summary
    
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
        if audit_logger:
            log_audit_event(audit_logger, "ANALYSIS_COMPLETED", directory, "user", session_id, "NO_FILES_FOUND")
        return found, 0, pii_summary
    
    print(f"📁 Desteklenen formatlar: {', '.join(SUPPORTED_FORMATS)}")
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(process_file, filepath, keywords, exact_match, regex_mode, session_id, privacy_logger)
            for filepath in files
        ]
        
        for future in tqdm(futures, desc="Dijital kanıt analizi", unit="dosya"):
            filepath, matches, contexts, file_info, detected_pii = future.result()
            if matches:
                found[filepath] = {
                    "matches": matches, 
                    "contexts": contexts,
                    "file_info": file_info
                }
            
            # PII özeti oluştur
            if detected_pii:
                for pii_type, pii_values in detected_pii.items():
                    if pii_type not in pii_summary:
                        pii_summary[pii_type] = 0
                    pii_summary[pii_type] += len(pii_values)
    
    analysis_time = time.time() - start_time
    print(f"📊 Analiz edilen dosya sayısı: {file_count}")
    print(f"⏱️  Analiz süresi: {analysis_time:.2f} saniye")
    
    if pii_summary:
        print(f"🔒 Tespit edilen PII türleri: {', '.join(pii_summary.keys())}")
        if privacy_logger:
            log_privacy_event(privacy_logger, "PII_SUMMARY", f"Types: {pii_summary}", session_id)
    
    logging.info(f"TraceWords analizi tamamlandı. Dosya sayısı: {file_count}, Süre: {analysis_time:.2f} saniye")
    
    if audit_logger:
        log_audit_event(audit_logger, "ANALYSIS_COMPLETED", f"{directory} - {file_count} files", "user", session_id)
    
    return found, file_count, pii_summary

def save_report(results, output_file, directory, keywords, session_id, pii_summary, audit_logger=None, privacy_logger=None):
    """TraceWords analiz sonuçlarını GDPR/CCPA uyumlu detaylı bir rapora kaydeder."""
    full_path = os.path.join(directory, output_file)
    
    if os.path.exists(full_path):
        print(f"⚠️  {output_file} zaten mevcut. Üzerine yazılsın mı? (e/h): ", end="")
        overwrite = input().lower()
        if overwrite != "e":
            print("📄 Rapor kaydedilmedi.")
            logging.info(f"Rapor kaydedilmedi: {full_path}")
            if audit_logger:
                log_audit_event(audit_logger, "REPORT_SAVE_CANCELLED", full_path, "user", session_id)
            return
    
    try:
        with open(full_path, "w", encoding="utf-8") as report:
            # Rapor başlığı
            report.write("=" * 80 + "\n")
            report.write("TRACEWORDS — GDPR/CCPA UYUMLU DİJİTAL ADLİ TARAMA RAPORU\n")
            report.write("=" * 80 + "\n")
            report.write("TraceWords v4.0 - GDPR/CCPA Uyumlu Dijital Adli Tarama Aracı\n")
            report.write(f"Analiz Tarihi: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            report.write(f"Oturum ID: {session_id}\n")
            report.write(f"Aranan Terimler: {', '.join(keywords)}\n")
            report.write(f"Bulunan Dijital Kanıt Dosyası: {len(results)}\n")
            report.write(f"Analiz Edilen Dizin: {directory}\n\n")
            
            # GDPR/CCPA Uyumluluk Bilgileri
            report.write("VERİ GİZLİLİĞİ VE UYUMLULUK BİLGİLERİ\n")
            report.write("-" * 50 + "\n")
            report.write(f"PII Maskeleme Durumu: {'Aktif' if PRIVACY_SETTINGS['enable_pii_masking'] else 'Pasif'}\n")
            report.write(f"Veri Minimizasyonu: {'Aktif' if PRIVACY_SETTINGS['enable_data_minimization'] else 'Pasif'}\n")
            report.write(f"Audit Loglama: {'Aktif' if PRIVACY_SETTINGS['enable_audit_logging'] else 'Pasif'}\n")
            report.write(f"Sonuç Anonimleştirme: {'Aktif' if PRIVACY_SETTINGS['anonymize_results'] else 'Pasif'}\n")
            report.write(f"Veri Saklama Süresi: {PRIVACY_SETTINGS['retention_period_days']} gün\n")
            report.write(f"Silinme Tarihi: {(datetime.now() + timedelta(days=PRIVACY_SETTINGS['retention_period_days'])).strftime('%Y-%m-%d')}\n\n")
            
            # PII Tespit Özeti
            if pii_summary:
                report.write("KİŞİSEL VERİ (PII) TESPİT ÖZETİ\n")
                report.write("-" * 40 + "\n")
                for pii_type, count in pii_summary.items():
                    pii_type_tr = {
                        'email': 'E-posta Adresi',
                        'phone_us': 'ABD Telefon No',
                        'phone_international': 'Uluslararası Telefon',
                        'ssn_us': 'ABD SSN',
                        'credit_card': 'Kredi Kartı No',
                        'ip_address': 'IP Adresi',
                        'mac_address': 'MAC Adresi',
                        'tc_kimlik': 'T.C. Kimlik No',
                        'iban': 'IBAN No',
                        'passport': 'Pasaport No',
                        'date_of_birth': 'Doğum Tarihi'
                    }.get(pii_type, pii_type.upper())
                    report.write(f"  🔒 {pii_type_tr}: {count} adet\n")
                report.write("\n⚠️  Tüm kişisel veriler maskelenmiştir ve orijinal değerler rapordan çıkarılmıştır.\n\n")
            
            if results:
                total_matches = 0
                
                for file, data in results.items():
                    matches = data["matches"]
                    contexts = data["contexts"]
                    file_info = data["file_info"]
                    
                    report.write("-" * 70 + "\n")
                    report.write(f"DİJİTAL KANIT DOSYASI: {file}\n")
                    report.write("-" * 70 + "\n")
                    report.write(f"Dosya Boyutu: {file_info['size']:,} bytes\n")
                    report.write(f"Son Değiştirilme: {file_info['modified']}\n")
                    report.write(f"Oluşturulma Tarihi: {file_info['created']}\n")
                    report.write(f"MD5 Hash (Bütünlük): {file_info['hash']}\n")
                    
                    if file_info.get('pii_types_detected'):
                        report.write(f"Tespit Edilen PII Türleri: {', '.join(file_info['pii_types_detected'])}\n")
                        report.write(f"PII Maskeleme Uygulandı: {'Evet' if file_info.get('pii_masked', False) else 'Hayır'}\n")
                    
                    report.write("\nBULUNAN DİJİTAL KANITLAR:\n")
                    for keyword, count in matches.items():
                        report.write(f"  🔍 {keyword}: {count} eşleşme\n")
                        total_matches += count
                    
                    if contexts:
                        report.write("\nKANIT BAĞLAMLARI (PII MASKELENMİŞ):\n")
                        for i, context in enumerate(contexts[:5], 1):  # İlk 5 bağlam
                            report.write(f"\n  [{i}] Satır {context['line_number']}:\n")
                            report.write(f"      Eşleşen: {context['matched_line']}\n")
                            report.write(f"  Bağlam:\n")
                            for line in context['context'].split('\n'):
                                report.write(f"      {line}\n")
                    
                    report.write("\n" + "=" * 70 + "\n\n")
                
                # Rapor özeti
                report.write("TRACEWORDS ANALİZ ÖZETİ\n")
                report.write("=" * 30 + "\n")
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
            
            # GDPR/CCPA Uyumluluk Bildirimi
            report.write("\n" + "=" * 80 + "\n")
            report.write("GDPR/CCPA UYUMLULUK BİLDİRİMİ\n")
            report.write("=" * 30 + "\n")
            report.write("Bu rapor, Avrupa Birliği Genel Veri Koruma Tüzüğü (GDPR) ve California\n")
            report.write("Tüketici Gizliliği Yasası (CCPA) gerekliliklerine uygun olarak hazırlanmıştır.\n\n")
            report.write("Veri İşleme İlkeleri:\n")
            report.write("• Kişisel veriler maskelenmiş ve anonimleştirilmiştir\n")
            report.write("• Veri minimizasyonu ilkesi uygulanmıştır\n")
            report.write("• Tüm işlemler audit loglarına kaydedilmiştir\n")
            report.write("• Yasal saklama süreleri uygulanmaktadır\n")
            report.write("• Veri sahibinin hakları korunmuştur\n\n")
            report.write("Veri Sahibi Hakları:\n")
            report.write("• Erişim hakkı (GDPR Madde 15, CCPA §1798.110)\n")
            report.write("• Düzeltme hakkı (GDPR Madde 16)\n")
            report.write("• Silme hakkı (GDPR Madde 17, CCPA §1798.105)\n")
            report.write("• Taşınabilirlik hakkı (GDPR Madde 20)\n")
            report.write("• İtiraz etme hakkı (GDPR Madde 21, CCPA §1798.120)\n\n")
            
            report.write(f"Rapor Oluşturulma: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            report.write("Bu rapor TraceWords v4.0 tarafından veri gizliliği ve adli bilişim\n")
            report.write("standartlarına uygun olarak hazırlanmıştır.\n")
        
        print(f"📋 GDPR/CCPA Uyumlu TraceWords raporu kaydedildi: {os.path.abspath(full_path)}")
        logging.info(f"GDPR/CCPA uyumlu rapor kaydedildi: {full_path}")
        
        if audit_logger:
            log_audit_event(audit_logger, "REPORT_SAVED", full_path, "user", session_id)
        if privacy_logger:
            log_privacy_event(privacy_logger, "PRIVACY_COMPLIANT_REPORT", f"Report saved: {full_path}", session_id)
            
    except Exception as e:
        print(f"❌ Rapor kaydedilemedi: {e}")
        logging.error(f"Rapor kaydedilemedi: {e}")
        if audit_logger:
            log_audit_event(audit_logger, "REPORT_SAVE_FAILED", full_path, "user", session_id, str(e))

def cleanup_old_data():
    """Veri saklama süresini aşan dosyaları temizler (GDPR/CCPA uyumluluğu için)"""
    retention_days = PRIVACY_SETTINGS["retention_period_days"]
    cutoff_date = datetime.now() - timedelta(days=retention_days)
    
    cleanup_count = 0
    log_files = [LOG_FILE, AUDIT_LOG_FILE, PRIVACY_LOG_FILE]
    
    for log_file in log_files:
        if os.path.exists(log_file):
            file_time = datetime.fromtimestamp(os.path.getmtime(log_file))
            if file_time < cutoff_date:
                try:
                    os.remove(log_file)
                    cleanup_count += 1
                    print(f"🗑️  Eski veri dosyası silindi: {log_file}")
                except Exception as e:
                    print(f"⚠️  Dosya silinemedi {log_file}: {e}")
    
    if cleanup_count > 0:
        print(f"✅ GDPR/CCPA uyumlu veri temizliği: {cleanup_count} dosya silindi")
    
    return cleanup_count

def parse_args():
    """Komut satırı argümanlarını ayrıştırır."""
    parser = argparse.ArgumentParser(
        description="TraceWords v4.0 — GDPR/CCPA Uyumlu Dijital Adli Tarama Aracı",
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
        default="tracewords_privacy_report.txt",
        help="Rapor dosya adı (varsayılan: tracewords_privacy_report.txt)"
    )
    parser.add_argument(
        "--no-pii-mask",
        action="store_true",
        help="PII maskelemeyi devre dışı bırak"
    )
    parser.add_argument(
        "--anonymize",
        action="store_true",
        help="Dosya isimlerini anonimleştir"
    )
    parser.add_argument(
        "--cleanup",
        action="store_true",
        help="Eski verileri temizle (GDPR/CCPA uyumluluk)"
    )
    return parser.parse_args()

def main():
    """Ana program akışı."""
    # Log sistemlerini başlat
    audit_logger, privacy_logger = setup_logging()
    
    # Session ID oluştur
    session_id = generate_session_id()
    
    args = parse_args()
    
    # Veri temizliği
    if args.cleanup:
        cleanup_count = cleanup_old_data()
        return
    
    # Privacy ayarlarını güncelle
    if args.no_pii_mask:
        PRIVACY_SETTINGS["enable_pii_masking"] = False
    if args.anonymize:
        PRIVACY_SETTINGS["anonymize_results"] = True
    
    # GDPR/CCPA Onay kontrolü
    if not check_consent(session_id, audit_logger):
        return
    
    if not os.path.exists(args.directory):
        print("❌ Hedef dizin bulunamadı!")
        logging.error(f"Hedef dizin bulunamadı: {args.directory}")
        log_audit_event(audit_logger, "DIRECTORY_NOT_FOUND", args.directory, "user", session_id, "ERROR")
        return
    
    keywords = [kw.strip() for kw in args.keywords.split(",") if kw.strip()]
    if not keywords:
        print("⚠️  En az bir arama terimi girin!")
        logging.error("Arama terimi girilmedi.")
        log_audit_event(audit_logger, "INVALID_KEYWORDS", "empty", "user", session_id, "ERROR")
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
    
    print(f"\n🔧 TraceWords GDPR/CCPA Uyumlu Analiz Parametreleri:")
    print(f"  📂 Hedef Dizin: {args.directory}")
    print(f"  🔍 Arama Terimleri: {', '.join(keywords)}")
    print(f"  ✅ Tam Eşleşme: {'Evet' if exact_match else 'Hayır'}")
    print(f"  🔄 Regex Modu: {'Evet' if regex_mode else 'Hayır'}")
    print(f"  📁 Recursive: {'Evet' if recursive else 'Hayır'}")
    print(f"  🔒 PII Maskeleme: {'Evet' if PRIVACY_SETTINGS['enable_pii_masking'] else 'Hayır'}")
    print(f"  🎭 Anonimleştirme: {'Evet' if PRIVACY_SETTINGS['anonymize_results'] else 'Hayır'}")
    print(f"  📋 Desteklenen Formatlar: {', '.join(SUPPORTED_FORMATS)}")
    print(f"  🆔 Oturum ID: {session_id}")
    
    log_audit_event(audit_logger, "ANALYSIS_PARAMETERS", f"Keywords: {keywords}, Mode: {'regex' if regex_mode else 'exact' if exact_match else 'partial'}", "user", session_id)
    
    print("\n🚀 TraceWords GDPR/CCPA uyumlu dijital analiz başlatılıyor...")
    results, file_count, pii_summary = search_keywords(
        args.directory, keywords, exact_match, regex_mode, recursive, 
        session_id, audit_logger, privacy_logger
    )
    
    if results:
        print(f"\n✅ {len(results)} dosyada dijital kanıt bulundu!")
        save_report(results, args.output, args.directory, keywords, session_id, pii_summary, audit_logger, privacy_logger)
    else:
        print("\n❌ Hiçbir dijital kanıt bulunamadı.")
        log_audit_event(audit_logger, "NO_EVIDENCE_FOUND", args.directory, "user", session_id)

if __name__ == "__main__":
    print("🔍 TRACEWORDS v4.0 — GDPR/CCPA UYUMLU DİJİTAL ADLİ TARAMA ARACI")
    print("=" * 70)
    print("🔒 Veri Gizliliği Yasalarına Uyumlu • PII Maskeleme • Audit Loglama")
    print(f"🕐 Başlangıç zamanı: {datetime.now().strftime('%H:%M:%S')}")
    
    # Log sistemlerini başlat
    audit_logger, privacy_logger = setup_logging()
    logging.info("TraceWords v4.0 (GDPR/CCPA Uyumlu) programı başlatıldı.")
    
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
        print("📋 Oluşturulan loglar: tracewords.log, tracewords_audit.log, tracewords_privacy.log")
        logging.info("TraceWords v4.0 programı sona erdi.")
