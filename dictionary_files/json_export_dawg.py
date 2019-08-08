

"""Krishna Kahn
   Script used to export create DAG and export the JSON file"""

from Dawg import *

def main():
	dict_dawg = Dawg()
	dictfile = open('Dict.txt') #= open(input("input file: "))
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

if __name__ == '__main__':
	main()