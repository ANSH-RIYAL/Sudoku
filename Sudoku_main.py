from math import sqrt
import random

class SudokuBoard():

	def __init__(self, size = 9):
		self.grid = [[0 for x in range(size)] for y in range(size)]
		self.size = size
		self.RootSize = int(sqrt(size))
		self.HiddenSquares = []

	def availableEntries(self, row, col):

		'''
		Returns a list of numbers that can be put in a particular
		empty square at a given time.
		'''

		available = []

		for i in range(1, self.size + 1):
			if self.validNum(row, col, i):
				available.append(i)

		return available

	def CheckBox(self, row, col, val):

		'''
		Checks if the number has been places in the same 3x3 Box to 
		ensure there is not repetition in that box.
		'''

		StartingRow = row - row%self.RootSize
		StartingColumn = col - col%self.RootSize

		for i in range(self.RootSize):
			for j in range(self.RootSize):
				if self.grid[StartingRow + i][StartingColumn + j] == val:
					return False

		return True

	def CheckRow(self, row, val):

		'''
		Checks if the number has been places in the same Row to 
		ensure there is not repetition in that row.
		'''

		for i in range(self.size):
			if self.grid[row][i] == val:
				return False

		return True

	def CheckColumn(self, col, val):

		'''
		Checks if the number has been places in the same 3x3 Column to 
		ensure there is not repetition in that column.
		'''

		for i in range(self.size):
			if self.grid[i][col] == val:
				return False

		return True

	def validNum(self, row, col, val):

		'''
		Combines the CheckColumn, CheckRow and CheckBox function to ensure
		that the proper Sudoku rules are followed.
		'''

		validRow = self.CheckRow(row, val)
		validColumn = self.CheckColumn(col, val)
		validBox = self.CheckBox(row, col, val)

		if not validRow:
			print "INVALID ENTRY: SAME ENTRY FOUND IN THE SAME ROW."
			return False

		elif not validColumn:
			print "INVALID ENTRY: SAME ENTRY FOUND IN THE SAME COLUMN."
			return False
		
		elif not validBox:
			print "INVALID ENTRY: SAME ENTRY FOUND IN THE SAME BOX."
			return False
		
		else:
			return True

	def fillNum(self, row, col, val):

		'''
		Assigns a number to a particular position in the Sudoku.
		'''

		self.grid[row][col] = val

	def UnfilledSquares(self):

		'''
		Return a list of squares that still have to be filled in order
		to consider a Sudoku fully filled.
		'''

		unfilled = []

		for i in range(self.size):
			for j in range(self.size):
				if self.grid[i][j] == 0:
					unfilled.append((i, j))

		return unfilled

	def Solve(self):

		'''
		Solve() would change the current grid into a possile solution.
		It uses a simple backtracking algorithm and recursively tries to 
		fill a position unless a correct configuration of all the numbers
		in the Sudoku is found.

		NOTE: There can be multiple correct solutions to a Sudoku Puzzle
			  ans this function would return only one of them.

		'''

		EmptySquares = self.UnfilledSquares()

		if len(EmptySquares) == 0:
			return True

		self._Solve()

	def _Solve(self):

		EmptySquares = self.UnfilledSquares()

		if len(EmptySquares) == 0:
			return True

		for i in sorted(range(1, self.size + 1), key = lambda k: random.random()):

			if self.validNum(EmptySquares[0][0], EmptySquares[0][1], i):

				self.fillNum(EmptySquares[0][0], EmptySquares[0][1], i)

				if self._Solve() == True:
					return True

				self.fillNum(EmptySquares[0][0], EmptySquares[0][1], 0)

		return False

	def PrintSudokuBoard(self):

		'''
		Prints the current state of the Sudoku.
		'''

		for i in range(self.size):
			for j in range(self.size):
				print self.grid[i][j],
			print

	def HideNumbers(self, k):

		'''
		Hides K numbers randomly in the grid and updates
		the squares that are hidden.
		'''

		AlreadyHidden = []

		i = 0

		while i < k:
			row = random.randint(0, self.size-1)
			col = random.randint(0, self.size-1)
			if (row, col) not in AlreadyHidden:
				AlreadyHidden.append((row, col))
				i += 1
				self.grid[row][col] = 0

		self.HiddenSquares = []

		for i in range(self.size):
			for j in range(self.size):
				if self.grid[i][j] == 0:
					self.HiddenSquares.append((i, j))

	def Mistakes(self):

		'''
		Return a list of numbers where there are possible repetitions
		and straight forward mistakes.
		Eg: Placing a number twice in the same row,
		'''

		mistakes = set()

		for i in range(self.size):
			for j in range(self.size):
				if self.grid[i][j] == 0:
					continue
				for k in range(self.size):
					# Same row check
					if k != j and grid[i][k] == grid[i][j]:
						if (i, j) in self.HiddenSquares:
							mistakes.add((i, j))
						if (i, k) in self.HiddenSquares:
							mistakes.add((i, k))
					# Same column check
					if k != i and grid[k][j] == grid[i][j]:
						if (i, j) in self.HiddenSquares:
							mistakes.add((i, j))
						if (k, j) in self.HiddenSquares:
							mistakes.add((k, j))

				#Same box check

				row = i - i%self.RootSize
				column = j - j%self.RootSize

				for x in range(self.RootSize):
					for y in range(self.RootSize):
						if (x == i and y == j) or grid[x][y] == 0:
							continue
						if self.grid[x][y] == self.grid[i][j]:
							if (x, y) in self.HiddenSquares:
								mistakes.add((x, y))
							if (i, j) in self.HiddenSquares:
								mistakes.add((i, j))

		return list(mistakes)

sudoku = SudokuBoard()
sudoku.Solve()
sudoku.HideNumbers(10)
sudoku.PrintSudokuBoard()
