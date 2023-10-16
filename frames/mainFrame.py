from typing import Optional, Tuple, Union
import tkinter as tk
import customtkinter
from PIL import Image
from utils.tracker import*
from math import dist
from utils.pathUtils import getFrameImagePath
from utils.pathUtils import getFrameUtilPath
from frames.videoFrame import PlayVideo
import cv2
import pandas as pd
from ultralytics import YOLO
from utils.tracker import*
import time
import PIL.Image, PIL.ImageTk
from math import dist
model=YOLO('yolov8s.pt')

class MainFrame(customtkinter.CTk):        
    def __init__(self):
        super().__init__()
                
        #self.title_font = customtkinter.CTkFont(size=20, weight="bold")
        self.title("Vechile Speed System")
        self.geometry(f"{1250}x{600}+{0}+{0}")
        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image          
        self.logo_image = customtkinter.CTkImage(Image.open(getFrameImagePath("speed_radar.png")), size=(32, 32))
        self.cctv_title_image = customtkinter.CTkImage(light_image = Image.open(getFrameImagePath("cctv_title_dark.png")),
                                                       dark_image = Image.open(getFrameImagePath("cctv_title.png")),size=(32, 32))
        self.road_image = customtkinter.CTkImage(light_image = Image.open(getFrameImagePath("road_dark.png")),
                                                 dark_image = Image.open(getFrameImagePath("road.png")),size=(32, 32))
        
        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(3, weight=1)
    
        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  한문철 카메라", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(family = "Segoe UI", size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)
        
        self.frame_1_button = customtkinter.CTkButton(self.navigation_frame, font=customtkinter.CTkFont(family = "Segoe UI", size=13, weight="bold"), 
                                                   corner_radius=0, height=40, border_spacing=10, text="Cctv",                                                   
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.cctv_title_image, anchor="w", command=self.frame_1_button_event)
        self.frame_1_button.grid(row=1, column=0, sticky="ew")
        
        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, font=customtkinter.CTkFont(family = "Segoe UI", size=13, weight="bold"),
                                                      corner_radius=0, height=40, border_spacing=10, text="차선인식",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.road_image, anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")
        
        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Dark", "Light"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")
        
        # create cctv frame                    
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="#1B1A1D")
        self.home_frame.grid_columnconfigure(0, weight=1)
        self.home_frame.grid_rowconfigure(0, weight=9)
        self.home_frame.grid_rowconfigure(1, weight=1)        
        
        # create cctv first_frame 
        self.first_frame = customtkinter.CTkFrame(self.home_frame, corner_radius=0, bg_color="gray27", fg_color="transparent")
        self.first_frame.grid(row=0, column=0, sticky="nsew")  
        self.display = customtkinter.CTkLabel(self.first_frame) 
        self.display.grid(row=0, column=0, sticky="nsew")            
        #self.first_frame_label = customtkinter.CTkLabel(self.first_frame, 
        #                                                 text="  create second frame", 
        #                                                 compound="left", 
        #                                                 font=customtkinter.CTkFont(size=15, weight="bold"))
        #self.first_frame_label.grid(row=0, column=0, padx=20, pady=20)
                        
        # create cctv second_frame
        self.second_frame = customtkinter.CTkFrame(self.home_frame, corner_radius=0, fg_color="transparent")
        self.second_frame.grid(row=1, column=0, sticky="nsew")                                             
        self.home_frame_button_1 = customtkinter.CTkButton(self.second_frame, width = 140,
                                                            height   = 30,
                                                            text     = "SELECT FILES", 
                                                            font     = customtkinter.CTkFont(size=12, weight="bold"),
                                                            border_spacing = 0,
                                                            command        = self.open_files_action)
        self.home_frame_button_1.grid(row=0, column=0, padx=420, pady=5)          
        
        #create lane frame
        self.lane_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        
        # select default frame
        self.select_frame_by_name("cctv")
        customtkinter.set_appearance_mode("Dark")         
    
    #function 관련
    def check_supported_selected_files(self, uploaded_file_list):
        supported_file_extensions = ['.mp4', '.MP4',
                            '.webm', '.WEBM',
                            '.mkv', '.MKV',
                            '.flv', '.FLV',
                            '.gif', '.GIF',
                            '.m4v', ',M4V',
                            '.avi', '.AVI',
                            '.mov', '.MOV',
                            '.qt', '.3gp', '.mpg', '.mpeg']
        supported_files_list = []

        for file in uploaded_file_list:
            for supported_extension in supported_file_extensions:
                if supported_extension in file:
                    supported_files_list.append(file)

        return supported_files_list
    
    #GUI 관련
    def place_up_background(self):
        up_background = customtkinter.CTkLabel(master  = self.home_frame, 
                                text    = "",
                                fg_color = "#080808",
                                font     = customtkinter.CTkFont(family = "Segoe UI", size = 12, weight = "bold"),
                                anchor   = "w")
        
        up_background.place(relx = 0.5, 
                            rely = 0.0, 
                            relwidth = 1.0,  
                            relheight = 1.0,  
                            anchor = tk.CENTER) 
    
    def open_files_action(self):    
        uploaded_files_list = list(customtkinter.filedialog.askopenfilenames())
        uploaded_files_counter = len(uploaded_files_list)
        
        if uploaded_files_counter > 1 :
            tk.messagebox.showerror("확인", "파일은 하나만 선택 해 주세요.")            
            return

        supported_files_list = self.check_supported_selected_files(uploaded_files_list)
        supported_files_counter = len(supported_files_list)
        
        if supported_files_counter == 1:    
            self.drawCamArea(supported_files_list[0])
            #PlayVideo(self.first_frame, supported_files_list[0])
    
    def select_frame_by_name(self, name):
        # set button color for selected button
        self.frame_1_button.configure(fg_color=("gray75", "gray25") if name == "cctv" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "lane" else "transparent")        

        # show selected frame
        if name == "cctv":            
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
            
        if name == "lane":
            self.lane_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.lane_frame.grid_forget()
        
    def frame_1_button_event(self):
        self.select_frame_by_name("cctv")

    def frame_2_button_event(self):
        self.select_frame_by_name("lane")
    
    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)
    
    #cctv 구현
    def drawCamArea(self, filePath):
        """
        영상 표시 영역
        """

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
            self.self.display.imgtk = imgtk
            self.self.display.configure(image=imgtk)                    
            self.after(self.delay, self.drawCamArea(filePath))
            
            if cv2.waitKey(1) & 0xFF==27:
                break
            
        cap.release()
        cv2.destroyAllWindows()
                            
    def showFrame(self):
        self.mainloop()