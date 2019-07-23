import bruteforcer
import Scrabble

class ScrabblePlayer:
	def __init__(self, program):
		self.program = program

	def get_move(self, game):
		return self.program(game)

class GreedyPlayer(ScrabblePlayer):
	def __init__(self):
		ScrabblePlayer.__init__(self, bruteforcer.highest_scoring_move)	

def play_game(players):
	game = Scrabble.Scrabble(len(players))
	for player in game.players:
		player.rack.refill()
	while not game.get_winner():
		current_player = players[game.current_player_index]
		move = current_player.get_move(game)
		game = game.apply_move(move)
		print(game.board)
		print("Player {} made {} points".format(game.current_player_index, game.last_move_score))


	

def main():
	play_game([GreedyPlayer(), GreedyPlayer()])



if __name__ == '__main__':
	main()