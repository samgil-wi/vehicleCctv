from tkinter import Canvas, PhotoImage, Frame
import tkinter as tk
from utils.pathUtils import getFrameUtilPath
import cv2
import pandas as pd
import numpy as np
from ultralytics import YOLO
from utils.tracker import*
import time
import PIL.Image, PIL.ImageTk
from math import dist
model=YOLO('yolov8s.pt')

class PlayVideo(Frame):    
        
    def __init__(self, master, filePath):
        Frame.__init__(self, master)
        
        self.__frameRoundedBg = "#2F2B36"            
        self.__filePath = filePath       
        self.photo = None
        self.master = master
        
        #self.canvas = Canvas(self.master, 
        #                     bg = self.__frameRoundedBg, 
        #                     height = 500, 
        #                     width = 1050, 
        #                     bd = 0, 
        #                     highlightthickness = 0,
        #                     relief = "ridge")
        #self.canvas.grid(row = 0, column=0)
        #self.canvas.pack()
        #print("filePath : ",filePath)
        self.vid = tk.Label(self.master)
        self.vid.grid(row=0, column=0)
        
        self.delay = 15        
        self.drawCamArea(self.__filePath)
    '''
    def RGB(event, x, y):
        if event == cv2.EVENT_MOUSEMOVE :  
            colorsBGR = [x, y]
            print(colorsBGR)
    '''
        
    def drawCamArea(self, filePath):
        """
        영상 표시 영역
        """
        #cv2.namedWindow('RGB')
        #cv2.setMouseCallback('RGB', self.RGB)

        cap = cv2.VideoCapture(filePath)
        
        my_file = open(getFrameUtilPath("coco.txt"), "r")
        data = my_file.read()
        class_list = data.split("\n")
        
        count = 0

        tracker = Tracker()

        cy1 = 322
        cy2 = 368

        offset = 6

        vh_down = {}
        counter = []

        vh_up = {}
        counter1 = []
        
        while True:    
            ret, frame = cap.read()
            
            if not ret:
                break
            
            count += 1
            if count % 3 != 0:
                continue
            frame = cv2.resize(frame,(1020,500)) 
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            results = model.predict(frame)
        
            a = results[0].boxes.boxes
            px = pd.DataFrame(a).astype("float")        
            list=[]
                    
            for index,row in px.iterrows():        
                x1 = int(row[0])
                y1 = int(row[1])
                x2 = int(row[2])
                y2 = int(row[3])
                d = int(row[5])
                c = class_list[d]
                
                if 'car' in c:
                    list.append([x1,y1,x2,y2])
                    
            bbox_id = tracker.update(list)
            
            for bbox in bbox_id:
                x3,y3,x4,y4,id=bbox
                cx=int(x3+x4)//2
                cy=int(y3+y4)//2
                
                cv2.rectangle(frame,(x3,y3),(x4,y4),(0,0,255),2)
                
                if cy1<(cy+offset) and cy1 > (cy-offset):
                    vh_down[id] = time.time()

                if id in vh_down:                                    
                    if cy2 < (cy+offset) and cy2 > (cy-offset):
                        elapsed_time = time.time() - vh_down[id]                        
                    if counter.count(id) == 0:
                        counter.append(id)
                        distance = 10 # meters
                        a_speed_ms = distance / elapsed_time
                        a_speed_kh = a_speed_ms * 3.6
                        cv2.circle(frame,(cx,cy),4,(0,0,255),-1)
                        cv2.putText(frame,str(id),(x3,y3),cv2.FONT_HERSHEY_COMPLEX,0.6,(255,255,255),1)
                        cv2.putText(frame,str(int(a_speed_kh))+'Km/h',(x4,y4 ),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)

                        
                #####going UP#####     
                if cy2 < (cy+offset) and cy2 > (cy-offset):
                    vh_up[id] = time.time()
                    
                if id in vh_up:                    
                    if cy1<(cy+offset) and cy1 > (cy-offset):
                        elapsed1_time=time.time() - vh_up[id]
                    if counter1.count(id)==0:
                        counter1.append(id)      
                        distance1 = 10 # meters
                        a_speed_ms1 = distance1 / elapsed1_time
                        a_speed_kh1 = a_speed_ms1 * 3.6
                        cv2.circle(frame,(cx,cy),4,(0,0,255),-1)
                        cv2.putText(frame,str(id),(x3,y3),cv2.FONT_HERSHEY_COMPLEX,0.6,(255,255,255),1)
                        cv2.putText(frame,str(int(a_speed_kh1))+'Km/h',(x4,y4),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)
                        
            cv2.line(frame,(274,cy1),(814,cy1),(255,255,255),1)
            cv2.putText(frame,('L1'),(277,320),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)
            cv2.line(frame,(177,cy2),(927,cy2),(255,255,255),1)
        
            cv2.putText(frame,('L2'),(182,367),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)
            d = (len(counter))
            u = (len(counter1))
            cv2.putText(frame,('goingdown:-')+str(d),(60,90),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)

            cv2.putText(frame,('goingup:-')+str(u),(60,130),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)
            #cv2.imshow("RGB", frame)
            
            #self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            img = PIL.Image.fromarray(frame)
            imgtk = PIL.ImageTk.PhotoImage(image=img)
            self.vid.imgtk = imgtk
            self.vid.configure(image=imgtk)                    
            self.vid.after(self.delay, self.drawCamArea(filePath))
            
            if cv2.waitKey(1) & 0xFF==27:
                break
            
        cap.release()
        cv2.destroyAllWindows()