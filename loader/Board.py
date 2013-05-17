from Postit import Postit

class Board:
	postits = []
	title = ""
	background = ""
	sizeX = 800
	sizeY = 600

	def __init__(self, postits=[], title = "", background="", sizeX=800, sizeY=600):
		self.postits = postits
		self.title = title
		self.background = background
		self.sizeX = sizeX
		self.sizeY = sizeY
	
	def addPostit(self, p):
		self.postits.append(p)
