"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
Base = declarative_base()

from Postit import Postit
"""
import pickle

class Board(object):
    """
    __tablename__ = 'board'
    id = Column(Integer, primary_key=True)
    postits = []
    title = Column(String)
    background = Column(String)
    sizeX = Column(Integer)
    sizeY = Column(Integer)
    """
    id = 0
    postits = []
    title = ""
    background = ""
    sizeX = 0
    sizeY = 0

    def __init__(self, postits=[], title = "", background="", sizeX=800, sizeY=600):
        self.postits = postits
        self.title = title
        self.background = background
        self.sizeX = sizeX
        self.sizeY = sizeY
    
    def addPostit(self, p):
        self.postits.append(p)

    def save(self):
        fp = open(self.title+'.pkl', 'w+')
        pickle.dump(self, fp)

    @staticmethod
    def load(title):
        fp = open(title+'.pkl', 'r')
        return pickle.load(fp)

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
