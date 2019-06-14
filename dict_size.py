import sys, dawg_parser

def main():
	evaluated = list()

	dict = dawg_parser.get_dawg("dictionary.json")

	def count(node):
		