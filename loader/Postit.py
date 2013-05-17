
class Postit:
	path = ""
	posX = 0
	posY = 0
	sizeX = 0
	sizeY = 0

	def __init__(self, path="", posX=0, posY=0, sizeX=0, sizeY=0):
		self.path = path
		self.posX = posX
		self.posY = posY
		self.sizeX = sizeX
		self.sizeY = sizeY
	
	def moveTo(self, x, y):
		self.posX = x
		self.posY = y
	
	def getPosition(self):
		l = [self.posX, self.posY]
		return l
	


