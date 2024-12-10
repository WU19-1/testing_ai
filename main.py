# import library
import nltk
from nltk.corpus import stopwords, words
from nltk.stem import WordNetLemmatizer
import pandas as pd
from html import unescape
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report

# download stopwords, english words, tagging for verb or nouns
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('words')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger_eng')
stop_words = set(stopwords.words("english"))
words = words.words()

# lemmatizer
lemmatizer = WordNetLemmatizer()

# initialize for new preprocessed text

data = {
    "tweets": []
}

# read the data
df = pd.read_csv("./raw.csv")

for i in df.index:
    # remove mentions and html encoded strings
    cleaned_tweet = re.sub(r"@\w+", "", unescape(df["tweet"][i])).strip()

    # remove hashtags
    cleaned_tweet = re.sub(r"#\w+", "", cleaned_tweet).strip()

    # only take words, remove all symbols
    cleaned_tweet = re.sub(r"[^a-zA-Z0-9\s]", "", cleaned_tweet)

    # filter all stop words
    # filtered_words = [word for word in cleaned_tweet.lower().split(" ") if word not in stop_words]

    # lemmatize the words
    # cleaned_tweet = [lemmatizer.lemmatize(word) for word in cleaned_tweet.lower().split()]
    cleaned_tweet = cleaned_tweet.lower().split()
    pos_tags = nltk.pos_tag(cleaned_tweet)

    for i, obj in enumerate(pos_tags):
        # lemmatize nouns
        if obj[1].startswith("NN"):
            cleaned_tweet[i] = lemmatizer.lemmatize(obj[0], pos="n")
        # lemmatize verbs
        elif obj[1].startswith("VB"):
            cleaned_tweet[i] = lemmatizer.lemmatize(obj[0], pos="v")
        # lemmatize without information
        else:
            cleaned_tweet[i] = obj[0]

    # filter non english words like name
    cleaned_tweet = [word for word in cleaned_tweet if word in words]
    
    # replace the actual tweet with the filtered words
    data["tweets"].append(" ".join(cleaned_tweet))
    # df["suicide"][i] = df["suicide"][i].strip()
    df.loc[i, "suicide"] = df["suicide"][i].strip()

new_df = pd.DataFrame(data)

# seperate dataset and labels
tweets = new_df["tweets"]
sentiments = df["suicide"]

# feature extraction
vectorizer = TfidfVectorizer()
tweets = vectorizer.fit_transform(tweets)

# train model with test from 20% of the data set
tweets_train, tweets_test, sentiments_train, sentiments_test = train_test_split(tweets, sentiments, test_size=0.2, random_state=42)

# create and train a naive bayes classifier
clf = MultinomialNB()
clf.fit(tweets_train, sentiments_train)

# make predictions on the test set
sentiments_prediction = clf.predict(tweets_test)

# evaluate model, trying to get > 50%
print(classification_report(sentiments_test, sentiments_prediction))

# make unlimited input to read from command line and evalute with current model
while True:
    sentence = input("Insert text for you to predict: ")
    # remove mentions and html encoded strings
    sentence = re.sub(r"@\w+", "", sentence).strip()
    print("\nfirst {}".format(sentence))

    # remove hashtags
    sentence = re.sub(r"#\w+", "", sentence).strip()
    print("\nsecond {}".format(sentence))

    # only take words, remove all symbols
    sentence = re.sub(r"[^a-zA-Z0-9\s]", "", sentence)
    print("\nthird {}".format(sentence))

    # filter all stop words
    # sentence = [word for word in sentence.split(" ") if word not in stop_words]
    # print("\nfourth {}".format(sentence))

    # lemmatize all words
    # sentence = [lemmatizer.lemmatize(word) for word in sentence.lower().split(" ")]
    sentence = sentence.lower().split(" ")
    pos_tags = nltk.pos_tag(sentence)

    for i, obj in enumerate(pos_tags):
        if obj[1].startswith("NN"):
            sentence[i] = lemmatizer.lemmatize(obj[0], pos="n")
        elif obj[1].startswith("VB"):
            sentence[i] = lemmatizer.lemmatize(obj[0], pos="v")
        else:
            sentence[i] = obj[0]
    print("\nfourth {}".format(sentence))

    # filter non english words like name
    sentence = [word for word in sentence if word in words]
    print("\nfifth {}".format(sentence))

    sentence = " ".join(sentence)

    print("\nnew sentence: {}".format(sentence))

    sentence_vectorized = vectorizer.transform([sentence])
    prediction = clf.predict(sentence_vectorized)
    print("prediction: {}".format(" ".join(prediction).strip()))
