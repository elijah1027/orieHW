from mrjob.job import MRJob
from mrjob.step import MRStep
import time
import re
import operator


class MRWordCounter(MRJob):
    def steps(self):
        return [
                MRStep(mapper=self.mapper,
                       
                       reducer=self.reducer_step1),
                MRStep(reducer=self.reducer_alpha)
            ]
    def mapper(self, key, line):
        #Reference:
        #https://docs.python.org/2/library/re.html(Link:findall)

        #https://stackoverflow.com/questions/16312955/what-is-the-regular-expression-in-python-that-match-alphabet-only(Link: find alphabet)
        line_split = re.findall(r"[a-zA-Z]+",line)
        for word in line_split:
            yield word,1            
            
    def reducer_step1(self, word, counts):
        #This step is referred to:
        ##https://pythonhosted.org/mrjob/guides/writing-mrjobs.html(Link:MRjob tutorial)
        yield None, (sum(counts),word)
    
    def reducer_alpha(self, _, pairs):
        lst = []
        for v in pairs:
            lst.append(v)
        lst.sort(reverse=True)
        for i in range(0,10,1):
            
            yield lst[i]

if __name__ == '__main__':
    #run: python count_word.py -o 'output_dir' --no-output 'location_input_file or files'
    #e.g. python count_word.py -o 'results_count_word' --no-output 'data_count_word/*.txt'
    st = time.time()
    MRWordCounter.run()
    end = time.time()
    print (end - st)
