from pathlib import Path
from create_dataset import webcam
from create_dataset_v1 import webcam_v1
from train_model import train_model
from detect import detection

model_file = 'Trained_model_backup.h5'

# Path Checking
tr_path = f".\\signs\\training\\"
v_path = f".\\signs\\validation\\"
te_path = f".\\signs\\test\\"
paths = [tr_path, v_path, te_path]
for path in paths:
    Path(path).mkdir(parents=True, exist_ok=True)

print("Sign Language Recognizer Program")
print("""1 - Manual Capture (More accurate)
2 - Automatic Capture (Less accurate)""")

user_input = input("Which option: ")

while True:
    
    print("Type 'exit' to exit")
    ges_name = input("Enter gesture name: ")
    if ges_name == "exit":
        exit()
        
    # Add gesture names to the training + validation path
    tr_path += ges_name
    v_path += ges_name
    
    # Webcam - create_database
    # if user_input == "1":
        # webcam(tr_path, v_path)
    # if user_input == "2":
        # webcam_v1(ges_name, tr_path)
        
    # Train model
    # train_model(tr_path, v_path, model_file)
    
    # Test model
    detection(te_path + 'hand.jpg', model_file)
    
    
    
    