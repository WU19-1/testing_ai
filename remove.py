import pandas as pd
import re
import os

# Path file input
excel_file_path = 'raw.xlsx'

try:
    # Membaca file Excel
    df = pd.read_excel(excel_file_path)  # read file excel
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]  # hapus kolom kosong

    # Menghapus username Twitter dan karakter non-ASCII
    df['Tweet'] = df['Tweet'].str.replace(r'@\w+', '', regex=True)  # hapus username
    df['Tweet'] = df['Tweet'].str.replace(r'[^\x00-\x7F]+', '', regex=True)  # hapus karakter non-ASCII\

    # Menghapus entitas HTML seperti &quot
    df['Tweet'] = df['Tweet'].str.replace('&quot', '', regex=False)

    # Menggabungkan kolom 'Tweet', 'Tweet 2', dan 'Tweet 3' ke dalam kolom 'Tweet'
    if 'Tweet 2' in df.columns:
        df['Tweet'] = df['Tweet'] + ' ' + df['Tweet 2'].fillna('')
    if 'Tweet 3' in df.columns:
        df['Tweet'] = df['Tweet'] + ' ' + df['Tweet 3'].fillna('')

    # Memisahkan kolom 'Tweet' dan 'Category'
    df[['Tweet', 'Category']] = df['Tweet'].str.rsplit(',', n=1, expand=True)  # split Tweet dan Category

    # Membersihkan spasi di awal dan akhir string
    df['Tweet'] = df['Tweet'].str.strip()
    df['Category'] = df['Category'].str.strip()

    # Menghapus kolom 'Tweet 2' dan 'Tweet 3'
    df.drop(columns=['Tweet 2', 'Tweet 3'], inplace=True, errors='ignore')

    # print(df.head(10)) #print hasil

    # Path untuk menyimpan file
    output_directory = 'C:/Users/Zahran/Documents/Punya Zahran/Zahran Unpad/Skripsi New/Code/Skripsi'
    output_file_path = os.path.join(output_directory, 'processed_data.xlsx')

    # Cek dan buat direktori jika belum ada
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Menyimpan hasil ke file Excel, menimpa file lama
    df.to_excel(output_file_path, index=False) 
    print(f"File berhasil ditimpa di {output_file_path}")

except Exception as e:
    # Menampilkan pesan kesalahan
    print(f"Terjadi kesalahan: {e}")