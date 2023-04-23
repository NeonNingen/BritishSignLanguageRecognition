import cv2 #opencv
import numpy as np
from pathlib import Path

accumlated_weight = 0.5
background = None


FOV_left = 250 # FOV = Frame Of View
FOV_right = 50
FOV_top = 100
FOV_bottom = 300

x = 64 # Size of saved photo
y = 64 

# differentiating the background with the frame to distinguish the foreground
def avg_weight(frame, accumlated_weight):
	global background

	if background is None:
		background = frame.copy().astype("float")
		return None

	cv2.accumulateWeighted(frame, background, accumlated_weight)

# Detecting a hand within the frame (FOV).
def fov_hands(frame, threshold=25):
	global background

	_, threshold = cv2.threshold(cv2.absdiff(background.astype("uint8"),
								 frame), threshold, 255, cv2.THRESH_BINARY)

	# Grab the external outlines for the hand within the frame
	outlines, hierarchy = cv2.findContours(threshold.copy(),
						  cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	print(outlines, hierarchy)
	if len(outlines) == 0:
		return None
	else:
		return (threshold, max(outlines, key=cv2.contourArea))

# Saving the images of the hands using the webcam
def webcam_v1(ges_name, path):
	num_imgs_taken = 0
	num_frames = 0

	cam = cv2.VideoCapture(0)

	while True:
		_, frame = cam.read()
		frame = cv2.flip(frame, 1) # prevent inverted image
		frame_copy = frame.copy()

		fov = frame[FOV_top:FOV_bottom, FOV_right:FOV_left]

		# Turn the hand within the frame from colour to grayscale
		gray_frame = cv2.GaussianBlur(cv2.cvtColor(fov, cv2.COLOR_BGR2GRAY),
					 				  (9, 9), 0)
		# Setting background
		if num_frames < 60:
			avg_weight(gray_frame, accumlated_weight)
			if num_frames <= 50:
				cv2.putText(frame_copy, "FETCHING BACKGROUND...PLEASE WAIT",
					       (80, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
					       (0,0,255), 2)
		# Setting foreground + hand data
		elif num_frames <= 300:
			hand = fov_hands(gray_frame)
			cv2.putText(frame_copy, "Adjust hand...Gesture for" +
				    ges_name, (200, 400), cv2.FONT_HERSHEY_SIMPLEX, 1,
				       (0,0,255), 2)
			# Check the hand is actually detected by num of outlines
			if hand is not None:
				threshold, hand_segment = hand # Assign hand with data
				# Drawing outline around hand
				cv2.drawContours(frame_copy, [hand_segment +
								(FOV_right, FOV_top)], -1, (255, 0, 0), 1)

				cv2.putText(frame_copy, str(num_frames), (70, 45), 
						 	cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
				cv2.putText(frame_copy, str(num_imgs_taken) + 'image' +
							'For' + ges_name, (200, 400),
							cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

				# Showuing the thresholded (grayscaled) image
				cv2.imshow('Grayscale Img', threshold)
				if num_imgs_taken <= 300:
					# Resize img and save
					save_img = cv2.resize(threshold, (64, 64))
					cv2.imwrite(f"{path}/{str(num_imgs_taken)}.jpg", save_img)
				else:
					break
				num_imgs_taken += 1
			else:
				cv2.putText(frame_copy, 'No hand detected...', (200, 400), 
							cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

		# Drawing FOV on copied frame
		cv2.rectangle(frame_copy, (FOV_left, FOV_top),
					 (FOV_right, FOV_bottom), (255,128,0), 3)
		cv2.putText(frame_copy, "Sign Language recognition...", (10, 20),
					cv2.FONT_ITALIC, 0.5, (51,255,51), 1)

		# increment the number of frames for tracking
		num_frames += 1
		cv2.imshow('hs detection', frame_copy) # Display segmented hand

		key = cv2.waitKey(1) & 0xFF
		if key == 27:
			break

	cam.release()
	cv2.destroyAllWindows()