import pandas as pd
import nltk
import pymorphy2
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer

nltk.download('punkt')
nltk.download('stopwords')

morph = pymorphy2.MorphAnalyzer()

russian_stop_words = stopwords.words("russian") + list(string.punctuation + "»«-''\\/``1234567890")
snowball = SnowballStemmer(language="russian")
table1 = pd.read_excel("./Реестр проектов.xlsx").iloc[4:996]
table2 = pd.read_excel("./Перечень открытых запросов.xlsx").iloc[2:]


def tokenize_sentence(sentence):
    tokens_arr = word_tokenize(sentence, language="russian")
    tokens_arr = [i for i in tokens_arr if i not in russian_stop_words]
    tokens_arr = [morph.parse(i)[0].normal_form for i in tokens_arr]
    return tokens_arr


def get_match_count(s1, s2):
    return len(set(s1).intersection(set(s2)))  # need optimize


def get_best_variants(tokens_arr, sentence):
    r = tokenize_sentence(sentence)
    res = []
    for n, elem in enumerate(tokens_arr):
        res.append((get_match_count(r, elem), elem, n))
    res.sort(reverse=True)

    return res


tokens = []
for line in table1.values:
    tokens.append(line[1] + line[2] if type(line[2]) == str else line[1])
    tokens[-1] = tokens[-1].replace("ё", "е").replace("Ё", "Е")
    tokens[-1] = tokenize_sentence(tokens[-1])


def get_variants(sentence, limit):  # need edit, make table1 as field in model
    variants = get_best_variants(tokens, sentence)
    return [list(table1.iloc[i[2]].values) + [i[0] / float(len(i[1]))] for i in variants[:limit]]


tokens2 = []
for line in table2.values:
    tokens2.append(line[2])
    tokens2[-1] = tokens2[-1].replace("ё", "е").replace("Ё", "Е")
    tokens2[-1] = tokenize_sentence(tokens2[-1])

def get_open_requests(sentence, limit=3):
    variants = get_best_variants(tokens2, sentence)
    return [list(table2.iloc[i[2]].values) + [i[0] / float(len(i[1]))] for i in variants[:limit]]
