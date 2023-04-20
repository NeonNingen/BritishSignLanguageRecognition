import cv2
import numpy as np
from test_model import predict

def empty(x): pass

FOV_left = 425 # FOV = Frame Of View
FOV_right = 625
FOV_top = 200
FOV_bottom = 400

img_x, img_y = 64, 64

def detection(img_name, model_file):
    cam = cv2.VideoCapture(0)
    
    cv2.namedWindow("Trackbars")
    cv2.createTrackbar("L - H", "Trackbars", 0, 179, empty)
    cv2.createTrackbar("L - S", "Trackbars", 0, 255, empty)
    cv2.createTrackbar("L - V", "Trackbars", 0, 255, empty)
    cv2.createTrackbar("U - H", "Trackbars", 179, 179, empty)
    cv2.createTrackbar("U - S", "Trackbars", 255, 255, empty)
    cv2.createTrackbar("U - V", "Trackbars", 255, 255, empty)

    cv2.namedWindow("Webcam")

    img_text = ''
    while True:
    
        _, frame = cam.read()
        frame = cv2.flip(frame, 1) # prevent inverted image

        l_h = cv2.getTrackbarPos("L - H", "Trackbars")
        l_s = cv2.getTrackbarPos("L - S", "Trackbars")
        l_v = cv2.getTrackbarPos("L - V", "Trackbars")
        u_h = cv2.getTrackbarPos("U - H", "Trackbars")
        u_s = cv2.getTrackbarPos("U - S", "Trackbars")
        u_v = cv2.getTrackbarPos("U - V", "Trackbars")
    
        rect_frame = cv2.rectangle(frame, (FOV_left, FOV_top), (FOV_right, FOV_bottom), (255, 0, 0), thickness=2, lineType=8, shift=0)
    
        lower_blue = np.array([l_h, l_s, l_v])
        upper_blue = np.array([u_h, u_s, u_v])
        imcrop = rect_frame[202:398, 427:623]
        hsv = cv2.cvtColor(imcrop, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_blue, upper_blue)

        cv2.putText(frame, img_text, (30, 400), cv2.FONT_HERSHEY_DUPLEX, 1.5, (255, 0, 0))
        cv2.imshow("Webcam", frame)
        cv2.imshow("mask", mask)
    
        
        save_img = cv2.resize(mask, (img_x, img_y))
        cv2.imwrite(img_name, save_img)
        print(f"{img_name} written!")
        img_text = predict(model_file)
    
        if cv2.waitKey(1) == 27:
            break
            
    cam.release()
    cv2.destroyAllWindows()