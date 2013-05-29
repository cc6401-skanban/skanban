import numpy as np
import cv2
import math
import sys, os
sys.path.insert(0,"../loader/")
from Postit import *
from Board import *

class InvalidPath(Exception):
    pass

class Parser(object):
    def __init__(self):
        pass
        
    #guarda el postit i para el imagen original "path" dado un Mat img. Retorna la ruta final relativa a la carpeta de donde se corre
    def saveImage(self, path, i, img):
        head, tail = os.path.split(path)
        f = os.path.splitext(tail)[0]
        d = os.path.join('images/'+f)   
           
        if not os.path.exists(d):
            os.makedirs(d)
        filename = d+"/postit_"+str(i)+".jpg"
        cv2.imwrite(filename, img)
        return filename
        
    def isPostitEncontrado(self, postits, postitr):
        for i in xrange(0, len(postits)):
            postit = postits[i] 
            #calculamos el centro de gravedad
            xc = (postit[0][0] + postit[1][0] + postit[2][0] + postit[3][0])/4.0
            yc = (postit[0][1] + postit[1][1] + postit[2][1] + postit[3][1])/4.0

            perimetro = cv2.arcLength(postit, True)

            
            #calculamos el centro de gravedad
            xcr = (postitr[0][0] + postitr[1][0] + postitr[2][0] + postitr[3][0])/4.0
            ycr = (postitr[0][1] + postitr[1][1] + postitr[2][1] + postitr[3][1])/4.0

            #si las distancias de los centros de gravedad son muy chicas no agregar postit a lista final
            if math.sqrt((xc-xcr)**2 + (yc-ycr)**2) < perimetro/8:
                return True
        return False
                
    def parse(self,path):
        postits = []
        rects = []
        if not path:
            return postits
            
        img = cv2.imread(path)
        if img == None:
            raise InvalidPath
        img = cv2.resize(img, (800,600))
        img = cv2.GaussianBlur(img, (5, 5), 0)
        #aca guardamos los postits encontrados
                
        for gray in cv2.split(img):
            for thr in xrange(0, 255, 25):
                if thr == 0:
                    imgc2 = cv2.Canny(gray, 20,150,5)
                else:
                    retval, imgc2 = cv2.threshold(gray,thr,255,cv2.THRESH_BINARY_INV)
                """    
                cv2.imshow("window", img)
                cv2.imshow("window1", imgc2)
                cv2.waitKey()
                """
                #encontramos contornos
                contours, hierarchy = cv2.findContours(imgc2,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
                               
                
                for cnt in contours:
                    cnt_len = cv2.arcLength(cnt, True)
                    cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
                    area = cv2.contourArea(cnt)
                    min_postit = 5000
                    
                    if area>min_postit and area < min_postit*20 and len(cnt) == 4 and cv2.isContourConvex(cnt):
                        rect = cv2.boundingRect(cnt)
                        cnt = cnt.reshape(-1, 2)
                        #si no esta repetido, se agrega, si no se ignora
                        if not self.isPostitEncontrado(postits, cnt):
                            rects.append(rect)                            
                            postits.append(cnt)
                        
           
        """
        blank = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
        cv2.drawContours( blank, postits, -1, (255,255,255),-1)
        blank = cv2.cvtColor(blank, cv2.COLOR_BGR2GRAY)
        
        
        cv2.imshow("img", blank)
        cv2.waitKey()      
        
        postits, hierarchy = cv2.findContours(blank,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)      
        print len(postits)
       
        cv2.drawContours(blank,postits,0,(255,255,255),3)
        cv2.imshow("img", blank)
        """

        

        #dibujar contornos de postits no repetidos
        #cv2.drawContours( img, postits, -1, (255,0,0),3)
        #cv2.imshow("img", img)
        #cv2.waitKey()
        
        #si encontre mas de un postit
        i=0        
        board = []
        for postit in postits:
            #Recortar y mostrar el primero            
            x,y,w,h = rects[i]
        
            img2 = cv2.getRectSubPix(img, (w, h), (x+w/2, y+h/2))
            
            path_ = self.saveImage(path, i, img2)
            board.append(Postit(path_, x, y, w, h))
            
            #cv2.imshow("imagen", img2)
            #cv2.waitKey()      
            i+=1
        return Board(board, "Titulo", "#ffffff", 800, 600)
                        
                        
#asi se usa:                        
Parser().parse('../image.jpg')
                        
                        
                        
                        
                        
                        
                        
                        
                        
