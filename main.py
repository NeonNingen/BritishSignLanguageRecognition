import cv2 #opencv
import numpy as np
from pathlib import Path
from create_dataset import webcam

ges_name = input("Enter gesture name: ").capitalize()
path = f".\\signs\\training\\{ges_name}"
Path(path).mkdir(parents=True, exist_ok=True)
webcam(ges_name, path)
