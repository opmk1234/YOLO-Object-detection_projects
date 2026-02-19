import cv2
from ultralytics import YOLO
import cvzone
import math
import numpy as np
from sort import *

classNames =["person", "bicycle", "car", "motorbike", "aeroplane", 
            "bus", "train", "truck", "boat", "traffic light", 
            "fire hydrant", "stop sign", "parking meter", "bench", 
            "bird", "cat", "dog", "horse","sheep", "cow", "elephant", 
            "bear", "zebra", "giraffe", "backpack", "umbrella", 
            "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard",
            "sports ball", "kite", "baseball bat", "baseball glove", 
            "skateboard","surfboard", "tennis racket", "bottle", 
            "wine glass", "cup", "fork", "knife", "spoon", "bowl",
            "banana", "apple", "sandwich", "orange", "broccoli", 
            "carrot","hot dog", "pizza", "donut", "cake", "chair", 
            "sofa", "pottedplant", "bed", "diningtable","toilet", 
            "tvmonitor", "laptop", "mouse", "remote", "keyboard", 
            "cell phone", "microwave","oven", "toaster", "sink", 
            "refrigerator", "book", "clock", "vase", "scissors", 
            "teddy bear", "hair drier", "toothbrush"]

model =YOLO('../Yolo-Weights/yolov8n.pt')
cap =cv2.VideoCapture('Cars/1.mp4')
# cap.set(3,1280)
# cap.set(4,720)
mask = cv2.imread('Area.png')
#tracking
tracker = Sort(max_age=20,min_hits=3,iou_threshold=0.3)

limits =[330,450,1150,450]
totalCount = []

while(True):
    suc,frame=cap.read()
    if not suc:
        break
    frameregion = cv2.bitwise_and(frame,mask)   
    result = model(frameregion,stream=True)
    cv2.line(frame,(limits[0],limits[1]),(limits[2],limits[3]),(0,0,255),5)
    detections = np.empty((0,5))
    
    #because of stream we have multiple results a list
    for r in result:
       boxes = r.boxes
       for box in boxes:
          x1,y1,x2,y2= box.xyxy[0]
          x1,y1,w,h = int(x1),int(y1),int(x2-x1),int(y2-y1)
          cvzone.cornerRect(frame,(x1,y1,w,h),l=15,rt=5,colorR=(255,255,255),colorC=(0,0,255))
          conf = (math.ceil(box.conf[0]*100)/100)
          cls=int(box.cls[0])
          CurrentClass =classNames[cls]
          if CurrentClass in ['car','truck','motorbike'] and conf>0.3:
           CurrentArray= np.array([x1,y1,x2,y2,conf])
           detections=np.vstack((detections,CurrentArray))
    
    resultTracker = tracker.update(detections)
    for result in resultTracker:
       x1,y1,x2,y2,id = result
       x1,y1,w,h = int(x1),int(y1),int(x2-x1),int(y2-y1)
       #cvzone.cornerRect(frame,(x1,y1,w,h),l=15,rt=5,colorR=(0,0,255),colorC=(0,0,255))     
       cvzone.putTextRect(frame,f'{int(id)}',(max(0,x1),max(65,y1)),scale=2,thickness=3,offset=10)
       cx,cy = (x1+w//2),(y1+h//2)
       if limits[0]<cx<limits[2] and limits[1]-15<cy<limits[1]+15:
        if id not in totalCount:
          totalCount.append(id)
          cv2.line(frame,(limits[0],limits[1]),(limits[2],limits[3]),(0,255,0),5)
       cv2.circle(frame,(cx,cy),5,(0,0,0),5,cv2.FILLED)
    cvzone.putTextRect(frame,f'Count{len(totalCount)}',(50,50),scale=2,thickness=3,offset=10)
         
    cv2.imshow('webcam',frame)
    #cv2.imshow('workingArea',frameregion)
    if cv2.waitKey(1) & 0XFF == ord('q'):
      break

cap.release()
cv2.destroyAllWindows()
