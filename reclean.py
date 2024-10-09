import pandas as pd
import re
import os
from textblob import TextBlob
import html  # Untuk menghapus entitas HTML lebih efisien

# Path file input
excel_file_path = 'processed_data.xlsx'

# Daftar kata-kata informal yang ingin dilewati
informal_words = [
    'ain’t', 'ASAP', 'babe', 'bday', 'bff', 'bffls', 'bet', 'bby', 'brb', 'bruh', 'chillin', 
    "c'mon", 'cu', 'cuz', 'dead', 'dawg', 'dunno', 'damn', 'dam', 'emo', 'fam', 'friggin', 
    'fr', 'frfr', 'gr8', 'graceeeeee', 'gimme', "g'morning", 'gonna', 'gotta', 'gunna', 
    'h', 'hmu', 'hell no', 'hell yes', 'hella', "how's it goin", 'id', 'idk', 'ikr', 'im', 
    'it’s all good', 'jk', 'k', 'kinda', 'l', 'lame', 'lemme', 'lol', 'lmao', 'm8', 'me thinks', 
    'n', 'n/a', 'probs', 'p', 'pissed', 'plz', 'rn', 'rip', 's', 'smh', 'sm', 'sry', 'sup', 
    'tbh', 'tis', 'tmi', 'tired of everything', 'ty', 'u', 'ur', 'w', 'w/', 'wtf', 'who tf', 
    'w/', 'xoxo', 'ya', 'y', 'yep', 'yolo'
]

# Fungsi untuk mengoreksi kata jika tidak ada dalam list informal
def correct_word(word):
    # Jika kata ada dalam daftar kata informal, biarkan tetap
    if word.lower() in informal_words:
        return word
    
    # Normalisasi huruf berulang (misalnya "goooood" menjadi "good")
    word = re.sub(r'(.)\1{2,}', r'\1', word)
    
    # Koreksi ejaan menggunakan TextBlob
    blob = TextBlob(word)
    try:
        return str(blob.correct())
    except Exception as e:
        print(f"Error pada TextBlob: {e}")
        return word  # Kembali ke kata asli jika terjadi error

# Fungsi untuk mengoreksi seluruh kalimat
def correct_sentence(sentence):
    if not isinstance(sentence, str):
        return ''  # Jika bukan string (misalnya NaN), kembalikan string kosong
    
    # Pisahkan kalimat menjadi kata-kata
    words = sentence.split()
    
    # Koreksi tiap kata satu per satu
    corrected_words = [correct_word(word) for word in words]
    
    # Gabungkan kata-kata yang sudah dikoreksi menjadi kalimat
    return ' '.join(corrected_words)

try:
    # Membaca file Excel
    df = pd.read_excel(excel_file_path)  # Membaca file excel
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]  # Menghapus kolom kosong

    # Menghapus username Twitter, karakter non-ASCII, URL, hashtag, dan entitas HTML
    df['Tweet'] = df['Tweet'].astype(str)  # Konversi semua entri menjadi string
    df['Tweet'] = df['Tweet'].str.replace(r'@\w+', '', regex=True)  # Hapus username
    df['Tweet'] = df['Tweet'].str.replace(r'[^\x00-\x7F]+', '', regex=True)  # Hapus karakter non-ASCII
    df['Tweet'] = df['Tweet'].str.replace(r'https?://\S+', '', regex=True)  # Hapus URL
    df['Tweet'] = df['Tweet'].str.replace(r'#\w+', '', regex=True)  # Hapus hashtag
    df['Tweet'] = df['Tweet'].apply(lambda x: html.unescape(x))  # Menghapus entitas HTML (lebih menyeluruh)

    # Menghapus emotikon seperti XDDDD, :-D, :-P
    emoticons_pattern = r'X+D+|:-[DPdp]'  # Regex untuk XDDDD dan variasi :-D, :-P
    df['Tweet'] = df['Tweet'].str.replace(emoticons_pattern, '', regex=True)

    # Normalisasi kata dengan huruf berulang (contoh: Gooooood -> good)
    df['Tweet'] = df['Tweet'].str.replace(r'(.)\1{2,}', r'\1', regex=True)

    # Terapkan koreksi teks pada setiap tweet
    df['Tweet'] = df['Tweet'].apply(correct_sentence)

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