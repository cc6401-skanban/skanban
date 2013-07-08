import sys
import wx
import DragCanvas
import Board
import cv2
import numpy as np
from Postit import *
import os 
class drawKanban():
    # recibe un objeto Board que contiene el kanban
    def __init__(self, kanban):
        self.app = wx.PySimpleApp()
        self.frame = wx.Frame(None, -1, kanban.title, pos=(50,50), size=(kanban.sizeX, kanban.sizeY), style=wx.DEFAULT_FRAME_STYLE, name="run a sample")

        # recibe la imagen de fondo y una lista de los objetos postIt
        self.dc = DragCanvas.DragCanvas(self.frame,-1, kanban.background, kanban)
        self.kanban = kanban
        self.customPostit()

    def showKanban(self):
        self.frame.Show(1)
        self.app.MainLoop()

    def customPostit(self):
        print "new"
        self.adding = True
        img = cv2.imread(self.kanban.path)

        self.img = cv2.resize(img, (800,600))
        self.img_clean = np.copy(self.img)
        
        self.nPoints = []
        cv2.imshow("window", self.img)
        cv2.setMouseCallback("window", self.onmouse)

        
        while self.adding:           
            cv2.waitKey(60)
        cv2.destroyWindow("window")
        
        

    def onmouse(self, event, x, y, flags, param):
    	
        if flags & cv2.EVENT_FLAG_LBUTTON:
            print "left"
            self.nPoints+=[[[x,y]]]
            if len(self.nPoints)>=4:
               self.cutPostit()
            cv2.circle(self.img, (x, y), 2, (0, 0, 255), -1)
            cv2.imshow("window", self.img)
            
    def cutPostit(self):
    	print "cuting"
    	rect = cv2.boundingRect(np.array(self.nPoints))
    	x,y,w,h = rect
    	img = cv2.getRectSubPix(self.img_clean, (w, h), (x+w/2, y+h/2))  


        path_ = self.saveImage(self.kanban.path, len(self.kanban.postits)+1, img)
        self.kanban.postits.append(Postit(path_, x, y, w, h))
        self.kanban.save()
        
        self.dc.reInit(self.kanban)
        self.adding = False

        

    def saveImage(self, path, i, img):
				# divide el path considerando el /
        head, tail = os.path.split(path)
        f = os.path.splitext(tail)[0]
        d = os.path.join('images/'+f)   
           
        if not os.path.exists(d):
            os.makedirs(d)
        filename = d+"/postit_"+str(i)+".jpg"
        cv2.imwrite(filename, img)
        return filename
        
    
