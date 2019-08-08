from dictionary_files.build_dictionary import *

class Scrabble_Dictionary():
	def __init__(self):
		self.starting_node = get_dictionary()
	def __contains__(self, word):


		if not isinstance(word, str):
			raise TypeError("Expected type str, got {}".format(type(word)))
		return check_word(word, self.dictionary)