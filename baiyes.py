import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Path file input
input_file_path = 'C:/Users/Zahran/Documents/Punya Zahran/Zahran Unpad/Skripsi New/Code/Skripsi/stopwords_data.xlsx'

# Memuat data
try:
    df = pd.read_excel(input_file_path)

    # Menampilkan beberapa data untuk memastikan format
    print(df.head())

    # Menghapus baris dengan nilai NaN di kolom 'Tweet'
    df = df.dropna(subset=['Tweet'])

    # Mengambil kolom tweet dan category
    X = df['Tweet']  # Data fitur (tweets)
    y = df['Category']  # Target label ('suicidal post' atau 'not suicidal post')

    # Membagi data ke dalam data latih dan uji (80% latih, 20% uji)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Ekstraksi fitur dengan TF-IDF
    vectorizer = TfidfVectorizer(max_features=5000)  # Batas maksimal fitur
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    # Membuat dan melatih model Naive Bayes
    model = MultinomialNB()
    model.fit(X_train_tfidf, y_train)

    # Prediksi data uji
    y_pred = model.predict(X_test_tfidf)

    # Evaluasi model
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, target_names=['not suicidal post', 'suicidal post'])
    cm = confusion_matrix(y_test, y_pred)

    # Menampilkan hasil
    print(f"Akurasi: {accuracy:.2f}")
    print("Classification Report:")
    print(report)
    print("Confusion Matrix:")
    print(cm)

except Exception as e:
    print(f"Terjadi kesalahan: {e}")
