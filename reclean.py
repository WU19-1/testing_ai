import pandas as pd
import re
import os
from textblob import TextBlob

# Path file input
excel_file_path = 'processed_data.xlsx'

try:
    # Membaca file Excel
    df = pd.read_excel(excel_file_path)  # read file excel
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]  # hapus kolom kosong

    # Menghapus username Twitter, karakter non-ASCII, URL, hashtag, dan entitas HTML
    df['Tweet'] = df['Tweet'].str.replace(r'@\w+', '', regex=True)  # hapus username
    df['Tweet'] = df['Tweet'].str.replace(r'[^\x00-\x7F]+', '', regex=True)  # hapus karakter non-ASCII
    df['Tweet'] = df['Tweet'].str.replace(r'https?://\S+', '', regex=True)  # hapus URL
    df['Tweet'] = df['Tweet'].str.replace(r'#\w+', '', regex=True)  # hapus hashtag
    df['Tweet'] = df['Tweet'].str.replace('&quot', '', regex=False)  # hapus entitas HTML &quot
    df['Tweet'] = df['Tweet'].str.replace('&lt', '', regex=False)  # hapus entitas HTML &quot

    # Menghapus emotikon seperti XDDDD, :-D, :-P
    emoticons_pattern = r'X+D+|:-[DPdp]'  # Regex untuk XDDDD dan variasi :-D, :-P
    df['Tweet'] = df['Tweet'].str.replace(emoticons_pattern, '', regex=True)

    # Normalisasi kata dengan huruf berulang (contoh: Gooooood -> good)
    df['Tweet'] = df['Tweet'].str.replace(r'(.)\1{2,}', r'\1', regex=True)

    # Mengatasi NaN dengan mengisi entri yang kosong
    df['Tweet'] = df['Tweet'].fillna('')  # Mengganti NaN dengan string kosong

    # Koreksi ejaan otomatis menggunakan TextBlob (hanya untuk teks yang tidak kosong)
    def correct_text(text):
        if text.strip():  # Hanya proses jika teks tidak kosong
            blob = TextBlob(text)
            return str(blob.correct())
        return text  # Kembalikan teks aslinya jika kosong

    df['Tweet'] = df['Tweet'].apply(correct_text)

    # print(df.head(10)) #print hasil

    # Path untuk menyimpan file
    output_directory = 'C:/Users/Zahran/Documents/Punya Zahran/Zahran Unpad/Skripsi New/Code/Skripsi'
    output_file_path = os.path.join(output_directory, 'clean_data.xlsx')

    # Cek dan buat direktori jika belum ada
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Menyimpan hasil ke file Excel, menimpa file lama
    df.to_excel(output_file_path, index=False) 
    print(f"File berhasil ditimpa di {output_file_path}")

except Exception as e:
    # Menampilkan pesan kesalahan
    print(f"Terjadi kesalahan: {e}")