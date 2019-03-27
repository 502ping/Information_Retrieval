# Information Retrieval
A Course porject, it aims to create an inverted index for a set of documents, and then the inverted index is used to implement quick search for various kinds of query. The input of the program is a large collection of English documents.
## Operation Steps:
Write an interface for the program which is able to<br>
(1) Users input the document directory for indexing;
(2) Users input the query they want to search(available for both words and phrases);
(3) Display the names of the retrieved documents for users.
## Functions intro
def combine_indexes(): input documents and ouput combined indexes
def parse_input(): delete the punctuations of query
def stemming(word): get the stem words
def create_inverted_index(): input file list and ouput the inverted index
def search(): input query and output the retrieval results
class gui(): create a wxPython GUI interface to encapsulate the retrieval function
## Package
wxPython(GUI), nltk.tokenize
## Others 
Python 3.6
