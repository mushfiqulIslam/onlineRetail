import pickle

import nltk
import numpy as np
from keras.src.saving import load_model
from nltk import WordNetLemmatizer


class ChatBot:

    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        try:
            self.words = pickle.load(open("core/chatbot/words.pkl", "rb"))
            self.classes = pickle.load(open("core/chatbot/classes.pkl", "rb"))
            self.model = load_model("core/chatbot/chatbot_model.h5")
        except Exception:
            print("Please train the model first then start this service")

    def clean_up_sentence(self, sentence):
        sentence_words = nltk.word_tokenize(sentence)
        sentence_words = [self.lemmatizer.lemmatize(word) for word in sentence_words]
        return sentence_words

    def bag_of_words(self, sentence):
        sentence_words = self.clean_up_sentence(sentence)
        bag = [0] * len(self.words)
        for w in sentence_words:
            for i, word in enumerate(self.words):
                if word == w:
                    bag[i] = 1

        return np.array(bag)

    def predict_class(self, sentence):
        bow = self.bag_of_words(sentence)
        res = self.model.predict(np.array([bow]))[0]
        results = [[i, r] for i, r in enumerate(res) if r > 0.25]

        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in results:
            return_list.append({'intent': self.classes[r[0]], 'probability': str(r[1])})
        return return_list
