import pandas as pd
import nltk
import pymorphy2
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
import numpy as np


nltk.download('punkt')
nltk.download('stopwords')

morph = pymorphy2.MorphAnalyzer()

russian_stop_words = stopwords.words("russian") + list(string.punctuation + "»«-''\\/``1234567890")
snowball = SnowballStemmer(language="russian")


def tokenize_sentence(sentence):
    tokens = word_tokenize(sentence, language="russian")
    tokens = [i for i in tokens if i not in russian_stop_words]
    tokens = [morph.parse(i)[0].normal_form for i in tokens]
    return tokens


def get_match_count(s1, s2):
    return len(set(s1).intersection(set(s2)))


def get_best_variants(tokens_arr, sentence):
    r = tokenize_sentence(sentence)
    res = []
    for n, elem in enumerate(tokens_arr):
        res.append((get_match_count(r, elem), elem, n))
    res.sort(reverse=True)

    print([i[2] + 1 for i in res][:5])


if __name__ == "__main__":

    table1 = pd.read_excel("./Реестр проектов.xlsx").iloc[4:996]
    table2 = pd.read_excel("./Перечень открытых запросов.xlsx").iloc[2:]
    tokens = []
    for line in table1.values:
        tokens.append(line[1] + line[2] if line[2] is string else line[1])
        tokens[-1] = tokens[-1].replace("ё", "е").replace("Ё", "Е")
        tokens[-1] = tokenize_sentence(tokens[-1])
    # print(table2.iloc[4])
    get_best_variants(tokens, "автоматическое выявление и распознавание коммерческих неисправностей (состояние люков, дверей, бортов и кузовов вагонов, нарушения при размещении и креплении грузов на открытом подвижном составе, наличие и состояние запорно-пломбировочных устройств (ЗПУ), перегруз, нарушение габаритов, загрязнение, остатки груза в вагоне) с использованием имеющихся технических средств (АСКО ПВ) или со своими техническими средствами;")
    # get_best_variants(tokens, table2.iloc[4].values[2])
