# -*- coding: utf-8 -*-
"""spam email classification.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1gdQ4dEGKRT1NftJ3fghn0aEXNQ2ao_sH
"""


import streamlit as st
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk

# Download NLTK data
nltk.download('stopwords')
nltk.download('wordnet')

# Streamlit app
st.title("Spam Email Classification")

# File uploader to upload a dataset
uploaded_file = st.file_uploader("Upload CSV", type="csv")

if uploaded_file is not None:
    # Load the dataset
    df = pd.read_csv(uploaded_file, encoding='latin-1')
    df = df.iloc[:, :2]
    df.columns = ['label', 'text']
    df['label'] = df['label'].map({'ham': 0, 'spam': 1})

    # Text preprocessing function
    def preprocess_text(text):
        text = re.sub(r'\W', ' ', text)  # Remove non-word characters
        text = re.sub(r'\s+', ' ', text)  # Remove extra whitespace
        text = text.lower()  # Convert to lowercase
        text = ' '.join([WordNetLemmatizer().lemmatize(word) for word in text.split()
                         if word not in stopwords.words('english')])  # Remove stopwords and lemmatize
        return text

    # Apply preprocessing to the text data
    df['text'] = df['text'].apply(preprocess_text)

    # Plot data distribution
    def plot_data_distribution(df):
        plt.figure(figsize=(6, 4))
        sns.countplot(data=df, x='label')
        plt.title("Distribution of Spam and Ham Messages")
        plt.xlabel("Label (0 = Ham, 1 = Spam)")
        plt.ylabel("Count")
        plt.xticks([0, 1], ['Ham', 'Spam'])
        st.pyplot()

    # Generate a word cloud for spam and ham
    def generate_wordcloud(data, label):
        text = ' '.join(data[data['label'] == label]['text'])
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        title = "Spam" if label == 1 else "Ham"
        plt.title(f"Word Cloud for {title} Messages")
        st.pyplot()

    # Plot data distribution
    plot_data_distribution(df)

    # Generate word clouds
    generate_wordcloud(df, label=1)  # Spam
    generate_wordcloud(df, label=0)  # Ham

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(df['text'], df['label'], test_size=0.2, random_state=42)

    # Convert text to numerical format using TfidfVectorizer
    vectorizer = TfidfVectorizer(max_features=3000)
    X_train_vect = vectorizer.fit_transform(X_train)
    X_test_vect = vectorizer.transform(X_test)

    # Train a Multinomial Naive Bayes classifier
    model = MultinomialNB()
    model.fit(X_train_vect, y_train)

    # Make predictions
    y_pred = model.predict(X_test_vect)

    # Evaluate the model
    st.write("### Classification Report:")
    st.text(classification_report(y_test, y_pred))

    st.write("### Accuracy Score:")
    st.text(f"Accuracy: {accuracy_score(y_test, y_pred)}")

    # Plot confusion matrix
    def plot_confusion_matrix(y_test, y_pred):
        cm = confusion_matrix(y_test, y_pred)
        plt.figure(figsize=(6, 4))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Ham', 'Spam'], yticklabels=['Ham', 'Spam'])
        plt.title("Confusion Matrix")
        plt.xlabel("Predicted")
        plt.ylabel("Actual")
        st.pyplot()

    # Plot confusion matrix
    plot_confusion_matrix(y_test, y_pred)

    # Test with custom input
    custom_text = st.text_input("Enter a message to classify as Spam or Ham")
    if custom_text:
        custom_text_preprocessed = vectorizer.transform([preprocess_text(custom_text)])
        prediction = model.predict(custom_text_preprocessed)
        st.write("Prediction for custom text:", "Spam" if prediction[0] == 1 else "Ham")

