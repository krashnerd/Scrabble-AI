from string import ascii_uppercase

class AlphaDict(object):
	def __init__(self):
		for l in ascii_uppercase:
			setattr(self, l, None)

	def __getitem__(self, letter):
		getattr(self, letter)

	def __setitem__(self, letter, value):
		setattr(self, letter, value)

	def __contains__(self, letter):
		return getattr(self, letter) is not None



