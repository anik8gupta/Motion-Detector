import cv2, time, pandas
from datetime import datetime
import threading
first_frame=None



class VideoCamera(object):
    
    def __init__(self):
        # Open a camera
        self.cap = cv2.VideoCapture(0)
      
        # Initialize video recording environment
        self.is_record = False
        self.out = None

    
    def __del__(self):
        self.cap.release()
    
    def get_frame(self):
        global first_frame
        while True:
            ret, frame = self.cap.read()
        
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray,(21,21),0)
    
            if  first_frame is None :
                first_frame = gray
                continue
    
            delta_frame = cv2.absdiff(first_frame,gray)
            thresh_delta = cv2.threshold(delta_frame,30,255,cv2.THRESH_BINARY)[1]
            thresh_delta = cv2.dilate(thresh_delta, None, iterations=0)
    
            (cnts,_) = cv2.findContours(thresh_delta.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
            for contour in cnts:
                if cv2.contourArea(contour) < 1000:
                    continue
                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x,y), (x+w,y+h), (0, 255, 0), 3)

            if ret:
                ret, jpeg = cv2.imencode('.jpg', frame)

            # Record video
                if self.is_record:
                    if self.out == None:
                        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
                        self.out = cv2.VideoWriter('./static/video.avi',fourcc, 20.0, (640,480))
                
                    
                    if ret:
                        self.out.write(frame)
                    else:
                        if self.out != None:
                            self.out.release()
                            self.out = None  

                return jpeg.tobytes()
      
            else:
                return None

    def start_record(self):
        self.is_record = True


    def stop_record(self):
        self.is_record = False


            