import cv2
from ultralytics import YOLO
import cvzone
import math
from PokerHandFunc import poker_hand
classNames =[
              "10C","10D","10H","10S",
              "2C","2D","2H","2S",
              "3C","3D","3H","3S",
              "4C","4D","4H","4S",
              "5C","5D","5H","5S",
              "6C","6D","6H","6S",
              "7C","7D","7H","7S",
              "8C","8D","8H","8S",
              "9C","9D","9H","9S",
              "AC","AD","AH","AS",
              "JC","JD","JH","JS",
              "KC","KD","KH","KS",
              "QC","QD","QH","QS"]    
model =YOLO('../Yolo-Weights/Poker.pt')
cap =cv2.VideoCapture('1.mp4')
# cap.set(3,1280)
# cap.set(4,720)
while(True):
    suc,frame=cap.read()
    result = model(frame,stream=True)
    hands=[]
    #because of stream we have multiple results a list
    for r in result:
       boxes = r.boxes
       for box in boxes:
      #     x1,y1,x2,y2 = box.xyxy[0]
      #     x1,y1,x2,y2 = int(x1),int(y1),int(x2),int(y2)
      #     print(x1,y1,x2,y2)
          #cv2.rectangle(frame,(x1,y1),(x2,y2),(255,0,0),3)
          x1,y1,x2,y2= box.xyxy[0]
          x1,y1,w,h = int(x1),int(y1),int(x2-x1),int(y2-y1)
          cvzone.cornerRect(frame,(x1,y1,w,h))
          conf = (math.ceil(box.conf[0]*100)/100)
          cls=int(box.cls[0])
          hands.append(classNames[cls])
          cvzone.putTextRect(frame,f'{classNames[cls]} {conf}',(max(0,x1),max(65,y1)),scale=0.7,thickness=1)
    hands = list(set(hands))
    if len(hands)==5:
      results = poker_hand(hands)
      cvzone.putTextRect(frame,f'Your Hand: {results}',((50,50)),scale=2,thickness=3)     
    cv2.imshow('webcam',frame)
    if cv2.waitKey(1) & 0XFF == ord('q'):
      break
cap.release()
cv2.destroyAllWindows()