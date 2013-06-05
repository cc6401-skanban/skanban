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
        
    def getTitulo(self, path):
        head, tail = os.path.split(path)
        f = os.path.splitext(tail)[0]
        return f

    #guarda el postit i para el imagen original "path" dado un Mat img. Retorna la ruta final relativa a la carpeta de donde se corre
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
    def findPostits(self, img, imgc2, rects, postits):
        
        cv2.imshow("window", img)
        cv2.imshow("window1", imgc2)
        cv2.waitKey()
        
        #encontramos las fronteras en la imagen de 0 y 1, cv2.RETR_EXTERNAL devuelve contorno externo, cv2.CHAIN_APPROX_SIMPLE : algoritmo utilizado para detectar contornos
        contours, hierarchy = cv2.findContours(imgc2,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        
        # blank = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
        ##cv2.drawContours( blank, contours, -1, (255,255,255),-1)
        # blank = cv2.cvtColor(blank, cv2.COLOR_BGR2GRAY)
        ##cv2.drawContours(blank,contours,0,(255,255,255),3)
        # cv2.drawContours( blank, contours, -1, (255,255,255),-1)
        # cv2.imshow("img", blank)
        # cv2.waitKey()
                        
        aux = []
        descartados = []
                        
        for cnt in contours:
            # obtenemos el perimetro
            cnt_len = cv2.arcLength(cnt, True)
            # se aproxima el contorno a un poligono
            cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
            # se calcula el area
            area = cv2.contourArea(cnt)
            # area minima para que se considere un post-it
            min_postit = 3000
            
            # si el area es mayor que el area minima y mas chica que el area minima por 20 y es un poligono de 4 lados y es convexo
            if area>min_postit and area < min_postit*20 and len(cnt) <6 and len(cnt) >=4 and cv2.isContourConvex(cnt):
                # se obtiene el rectangulo minimo que lo contiene orientado con respecto a la orientacion de los bordes de la imagen 
                rect = cv2.boundingRect(cnt)
                                        # ?
                cnt = cnt.reshape(-1, 2)
                #si no esta repetido, se agrega, si no se ignora
                aux.append(cnt)
                if not self.isPostitEncontrado(postits, cnt):
                    rects.append(rect)                            
                    postits.append(cnt)
            elif 0:
                print area, len(cnt)
                cv2.drawContours(img, [cnt], 0,(255,0,255),3) 
                cv2.imshow("window", img)
                cv2.waitKey()
                
        # blank = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
        # blank = cv2.cvtColor(blank, cv2.COLOR_BGR2GRAY)
        # #cv2.drawContours(blank,aux,0,(255,255,255),3)
        # cv2.drawContours( blank, aux, -1, (255,255,255),-1)
        # cv2.imshow("img", blank)
        # cv2.waitKey()

        return [postits, rects]


    def invertImage(self, img):
        img2 = img[:]
        img2 *= -1
        img2 += 1

        return img2

    def parse(self,path):
        titulo = self.getTitulo(path)
        if os.path.isfile(titulo+'.pkl'):
            return Board.load(titulo)

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
            imgc2 = cv2.Canny(gray, 20,150,5)
            postits, rects = self.findPostits(img, imgc2, rects, postits)

            retval, imgc2 = cv2.threshold(gray,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            postits, rects = self.findPostits(img, imgc2, rects, postits)            

            retval, imgc2 = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
            postits, rects = self.findPostits(img, imgc2, rects, postits)            

            for thr in xrange(0, 255, 25):
                retval, imgc2 = cv2.threshold(gray,thr,255,cv2.THRESH_BINARY)
                postits, rects = self.findPostits(img, imgc2, rects, postits)            
                retval, imgc2 = cv2.threshold(gray,thr,255,cv2.THRESH_BINARY_INV)
                postits, rects = self.findPostits(img, imgc2, rects, postits)            
                
                
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
        
            # subimagen que contiene el postit detectado
            img2 = cv2.getRectSubPix(img, (w, h), (x+w/2, y+h/2))
            
            path_ = self.saveImage(path, i, img2)
            board.append(Postit(path_, x, y, w, h))
            
            #cv2.imshow("imagen", img2)
            #cv2.waitKey()      
            i+=1
        return Board(board, self.getTitulo(path), "#ffffff", 800, 600)
                        
                        
#asi se usa:                        
#Parser().parse('../image.jpg')