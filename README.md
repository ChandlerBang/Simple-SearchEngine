# Simple-SearchEngine
A simple search engine used for fulltext retrieval, implemented by Python.

We are required to create a mini search engine which can handle inquiries over “The Complete Works of William Shakespeare” (http://shakespeare.mit.edu/). The search engine is offline, which means we should download all the contents from first, and then create inverted index over the contents where the search program is based.

Tasks Description
1)	Spider.py
    Download all the contents from http://shakespeare.mit.edu/ and store them in respective text files.
2)	main.py
    Transform all these text files into a form that program can handle. e.g., a dict of python. 
    Use filter to remove the non-word characters and stop words from the dict.
    Create inverted index over the dict with word stemming or lemmatization.
    Write a query program on top of the inverted file index.
    Test the query program.

Results are as follows,
！[image](https://github.com/ChandlerBang/Simple-SearchEngine/blob/master/result.png)
