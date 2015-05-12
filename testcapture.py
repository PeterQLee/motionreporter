import cv2
from detection import *
cam=cv2.VideoCapture(0)
            
while True:
        #capture video
    ret,frame=cam.read()


    gray1=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                #gray1=cv2.fastNlMeansDenoising(gray1)
    ret,frame=cam.read()
    gray2=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                #gray2=cv2.fastNlMeansDenoising(gray2)
    ret,frame=cam.read()
    gray3=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                #gray3=cv2.fastNlMeansDenoising(gray3)
                #get summated greyscale
                
    disp=getConstantMotionValue((gray1,gray2,gray3))
    meanconst=cv2.mean(disp)
                #need to save timelapsed values as well
                #meanlapse=
    print(meanconst)
    cv2.imshow('frame',disp)
    if cv2.waitKey(1) & 0xFF == ord('q'):
    break
cam.release()
cv2.destroyAllWindows()
