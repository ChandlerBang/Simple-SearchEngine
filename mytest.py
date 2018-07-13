import json
from search_method import split_query

doc_file = r'./data/documents.json'
database = r'./data/database.json'

## testing file

# this funciton is to do the test1
# see more in our document
def test_inverted_index():

    f = open(doc_file, 'r')
    documents = json.loads(f.read())  # loads: Convert a string to a dictionary
    f.close()

    f = open(database, 'r')
    inverted_index = json.loads(f.read())  # loads: Convert a string to a dictionary
    f.close()

    flag = False
    for word, locations in inverted_index.items():   # {'word': {'id1':[(1, 1)], 'id2':[ (1, 1)],}}
        for doc in locations.keys():
            if word not in documents[doc].lower() :
                flag = True
                print("Error! word NOT in doc!")

    if flag == False:
        print('Congratulations! No error in inverted index!')



# when testing, use this function to generate new querylist,
# and put it in the set_and_search.py to run the file
def test_threshold(threshold=1):
    query = '''Our house, my  , little deserves
                of greatness to be used on it;
                And that same greatness too which our own 
                Have  to make so will not here before your grace.'''
    query_list = split_query(query)
    query_dict = {}
    for word in query_list:
        if word in query_dict:
            query_dict[word] += 1
        else:
            query_dict.setdefault(word, 1)
    query_list = sorted(query_dict.items(), key=lambda item: item[1], reverse=True)
    query_list = [word for word, tf in query_list[:round(threshold*len(query_list))]]

    # convert list to string
    query = ' '.join(query_list)
    return query

if __name__ =='__main__':
    test_inverted_index()