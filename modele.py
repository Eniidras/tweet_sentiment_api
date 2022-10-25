import sys

import numpy as np

import re
import string
import pandas as pd
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from keras.preprocessing.text import Tokenizer
from keras_preprocessing.sequence import pad_sequences

from joblib import load
saves="saves/"

#######################
# Traitement du texte #
#######################

def norm_text(text):
    '''Make text lowercase, remove text in square brackets,remove links,remove punctuation
    and remove words containing numbers and starting with @.'''
    text = text.lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('@\w*', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)
    return text

def lem_word(x):
    lem = WordNetLemmatizer()
    return [lem.lemmatize(w) for w in x]

def combine_text(list_of_text):
    '''Takes a list of text and combines them into one large chunk of text.'''
    combined_text = ' '.join(list_of_text)
    return combined_text

def remove_words(l):
    selected_words = load(saves+"selected_words.joblib")
    l = [w for w in l if (w in selected_words)]
    l = [w for w in l if (len(w) > 1)]
    return l

def preprocess_sentence(w):
    '''Apply some preprocess functions on a sentence, 
    returns a string if combine=True, else returns a string list'''

    # To transform sentences into list of words
    tokenizer_preproc=RegexpTokenizer(r'\w+')
    tokenize_text = lambda x:tokenizer_preproc.tokenize(x)

    w = norm_text(w) # Normalize sentences format
    wt = tokenize_text(w) 
    wt = lem_word(wt) # apply lemmatization
    wt = remove_words(wt)
    wt = wt[:32]
    w = combine_text(wt)
    return w



def extract_features(s):
    tokenizer_lstm = load(saves+"tokenizer_lstm.joblib")
    X = tokenizer_lstm.texts_to_sequences(pd.Series([s]))
    X = pad_sequences(X)
    l = len(X[0,:])
    X = np.hstack((np.zeros((1,32-l)), X))
    return X



def extract_result(X):
    model = load(saves+"model_1_bi_lstm.joblib")
    r = model.predict(X)
    i = np.argmax(r)
    if i:
        return "positive"
    else:
        return "negative"
    return r

def sentiment_tweet(s):
    s = preprocess_sentence(s)
    X = extract_features(s)
    result = extract_result(X)
    return result

if __name__ == "__main__":
    if len(sys.argv) == 1:
        sentence = input("Saisir le texte à tester : ")
    else:
        sentence = sys.argv[1]
    s = sentence

    print("Phrase à étudier :")
    print(sentence)

    sentence = preprocess_sentence(sentence)
    print("\nPhrase nettoyée :")
    print(sentence)

    X = extract_features(sentence)
    print("\nLongueur du vecteur :", X.shape)

    result = extract_result(X)

    print("\nResultat :", result)

    sentiment_tweet(s)