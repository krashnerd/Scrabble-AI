import players, datetime, copy, Scrabble, bruteforcer

class SmarterPlayer(players.ScrabblePlayer):
	def __init__(self):
		players.ScrabblePlayer.__init__(self, None)

	def get_best_move(self, game):
		moves = bruteforcer.all_moves(game)
		



def main():
	player = SmarterPlayer()
	game = Scrabble.Scrabble()
	player.test_memory_leak(game)

if __name__ == '__main__':
	main()