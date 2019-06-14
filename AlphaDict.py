class AlphaDict(object):
	def __init__(self):
		self.elements = [None] * 27

	def ind(self, letter):
		try:
			if letter == '$':
				return 26

			return ord(letter) - ord('A')
		except:
			return

	def __getitem__(self, letter):
		return self.elements[self.ind(letter)]

	def __setitem__(self, letter, value):
		self.elements[self.ind(letter)] = value

	def __contains__(self, letter):
		i = self.ind(letter)
		return i is not None and self.elements[i] is not None
