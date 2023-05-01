import cv2, pymsgbox, os
import tensorflow as tf
import numpy as np

def empty(x): pass

state = False

def predict(model_path):
    # Load the trained model
    model = tf.keras.models.load_model(model_path)

    test_image = tf.keras.preprocessing.image.load_img('./signs/test/hand.jpg',
                                                       target_size=(64, 64))
    test_image = tf.keras.preprocessing.image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis = 0)
    result = model.predict(test_image)
    
    folder = './signs/training'
    sub_folders = [name.upper() for name in os.listdir(folder) if os.path.isdir(os.path.join(folder, name))]
    
    for i in range(len(sub_folders)):
            if result[0][i] == 1:
                    return sub_folders[i]


def detection(img_name, model_file, state=False, countdown=0,
              lh_value=0, ls_value=0, lv_value=0):
        
        FOV_left = 425 # FOV = Frame Of View
        FOV_right = 625
        FOV_top = 200
        FOV_bottom = 400

        img_x, img_y = 64, 64
        cam = cv2.VideoCapture(0)
    
        cv2.namedWindow("Trackbars")
        cv2.createTrackbar("L - H", "Trackbars", lh_value, 179, empty)
        cv2.createTrackbar("L - S", "Trackbars", ls_value, 255, empty)
        cv2.createTrackbar("L - V", "Trackbars", lv_value, 255, empty)
        cv2.createTrackbar("U - H", "Trackbars", 179, 179, empty)
        cv2.createTrackbar("U - S", "Trackbars", 255, 255, empty)
        cv2.createTrackbar("U - V", "Trackbars", 255, 255, empty)

        cv2.namedWindow("Webcam")

        img_text = ''
        while countdown >= 0:
                _, frame = cam.read()
                frame = cv2.flip(frame, 1) # prevent inverted image

                l_h = cv2.getTrackbarPos("L - H", "Trackbars")
                l_s = cv2.getTrackbarPos("L - S", "Trackbars")
                l_v = cv2.getTrackbarPos("L - V", "Trackbars")
                u_h = cv2.getTrackbarPos("U - H", "Trackbars")
                u_s = cv2.getTrackbarPos("U - S", "Trackbars")
                u_v = cv2.getTrackbarPos("U - V", "Trackbars")
    
                rect_frame = cv2.rectangle(frame, (FOV_left, FOV_top),
                                           (FOV_right, FOV_bottom), 
                                           (255, 0, 0), thickness=2,
                                           lineType=8, shift=0)
    
                lower_blue = np.array([l_h, l_s, l_v])
                upper_blue = np.array([u_h, u_s, u_v])
                imcrop = rect_frame[202:398, 427:623]
                        
                hsv = cv2.cvtColor(imcrop, cv2.COLOR_BGR2HSV)
                mask = cv2.inRange(hsv, lower_blue, upper_blue)
                
                cv2.putText(frame, 
                            "The timer will countdown when you press C.",
                            (10, 30), cv2.FONT_HERSHEY_DUPLEX, 0.8,
                            (0, 102, 255))
                
                cv2.putText(frame, 
                            "To capture the letter. Adjust the trackbars",
                            (10, 55), cv2.FONT_HERSHEY_DUPLEX, 0.8,
                            (0, 102, 255))
                
                cv2.putText(frame,
                            "to get desired results!",
                            (10, 85), cv2.FONT_HERSHEY_DUPLEX, 0.9,
                            (0, 102, 255))
                
                cv2.putText(frame,  str(countdown), (30, 440),
                            cv2.FONT_HERSHEY_DUPLEX, 0.8, (127, 127, 255))
                
                cv2.putText(frame, img_text, (30, 400),
                            cv2.FONT_HERSHEY_DUPLEX, 1.5, (255, 255, 0))
                cv2.imshow("Webcam", frame)
                cv2.imshow("mask", mask)
                
                save_img = cv2.resize(mask, (img_x, img_y))
                cv2.imwrite(img_name, save_img)
                print(f"{img_name} written!")
                img_text = predict(model_file)

                if countdown > 0:
                        countdown -= 1
                        print(countdown)
                if countdown == 0 and state == True:
                        countdown = 0
                        _file = open('.\\signs\\phrase.txt', 'a')
                        _file.write(img_text)
                        _file.close()
                        state = False
                        pymsgbox.alert("Letter Added! Press C if you " +
                                         "would like to add another letter " +
                                         "or press V to exit. Word will " +
                                         "show in GUI once exited.",
                                         "IMPORTANT", button='OK',
                                         timeout=3000)
        
                if cv2.waitKey(1) == ord('c'):
                        pymsgbox.alert('Starting Countdown...', 'Get Ready',
                                         button='OK',timeout=1500) 
                                         # 1.5 second countdown
                        state = True
                        break
                
                if cv2.waitKey(1) == ord('s'):
                        _file = open('.\\signs\\phrase.txt', 'a')
                        _file.write(' ')
                        _file.close()
                        pymsgbox.alert("Space added", "Space Alert",
                                       timeout=1000)
                        
                if cv2.waitKey(1) == ord('v'):
                        break
                        
        
                if cv2.waitKey(1) == 27:
                        break
                
        if state == True:
                detection(img_name, model_file, state=state,
                          countdown=100, lh_value=l_h,
                          lv_value=l_v, ls_value=l_s)
        else:
                cam.release()
                cv2.destroyAllWindows()