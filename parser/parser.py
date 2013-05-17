import numpy as np
import cv2

class Parser(object):
    def __init__(self):
        pass
    def parse(self,path):
        postits = []
        rects = []
        if not path:
            return postits
            
        img = cv2.imread(path)
        img = cv2.resize(img, (800,600))
        img = cv2.GaussianBlur(img, (5, 5), 0)
        #aca guardamos los postits encontrados
                
        for gray in cv2.split(img):
            for thr in xrange(0, 255, 256):
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
        cv2.drawContours( img, postits, -1, (255,0,0),3)
        print postits[0]
        x,y,w,h = rects[0]
        
        img2 = cv2.getRectSubPix(img, (w, h), (x+w/2, y+h/2))
        cv2.imshow("img", img2)
        cv2.waitKey()      
           
        return postits
                        
                        
                        
Parser().parse('../image.jpg')
                        
                        
                        
                        
                        
                        
                        
                        
                        
