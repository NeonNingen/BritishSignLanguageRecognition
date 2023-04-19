# Early capturing for database

import cv2, os
import numpy as np
from PIL import Image

camera = cv2.VideoCapture(0)

while True:
    ret, frame = camera.read()
    
    # Display the webcam and wait for a keypress
    cv2.imshow('Webcam', frame)
    key = cv2.waitKey(1)
    
    # If 'c' pressed. then save hand img to train directory
    if key == ord('c'):
        filename = 'hand.jpg'
        filepath = os.path.join(f".\\signs\\training\\test\\", filename)
        cv2.imwrite(filepath, frame)
        print('Saved test image:', filename)
        break
    

# Convert to grayscale + apply threshold
img = cv2.imread('.\\signs\\training\\f\\hand.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)

# Find the largest contour
contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
largest_contour = max(contours, key=cv2.contourArea)

# Create a mask of the same size as the image and fill it with zeros
mask = np.zeros_like(gray)

# Draw the largest contour on the mask with white color + extract hand region
cv2.drawContours(mask, [largest_contour], 0, 255, -1)
hand = cv2.bitwise_and(gray, gray, mask=mask)

# Resize the hand image to a smaller size + Save
hand = Image.fromarray(hand)
hand = hand.resize((64, 64))
hand.save('hand_grayscale.jpg')