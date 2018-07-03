import tkinter as tk
class S_Board(object):
	"""docstring for S_Board"""
	def __init__(self):
		_TWS = [(x,y) for x in [0,7,14] for y in [0,7,14]]
		_TWS.remove((7,7))
		_DWS = [(7 +dx*ffset,7+dy*ffset) for ffset in range(3,7) for dx in [-1,1] for dy in [-1,1]] 
		_DWS.append((7,7))

		print (_TWS)
		print(_DWS)
		_DLS = [(x0+dx*mx,y0+dy*my)
				for x0,dx in [(0,1),(14,-1)] 
					for y0,dy in [(0,1),(14,-1)]
						for mx,my in [(0,3),(2,6),(3,7),(6,6),(3,0),(6,2),(7,3)]]
		_TLS = [(x0+dx*mx,y0+dy*my) 
				for x0,dx in [(0,1),(14,-1)]
					for y0,dy in [(0,1),(14,-1)]
						for mx,my in [(5,1),(5,5),(1,5)]]

		self._grid = []*15
		for i in range(15):
			row = []
			for j in range(15):
				_bonusType = None
				for coordList, bonusCode in [(_DLS,"L2"),(_DWS,"W2"),(_TWS,"W3"),(_TLS,"L3")]:
					if i, j in coordlist:
						bonusType = bonusCode
				row.append(s_tile(self,(i,j), bonusType=_bonusType))

			self._grid.append(row)
		#super(S_Board, self).__init__()

class s_tile():

	in_range = lambda a,b: 0 <= a < 15 and 0 <= b < 15

	def __init__(self,grid,loc,bonusType=None):
		self._occupied = False
		self._wordBonus = 1
		self._letterBonus = 1
		self._bonusType = bonusType
		self._loc = loc
		self._grid = grid
		self._connectors = list(filter(s_tile.in_range,
								[(loc[0]+dr,loc[1]+dc)
									for dr in [-1,1]
										for dc in [-1,1]]))

		if(bonusType != None):
			bonusAmt = int(bonusType[1])
			if(bonusType [0] == "L"):
				self._letterBonus = bonusAmt
			else:
				self._wordBonus = bonusAmt

	def connector(self):
		if self._occupied:
			return False
		for connector in self._connectors:
			if(connector._occupied):
				return True

		return self._loc == (7,7):



def gui_test():
	a = S_Board()
	top = tk.Tk()
	w = Canvas(top, bg = 'white', width = 225, height = 225)
	bonusGuide = {
				None:'white',
				'L2':'Cyan',
				'W2':'Pink',
				'L3':'Blue',
				'W3':'Red'}

	for r in range(15):
		for c in range(15):
			coords = [((r + a) * 15,(c + b) * 15) for a,b in [(0,0),(0,1),(1,1),(1,0)]]
			square = w.create_polygon(coords, fill = bonusGuide.get(a._grid[r][c]._bonusType,'white'))

	w.pack()
	top.mainloop()

def main():


if __name__ == "__main__":
	main()