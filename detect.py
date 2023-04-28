import cv2
import tensorflow as tf
import numpy as np
#from test_model import predict
from time import sleep

def empty(x): pass

FOV_left = 425 # FOV = Frame Of View
FOV_right = 625
FOV_top = 200
FOV_bottom = 400

img_x, img_y = 64, 64


def predict(model_path):
    # Load the trained model
    model = tf.keras.models.load_model(model_path)

    test_image = tf.keras.preprocessing.image.load_img('./signs/test/hand.jpg', target_size=(64, 64))
    test_image = tf.keras.preprocessing.image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis = 0)
    result = model.predict(test_image)

    if result[0][0] == 1:
            return 'A'
    elif result[0][1] == 1:
            return 'B'
    elif result[0][2] == 1:
            return 'C'
    elif result[0][3] == 1:
            return 'D'
    elif result[0][4] == 1:
            return 'E'


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

        cv2.putText(frame, img_text, (30, 400), cv2.FONT_HERSHEY_DUPLEX, 1.5, (255, 255, 0))
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