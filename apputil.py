"""
📘 Week 8 — Markov Text Generator
Exercise 1: Basic Markov Chain (single-word prediction)
Exercise 2: Text Generation using the basic Markov model
Bonus: Improved Markov Chain using word pairs (bi-grams) for smoother text
"""

from collections import defaultdict
import random
import requests
import re

# -----------------------------------
# 📗 Exercise 1: Load and Clean Data
# -----------------------------------

# Download a quotes dataset from GitHub
url = 'https://raw.githubusercontent.com/leontoddjohnson/datasets/main/text/inspiration_quotes.txt'
content = requests.get(url)
quotes_raw = content.text

# Clean up the dataset
quotes = quotes_raw.replace('\n', ' ')           # remove newlines
quotes = re.split("[“”]", quotes)                # split by fancy quote marks
quotes = quotes[1::2]                            # take every other element (actual quotes)
corpus = ' '.join(quotes)                        # join into a single text
corpus = re.sub(r"\s+", " ", corpus).strip()     # remove extra spaces

print("✅ Corpus Preview:")
print(corpus[:300], "\n")  # show a small preview of the text


# -----------------------------------
# 📘 Exercise 2: Basic Markov Text Generator
# -----------------------------------

class MarkovText(object):
    """
    A simple Markov text generator that builds a dictionary of word transitions.
    Example: {'life': ['is', 'gives'], 'is': ['beautiful', 'hard']}
    """

    def __init__(self, corpus):
        self.corpus = corpus
        self.tokens = self.corpus.split()
        self.term_dict = None  # Will store the mapping of word → possible next words

    def get_term_dict(self):
        """Build a dictionary mapping each word to the list of words that follow it."""
        term_dict = defaultdict(list)
        for i in range(len(self.tokens) - 1):
            term_dict[self.tokens[i]].append(self.tokens[i + 1])
        self.term_dict = term_dict
        return term_dict

    def generate(self, seed_term=None, term_count=15):
        """Generate text starting from a random or given seed word."""
        if self.term_dict is None:
            raise ValueError("Run get_term_dict() first.")

        # Pick a starting word (random if none given)
        if seed_term is None:
            seed_term = random.choice(list(self.term_dict.keys()))
        elif seed_term not in self.term_dict:
            raise ValueError(f"Seed term '{seed_term}' not in corpus.")

        output = [seed_term]
        current = seed_term

        # Generate text by randomly choosing next words
        for _ in range(term_count - 1):
            next_terms = self.term_dict.get(current)
            if not next_terms:
                break  # stop if no possible next word
            current = random.choice(next_terms)
            output.append(current)

        return ' '.join(output)


# Example run for Exercise 2
print("🧩 Exercise 2: Generating text using single-word Markov model...\n")
text_gen = MarkovText(corpus)
text_gen.get_term_dict()
print(text_gen.generate(term_count=30), "\n")


# -----------------------------------
# 🌟 BONUS: Markov Chain with Word Pairs (Bi-grams)
# -----------------------------------

class MarkovTextPairs(object):
    """
    An improved Markov model that uses pairs of words (bi-grams)
    for more realistic text generation.
    Example: {('life', 'is'): ['beautiful', 'hard']}
    """

    def __init__(self, corpus):
        self.corpus = corpus
        self.tokens = self.corpus.split()
        self.term_dict = None  # Will store (word1, word2) → next word list

    def get_term_dict(self):
        """Build dictionary mapping word pairs to the possible next word."""
        term_dict = defaultdict(list)
        for i in range(len(self.tokens) - 2):
            key = (self.tokens[i], self.tokens[i + 1])
            term_dict[key].append(self.tokens[i + 2])
        self.term_dict = term_dict
        return term_dict

    def generate(self, term_count=20, seed_pair=None):
        """Generate text starting from a random or given seed pair."""
        if self.term_dict is None:
            raise ValueError("Run get_term_dict() first.")

        # Pick a random seed pair if none provided
        if seed_pair is None:
            seed_pair = random.choice(list(self.term_dict.keys()))
        elif seed_pair not in self.term_dict:
            raise ValueError(f"Seed pair '{seed_pair}' not in corpus.")

        output = [seed_pair[0], seed_pair[1]]
        current_pair = seed_pair

        for _ in range(term_count - 2):
            next_terms = self.term_dict.get(current_pair)
            if not next_terms:
                break
            next_word = random.choice(next_terms)
            output.append(next_word)
            # Move the window forward by one word
            current_pair = (current_pair[1], next_word)

        return ' '.join(output)


# Example run for BONUS
print("💎 BONUS: Generating smoother text using word-pair Markov model...\n")
text_gen2 = MarkovTextPairs(corpus)
text_gen2.get_term_dict()
print(text_gen2.generate(term_count=40))