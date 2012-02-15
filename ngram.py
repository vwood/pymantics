#!/usr/bin/python

import dicttools
import random

def weighted_random_selection(d):
	"""Randomly selects a key from a dictionary if the values are weights"""
	total = 0
	for value in d.itervalues():
		total += value

	selection = random.randint(0, total)
	for key, value in d.iteritems():
		selection -= value
		if selection <= 0:
			return key

class NGram():
	"""Stores an n-gram model."""
	def __init__(self, n = 1):
		self.ngrams = {}
		self.n = n
		self.reset_context()
		self.ngram_count = 0

	def read_file(self, file, ignore_chars = "[](),:=.-\"'", lowercase = True):
		"""Reads n-grams in from a file."""
		self.reset_context()
		for line in file:
			if lowercase:
				line = line.lower()
			for char in ignore_chars:
				line = line.replace(char, " ")
			line = line.split()
			for word in line:
				self.add_word(word)
		self.finish_adding()

	def add_word(self, word):
		"""Adds a word to the n-gram model using the current context."""
		if self.ngrams.has_key(self.context):
			self.ngrams[self.context][word] = \
				self.ngrams[self.context].get(word, 0) + 1
		else:
			self.ngrams[self.context] = {word:1}
			self.ngram_count += 1
		self.shift_context(word)

	def finish_adding(self):
		"""Adds the last context to the n-gram model.
		This resets the context."""
		for i in range(len(self.context)):
			self.add_word(None)

	def shift_context(self, word):
		"""Destructively updates the context to have word at the end."""
		self.context = self.context[1:] + (word,)

	def reset_context(self):
		"""Resets the context. This shouldn't be necessary if finish_adding() is used."""
		self.context = (None,) * self.n

	def search(self, *words):
		"""Find a list of words in the model."""
		result = {}
		for i in range(len(words) - self.n + 1):
			dicttools.dunion_add(result, self.find_ngram(tuple(words[i:i+self.n]))) 
		return result

	def generate_next(self, *words):
		"""Randomly generate the next word in the model."""
		if len(words) > self.n:
			words = words[len(words)-self.n:]
		elif len(words) < self.n:
			words = ([None] * (self.n - len(words))) + words
		words = tuple(words)
		
		return weighted_random_selection(self.find_ngram(words))

	def find_ngram(self, tuple):
		"""Find an n-gram in the model."""
		return self.ngrams.get(tuple, {})

if __name__ == '__main__':
	import sys
	ngrams = NGram()
	if len(sys.argv) > 1:
		with open(sys.argv[1]) as f:
			ngrams.read_file(f)
	try:
		input = raw_input("Query> ")
		while input:
			input = input.split()
			print ngrams.search(*input)
			print ngrams.generate_next(*input)
			input = raw_input("Query> ")
	except EOFError:
		pass
	except KeyboardInterrupt:
		pass
	print
