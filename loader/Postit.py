# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import Column, Integer, String

# Base = declarative_base()

class Postit():
    # __tablename__ = 'postit'
    # id = Column(Integer, primary_key=True)
    # path = Column(String)
    # posX = Column(Integer)
    # posY = Column(Integer)
    # sizeX = Column(Integer)
    # sizeY = Column(Integer)

    def __init__(self, path="", posX=0, posY=0, sizeX=0, sizeY=0):
        self.path = path
        self.posX = posX
        self.posY = posY
        self.sizeX = sizeX
        self.sizeY = sizeY
    
    def moveTo(self, x, y):
        self.posX = x
        self.posY = y
        
        # Mensaje de prueba
        print "Me movi a " + str(self.posX) + ", " + str(self.posY)
    
    def getPosition(self):
        l = [self.posX, self.posY]
        return l


