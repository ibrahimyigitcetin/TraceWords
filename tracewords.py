import os
import time
import json
import pandas as pd

def read_file_content(filepath):
    try:
        if filepath.endswith(".txt"):
            with open(filepath, "r", encoding="utf-8", errors="ignore") as file:
                return file.read().lower()
        elif filepath.endswith(".json"):
            with open(filepath, "r", encoding="utf-8", errors="ignore") as file:
                data = json.load(file)
                return json.dumps(data).lower()
        elif filepath.endswith(".csv"):
            df = pd.read_csv(filepath, encoding="utf-8")
            return df.to_string().lower()
    except Exception as e:
        print(f"{os.path.basename(filepath)} okunamadı: {e}")
        return ""

def search_keywords(directory, keywords, exact_match=False):
    found = {}
    start_time = time.time()
    print(f"Taranan klasör: {directory}")
    if not os.path.exists(directory):
        print("Klasör bulunamadı!")
        return found
    file_count = 0
    for filename in os.listdir(directory):
        if filename.endswith((".txt", ".json", ".csv")):
            file_count += 1
            filepath = os.path.join(directory, filename)
            print(f"Tarama: {filename}")
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
            if matches:
                found[filename] = matches
    print(f"Taranan dosya sayısı: {file_count}")
    print(f"Tarama süresi: {time.time() - start_time:.2f} saniye")
    return found

def save_report(results, output_file, directory):
    full_path = os.path.join(directory, output_file)
    with open(full_path, "w", encoding="utf-8") as report:
        report.write("Dijital Adli Bilişim Raporu\n")
        report.write(f"Tarih: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        if results:
            for file, matches in results.items():
                report.write(f"Dosya: {file}\n")
                for keyword, count in matches.items():
                    report.write(f"  - {keyword}: {count} eşleşme\n")
                report.write("\n")
        else:
            report.write("Hiçbir eşleşme bulunamadı.\n")
    print(f"Rapor kaydedildi: {os.path.abspath(full_path)}")

def main():
    dir_path = input("Taranacak klasör yolunu gir: ").strip()
    if not os.path.exists(dir_path):
        print("Klasör bulunamadı!")
        return
    
    keywords = input("Aranacak kelimeleri virgülle ayırarak gir (örn: hata,şifre): ").split(",")
    keywords = [kw.strip() for kw in keywords if kw.strip()]
    if not keywords:
        print("En az bir kelime gir!")
        return
    
    match_type = input("Tam eşleşme (e/h): ").strip().lower()
    exact_match = True if match_type == "e" else False
    
    output_file = input("Rapor dosya adını gir (örn: rapor.txt): ").strip() or "forensic_report.txt"
    
    print("\nTarama yapılıyor...")
    results = search_keywords(dir_path, keywords, exact_match)
    save_report(results, output_file, dir_path)

if __name__ == "__main__":
    print("Dijital Adli Bilişim Analiz Aracı")
    print(f"Başlangıç saati: {time.strftime('%H:%M:%S', time.localtime())}")
    try:
        main()
    except KeyboardInterrupt:
        print("\nTarama iptal edildi.")
    except Exception as e:
        print(f"Hata oluştu: {e}")
    finally:
        print("Program sona erdi.")