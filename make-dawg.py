import string
from functools import reduce
# EOF = dawg_node(True);
global counter

counter = 0
class dawg_node():
	""" Node of a Directed-Acrylic Word Graph, to be used for Scrabble AI"""
	def __init__(self, root, isEOF=False):
		self._paths = {}
		self._followers = [False] * 27
		self._parents = []
		self.SOF = isSOF
		self._root = root

		self._ind = 0
		
			

			# self._words_count_found = []

		self._num_words_test_counter = 0

		#Is this node terminal?
		self.term=isEOF		

	def add_parent(self, parent):
		self._parents.append(parent)
		self._root = parent._root

	def add_words(self, wordList):
		for word in wordList:
			self.add_word(word)

	def wordcount_test_increment(self):
		self._num_words_test_counter += 1

	def valid_paths(self):
		return filter(lambda x: x in self._paths, (list(string.ascii_uppercase) + ['$']))

	def add_node(self, letter):
		#Adds a new node where needed
		self._paths[letter]=dawg_node(self._root)

	def increment_counter(self):
		self._root.size_counter += 1

	def count_found(self, word):
		self._root.append(word)



	def count_words(self, parentStr = ""):
		#Counts the number of possible words that can be made from a given node. Recursive.

		# List of the child nodes' word counts
		
		children_wordcount = reduce((lambda a,b: a+b), 
				list(map(lambda path: self._paths[path].count_words(parentStr + path), 
					self.valid_paths())) + [0])

		if '$' in self._paths:
			# self.count_found(parentStr)
			return 1 + children_wordcount
		else: 
			return children_wordcount

	def add_word(self, word):
		if(word==''):
			self._paths['$']=dawg_node(self._root,True)
			self._paths['$'].add_parent(self)
			return
		letter = word[0]
		if letter not in self._paths:
			self.increment_counter()
			self._paths[letter] = dawg_node(self._root)
			self._paths[letter].add_parent(self)		
			self._root._all_nodes.append(self._paths[letter])

		self._paths[letter].add_word(word[1:])
		if len(self._paths[letter]._parents) == 0:
			print("WTF")

	def has_path(self, letter):
		return (letter in self._paths)

	def contains_node(self, other):
		if(self == other):
			return False
		for node in self.valid_paths():
			if self._paths[node].contains_node(other):
				return False
		return True
	def contains(self, word):

		#if the word is empty, return true iff the node contains EOS marker
		if(word == ''):
			return '$' in self._paths

		#if the first letter of the word can't go anywhere, return false
		if word[0] not in self._paths:
			return False

		return self._paths[word[0]].contains(word[1:])

	def __ne__(self,other):
		return self.__class__ != other.__class__ or not self.__eq__(other)

	def __eq__(self, other):
		if other.__class__.__name__ != 'dawg_node':
			return False

		# if self.term != other.term:
		# 	return False

		if "".join(self.valid_paths()) != "".join(other.valid_paths()):
			return False

		# for char in string.ascii_uppercase:
		# 	if(char in self._paths != char in other._paths):
		# 		return False

		for char in self.valid_paths():
			if(self._paths[char] != other._paths[char]):
				return False

		return True

	def prettyprint(self, offset = 0):
		#Pretty printing
		#Offset all but the first permutation by 'offset' spaces
		lst_perms = [" " + path  + self._paths[path].prettyprint(offset + 1) for path in self.valid_paths()]
		lst_perms = list(filter(lambda x: x.strip() != "$",lst_perms))
		return ("\n"+"  " * (offset)).join(lst_perms)


	# def __str__(self):
	# 	result = ""
	# 	for follower in self._valid+paths

	def __str__(self):
		result = ""
		for follower in self.valid_paths():
			if follower == "$":
				result += "$"
			else: 
				result += "(" + follower + str(self._paths[follower])
			result += "|"
		result = result[:-1] + ")"
		return result


class starter_dawg_node(dawg_node):
	def __init__(self):
		dawg_node.__init__(self, self)
		self.size_counter = 1
		self._root = self
		self._all_nodes = []


	def remove_dupes(self):
		





def testOutcome(expected, actual):
	if expected==actual:
		return "TEST PASSED\n\n"
	else:
		return "Expected: %d Actual: %d\n\n" % (expected, actual)

def test_wordcount():
	dawg = starter_dawg_node()
	filename = "dict-sample.txt"

	words_in_file = [(w[:-1] if w[-1]=='\n' else w)
						for w in open(filename).readlines()]

	expected_words = len(words_in_file)

	dawg.add_words(words_in_file)

	print("Testing wordcount...\n")
	print(testOutcome(expected_words,dawg.count_words()))

	# print("word_count_found len: %d" %len(dawg._words_count_found))
	# if(for word in words_in_file:
	# 	if(word not in dawg._words_count_found):
	# 		print("Count didn't find %s" % word)


	if(expected_words > dawg.count_words()):
		test_wordcontents()

	print([str(x) for x in dawg._all_nodes])
	print("nodes: %d" % dawg.size_counter)
	print(dawg)
	print(dawg.prettyprint())

def test_wordcontents():
	dawg = starter_dawg_node()

	filename = "dict-sample.txt"
	nl = '\n'
	words_in_file = open(filename).read().split('\n')
	print(words_in_file)
	dawg.add_words(words_in_file)
	found = 0
	total = 0

	for word in words_in_file:
		total += 1
		if (dawg.contains(word)):
			found += 1
		else:
			print("Dawg does not contain %d" % word)
	print("Found %d words out of %d" % (found,total))







def main():
	counter = 0
	dawg = dawg_node(False,True)

	lst_nodes = []
	lettercount = 0
	# for word in open("dict-sample.txt").readlines():
	# 	dawg.wordcount_test_increment += 1
	# 	wrd = word[:-1]#get rid of whitespace

	# 	lettercount += len(wrd)
	# 	dawg.add_word(wrd)

	test_wordcount()

	# print('Testing wordcount:\n')
	 



if __name__ == "__main__":
	main()

