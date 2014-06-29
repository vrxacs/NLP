# -*- coding: utf-8 -*-
"""
Created on Sun Apr 27 19:15:13 2014

@author: Valeri
"""

from __future__ import division

import nltk
import random
import re

def extractSentences(text):
    """
    This function uses NLTK Punkt English-trained tokenizer to 
    correctly split the text into sentences.
    If you want to use this script with a different language, you
    need to either use a different pre-trained tokenizer or train
    a tokenizer yourself.
    """
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    return sent_detector.tokenize(text.strip())

def extractWordSeq(text, length):
    """
    Extracts all the different word sequences of the specified length 
    in the given text
    """
    tokens = {}
    sentences = extractSentences(text)
    
    for sent in range(len(sentences)):
        temp = nltk.word_tokenize(sentences[sent])
        for t in range(-length+1, len(temp)):
            tup = ()
            for i in range(length-1):
                if t+i < 0:
                    tup += ('--begin',) # Beginning-of-sentence token
                elif t+i >= len(temp):
                    tup += ('--end',) # End-of-sentence token
                else:
                    tup += (temp[t+i],)
            
            if not tup in tokens:
                tokens[tup] = {}
            
            if t+length-1 >= len(temp):
                key = "--end" # End-of-sentence token
            else:
                key = temp[t+length-1]
            
            if key in tokens[tup]:
                tokens[tup][key] += 1
            else:
                tokens[tup][key] = 1    
    
    return tokens

def normalize(ngrams):
    """
    Normalizes the ngram probabilities
    """
    for key in ngrams.iterkeys():
        tempSum = sum(ngrams[key].values())
        for key2 in ngrams[key]:
            ngrams[key][key2] /= tempSum
    
    return ngrams

def ngramProbGen(text, length):
    """
    Given a string text, this function returns ngrams of the supplied length 
    """
    ngrams = extractWordSeq(text, length)
    return normalize(ngrams)

def ngramsFromFile(filename, length):
    """
    Given a file name, this function returns ngrams of the supplied length. 
    The whole file is loaded into memory so be careful with very big files.
    """
    tempfile = open(filename, 'r')
    text = tempfile.read()
    return ngramProbGen(text, length)
    
def rouletteSampling(probs):
    """
    Selects a word from the dictionary based on their probabilities
    """
    random.seed()
    t = random.random()
    tempSum = 0.0
    
    for key in probs.keys():
        tempSum += probs[key]
        if tempSum > t:
            return key
    # Defaults to the first value
    return probs.keys()[0]

def textGenerator(ngrams, num):
    """
    Generates num sentences from the provided ngrams.
    In this current version, the generator has problems with spacing punctuation
    and handling ' when it's used in dialogue.
    """
    startingTup = ()
    for i in range(len(ngrams.keys()[0])):
        startingTup += ('--begin',)

    endingTup = ()
    for i in range(len(ngrams.keys()[0])):
        endingTup += ('--end',)

    for n in range(num):
        tup = startingTup
        sentence = ''
        while tup != endingTup:
            nextWord = rouletteSampling(ngrams[tup])
            if nextWord != '--end':
                sentence += " " + nextWord
            tup = tup[1:] + (nextWord,)
        print(sentence)