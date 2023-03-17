import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

# Load data
df = pd.read_excel('/Users/mrina/Downloads/careeronestop_data.xlsx')

# Clean data
df.drop(["job_link"], axis=1, inplace=True)
df.dropna(inplace=True)
df.reset_index(drop=True, inplace=True)

# Tokenize and lemmatize job descriptions
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
stop_words = stopwords.words("english")
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    words = word_tokenize(text.lower())
    words = [w for w in words if w.isalpha() and w not in stop_words]
    words = [lemmatizer.lemmatize(w) for w in words]
    return " ".join(words)

df["description_cleaned"] = df["description"].apply(preprocess_text)

# Topic modeling using LDA
n_topics = 5
vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
doc_word = vectorizer.fit_transform(df["description_cleaned"])
lda_model = LatentDirichletAllocation(n_components=n_topics, max_iter=10, learning_method='online')
doc_topic = lda_model.fit_transform(doc_word)

# Visualize topics
top_n_words = 10
feature_names = vectorizer.get_feature_names()
topic_keywords = []
for topic_weights in lda_model.components_:
    top_keyword_locs = (-topic_weights).argsort()[:top_n_words]
    topic_keywords.append([feature_names[i] for i in top_keyword_locs])
    
df_topic_keywords = pd.DataFrame(topic_keywords)
df_topic_keywords.columns = ["Word " + str(i) for i in range(1, top_n_words+1)]
df_topic_keywords.index = ["Topic " + str(i) for i in range(1, n_topics+1)]
print(df_topic_keywords)

# Visualize topic weights
df_topic_weights = pd.DataFrame(doc_topic)
df_topic_weights.columns = ["Topic " + str(i) for i in range(1, n_topics+1)]
df_topic_weights["Dominant Topic"] = df_topic_weights.idxmax(axis=1)
df_topic_weights["Job Title"] = df["job_title"]
df_topic_weights["Description"] = df["description_cleaned"]
print(df_topic_weights.head())

# Plot histogram of topic weights
fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(20, 10))
for i, ax in enumerate(axes.flatten()):
    if i < n_topics:
        ax.hist(df_topic_weights["Topic " + str(i+1)], bins=30)
        ax.set_title("Topic " + str(i+1))
plt.tight_layout()

# Plot dominant topics for each job title
fig, ax = plt.subplots(figsize=(10, 6))
sns.countplot(x="Dominant Topic", hue="Job Title", data=df_topic_weights, ax=ax)
ax.set_title("Dominant Topic Count by Job Title")
plt.show()

