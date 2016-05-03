from __future__ import division  # floating point division
from nltk import word_tokenize, sent_tokenize
from matplotlib import pyplot as plt  # for plotting
import codecs  # unicode handling
import os
import sys  # for command line arguments
from collections import Counter
import numpy as np

from ngram import NGram
from utils import normalize, basic_count, length_count, expectation

__author__='Megan OKeefe'

def num_hapaxes(countdict):
    """return the number of items that occur exactly once
    Example: num_hapaxes[{'a': 2, 'b': 1, 'c': 1}] -> 2
    """
    #count the number of keys whose value is 1, in counttdict. 
    return countdict.values().count(1)

def tokenize(filename, casefold):
    """Read a text file and return a list of sentences,
    where each sentences is a list of tokenized words,
    using NLTK's tokenization functions.
    """
    with open(filename) as file:
    	content = file.read()
    	content = content.decode("utf8") #deals w/ unicode bugs I got
    	if casefold:
    		content = content.lower() 
    	#generate list (sentences) of lists (words)
    	output = [word_tokenize(t) for t in sent_tokenize(content)]
    return output
    	

class Corpus:
    """Class for reading and processing text data from a file
    and computing various statistics."""

    def __init__(self, filename, casefold=True):
        """Read file and compute various statistics on its text.
        """
        self.filename = os.path.splitext(filename)[0]   # remove extension

        self.tokenized_sents = tokenize(filename, casefold)  #list of sentences
        self.tokenized_words = [word for sentence in self.tokenized_sents for word in sentence]

        self.word_counts = basic_count(self.tokenized_words)
        self.char_counts = basic_count(''.join(self.tokenized_words))  # takes count of characters

        self.numsents = len(self.tokenized_sents)   # number of sentences
        self.numtokens = len(self.tokenized_words)  # number of word tokens
        self.numtypes = len(self.word_counts)   # number of word types

        self.type_lengths = normalize(length_count(self.word_counts.keys()))  # proportion of word types of each length
        self.token_lengths = normalize(length_count(self.tokenized_words))  # proportion of word tokens of each length

    def plot_lengths(self, plotfilename):
		"""plot distribution over word token and type lengths,
		save to plotfilename"""
		plt.figure(1).set_size_inches(20, 20)
		#SUBPLOT 1: TOKENS
		plt.subplot(211)
		plt.bar(self.token_lengths.keys(), self.token_lengths.values())
		plt.title('Tokens')
		#SUBPLOT 2: TYPES
		plt.subplot(212)
		plt.bar(self.type_lengths.keys(), self.type_lengths.values())
		plt.title('Types')
		plt.xlabel('Word Length')
		plt.ylabel('Frequency')
		plt.savefig(plotfilename)

    def plot_freq(self, plotfilename):
        """plot word type frequency against rank on a log10-log10 plot,
        save to plotfilename
        """
        #get word type frequencies 
        tw = self.tokenized_words
        counts = Counter(tw).most_common()
        freqs = [word[1] for word in counts]
        plt.loglog(range(len(freqs)), freqs, basex=10, basey=10)
        plt.savefig(plotfilename)
    

    def display_stats(self):
        """summary statistics for this corpus"""
        # comment out lines dependent on methods that you haven't yet implemented
        print "Statistics for", self.filename

        print self.numsents, "sentences"
        print self.numtokens, "word tokens"
        print self.numtypes, "word types"

        print '{0:.2f} average tokens per type'.format(self.numtokens/self.numtypes)
        print '{0:.2f} average sentence length'.format(self.numtokens/self.numsents)

        print '{0:.2f} average word token length'.format(expectation(self.token_lengths))
        print '{0:.2f} average word type length'.format(expectation(self.type_lengths))
        
        print "Hapax legomena comprise {0:.2%} of the types".format(num_hapaxes(self.word_counts)/self.numtypes)

        self.plot_freq(self.filename+'_freq.png')
        self.plot_lengths(self.filename+'_lengths.png')

if __name__=='__main__':
    filename = sys.argv[1]
    corpus = Corpus(filename, casefold=True)
    corpus.display_stats()

    print
    word_model = NGram(1, 'word', corpus.word_counts)
    word_model.display_stats()

    print
    char_model = NGram(1, 'character', corpus.char_counts)
    char_model.display_stats()
