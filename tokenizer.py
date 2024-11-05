import pandas as pd
import spacy
import os

# Memuat model bahasa Inggris dari spaCy
nlp = spacy.load("en_core_web_sm")

# Path file input
input_file_path = 'clean_data.xlsx'

# Path file output
output_directory = 'C:/Users/Zahran/Documents/Punya Zahran/Zahran Unpad/Skripsi New/Code/Skripsi'
output_file_path = os.path.join(output_directory, 'tokenize_data.xlsx')

# Fungsi untuk tokenisasi
def tokenize_sentence(sentence):
    if isinstance(sentence, str):  # Pastikan input adalah string
        doc = nlp(sentence)
        return [token.text for token in doc]
    else:
        return []  # Kembalikan list kosong jika input bukan string

try:
    # Membaca file Excel
    df = pd.read_excel(input_file_path)

    # Pastikan kolom 'Tweet' tidak mengandung NaN dan ubah semua nilai menjadi string
    df['Tweet'] = df['Tweet'].fillna('').astype(str)

    # Tokenisasi tiap tweet
    df['Tokenized_Tweet'] = df['Tweet'].apply(tokenize_sentence)

    # Cek dan buat direktori jika belum ada
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Menyimpan hasil tokenisasi ke file Excel baru
    df.to_excel(output_file_path, index=False)
    print(f"File tokenisasi berhasil disimpan di {output_file_path}")

except Exception as e:
    # Menampilkan pesan kesalahan jika terjadi error
    print(f"Terjadi kesalahan: {e}")
