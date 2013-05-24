import numpy as np
import cv2
import math

class InvalidPath(Exception):
    pass

class Parser(object):
    def __init__(self):
        pass
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
                    
                #cv2.imshow("window", img)
                #cv2.imshow("window1", imgc2)
                #cv2.waitKey()
                
                #encontramos contornos
                contours, hierarchy = cv2.findContours(imgc2,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
                               
                
                for cnt in contours:
                    cnt_len = cv2.arcLength(cnt, True)
                    cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
                    area = cv2.contourArea(cnt)
                    min_postit = 1000
                    
                    if area>min_postit and area < min_postit*100 and len(cnt) == 4 and cv2.isContourConvex(cnt):
                        rects.append(cv2.boundingRect(cnt))
                        cnt = cnt.reshape(-1, 2)
                        postits.append(cnt)
                        
            break
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

        #Quitar post-its repetidos
        postitsnr = []

        for i in xrange(0, len(postits)):
            postit = postits[i] 
            xc = (postit[0][0] + postit[1][0] + postit[2][0] + postit[3][0])/4.0
            yc = (postit[0][1] + postit[1][1] + postit[2][1] + postit[3][1])/4.0

            perimetro = cv2.arcLength(postit, True)

            for j in xrange(i+1, len(postits)):
                postitr = postits[j] 
                xcr = (postitr[0][0] + postitr[1][0] + postitr[2][0] + postitr[3][0])/4.0
                ycr = (postitr[0][1] + postitr[1][1] + postitr[2][1] + postitr[3][1])/4.0


                if math.sqrt((xc-xcr)**2 + (yc-ycr)**2) < perimetro/8:
                    break

                if j == len(postits)-1:
                    postitsnr.append(postit)

            if i == len(postits)-1:
                postitsnr.append(postit)


        cv2.drawContours( img, postitsnr, -1, (255,0,0),3)
        cv2.imshow("img", img)
        cv2.waitKey()
        if len(postits) != 0:
            print postits[0]
            x,y,w,h = rects[0]
        
            img2 = cv2.getRectSubPix(img, (w, h), (x+w/2, y+h/2))
            cv2.imshow("img", img2)
            cv2.waitKey()      
           
        return postitsnr
                        
                        
                        
#Parser().parse('../image.jpg')
                        
                        
                        
                        
                        
                        
                        
                        
                        
