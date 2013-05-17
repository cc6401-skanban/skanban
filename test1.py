import numpy as np
import cv2
import math
 
def segment_on_dt(a, img):
    border = cv2.dilate(img, None, iterations=5)
    border = border - cv2.erode(border, None)

    dt = cv2.distanceTransform(img, 2, 3)
    dt = ((dt - dt.min()) / (dt.max() - dt.min()) * 255).astype(np.uint8)
    _, dt = cv2.threshold(dt, 180, 255, cv2.THRESH_BINARY)
    lbl, ncc = label(dt)
    lbl = lbl * (255/ncc)
    # Completing the markers now. 
    lbl[border == 255] = 255

    lbl = lbl.astype(np.int32)
    cv2.watershed(a, lbl)

    lbl[lbl == -1] = 0
    lbl = lbl.astype(np.uint8)
    return 255 - lbl

def binarizar(im, thr):
  for j in range(len(im)):
    for i in range(len(im[j])):
      mean = np.mean(im[j,i])
      if mean > thr:
        im[j,i] = (0,0,0)
  return im
    
def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )

im = cv2.imread('imagen2.jpg')
im = cv2.resize(im, (800,600))
#a = np.asarray(im)
#im = cv2.fromarray(a)
#print a
for gray in cv2.split(im):
    imgray = gray
    #imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    #imgray = cv2.equalizeHist(imgray)

    #imgray[imgray>250] = 0
    #im = binarizar(im, 155)
    for thr in xrange(0, 255, 25):
        #retval, imgray = cv2.threshold(gray, thr, 255, cv2.THRESH_BINARY)
        #imgray[imgray>thr] = 255
        #imgray[imgray<=thr] = 0

	if thr == 0:
            imgc2 = cv2.Canny(gray, 20,150,5)
	else:
	    retval, imgc2 = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
	    #retval, imgc2 = cv2.threshold(gray,thr,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	    #retval, imgc2 = cv2.threshold(gray,thr,255,cv2.THRESH_BINARY)
	    """
            img_bin = cv2.morphologyEx(imgc2, cv2.MORPH_OPEN, np.ones((3, 3), dtype=int))
	
            result = segment_on_dt(im, img_bin)
	    cv2.imshow("cas", result)
            cv2.waitKey()
            """

	    #retval, imgc2 = cv2.threshold(gray,0,255,cv2.THRESH_OTSU)
            """
	    fg = cv2.erode(imgray,None,iterations = 2)
	    bgt = cv2.dilate(imgray,None,iterations = 3)
            ret,bg = cv2.threshold(bgt,1,128,1)
            marker = cv2.add(fg,bg)
	    marker32 = np.int32(marker)
            cv2.watershed(im,marker32)
            m = cv2.convertScaleAbs(marker32)
            ret,thresh = cv2.threshold(m,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
            res = cv2.bitwise_and(im,im,mask = thresh)
            imgc2 = imgray
            cv2.imshow("cas", im)
	    """
	

        cv2.imshow("window", imgray)
        cv2.imshow("window1", imgc2)
        cv2.waitKey()
        """
        lines = cv2.HoughLinesP(imgc2, 1, np.pi/180, 30, 30, 5)
        for line in lines[0]:
            #print line
            cv2.line(imgray, (line[0], line[1]), (line[2],line[3]), (0,0,255), 2)
        """
        #imgray = cv2.blur(imgray,(3,3))
        #imgray = cv2.GaussianBlur(imgray,(5,5),0)
        ret,thresh = cv2.threshold(imgc2,127,255,0)
        contours, hierarchy = cv2.findContours(imgc2,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        squares = []
        rejected = []
        random = []
        donde = []
        for cnt in contours:
            cnt_len = cv2.arcLength(cnt, True)
            #cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
            if cv2.contourArea(cnt)>1000: #len(cnt) == 4 and cv2.contourArea(cnt) > 6:# and cv2.isContourConvex(cnt):
                cnt = cnt.reshape(-1, 2)
                max_cos = np.max([angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in xrange(4)])
                if max_cos < 0.1:
                    squares.append(cnt)
    	        else:
    		    squares.append(cnt)
                #cv2.drawContours(im,[cnt],0,(255,0,255),3)
    	        #print cv2.contourArea(cnt), cnt
                #cv2.imshow("window", im)
                #cv2.waitKey()
        	"""
        	cv2.drawContours(im,squares,-1,(0,255,0),3)
        	cv2.drawContours(im,rejected,-1,(255,0,0),3)
                cv2.imshow("window", im)
                cv2.waitKey()
    	        """
            elif cv2.contourArea(cnt)>10:
                random.append(cnt)
        	#cv2.drawContours(im,[cnt],0,(0,0,255),2)
                #random.append(cnt)
    	        """
                cv2.drawContours(im,random,-1,(0,0,255),3)
                cv2.imshow("window", im)
                cv2.waitKey()
    	        """
    	    else:
    	        """
                cv2.drawContours(im,[cnt],0,(255,0,255),3)
                cv2.imshow("window", im)
                cv2.waitKey()
    	        """
                """
    	        cv2.drawContours(im,[cnt],0,(255,0,255),3)
                cv2.imshow("window", im)
                cv2.waitKey()
    	        """
    	
        cv2.drawContours(im,squares,-1,(0,255,0),3)
        cv2.imshow("window", im)
        cv2.waitKey()
    break
    
