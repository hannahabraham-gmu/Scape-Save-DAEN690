import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('vader_lexicon')
nltk.download('wordnet')
nltk.download('omw-1.4')

# Load the data into a pandas DataFrame
data = pd.read_excel("C:/Users/mrina/Downloads/careeronestop_data.xlsx")

# Clean and preprocess the data
stop_words = set(stopwords.words('english'))
data['description'] = data['description'].apply(lambda x: x.lower())
data['description'] = data['description'].apply(lambda x: ' '.join([word for word in x.split() if word not in stop_words]))
data['description'] = data['description'].apply(lambda x: ''.join([word for word in x if word.isalpha() or word.isspace()]))
data['description'] = data['description'].apply(lambda x: x.strip())

# Tokenize the job descriptions
data['tokens'] = data['description'].apply(lambda x: word_tokenize(x))

# Perform named entity recognition
def get_entities(tokens):
    entities = []
    for token in tokens:
        if nltk.pos_tag([token])[0][1] == 'NNP':
            entities.append(token)
    return entities

data['entities'] = data['tokens'].apply(lambda x: get_entities(x))

# Perform sentiment analysis
sia = SentimentIntensityAnalyzer()
data['sentiment'] = data['description'].apply(lambda x: sia.polarity_scores(x)['compound'])

# Perform topic modeling
lemmatizer = WordNetLemmatizer()
data['lemmatized'] = data['tokens'].apply(lambda x: [lemmatizer.lemmatize(word) for word in x])
vectorizer = CountVectorizer(tokenizer=lambda x: x, lowercase=False)
doc_term_matrix = vectorizer.fit_transform(data['lemmatized'])
lda = LatentDirichletAllocation(n_components=5, random_state=42)
lda.fit(doc_term_matrix)
topics = lda.transform(doc_term_matrix)
data['topic'] = topics.argmax(axis=1)

# Visualize the results
import matplotlib.pyplot as plt
import seaborn as sns
sns.countplot(x='topic', data=data)
plt.xlabel('Topic')
plt.ylabel('Count')
plt.title('Job Demand by Topic')
