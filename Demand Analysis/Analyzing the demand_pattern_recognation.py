#About the program:This code initially builds a text preprocessing function that lowercases, eliminates punctuation and numerals, tokenizes, removes stop words, lemmatizes, and connects tokens back into a string.Then, the code applies the text preprocessing function to the dataset's "description" column and generates a "clean description" column with the cleaned text.After cleaning the text, the code produces a lexicon and corpus for topic modeling, trains an LSI model, and publishes the top 10 topics.Lastly, the code utilizes regular expressions to find "experience," "knowledge," and "skills" patterns in the "description" column and publishes the job title and cleaned description for every entry that matches#

import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from gensim import models
from gensim.corpora import Dictionary

# Load the dataset
df = pd.read_excel('C:/Users/mrina/Downloads/careeronestop_data.xlsx')

# Define a function for text preprocessing
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

# Create a dictionary and corpus for topic modeling
documents = df["clean_description"].tolist()
dictionary = Dictionary([doc.split() for doc in documents])
corpus = [dictionary.doc2bow(doc.split()) for doc in documents]

# Train an LSI model and print the top 10 topics
lsi_model = models.LsiModel(corpus, id2word=dictionary, num_topics=10)
for i, topic in enumerate(lsi_model.show_topics(num_topics=10, num_words=10)):
    print(f"Topic {i}: {topic[1]}")

# Identify patterns in the "description" column using regular expressions
for i, row in df.iterrows():
    if re.search(r"\bexperience\b|\bknowledge\b|\bskills\b", row["clean_description"]):
        print(f"{row['job_title']}: {row['clean_description']}")

# Interpretting the output: 
#Examine the subject titles: This should show you the algorithm's data topics.
#Analyze each topic's top words: This shows the most prevalent terms for each subject.
#Topic distribution: This shows how often each subject is in your data. 
#Study the pattern recognition results to see the algorithm's data patterns.
#Lastly, apply your domain expertise to generalize the findings. 