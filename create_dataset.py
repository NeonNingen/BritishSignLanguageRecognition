import cv2, time, pymsgbox
import numpy as np
from pathlib import Path

def empty(x): pass

FOV_left = 425 # FOV = Frame Of View
FOV_right = 625
FOV_top = 200
FOV_bottom = 400

img_x, img_y = 64, 64

'''
Setting up the webcam to manipulate the HSV values of an image
ges_name = gesture name
t_path = training path
v_path = validation path
FOV_left, right, top and down for positiing and the size of the frame
img_x, img_y = Size of the image when photo taken
'''

def webcam():
    countdown = 1000
    
    cam = cv2.VideoCapture(0)
    time.sleep(1)
    
    cv2.namedWindow("Trackbars")
    cv2.createTrackbar("L - H", "Trackbars", 0, 179, empty)
    cv2.createTrackbar("L - S", "Trackbars", 0, 255, empty)
    cv2.createTrackbar("L - V", "Trackbars", 0, 255, empty)
    cv2.createTrackbar("U - H", "Trackbars", 179, 179, empty)
    cv2.createTrackbar("U - S", "Trackbars", 255, 255, empty)
    cv2.createTrackbar("U - V", "Trackbars", 255, 255, empty)
    
    while countdown > 0:
            _, frame = cam.read()
            frame = cv2.flip(frame, 1) # prevent inverted image

            l_h = cv2.getTrackbarPos("L - H", "Trackbars")
            l_s = cv2.getTrackbarPos("L - S", "Trackbars")
            l_v = cv2.getTrackbarPos("L - V", "Trackbars")
            u_h = cv2.getTrackbarPos("U - H", "Trackbars")
            u_s = cv2.getTrackbarPos("U - S", "Trackbars")
            u_v = cv2.getTrackbarPos("U - V", "Trackbars")

            rect_frame = cv2.rectangle(frame, (FOV_left, FOV_top),
                                       (FOV_right, FOV_bottom), (255, 0, 0),
                                       thickness=2, lineType=8, shift=0)

            lower_blue = np.array([l_h, l_s, l_v])
            upper_blue = np.array([u_h, u_s, u_v])
            imcrop = rect_frame[202:398, 427:623]
            hsv = cv2.cvtColor(imcrop, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, lower_blue, upper_blue)

            result = cv2.bitwise_and(imcrop, imcrop, mask=mask)

            #cv2.putText colour is BGR
            cv2.putText(frame, 
            "The timer will countdown allowing you to",
            (10, 30), cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 102, 255))
            
            cv2.putText(frame, 
            "readjust your hand. Adjust the trackbars",
            (10, 55), cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 102, 255))
            
            cv2.putText(frame, 
            "to get desired results.",
            (10, 85), cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 102, 255))
            
            cv2.putText(frame, 
            "Recommend adjusting only L - V for training (First countdown)\n"+
            "then only L - S for validation (Second countdown)",
            (10, 105), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 102, 255))
            
            cv2.putText(frame,  str(countdown), (30, 440), 
            cv2.FONT_HERSHEY_DUPLEX, 0.8, (127, 127, 255))
            
            cv2.imshow("Countdown", frame)
            cv2.imshow("mask", mask)
            cv2.imshow("result", result)
            
            cv2.waitKey(10)
            countdown -= 1

            if cv2.waitKey(1) == 27:
                cam.release()
                cv2.destroyAllWindows()
                return 0
        
    cam.release()
    cv2.destroyAllWindows()
    return mask
    

def capture(t_path, v_path):
    
    taken_counter = 1
    training_set_image_name = 1
    mask = webcam()
            
    # Creates folders for the newly added gestures
    paths = [t_path, v_path]
    for path in paths:
        Path(path).mkdir(parents=True, exist_ok=True)
            
    while taken_counter < 351:
        
        if taken_counter <= 350:
            img_name = f"{t_path}\\{str(taken_counter)}.jpg"
            save_img = cv2.resize(mask, (img_x, img_y))
            cv2.imwrite(img_name, save_img)
            print(f"{img_name} written!")
            training_set_image_name += 1
                    
        taken_counter += 1
        if taken_counter == 351:
            break
        
    taken_counter == 351
    pymsgbox.alert("Creating new capture for validation",
                   "Validation data capture", timeout=1000)
    webcam()
        
    while taken_counter < 401:
            
        if taken_counter > 350 and taken_counter <= 400:
            img_name = f"{v_path}\\{str(taken_counter)}.jpg"
            cv2.imwrite(img_name, save_img)
            print(f"{img_name} written!")
                    
                    
        taken_counter += 1
        if taken_counter == 401:
            break
    
    if taken_counter == 401:
        return 1
    else:
        return 0