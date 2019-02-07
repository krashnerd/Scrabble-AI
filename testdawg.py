from Dawg import *


def new_dawg(wordList):
	new = Dawg()
	new.construct_dawg(wordList)
	return new

def testOutcome(expected, actual):
	if expected==actual:
		return "TEST PASSED\n\n"
	else:
		return "Expected: %d Actual: %d\n\n" % (expected, actual)

def compare(_dawg, i1, i2):
	n1 = _dawg._all_nodes[i1]
	n2 = _dawg._all_nodes[i2]

	for node in [n1,n2]:
		print(node.valid_paths)
		print(node._paths['$'])
		print(node._paths['$']._all_list_location)


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

	test_wordcontents()

	#print([str(x) for x in dawg._all_nodes])
	print("nodes before removing: %d" % dawg.size_counter)
	print(str(dawg))
	dawg.remove_dupes()
	print("nodes after removing: %d" % len(dawg._all_nodes))
	print(str(dawg))

	print(testOutcome(expected_words,dawg.count_words()))

def test_export(infile = "dict-sample.txt", outfile = "testoutput2"):
	_dawg = Dawg()
	word_list = open(infile).read().split("\n")
	_dawg.construct_dawg(word_list)
	_dawg.export(outfile)


def test_wordcontents(word_list, _dawg = None):

	if _dawg == None:

		dawg = Dawg()
		dawg.add_words(word_list)

	found = 0
	total = 0

	for word in word_list:
		total += 1
		if not dawg.contains(word):
			not_found += 1
		# else:
		# 	print("Dawg does not contain %d" % word)
	result = ("Found %d words out of %d" % (total-not_found,total))
	if(not_found != 0):
		result += "%d words in word_list not found" % not_found

def test_json_export():
	word_list = open("dict-sample.txt").read().split("\n")
	my_dawg = Dawg()
	my_dawg.construct_dawg(word_list)
	print(my_dawg.json_export())

def full_json_export():
	dict_dawg = Dawg()
	dictfile = open('dict.txt') #= open(input("input file: "))
	outf = open('full_output.json',"w")
	for word in dictfile:
		dict_dawg.add_word(word[:-1])
	dict_dawg.update_indices()
	dict_dawg.remove_dupes()
	dict_dawg.update_indices()
	
	all_attr = lambda d_node: {'len':len(d_node.valid_paths()), 'paths':[{path: d_node._paths[path]._all_list_location} for path in d_node.valid_paths()]}

	outf.write("[%s" % json.dumps(all_attr(dict_dawg._all_nodes[0]), separators=(',', ':')))

	for i in dict_dawg._all_nodes[1:]:
		outf.write(",")
		outf.write(json.dumps(all_attr(i), separators=(',', ':')))




			

def main():
	full_json_export()

	# test_export("dict-sample.txt","full_dict")

if __name__ == "__main__":
	main()
