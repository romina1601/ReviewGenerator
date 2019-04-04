from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
import nltk


class sentimentAnalyzer:
    def __init__(self):
        pass

    @staticmethod
    def analyzeSentence(sentence):
        sid = SentimentIntensityAnalyzer()
        ss = sid.polarity_scores(sentence)
        return ss
    
    @staticmethod
    def identifyPOS(sentence):
        sentence = nltk.word_tokenize(sentence)
        pos = nltk.pos_tag(sentence)
        return pos
