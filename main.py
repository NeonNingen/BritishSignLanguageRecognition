from pathlib import Path
from create_dataset import webcam
from create_dataset_v1 import webcam_v1
from train_model import train_model

print("Sign Language Recognizer Program")
print("""1 - Manual Capture (More accurate)
2 - Automatic Capture (Less accurate)""")

user_input = input("Which option: ")

while True:
    
    print("Type 'exit' to exit")
    ges_name = input("Enter gesture name: ")
    if ges_name == "exit":
        exit()
    
    # Path Checking
    t_path = f".\\signs\\training\\{ges_name}"
    v_path = f".\\signs\\validation\\{ges_name}"
    paths = [t_path, v_path]
    for path in paths:
        Path(path).mkdir(parents=True, exist_ok=True)
    
    # Webcam - create_database (V2)
    if user_input == "1":
        webcam(ges_name, t_path, v_path)
    if user_input == "2":
        webcam_v1(ges_name, t_path)
        
    # Train model (V2)
    train_model(t_path, v_path)
    