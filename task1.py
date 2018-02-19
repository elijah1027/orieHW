from mrjob.job import MRJob
import time
import re
import operator



class MRWordCounter(MRJob):
    def mapper(self, key, line):
        #Reference:
        #https://docs.python.org/2/library/re.html(Link:findall)
        #https://stackoverflow.com/questions/16312955/what-is-the-regular-expression-in-python-that-match-alphabet-only(Link: find alphabet)
        #Note: Code from the lecture does not work. It introduced non-alphabet chars. 
        line_split = re.findall(r"[a-zA-Z]+",line)
        for word in line_split:
            yield word[0].upper(),1            
            

    def reducer(self, word, counts):
        total = sum(counts)
        yield word, total

if __name__ == '__main__':
    #run: python count_word.py -o 'output_dir' --no-output 'location_input_file or files'
    #e.g. python count_word.py -o 'results_count_word' --no-output 'data_count_word/*.txt'
    st = time.time()
    MRWordCounter.run()
    end = time.time()
    print (end - st)
