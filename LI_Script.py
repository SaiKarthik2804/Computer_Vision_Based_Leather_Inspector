import cv2
import numpy as np
  

image = cv2.imread('growthmarks.jpg')

cv2.imshow("original img ",image)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
edged = cv2.Canny(gray, 40, 120)
contours, hierarchy = cv2.findContours(edged, 
cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)        

cv2.drawContours(image, contours, -1, (0, 0, 255), 5)
cv2.imshow("growthmark_defect.jpg", image)
cv2.imwrite("growthmark_defect.jpg", image)

ret, thresh1 = cv2.threshold(gray, 90, 255, cv2.THRESH_BINARY)

edged = cv2.Canny(thresh1, 40, 120)
contours, hierarchy = cv2.findContours(edged, 
cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
rth = gray.copy()
th = gray.copy()
recarea = 0
for i in contours:
    if cv2.contourArea(i) >0:
        rect = cv2.minAreaRect(i)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(rth,[box],0,(0,0,255),2)
        
        x,y,w,h = cv2.boundingRect(i)
        recarea = recarea + (w*h)
        cv2.rectangle(th,(x,y),(x+w,y+h),(0,255,0),2)

cv2.imshow("Defective areas optimized",rth)
cv2.imshow("Defective areas",th)

area = 0.0
for i in range(len(contours)):
            area = area+cv2.contourArea(contours[i])

def_area = (area/thresh1.size)*100
print("Total Area           = ",thresh1.size )
print("Defect curve area    = ",area)
print("Defect curve area(%) = "+str(def_area)+"%")
print("Defect rectagle area(%) = "+str((recarea/thresh1.size)*100)+"%")
