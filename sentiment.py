from apiclient.discovery import build
import pandas as pd
import time
import nltk
from nltk.probability import *
from nltk.corpus import stopwords
import pandas as pd
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
import csv


        
all = pd.read_csv("comments.csv")

stop_eng = stopwords.words('english')
customstopwords =[]

tokens = []
sentences = []
tokenizedSentences =[]
print("comments:",all.Comment)

for txt in all.Comment:
    sentences.append(txt.lower())
    tokenized = [t.lower().strip(":,.!?") for t in txt.split()]
    tokens.extend(tokenized)
    tokenizedSentences.append(tokenized)

hashtags = [w for w in tokens if w.startswith('#')]
ghashtags = [w for w in tokens if w.startswith('+')]
mentions = [w for w in tokens if w.startswith('@')]
links = [w for w in tokens if w.startswith('http') or w.startswith('www')]
filtered_tokens = [w for w in tokens if not w in stop_eng and not w in customstopwords and w.isalpha() and not len(w)<3 and not w in hashtags and not w in ghashtags and not w in links and not w in mentions]

fd = FreqDist(filtered_tokens)


###############
def word_feats(words):
    return dict([(word, True) for word in words])
###############

negids = movie_reviews.fileids('neg')
posids = movie_reviews.fileids('pos')
 
negfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
posfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posids]

trainfeats = negfeats + posfeats
 
classifier = NaiveBayesClassifier.train(trainfeats)
###############
csvs = ["Comments_scraped1.csv","Comments_scraped2.csv"]
ctr =1
for csv in csvs:
    all = pd.read_csv(csv)

    all['tokenized'] = all['Comment'].apply(lambda x: [t.lower().strip(":,.!?") for t in x.split()] )
    all['sentiment'] = all['tokenized'].apply(lambda x: classifier.prob_classify(word_feats(x)).prob('pos') - classifier.prob_classify(word_feats(x)).prob('neg') )
    header = ["Comment", "sentiment"]
    all.to_csv('Output'+str(ctr)+'.csv', columns = header)
    ctr+=1


