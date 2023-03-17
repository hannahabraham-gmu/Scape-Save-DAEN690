# Import necessary libraries
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
# Load the job description data
df = pd.read_excel('C:/Users/mrina/Downloads/careeronestop_data.xlsx')

# Pre-process the data
# (remove any unwanted columns, clean the text data, etc.)
def clean_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove punctuation and numbers
    text = re.sub(r"[^a-zA-Z]", " ", text)
    # Tokenize the text
    tokens = word_tokenize(text)
    # Remove stop words
    stop_words = set(stopwords.words("english"))
    tokens = [token for token in tokens if not token in stop_words]
    # Lemmatize the tokens
    lemmatizer = nltk.stem.WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    # Join the tokens back into a string
    clean_text = " ".join(tokens)
    return clean_text

# Clean the "description" column
df["clean_description"] = df["description"].apply(clean_text)
# Create a bag-of-words representation of the job descriptions
vectorizer = CountVectorizer(stop_words='english', max_features=5000)
bow = vectorizer.fit_transform(df['clean_description'])

# Apply k-means clustering to the bag-of-words data
kmeans = KMeans(n_clusters=5)
kmeans.fit(bow)

# Get the cluster labels for each job description
labels = kmeans.labels_

# Output the results
for i in range(5):
    print(f"Cluster {i}:")
    for j in range(len(df)):
        if labels[j] == i:
            print(f"  - {df['job_title'][j]}")