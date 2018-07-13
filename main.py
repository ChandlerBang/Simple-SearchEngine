# -*- coding: utf-8 -*-
import json
import os
from utils import *
import math
from config import opt
from search_method import search1, search2
from mytest import test_threshold
from time import time

def save_files():
    # Build the database
    documents = {}
    traverse(path, documents, start=len(path))
    inverted = {}
    all_time_tf = {}
    all_count = {}  # Word frequency used to save a word in all documents
    for doc_id, text in documents.items():
        inverted_dict, times = inverted_index(text)  # Time_tf is just all the word tf of one document
        inverted_add_doc_ids(inverted, doc_id, inverted_dict)  # {'word': {'id1':[(1, 1)], 'id2':[ (1, 1)],}}

        # calculate all_count, used to store the frequency of occurrence of a word in all documents.
        if (opt.stop_words == []):
            for word in times:
                if word in all_count:
                    all_count[word] += times[word]
                else:
                    all_count.setdefault(word, times[word])

        # calculate term frequency
        time_tf = Compute_TF(times, len(text))
        all_time_tf.setdefault(doc_id, time_tf)

    if (opt.stop_words == []):
        opt.stop_words = sorted(all_count.items(), key=lambda item: item[1], reverse=True)[:40]
        opt.stop_words = [word for word, frequency in opt.stop_words]

    total_doc_number = len(documents)
    for word in inverted.keys():
        idf = math.log(total_doc_number / len(inverted[word]))
        for id in inverted[word].keys():
            try:
                all_time_tf[id][word] = all_time_tf[id][word] * idf
            except:
                pass

    # Save data to json file
    jsDict = json.dumps(inverted)  # dumps：Convert a dictionary in python to a string
    print('========= saving database ==========')
    f = open(database, 'w')
    f.write(jsDict)
    f.close()

    jsDoc = json.dumps(documents)  # dumps：Convert a dictionary in python to a string
    print('========= saving document ==========')
    f = open(doc_file, 'w')
    f.write(jsDoc)
    f.close()

    all_tfidf = all_time_tf
    jsTfidf = json.dumps(all_tfidf)
    print('========= saving Tfdif==========')
    f = open(tfidf_file, 'w')
    f.write(jsTfidf)
    f.close()

# Read the document and return the corresponding text content of the index
def extract_text(doc, index):
    f = open(doc_file, 'r')
    documents = json.loads(f.read())  # loads: Convert a string to a dictionary
    f.close()
    return documents[doc][index:index + 70].replace('\n', ' ')

def query_and_search():
    # Print Inverted-Index
    for word in inverted.keys():
        print(word)

    while(True):
        query = input("\nPlease Input Your Query:  ")
        # query = test_threshold(0.8)

        time_start = time()
        print( "\n================ Search for '%s'================== " % query )# %s is str() output string %r is repr() output object

        if opt.use_search2:
            scores = search2(inverted, query, all_tfidf)
            print('time:    ', time() - time_start)
            result_cnt = 1
            break_flag = False
            for score in scores:
                if ((result_cnt - 1) % opt.show_result_cnt == 0 and result_cnt != 1):
                    str = input('Continue or not: Y/N\n')
                    if str == 'Y' or str == 'y':
                        pass
                    else:
                        break_flag = True
                        break
                print("Result{0}".format(result_cnt))
                result_cnt += 1
                print('\tScore  : "{0}" '.format(score[1]))
                print('\tFrom   : "{0}" '.format(score[0]))
            break
        else:
            result_docs, query_words = search1(inverted, query)
            if result_docs:
                scores = PageRank(result_docs, all_tfidf, query_words)

        if result_docs:
            break_flag = False
            result_cnt = 1
            print("time: {}".format(time() - time_start))
            for score in scores:
                doc = score[0]   # score[0] is doc_id , score[1] is score
                offsets = result_docs[doc]
                for offset in offsets:
                    if((result_cnt-1) % opt.show_result_cnt == 0 and result_cnt!=1):
                        str = input('Continue to show or not: Y/N\n')
                        if str == 'Y' or str == 'y':
                            pass
                        else:
                            break_flag = True
                            break
                    print("Result{0}".format(result_cnt))
                    result_cnt += 1
                    print('\tScore  : "{0}" '.format(score[1]))
                    print('\tFrom   : "{0}" '.format(doc))
                    print('\tOffset : {}'.format(offset))
                    print('\tContent: {}'.format(extract_text(doc, offset)))
                if break_flag:
                    break
        else:
            print( '================ Nothing found! ================')

        print("\n================ Press CTRL+C to end the process ... ================")

if __name__=="__main__":

    print('========= loading data ==========')
    path = opt.path
    database = opt.database
    doc_file = opt.doc_file
    tfidf_file = opt.tfidf_file
    if not os.path.exists(database):
        save_files()
    f = open(database, 'r')
    inverted = json.loads(f.read())  # loads: Convert a string to a dictionary
    f.close()

    f = open(tfidf_file, 'r')
    all_tfidf = json.loads(f.read())  # loads: Convert a string to a dictionary
    f.close()

    query_and_search()
