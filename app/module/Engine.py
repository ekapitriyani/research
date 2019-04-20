import pandas as pd
import numpy as np
import numpy.linalg as LA # operasi baris elementer

from sklearn.feature_extraction.text import CountVectorizer # tf-idf
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer # tf-idf
from sklearn.metrics.pairwise import cosine_similarity # cosine similarity
from nltk.corpus import stopwords # preprocessing
from nltk.stem import PorterStemmer # preprocessing bahasa inggris
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory  # preprocessing
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory #preprocessing
import string # ya buat string


stemmer = StemmerFactory().create_stemmer()  # Object stemmer
remover = StopWordRemoverFactory().create_stop_word_remover()  # objek stopword
translator = str.maketrans('', '', string.punctuation)

def stemmerEN(text):
    porter = PorterStemmer()
    stop = set(stopwords.words('english'))
    text = text.lower()
    text = [i for i in text.lower().split() if i not in stop]
    text = ' '.join(text)
    preprocessed_text = text.translate(translator)
    text_stem = porter.stem(preprocessed_text)
    return text_stem

def preprocess(text):
    text = text.lower()
    text_clean = remover.remove(text) #fungsi hapus stopword
    text_stem = stemmer.stem(text_clean)
    text_stem = stemmerEN(text_stem)
    return text_stem

class Engine:
    def __init__(self):
        self.cosine_score = []
        self.train_set = []  # Documents
        self.test_set = []  # Query

    def addDocument(self, word): # fungsi untuk menambahkan dokumen dataset ke dalam list train_set
        self.train_set.append(word)

    def setQuery(self, word):  # fungsi untuk menambahkan data query ke dalam list test_Set
        self.test_set.append(word)

    def process_score(self):
        stopWords = stopwords.words('english')
        vectorizer = CountVectorizer()

        transformer = TfidfTransformer()

        trainVectorizerArray = vectorizer.fit_transform(self.train_set).toarray()
        # menghitung Bobot dokumen dataset dan uji dan kemudian disimpan dalam bentuk array
        testVectorizerArray = vectorizer.transform(self.test_set).toarray()

        cx = lambda a, b: round(np.inner(a, b) / (LA.norm(a) * LA.norm(b)), 3)
        #fungsi tanpa nama untuk normalisasi data dan definisi rumus Cosine Similarity
        #         print testVectorizerArray
        output = []
        for i in range(0, len(testVectorizerArray)):
            output.append([])

        for vector in trainVectorizerArray:
            # print vector
            u = 0
            for testV in testVectorizerArray:
                #perhitungan Cosine Similarity dalam bentuk vector dari dataset dengan query
                #yang di masukan yang kemudian mengembalikan nilai cosine ke dalam variable
                #cosine_score dalam bentuk list.
                # print testV
                cosine = cx(vector, testV)
                #                 self.cosine_score.append(cosine)
                #                 bulatin = (round(cosine),2)
                output[u].append((cosine))
                u = u + 1
        return output