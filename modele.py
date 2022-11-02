import sys

import numpy as np

import re
import string
import pandas as pd

import spacy

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

def remove_words(l):
    selected_words = load(saves+"selected_words.joblib")
    l = [w for w in l if (w in selected_words)]
    l = [w for w in l if (len(w) > 1)]
    return l

def combine_text(list_of_text):
    '''Takes a list of text and combines them into one large chunk of text.'''
    combined_text = ' '.join(list_of_text)
    return combined_text

def preprocess_sentence(txt, combine=True):
    nlp = spacy.load("en_core_web_sm")
    txt = norm_text(txt)
    tokens = nlp(txt)
    tokens = [token.lemma_ for token in tokens if str(token) != ' ']
    tokens = remove_words(tokens)
    if combine:
        return combine_text(tokens)
    return tokens

#########################
# Analyse via le modele #
#########################

def extract_features(s):
    tokenizer_lstm = load(saves+"tokenizer_lstm.joblib")
    X = tokenizer_lstm.texts_to_sequences(pd.Series([s]))
    X = pad_sequences(X)
    l = len(X[0,:])
    X = np.hstack((np.zeros((1,31-l)), X))
    return X

def extract_result(X):
    model = load(saves+"model_1_bi_lstm.joblib")
    r = model.predict(X, verbose=0)
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

"""
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

    print(sentiment_tweet(s))
"""