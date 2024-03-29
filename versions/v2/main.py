from pathlib import Path
from create_dataset import webcam
from train_model import train_model
from detect import detection

model_file = 'Trained_model.h5'

# Path Checking
tr_path = f".\\signs\\training\\"
v_path = f".\\signs\\validation\\"
te_path = f".\\signs\\test\\"
paths = [tr_path, v_path, te_path]
for path in paths:
    Path(path).mkdir(parents=True, exist_ok=True)

def gesture_add():
    
    while True:
        
        print("Type 'exit' to exit")
        ges_name = input("Enter gesture name: ")
        if ges_name == "exit":
            exit()
        
        # Add gesture names to the training + validation path
        tr_path += ges_name
        v_path += ges_name
        
        # Webcam - create_database
        webcam(tr_path, v_path) 

print("Sign Language Recognizer Program")
# GUI Replacement

while True:
    print("Please select the listed options:" 
    +"\n1) Add gestures\n2) Train\n3) Recognise\nAny other key to Exit")
    user_input = input("Pick an option: ")
    
    if user_input == "1":
        gesture_add()
    elif user_input == "2":
        train_model(tr_path, v_path, model_file)
    elif user_input == "3":
        detection(te_path + 'hand.jpg', model_file)
    else:
        break