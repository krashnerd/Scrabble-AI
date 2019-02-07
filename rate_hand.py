import tensorflow as tf

def get_letter_ary(word):
	letter_ary = [0]*26
	for letter in word.upper():
		letter_ary[ord(letter)-ord('A')] += 1

	return letter_ary

def test_input(word):
	ary = get_letter_ary(word)
	for idx, lettercount in enumerate(ary):
		if lettercount != 0:
			print("'%s' x %d" % (chr(idx + ord('A')), lettercount))

