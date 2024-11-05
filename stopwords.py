import pandas as pd
import os
import requests

# Path file input dan output
input_file_path = r'C:\Users\Zahran\Documents\Punya Zahran\Zahran Unpad\Skripsi New\Code\Skripsi\tokenize_data.xlsx'
output_directory = r'C:\Users\Zahran\Documents\Punya Zahran\Zahran Unpad\Skripsi New\Code\Skripsi'
output_file_path = os.path.join(output_directory, 'stopwords_data.xlsx')

# URL untuk daftar stopwords
stopwords_url = 'https://raw.githubusercontent.com/stopwords-iso/stopwords-en/master/stopwords-en.txt'

# Mengambil daftar stopwords dari URL
response = requests.get(stopwords_url)
stopwords = set(response.text.splitlines())

# Fungsi untuk menghapus stopwords dari kalimat
def remove_stopwords(tokenized_sentence):
    return [word for word in tokenized_sentence if word.lower() not in stopwords]

try:
    # Membaca file Excel yang sudah di-tokenize
    df = pd.read_excel(input_file_path)

    # Menghapus stopwords dari setiap tweet
    df['Cleaned_Tweet'] = df['Tokenized_Tweet'].apply(eval)  # Konversi string token menjadi list
    df['Cleaned_Tweet'] = df['Cleaned_Tweet'].apply(remove_stopwords)

    # Cek dan buat direktori jika belum ada
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Menyimpan hasil ke file Excel baru
    df.to_excel(output_file_path, index=False)
    print(f"File stopwords removal berhasil disimpan di {output_file_path}")

except Exception as e:
    print(f"Terjadi kesalahan: {e}")
