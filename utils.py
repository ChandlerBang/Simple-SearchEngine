import os
import re
import json
from config import opt
import math


# This function reads all files in the path and adds all the contents of the file to the dict of the documents.
# We will get {file name: file content} {'xxxx.txt':'the girl has to deal with this problem'}
def traverse(path, documents,start):
    fs = os.listdir(path)
    for file in fs:
        tmp_path = os.path.join(path, file)
        if not os.path.isdir(tmp_path):       # If the file is not in the path
            f = open(tmp_path, 'r').read()    # read the content of file
            documents.setdefault(tmp_path[start:], f)
        else:
            traverse(tmp_path, documents,start)   # traverse again

# If the file is not in the path, this function is to get the word_list added index and offset information
# Index indicates that the word is in the document (after filtering stop words) is the first few words
# Offset indicates the specific location of the word in the document, such as "Tom often play basketball at night"
# 'Tom' index is 0, offset is 0; 'often' index is 1, offset is 4; 'play' index is 2, offset is 10;
def word_index(text):
    text_list = re.split(r'\W', text)   # 过滤所有非单词的字符
    text_list = [word for word in text_list if word.lower() not in opt.stop_words and len(word)>0] # Filter stop_words
    word_list = []
    time_low = {}       # 'time_low' is used to record the same word after word.lower()
    time = {}           # time is a dictionary used to record the number of occurrences of a word in the form {'word1': 3, 'word2':1, ...}
                        # The main purpose of using 'time' is to use 'text.index()' to get the offset of the word in the string
    for i, word in enumerate(text_list):  # 遍历text_list中的每一个word
        word_low = word.lower()
        if word in time:
            time[word] += 1         # If the word already exists in the time dictionary, the corresponding number of times  +1
        else:
            time.setdefault(word, 1)    # If the word is not in the time dictionary, this word is written into the dictionary, the number is recorded as 1
        if word_low in time_low:
            time_low[word_low] += 1
        else:
            time_low.setdefault(word_low, 1)
        if word.isalnum():  # If the word is English or numeric, it is added to word_list for index, offset, word
            word_list.append( (len(word_list), (FindOffset(text, word, time[word]), word.lower() )) )

    # word_list has the form like [(index1, (offset1, ‘word1’)), (index2, (offset2, ‘word2’)), (index3, (offset3, ‘word3’))]
    # time_low will be used to calculate term frequency(tf)
    return  word_list, time_low

#  calculate term frequency(tf), see more details in our documents
def Compute_TF(time, length):
    for word, count in time.items():
       time[word] = count/length
    return time


# This function also add index, using use_lemmatizer=True, similar to word_index()
# This means we use lemmatizer to lemmatize words
def lem_word_index(text):
    text_list = re.split(r'\W', text)
    text_list = [word for word in text_list if word.lower() not in opt.stop_words and len(word)>0]
    lem_text_list = [opt.wordnet_lemmatizer.lemmatize(word.lower(), 'v') for word in text_list]
    origin_time = {} # used to record the number of un-lemmatized words
    lem_time = {}   # used to record the number of lemmatized words
    word_list = []
    for i, word in enumerate(text_list):
        lem_word = lem_text_list[i]
        if word in origin_time:
            origin_time[word] += 1
        else:
            origin_time.setdefault(word, 1)
        if lem_text_list[i] in lem_time:
            lem_time[lem_word] += 1   # The number of times used to record the word prototype
        else:
            lem_time.setdefault(lem_word, 1)

        if lem_word.isalpha():  # if English
            word_list.append((len(word_list), (FindOffset(text, word, origin_time[word]), lem_word.lower())))  # Note: convert to lowercase
    # lem_time will be used to calculate term frequency(tf)
    return  word_list, lem_time

# This function also add index, using porter_stemmer, similar to word_index()
# This means we use porter_stemmer to do words stemming
def stem_word_index(text):
    text_list = re.split(r'\W', text)
    text_list = [word for word in text_list if word.lower() not in opt.stop_words and len(word)>0]
    stem_text_list = [opt.porter_stemmer.stem(word.lower()) for word in text_list]
    origin_time = {} # used to record the number of un-lemmatized words
    stem_time = {}   # stem_time
    word_list = []
    for i, word in enumerate(text_list):
        stem_word = stem_text_list[i]
        if word in origin_time:
            origin_time[word] += 1
        else:
            origin_time.setdefault(word, 1)
        if stem_text_list[i] in stem_time:
            stem_time[stem_word] += 1   # The number of times used to record the word prototype
        else:
            stem_time.setdefault(stem_word, 1)

        if stem_word.isalpha():  # if English
            word_list.append((len(word_list), (FindOffset(text, word, origin_time[word]), stem_word.lower())))  # Note: convert to lowercase
    return  word_list, stem_time

# This function is to find the position of the corresponding time word found in the document
# 'str' is the text content, word is the word to be searched,
# and 'time' is the number of times the word appears in the text
def FindOffset(str, word, time):
    start = 0
    for i in range(time):
        tmp = str.index(word, start)
        while(tmp>0 and  (tmp+len(word)) < (len(str)-1) and (str[tmp-1].isalpha() or str[tmp+len(word)].isalpha() )):
            tmp = str.index(word, tmp+1)
        start = tmp + 1
    return start - 1

# Segment text text and add index
def inverted_index(text):
    inverted_dict = {}
    if opt.use_lemmatizer:   # see more details in our document and config.py
        word_list, time_ = lem_word_index(text)
    else:
        if opt.use_stemmer:
            word_list, time_ = stem_word_index(text)
        else:
            word_list, time_ = word_index(text)
    for index, (offset, word) in word_list:
        # Do not directly setdefault(word, [(index, offset)]) because a word can correspond to multiple indexes
        locations = inverted_dict.setdefault(word, [])
        locations.append((index, offset))  # then inverted_dict has the form of {‘word1’:[(1, 1),(1, 2)], ‘word2’:[(1,2),(3, 4)]}

    return inverted_dict, time_    # {‘word1’:[(index, offset),(index, offset)], ‘word2’:[(index, offset),(index, offset)]}


# Add document information based on inverted_index
def inverted_add_doc_ids(inverted_dict_add, doc_id, inverted_dict):
    for word, locations in inverted_dict.items():
        id_and_locations = inverted_dict_add.setdefault(word, {})
        id_and_locations[doc_id] = locations  # Assign this dict
    return inverted_dict_add    # {‘word1’: {‘id1’:[(index, offset), (index, offset)], ‘id2’:[(index, offset), (index, offset)],}, ‘word2’: [(index, offset),(index, offset)]}

# rank the results
# this is only used in our search1 method
def PageRank(result_docs, all_tfidf, query_words):
    scores = {}
    for doc in result_docs.keys():
        scores.setdefault(doc, 0)
        for word in query_words:
           scores[doc] += all_tfidf[doc][word]  # we do the sum of the tfidf
    scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    return scores


if __name__ == '__main__':
    pass