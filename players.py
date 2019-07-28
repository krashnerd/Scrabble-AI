import bruteforcer, utils, datetime
import Scrabble

class ScrabblePlayer:
	def __init__(self, program):
		self.program = program
		self.time_taken = datetime.timedelta(0)

	def get_move(self, game):
		return self.program(game)

class GreedyPlayer(ScrabblePlayer):
	def __init__(self):
		ScrabblePlayer.__init__(self, bruteforcer.highest_scoring_move)	

def play_game(players):
	game = Scrabble.Scrabble(len(players))

	turn = 0
	while game.get_winner() is None:
		current_player = players[game.current_player_index]
		print("\n\nTurn {}\n:".format(turn))

		print("Player {} evaluating {} moves".format(game.current_player_index, utils.count(bruteforcer.all_moves(game))))
		t0 = datetime.datetime.now()
		move = current_player.get_move(game)
		t1 = datetime.datetime.now()

		time = t1-t0
		current_player.time_taken += time
		game.apply_move(move)
		print(game.board)
		turn += 1
		print("Player {} made {} points in time {}".format(game.current_player_index, game.last_move_score, time))
		for i in range(len(players)):
			print("Player {}: {}, rack: {}".format(i, game.players[i].score, "".join([tile.letter for tile in game.players[i].rack])))


	print("Winner: Player {}".format(game.get_winner()))
	for i, player in enumerate(players):
		print("Player {} total time: {}".format(i, player.time_taken))
	print("Total bingos: {}".format(game.bingo_count))



