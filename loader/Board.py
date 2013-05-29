from Postit import Postit
import sqlite3 as lite

class Board(object):
	_id = 0
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

	# def persist(self):
		# con = None

		# try:
			# con = lite.connect('skanban.db')
			
			# cur = con.cursor()    
			# cur.execute('SELECT * FROM board WHERE board.')
			
			# data = cur.fetchone()
			
			# print "SQLite version: %s" % data                
			
		# except lite.Error, e:
			
			# print "Error %s:" % e.args[0]
			# sys.exit(1)
			
		# finally:
			
			# if con:
				# con.close()