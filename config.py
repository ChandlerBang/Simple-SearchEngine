# configuration file
# If you change the following configuration, delete database.json and documents.json and rebuild
# Repeat: If you change the following configuration, delete database.json and documents.json and regenerate it!!!!!!!!

class Config():
    # show in screen up to 20 results every time
    show_result_cnt = 20

    # If you want to use a partial restore, leave use_lemmatizer = True and remove the following two comments
    from nltk import WordNetLemmatizer
    wordnet_lemmatizer = WordNetLemmatizer()
    use_lemmatizer = False  # Do not use part of speech restoration

    # If you want to use a part of speech recovery, let use_stemmer=True and remove the following two sentences
    from nltk.stem.porter import PorterStemmer
    porter_stemmer = PorterStemmer()
    use_stemmer = True   # Do not use stemming

    stop_words = ['the', 'and', 'i', 'to', 'of', 'a']
    # stop_words = ['the', 'and', 'i', 'to', 'of', 'a', 'you', 'my', 'that', 'in', 'is', 'not', 'it', 'me', 'for', 's', 'with', 'his',
    #               'be', 'he', 'this', 'your', 'but', 'have', 'as', 'thou', 'd', 'so', 'him', 'will', 'what', 'her', 'thy', 'all',
    #               'by', 'do', 'no', 'shall', 'we', 'if', 'are', 'thee', 'on', 'lord', 'o', 'our', 'king', 'sir', 'good', 'now']
    path = r'./The Complete Works of William Shakespeare'
    database = r'./data/database.json'
    doc_file = r'./data/documents.json'
    tfidf_file = r'./data/tfidf.json'

    interval = 3       # This is the requirement of word spacing for the search1 function
    use_search2 = False  # Use the search2 method to search the word

opt = Config()