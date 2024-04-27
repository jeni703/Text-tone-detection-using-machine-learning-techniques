# -*- coding: utf-8 -*-
"""airline dataset.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1E-zPC1ELdBPi95Nae-wU2o4b4aNr57Qi
"""

import numpy as np
import pandas as pd
import nltk
import seaborn as sns
import matplotlib.pyplot as plt

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score

nltk.download('stopwords')

nltk.download('punkt')

# Load the dataset
df = pd.read_csv("/content/Tweets.csv")

df.head(10)

df.columns

import re
def no_emo(text):
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
    return (emoji_pattern.sub(r'', text))

def clean_text(df):
    df['text'] =df['text'].apply(lambda x : x.lower().strip()) #case norm
    df['text'] =df['text'].apply(lambda x: re.sub("\S*@\S*\s?", '', x)) #email remove
    df['text'] =df['text'].apply(lambda x: re.sub(r'http\S+', '', x))# http remove
    df['text'].apply(no_emo)# remove emojis
    df['text'] =df['text'].apply(lambda x: re.sub('[^a-zA-Z\n\.]', ' ', x)) #Remove special characters, non-text characters
    df['text'] =df['text'].apply(lambda x:re.sub(r'([^\w\s]|_)+', ' ', x))#Remove repeated punctuations
    df['text'] =df['text'].apply(lambda x:re.sub(r'\s+', ' ',x))#Remove white spaces
    df['text'] = df['text'].apply(lambda x: re.sub(r'\bamp\b', '', x))

    df['text'] =df['text'].apply(lambda x:x.strip())

    return df

df['labels'] = df["airline_sentiment"].apply(lambda x: 0 if x == "negative" else 1 if x == "neutral" else 2)

import seaborn as sns
sns.set_style('whitegrid')
sns.countplot(x='labels',data=df, palette='YlGnBu_r')

import seaborn as sns
sns.set_style('whitegrid')
sns.countplot(x='airline_sentiment',data=df, palette='YlGnBu_r')

df = clean_text(df)

df.head()

sns.countplot(data=df,x='airline',hue='airline_sentiment')

sns.countplot(data=df,x='negativereason')
plt.xticks(rotation=90);

# top 20 most common words function
def common_words(rev):
    texts = df[df['airline_sentiment'] == rev]['text'].values
    vec = CountVectorizer(stop_words='english').fit(texts)
    bag_of_words = vec.transform(texts)
    sum_words = bag_of_words.sum(axis=0)
    words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
    return sorted(words_freq, key = lambda x: x[1], reverse=True)[:20]

g = sns.FacetGrid(df,col='airline_sentiment')
g.map(plt.hist,'airline_sentiment')

top_neg = dict(common_words('negative'))
pd.DataFrame.from_dict(top_neg, orient='index', columns=['count']).plot(kind='bar', figsize=(10, 6),title = 'Most common words in negative');

top_neg = dict(common_words('negative'))
pd.DataFrame.from_dict(top_neg, orient='index', columns=['count']).plot(kind='bar', figsize=(10, 6),title = 'Most common words in negative');

x = df['text']
y = df['labels']
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=101)

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

tfv = TfidfVectorizer(min_df=3,  max_features=None,
            strip_accents='unicode', analyzer='word',token_pattern=r'\w{1,}',
            ngram_range=(1, 2), use_idf=1,smooth_idf=1,sublinear_tf=1,
            stop_words = 'english')
tfv.fit(X_train)

X_train_tfv = tfv.transform(X_train)
X_test_tfv = tfv.transform(X_test)

X_train_tfv

# Train an SVR model with a linear kernel on the training data
svr = SVR(kernel='linear')
svr.fit(X_train_tfv, y_train)

df.shape

# Predict the labels of the testing data and convert the predictions to binary labels
y_pred = svr.predict(X_test_tfv)

from sklearn.metrics import ConfusionMatrixDisplay,classification_report
from sklearn.metrics import accuracy_score
def report(model):
    preds = model.predict(X_test_tfv)
    preds = pd.Series(preds).apply(lambda x: 0 if x < 0.5 else (1 if x < 1.5 else 2))
    print(classification_report(y_test,preds))
report(svr)

from sklearn.metrics import accuracy_score

len(y_test)

len(y_pred)

type(y_test)

type(y_pred)

pip install pandas

pd.Series(y_pred)

type(y_pred)

import pandas as pd
import numpy as np

np.array(y_test)

from sklearn.metrics import accuracy_score

df['text'][1]

df['labels'][1]

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
text = "plus you ve added commercials to the experience tacky"
X_test = tfv.transform([text])
pred = svr.predict(X_test)

pred

if(pred < 0.5):
  print('0')
elif(pred<1.5):
  print('2')
else:
  print('1')

"""Naive Bayes"""

from sklearn.naive_bayes import MultinomialNB
nb = MultinomialNB()
nb.fit(X_train_tfv,y_train)

report(nb)

pred = nb.predict(X_test)
if(pred < 0.5):
  print('0')
elif(pred<1.5):
  print('2')
else:
  print('1')

"""Logistic regression"""

from sklearn.linear_model import LogisticRegression
log = LogisticRegression(max_iter=1000)
log.fit(X_train_tfv,y_train)

report(log)

"""SVC"""

from sklearn.svm import LinearSVC
svc = LinearSVC()
svc.fit(X_train_tfv,y_train)

report(svc)

"""Random forest"""

from sklearn.ensemble import RandomForestClassifier

clf_rf = RandomForestClassifier()
clf_rf.fit(X_train_tfv, y_train)
y_pred_rf = clf_rf.predict(X_test_tfv)
y_pred_rf = [1 if pred > 0.5 else 0 for pred in y_pred_rf]
report(clf_rf)

"""Decision tree"""

from sklearn.tree import DecisionTreeClassifier
clf_dt = DecisionTreeClassifier()
clf_dt.fit(X_train_tfv, y_train)
y_pred_dt = clf_dt.predict(X_test_tfv)
y_pred_dt = [1 if pred > 0.5 else 0 for pred in y_pred_dt]

report(clf_dt)

"""Catboost"""

pip install catboost

import catboost
from catboost import CatBoostClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score



# Initialize the CatBoostClassifier
model = CatBoostClassifier()
# Train the model
s=model.fit(X_train_tfv, y_train)
# Make predictions on the test set
y_pred = model.predict(X_test_tfv)
# Evaluate the accuracy of the model
cat_accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {cat_accuracy}')

print("Classification Report:")
print(classification_report(y_test, y_pred))

# Confusion matrix
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

"""XGBOOST"""

pip install xgboost

import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


# Initialize the XGBoost classifier
xgmodel = xgb.XGBClassifier()

# Train the model
xgmodel.fit(X_train_tfv, y_train)

# Make predictions on the test set
y_pred = xgmodel.predict(X_test_tfv)

# Evaluate the accuracy of the model
xg_accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {xg_accuracy}')

report(xgmodel)

"""STOCHASTIC GRADIENT DESCENT"""

from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Initialize the SGDClassifier
sgdmodel = SGDClassifier(loss='log', max_iter=1000, random_state=42)

# Train the model
sgdmodel.fit(X_train_tfv, y_train)

# Make predictions on the test set
y_pred = sgdmodel.predict(X_test_tfv)

# Evaluate the accuracy of the model
sgd_accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {sgd_accuracy}')

