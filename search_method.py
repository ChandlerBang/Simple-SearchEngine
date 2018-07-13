# -*- coding: utf-8 -*-
from config import opt
import re
from functools import reduce


def split_query(query):
    query_list = re.split(r'\W', query)   # Filter all non-word characters
    query_list = [word.lower() for word in query_list if word.lower() not in opt.stop_words and len(word)>0] # filter stop_words
    if opt.use_lemmatizer:
        query_list = [opt.wordnet_lemmatizer.lemmatize(word, 'v') for word in query_list]
    if opt.use_stemmer:
        query_list = [opt.porter_stemmer.stem(word) for word in query_list]
    return query_list

def search1(inverted, query):
    # Traverse doc_set. For each doc in doc_set, find the index and offset of word1, word2,...
    # First find out the documents containing all the words in the query, and then analyze
    # the position of these words in the document, when the document contains no more than
    # 3 words between the query words
    # (We can also increase the spacing/interval of words, see more in the config.py)
    words = split_query(query)
    words = [word for word in words if word in inverted ]

    # Get a list of set [{},{},{},{}]
    doc_id= [set(inverted[word].keys()) for word in words]

    # doc_set is the set of doc_id that contains all the words in query
    doc_set = reduce(lambda x, y: x & y, doc_id) if doc_id else []
    precise_doc_dic = {}
    if doc_set:
        for doc in doc_set:
            # Index_list is the doc document, [[index1 of word1, index2 of word1], index1 of [word2]]
            index_list = [[indoff[0] for indoff in inverted[word][doc]] for word in words]
            offset_list = [[indoff[1] for indoff in inverted[word][doc]] for word in words]
            precise_doc_dic = precise(precise_doc_dic, doc, index_list, offset_list)  # Phrase query, Find the exact location
        return precise_doc_dic, words
    else:
        return {}, words

# this function aims to solve the interval problem
# Find adjacent phrases
def Intersection(x, y, interval=opt.interval):
    z = []
    for index_x in x:
        z += [index_y for index_y in y if  index_y >= (index_x - interval) and index_y<= index_x]
    return set(z)

# This function is to confirm whether several words in the document are adjacent.
# If they are adjacent, they will return the corresponding offset and index information.
def precise(precise_doc_dic, doc, index_list, offset_list):
    reversed_index = index_list[::-1]
    phrase_index = list(reduce(Intersection, reversed_index))
    if len(phrase_index):  # We emphasize that phrase_index may have more than one element
        phrase_offset = []
        for po in phrase_index:
            phrase_offset.append(offset_list[0][index_list[0].index(po)])  # Offset_list[0] represents the alphabetic offset of the first word
        precise_doc_dic[doc] = phrase_offset
    return precise_doc_dic

# our second search method
# see more in our document
def search2(inverted, query, all_tfidf):
    words = split_query(query)
    words = [word for word in words if word in inverted ]
    word_dict = {}
    for word in words:
        if word in word_dict:
            word_dict[word] += 1
        else:
            word_dict.setdefault(word, 1)

    doc_id = [set(inverted[word].keys()) for word in words]
    doc_set = reduce(lambda x, y: x & y, doc_id) if doc_id else []
    scores = {}
    if doc_set:
        for doc in doc_set:
            query_vector = []
            doc_vector = all_tfidf[doc]  # corresponding weight
            for word in doc_vector:
                if word in word_dict:
                    query_vector.append(word_dict[word]*doc_vector[word])
                else:
                    query_vector.append(0)
            scores.setdefault(doc, ComputeRelevance(doc_vector.values(), query_vector))
        scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
        return scores
    else:
        return  {}

# this funciton is to calculate the Cosine similarity
def ComputeRelevance(vector1, vector2):
    dot_product = 0.0
    normA = 0.0
    normB = 0.0
    for a,b in zip(vector1,vector2):
        dot_product += a*b
        normA += a**2
        normB += b**2
    if normA == 0.0 or normB==0.0:
        return None
    else:
        return dot_product / ((normA*normB)**0.5)