"""Project 4 search engine
For:
    CPE202
    Sections 7 & 9
    Fall 2019
Author:
    Adam Goldstein
"""
import os, math
from hashtables import import_stopwords
from hashtables import HashTableLinear

def entry_point(dir_name):
    ht = HashTableLinear()
    stop_words = import_stopwords('stop_words.txt', ht)
    search = SearchEngine(dir_name, stop_words)
    while True:
        s = input('Input Search: ')
        if s == 'q':
            break
        scores = search.search(s)
        print(scores)

class SearchEngine:
    """
    doc_length: the number of words contained in document contained in a hashtable
    term_freqs: a hashtable containing each word in text file and an inner hashtable containing the frequency count
    stopwords: a hashtable containing stop words
    """
    def __init__(self, directory, stopwords):
        self.doc_length = HashTableLinear()
        self.term_freqs = HashTableLinear()
        self.stopwords = stopwords
        self.index_files(directory)

    def read_file(self, infile):
        """A helper function to read a file
            Args:
                infile (str) : the path to a file
            Returns:
                list : a list of str read from a file
        """
        with open(infile, 'r') as fi:
            strings = fi.read()
            strings = strings.split()
            return strings

    def parse_words(self, lines):
        """split strings into words
        Convert words to lower cases and remove new line chars.
        Exclude stopwords.
        Args:
            lines (list) : a list of strings
        Returns:
            list : a list of words
        """
        list1 = []
        for line in lines:
            words = line.lower()
            words = words.split()
            for word in words:
                list1.append(word)
        list1 = self.exclude_stopwords(list1)
        return list1

    def exclude_stopwords(self, terms):
        """exclude stopwords from the list of terms
        Args:
            terms (list) :
        Returns:
            list : a list of str with stopwords removed
        """
        list1 = []
        for i in terms:
            if not self.stopwords.contains(i):
                list1.append(i)
        return list1         

    def count_words(self, filename, words):
        """
        Args:
            filename (str) : the file name
            words (list) : a list of words
        """
        for word in words:
            if word not in self.term_freqs:
                self.term_freqs[word] = HashTableLinear()
                self.term_freqs[word][filename] = 1
            else:
                if filename not in self.term_freqs[word]:
                    self.term_freqs[word][filename] = 1
                else:
                    self.term_freqs[word][filename] += 1
        self.doc_length.put(filename, len(words))

    def index_files(self, directory):
        """index all text files in a given directory
        Args:
            directory (str) : the path of a directory
        """
        file_list = os.listdir(directory)
        for item in file_list:
            val = os.path.join(directory, item)
            if os.path.isfile(val):
                parts = os.path.splitext(val)
                if parts[1] == '.txt':
                    words1 = self.read_file(val)
                    words2 = self.parse_words(words1)
                    self.count_words(val, words2)

    def get_wf(self, tf):
        """comptes the weighted frequency
        Args:
            tf (float) : term frequency
        Returns:
            float : the weighted frequency
        """
        if tf > 0:
            wf = 1 + math.log(tf)
        else:
            wf = 0
        return wf

    def get_scores(self, terms):
        """creates a list of scores for each file in corpus
        The score = weighted frequency / the total word count in the file.
        Compute this score for each term in a query and sum all the scores.
        Args:
            terms (list) : a list of str
        Returns:
            list : a list of tuples, each containing the filename and its relevancy score
        """
        scores = HashTableLinear()
        for term in terms:
            if self.term_freqs.contains(term):
                hashtable = self.term_freqs[term]
                for file1 in hashtable.slots:
                    if file1 != None and hashtable.contains(file1[0]):
                        if scores.contains(file1[0]):
                            key, val = scores.remove(file1[0])
                            scores.put(file1[0], val + self.get_wf(file1[1]))
                        else:
                            scores.put(file1[0], self.get_wf(file1[1]))
        for file1 in scores.slots:
            if file1 is not None:
                key, val = scores.remove(file1[0])
                val /= self.doc_length.get(file1[0])
                scores.put(file1[0], val)
        return scores

    def rank(self, scores):
        """ranks files in the descending order of relevancy
        Args:
            scores(list) : a list of tuples: (filename, score)
        Returns:
            list : a list of tuples: (filename, score) sorted in descending order of relevancy
        """
        no_none = []
        for val in scores.slots:
            if val != None:
                no_none.append(val)
        no_none = sorted(no_none, key = lambda x:x[1], reverse = True)
        new_line_out = ''
        for i in no_none:
            new_line_out += i[0] + '\n'
        return new_line_out
    
    def search(self, query):
        """ search for the query terms in files
        Args:
            query (str) : query input
        Returns:
            list :  list of files in descending order or relevancy
        """
        list1 = self.parse_words([query])
        scores = self.get_scores(list1)
        print(scores)
        return self.rank(scores)

if __name__ == '__main__':
    entry_point('docs')
