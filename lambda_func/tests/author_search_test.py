import unittest
from lambda_func import main_handler
import json
from lambda_func import author_search as AS


class TestAuthorSearch(unittest.TestCase):

    authors = []
    
    def test_load_file(self):
        authors = AS.load_file('tests/authors_test.txt')
        for author in authors:
            print(author)
        
        assert(authors is not None)
        assert(authors[0] == 'albert, einstein')
        assert(authors[4] == 'liima, lasse')

    def test_search(self):
        authors_found = ['Albert Einstein', 'Nikita Kuts']
        authors_close = ['Albert Ainstein', 'jobbs steve']
        authors_far = ['sorsa mies', 'John Locke']
        
        for author in authors_found:
            found = AS.search(author, False, 'tests/authors_test.txt')
            assert(found is not None)
        
        for author in authors_close:
            found = AS.search(author, True, 'tests/authors_test.txt')
            assert(found is not None)
        
        for author in authors_far:
            found = AS.search(author, False, 'tests/authors_test.txt')
            assert(found is None)
            
            found = AS.search(author, True, 'tests/authors_test.txt')
            assert(found is None)


    def test_closest_search(self):
        authors_found = ['Albert Einstein', 'Nikita Kuts']
        authors_close = ['Albert Ainstein', 'jobbs steve']
        authors_far = ['sorsa mies', 'John Locke']
        
        for author in authors_found:
            found = AS.search_closest(author, 'tests/authors_test.txt')
            assert(found is not None)
        
        for author in authors_close:
            found = AS.search_closest(author, 'tests/authors_test.txt')
            assert(found is not None)
        
        for author in authors_far:
            found = AS.search_closest(author, 'tests/authors_test.txt')
            assert(found is None)
            
            found = AS.search_closest(author, 'tests/authors_test.txt')
            assert(found is None)
     
     
    def test_normal_search(self):
        authors_found = ['Albert Einstein', 'Nikita Kuts']
        authors_close = ['Albert Ainstein', 'jobbs steve']
        authors_far = ['sorsa mies', 'John Locke']
        
        for author in authors_found:
            found = AS.search_normal(author, 'tests/authors_test.txt')
            assert(found is not None)
        
        for author in authors_close:
            found = AS.search_normal(author, 'tests/authors_test.txt')
            assert(found is None)
        
        for author in authors_far:
            found = AS.search_normal(author, 'tests/authors_test.txt')
            assert(found is None)
       

def main():  # pragma: no cover
    print("Main function")


if __name__ == '__main__':  # pragma: no cover
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAuthorSearch)
    unittest.TextTestRunner(verbosity=2).run(suite)
