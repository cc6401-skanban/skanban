from django.db import models

class Postit(models.Model):
    id = models.AutoField(primary_key=True)
    path = models.CharField(max_length=255)
    posX = models.IntegerField()
    posY = models.IntegerField()
    sizeX = models.IntegerField()
    sizeY = models.IntegerField()

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
