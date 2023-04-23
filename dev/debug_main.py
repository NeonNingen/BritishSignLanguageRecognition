from pathlib import Path
import sys
sys.path.append('./')
from create_dataset import webcam
from train_model import train_model
from detect import detection

model_file = 'Trained_model_backup.h5'

# Path Checking
tr_path = ".\\signs\\training\\"
v_path = ".\\signs\\validation\\"
te_path = ".\\signs\\test\\"
'''
# Creates Folders
paths = [tr_path, v_path, te_path]
for path in paths:
    Path(path).mkdir(parents=True, exist_ok=True)
'''
    
print("Welcome to the developer version of SLR program :0")

def gesture_add(tr_path, v_path):
    
    while True:
        
        print("Type 'exit' to exit")
        ges_name = input("Enter gesture name: ")
        if ges_name == "exit":
            exit()
        
        '''
        # Add gesture names to the training + validation path
        # Create new folders
        # Webcam - create_database
        '''
        paths = [tr_path + ges_name, v_path + ges_name]
        for path in paths:
            Path(path).mkdir(parents=True, exist_ok=True)
        
        check = webcam(paths[0], paths[1])
        if check:
            print("Status: Completed")
        elif check:
            print("Status: Incompleted")

print("Sign Language Recognizer Program")
# GUI Replacement

while True:
    print("Please select the listed options:" 
    +"\n1) Add gestures\n2) Train\n3) Recognise\nAny other key to Exit")
    user_input = input("Pick an option: ")
    
    if user_input == "1":
        gesture_add(tr_path, v_path)
    elif user_input == "2":
        train_model(tr_path, v_path, model_file)
    elif user_input == "3":
        detection(te_path + 'hand.jpg', model_file)
    else:
        break