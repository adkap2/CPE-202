import unittest
from project4 import entry_point
from project4 import SearchEngine
from hashtables import *
from docs import *

class TestCase(unittest.TestCase):
    """def test_count_words(self):
        search = SearchEngine('docs', 'stop_words.txt')
        #print(search.stopwords)
        search.count_words('data_structures.txt', 'text.txt')
        #print(search.doc_length)
        #print(search.term_freqs)"""
    
    """def test_index_files(self):
        search = SearchEngine('docs', 'stop_words.txt')
        search.index_files('docs')"""
    
    """def test_get_scores(self):
        ht = HashTableLinear()
        stopwords = import_stopwords('stop_words.txt', ht)
        search = SearchEngine('docs', stopwords)
        words = search.read_file('data_structure.txt')
        words = search.parse_words(words)
        #print(words)
        search.count_words('data_structure.txt', words)
        #print(search.term_freqs)
        #print(search.doc_length)
        search.get_scores(words)"""
        
    def test_entry_point(self):
        entry_point('docs')



def main():
    # execute unit tests[]
    unittest.main()

if __name__ == '__main__':
    # execute main() function
    main()