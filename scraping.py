import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL target berita CNN Indonesia
url_target = "https://www.cnnindonesia.com/nasional/20261004121954-20-1411432/kualitas-udara-makassar-memburuk-bmkg-duga-imbas-asap-karhutla"

# Mengatur headers agar dikenali sebagai browser
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

print("Sedang menghubungkan ke website CNN Indonesia...")
response = requests.get(url_target, headers=headers)

if response.status_code == 200:
    print("Berhasil terhubung!\n")
    
    # Parsing HTML dengan BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")
    
    # 1. Mengambil Judul Berita
    title_tag = soup.find("h1")
    judul_berita = title_tag.get_text(strip=True) if title_tag else "Judul tidak ditemukan"
    
    # 2. Mengambil Isi Berita (Semua paragraf <p>)
    paragraphs = soup.find_all("p")
    paragraf_list = []
    
    for p in paragraphs:
        text = p.get_text(strip=True)
        # Menyaring teks agar bersih dari iklan/footer
        if text and len(text) > 30 and "ADVERTISEMENT" not in text and "SCROLL TO CONTINUE" not in text:
            paragraf_list.append(text)
            
    # Menggabungkan seluruh paragraf menjadi satu teks utuh
    isi_lengkap = "\n\n".join(paragraf_list)
    
    # Menampilkan hasil di terminal
    print("=== JUDUL BERITA ===")
    print(judul_berita)
    print(f"\nTotal paragraf valid ditemukan: {len(paragraf_list)}")
    
    # 3. Memasukkan data ke Pandas DataFrame
    data = {
        "Judul Berita": [judul_berita],
        "Isi Berita": [isi_lengkap],
        "URL Sumber": [url_target]
    }
    
    df = pd.DataFrame(data)
    
    # 4. Menyimpan otomatis ke file CSV dan Excel
    nama_file_csv = "hasil_scraping.csv"
    nama_file_excel = "hasil_scraping.xlsx"
    
    # Menyimpan ke CSV
    df.to_csv(nama_file_csv, index=False, encoding="utf-8-sig")
    
    # Menyimpan ke XLSX (Excel)
    try:
        df.to_excel(nama_file_excel, index=False)
        print(f"\nBerhasil! File otomatis dibuat:\n- {nama_file_csv}\n- {nama_file_excel}")
    except Exception as e:
        print(f"\nFile CSV berhasil disimpan, namun untuk format Excel pastikan sudah menginstal openpyxl (jalankan: pip install openpyxl)")

else:
    print(f"Gagal mengakses halaman. Status code: {response.status_code}")
    