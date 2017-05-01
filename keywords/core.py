# venv/bin/python 3.5
# implementation of Rapid Automated Keyword Extraction Algorithm (RAKE)
# reference : https://github.com/aneesha/RAKE/blob/master/rake.py
"""RAKE implementation"""
from __future__ import print_function
import re

#check if text is number
def is_number(word):
    """
    Check if a given string is a number
    """
    try:
        float(word) if '.' in word else int(word)
        return True
    except ValueError:
        return False
#loading stop words from a file
def load_stop_words(stop_word_file):
    """
    Utility function to load stop words from a file and return as a list of words
    @param stop_word_file Path and file name of a file containing stop words.
    @return list A list of stop words.
    """
    stop_words = []
    for line in open(stop_word_file):
        if line.strip()[0:1] != "#":
            for word in line.split():  # in case more than one per line
                stop_words.append(word)
    return stop_words

#split to sentences
def split_sentences(text):

    """
    Utility function to return a list of sentences.
    @param text The text that must be split in to sentences.
    @return list List of sentences stripped off punctuations
    """
    sentence_delimiters = re.compile(u'[.!?,;:\t\\\\"\\(\\)\\\'\u2019\u2013]|\\s\\-\\s')
    sentences = sentence_delimiters.split(text)
    return sentences
# split phrase into words
def split_to_words(text):
    """
    Utility function to return a list of all words.
    @param text The text that must be split in to words.
    @param min_word_return_size The minimum no of characters a word must have to be included.
    """
    splitter = re.compile('[^a-zA-Z0-9_\\+\\-/]')
    words = []
    for single_word in splitter.split(text):
        current_word = single_word.strip().lower()
        if current_word != '' and not is_number(current_word):
            words.append(current_word)
    return words
#generate candidates from list of sentences by removing stop words
def generate_candidates(sentences, regex):
    """
    Utility that generates candidate words from given text.
    Currently this does not consider any association between keywords and stopwords.
    @param sentences List of sentences assuming sentences are stripped off punctuations
    @param stopwords List of words that are to be stripped off
    @return list  List of candidates
    """
    candidates = []
    for sentence in sentences:
        candidates.extend([candidate for candidate in regex.split(sentence) if candidate != ''])
    return candidates
#generate a regex pattern from stopwords list
def generate_regex(words):
    """
    Utility that generates regex from given list.
    @param words List of words that are to be put inside the regex
    @return re
    """
    regexwords = []
    for word in words:
        word_regex = r'\b' + word + r'(?![\w-])'
        regexwords.append(word_regex)
    stop_word_pattern = re.compile('|'.join(regexwords), re.IGNORECASE)
    return stop_word_pattern

# calculate scores according to the Rake paper
def calculate_word_scores(candidates):
    """
    Calculate word scores using degree and frequency
    """
    word_degree = {}
    word_frequency = {}
    for candidate in candidates:
        words = split_to_words(candidate)
        wordassociation = len(words) - 1
        for word in words:
            word_frequency.setdefault(word, 0)
            word_frequency[word] += 1
            word_degree.setdefault(word, 0)
            word_degree[word] += wordassociation
    for word in word_frequency:
        word_degree[word] += word_frequency[word]
        word_score = {}
    for item in word_frequency:
        word_score.setdefault(item, 0)
        word_score[item] = word_degree[item] / (word_frequency[item] * 1.0)
    return word_score
# calculate candidate scores from word scores
def calculate_candidate_scores(candidates, wordscores):
    """
    Calculate candidate scores by summing word scores
    """
    candidate_scores = {}
    for candidate in candidates:
        words = split_to_words(candidate)
        candidate_scores.setdefault(candidate, 0)
        for word in words:
            candidate_scores[candidate] += wordscores[word]
    return candidate_scores

# class to encapsulate above methods
class Rake(object):
    """
    Rake object. To be initialized with a stopwords file.
    """
    def __init__(self, stopwordfilepath):
        self.stopwordfilepath = stopwordfilepath
        stopwords = load_stop_words(stopwordfilepath)
        self.__stopwordregex = generate_regex(stopwords)
    def run(self, text):
        """
        Returns candidates with scores
        """
        sentences = split_sentences(text)
        candidates = generate_candidates(sentences, self.__stopwordregex)
        wordscores = calculate_word_scores(candidates)
        candidatescores = calculate_candidate_scores(candidates, wordscores)
        return candidatescores


