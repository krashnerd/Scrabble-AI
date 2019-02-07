""" Parsing JSON file and making DAWG """
import time
import json

def check_word(word, start):
	if(word[-1] != "$"):
		word += "$"
	curr = start
	for letter in word:
		if letter not in curr:
			return False
		curr = curr[letter]
	return True
def get_dawg(filename):
	data = json.loads(open(filename).read())
	dawg_nodes= []
	count = 0
	for element in data:
		dawg_nodes.append({})

	for idx, node in enumerate(data):
		for path in node['paths']:
			for key in path.keys():
				dawg_nodes[idx][key] = dawg_nodes[path[key]]

	return dawg_nodes[0]

def dict_REPL():
	dictionary = get_dawg("full_output.json")
	inp = None
	print("Input a word to check in the dictionary, or input 'Q' to quit")
	while inp != "Q":
		if inp:
			t1 = time.time()
			is_word = check_word(inp, dictionary)
			t2 = time.time()
			mic_seconds = int((t2 - t1) * 1000000)
			print("Time: %d microseconds\n%s is %s a word!\n" % (mic_seconds, inp, "" if is_word else "not"))
		inp = input("Word: ").upper()

def main():
	dict_REPL()

def read(filename):
	pass
	


if __name__ == '__main__':
	main()