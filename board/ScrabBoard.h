#include <Python.h>

struct Point
	{
	    int x, y;
	    Point(int x_, int y_) : x(x_), y(y_) {}
	}

class ScrabBoard
{
public:
	ScrabBoard()
	{
		for (size_t r=0;r<15;r++)
			for(size_t c=0;c<15;c++)
				grid[r][c]='_';

	}

	get(size_t r, size_t c)
	{
		return grid[r][c];
	}

		;
	~ScrabBoard();
private:
	struct space{
		size_t wordBonus,letterBonus;
		char letter;
		bool occupied;

		space(int _bWord, int _bLetter): 
			wordBonus(_bWord), letterBonus(bLetter), letter('_'){};

		space():wordBonus(1),letterBonus(1),letter('_'){};
	}

	space grid[15][15];



};