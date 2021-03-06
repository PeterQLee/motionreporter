import cv2
import numpy as np

def getConstantMotionValue(shots): #shots is a tuple of images which will be differentiated
    val1=cv2.absdiff(shots[0],shots[1])
    val2=cv2.absdiff(shots[1],shots[2])
    #average these values to get overall difference
    avg=cv2.add(val1,val2)
    avg=cv2.divide(avg,2)

    #finally calculate and return the weighted average
    return avg

def getTimelapseMotionValue(shots): 
    #gets difference value based on a larger time span
    #obviously the tolerance value for this will be much higher
    
    val=cv2.absdiff(shots[0],shots[1])
    return cv2.mean(val)

