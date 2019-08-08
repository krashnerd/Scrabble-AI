class OccupiedSpaceError(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)

class NegativeIndexError(IndexError):
    def __init__(self,*args,**kwargs):
        IndexError.__init__(self,*args,**kwargs)

class InvalidMoveError(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)


class EmptyMoveError(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)

class GameError(Exception):
	def __init__(self, *args, **kwargs):
		Exception.__init__(self, *args, **kwargs)

class GameOverError(GameError):

	def __init__(self, *args, **kwargs):
		GameError.__init__(self, *args, **kwargs)
		self.message = "Attempted play on a completed game"

class TileNotFoundError(GameError):
	def __init__(self, *args, **kwargs):
		Exception.__init__(self, *args, **kwargs)
		self.expression = expression
		self.message = "Tile not found in player rack"
