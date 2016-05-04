"""
Part 3 of the Ruhlman Project: Topic Modeling of the abstracts

Sorry that this is not in ipynb format- I was working with it as a script!
"""

#Megan O'Keefe. Last update 5/3/16
from __future__ import print_function
import numpy as np
import pandas as pd
import nltk
import re
import os
import codecs
from sklearn import feature_extraction
import mpld3
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans


def tokenize_and_stem(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    stems = [stemmer.stem(t) for t in filtered_tokens]
    return stems

def tokenize_only(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    return filtered_tokens


with open("data/removal.txt") as f:
    raw = f.readlines()

synopses = [r.lower().decode('unicode_escape').encode('ascii','ignore') for r in raw]


stopwords = nltk.corpus.stopwords.words('english')
stemmer = SnowballStemmer("english")

#not super pythonic, no, not at all.
#use extend so it's a big flat list of vocab
totalvocab_stemmed = []
totalvocab_tokenized = []
for i in synopses:
    allwords_stemmed = tokenize_and_stem(i) #for each item in 'synopses', tokenize/stem
    totalvocab_stemmed.extend(allwords_stemmed) #extend the 'totalvocab_stemmed' list
    allwords_tokenized = tokenize_only(i)
    totalvocab_tokenized.extend(allwords_tokenized)

vocab_frame = pd.DataFrame({'words': totalvocab_tokenized}, index = totalvocab_stemmed)

#define vectorizer parameters
#tfidf_vectorizer = TfidfVectorizer(max_df=0.8, max_features=200000, min_df=0.2, stop_words='english', use_idf=True, #tokenizer=tokenize_and_stem, ngram_range=(1,3))


#replaced vectorizer with a wider one (smaller min, bigger max) and doesn't use IDF because this seemed to not pick up any words....
tfidf_vectorizer = TfidfVectorizer(max_df=0.99, max_features=10000, min_df=0.01, stop_words='english', use_idf=False, ngram_range=(1,1))

tfidf_matrix = tfidf_vectorizer.fit_transform(synopses) #fit the vectorizer to synopses
print(tfidf_matrix.shape)
terms = tfidf_vectorizer.get_feature_names()

num_clusters = 13
km = KMeans(n_clusters=num_clusters)
km.fit(tfidf_matrix)
clusters = km.labels_.tolist()

from sklearn.externals import joblib
joblib.dump(km,  'doc_cluster.pkl')
km = joblib.load('doc_cluster.pkl')
clusters = km.labels_.tolist()

#PRINT CLUSTERS

print("Top terms per cluster:")
print()
order_centroids = km.cluster_centers_.argsort()[:, ::-1]

for i in range(num_clusters):
    print("Cluster %d words:" % i, end='')

    for ind in order_centroids[i, :40]: #replace 6 with n words per cluster
        if str(vocab_frame.ix[terms[ind].split(' ')].values.tolist()[0][0]) != 'nan':
            print(' %s' % vocab_frame.ix[terms[ind].split(' ')].values.tolist()[0][0], end=',')
    print() #add whitespace
    print() #add whitespace
