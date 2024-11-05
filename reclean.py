import pandas as pd
import re
import os
import html  # Untuk menghapus entitas HTML lebih efisien
import spacy

# Memuat model bahasa Inggris dari spaCy
nlp = spacy.load("en_core_web_sm")

# Path file input
excel_file_path = 'processed_data.xlsx'

# Daftar kata yang ingin diperluas
contractions = {
    r"\bI'm\b": "I am",
    r"\bIm\b": "I am",
    r"\bhe's\b": "he is",
    r"\bshe's\b": "she is",
    r"\bwe're\b": "we are",
    r"\bthey're\b": "they are",
    r"\bit's\b": "it is",
    r"\bits\b": "it is",
    r"\bthat's\b": "that is",
    r"\bthere's\b": "there is",
    r"\bwho's\b": "who is",
    r"\byou're\b": "you are",
    r"\bthey've\b": "they have",
    r"\bwe've\b": "we have",
    r"\bI've\b": "i have",
    r"\byou've\b": "you have",
    r"\bcan't\b": "cannot",
    r"\bcant\b": "cannot",
    r"\bcan t\b": "cannot",
    r"\bi'll\b": "i will",
    r"\bill\b": "i will",
    r"\bwon't\b": "will not",
    r"\bdon't\b": "do not",
    r"\bdon t\b": "do not",
    r"\bdont\b": "do not",
    r"\bdoesn't\b": "does not",
    r"\bdidn't\b": "did not",
    r"\bcouldn't\b": "could not",
    r"\bshouldn't\b": "should not",
    r"\bwasn't\b": "was not",
    r"\bweren't\b": "were not",
    r"\bain’t\b": "is not",
    r"\byou’ve\b": "you have",
    r"\bu’ve\b": "you have",
    r"\buve\b": "you have",
    r"\bwanna\b": "want to",
    r"\bwana\b": "want to",
}

# Daftar kata informal yang ingin dilewati
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

# Daftar kata kerja bantu yang harus diabaikan dari lemmatization
auxiliary_verbs = ["is", "are", "was", "were", "am", "be", "been", "being"]

# Fungsi untuk memperluas kontraksi
def expand_contractions(text):
    for contraction, expanded in contractions.items():
        text = re.sub(contraction, expanded, text, flags=re.IGNORECASE)
    return text

# Fungsi untuk mengoreksi kata jika tidak ada dalam list informal
def correct_word(word):
    # Jika kata ada dalam daftar kata informal, biarkan tetap
    if word.lower() in informal_words:
        return word
    
    # Lemmatization untuk kata yang bukan kata kerja bantu
    doc = nlp(word)
    lemmatized_word = [token.lemma_ for token in doc][0]  # Ambil lemmatization pertama

    # Jika kata kerja bantu ditemukan, kembalikan kata aslinya
    if word.lower() in auxiliary_verbs:
        return word
    
    return lemmatized_word

# Fungsi untuk menghapus tanda baca di awal kalimat
def remove_punctuation_at_start(text):
    return re.sub(r'^[\W_]+', '', text)

# Fungsi untuk menghapus semua tanda baca dari teks
def remove_all_punctuation(text):
    # Menghapus semua karakter yang bukan huruf atau angka
    return re.sub(r'[^\w\s]', '', text)

# Fungsi untuk mengoreksi seluruh kalimat
def correct_sentence(sentence):
    if not isinstance(sentence, str):
        return ''  # Jika bukan string (misalnya NaN), kembalikan string kosong
    
    # Mengubah semua huruf menjadi huruf kecil
    sentence = sentence.lower()
    
    # Menghapus tanda baca di awal kalimat
    sentence = remove_punctuation_at_start(sentence)

    # Menghapus semua tanda baca
    sentence = remove_all_punctuation(sentence)
    
    # Memperluas kontraksi terlebih dahulu
    sentence = expand_contractions(sentence)

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

    # Konversi semua entri menjadi huruf kecil (case folding)
    df['Tweet'] = df['Tweet'].str.lower()

    # Menghapus "rt" (retweet) di awal kalimat
    df['Tweet'] = df['Tweet'].str.replace(r'\brt\b', '', regex=True)

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