import tensorflow as tf
import numpy as np
from keras_preprocessing.image import ImageDataGenerator

def predict(model_file):
       # Load the trained model
       model = tf.keras.models.load_model(model_file)

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
       
def testing(model_path):
       # Load the trained model
       model = tf.keras.models.load_model(model_path)

       # Create an ImageDataGenerator instance for the test data
       test_datagen = ImageDataGenerator(rescale=1./255)
       test_generator = test_datagen.flow_from_directory(
              'signs/training',
              target_size=(64, 64),
              batch_size=32,
              class_mode='categorical')
       
       # Evaluate test data
       model.evaluate(test_generator)

       import numpy as np
       img_name = input('Enter Image Name: ')
       image_path = f'./signs/validation/{img_name}/351.jpg'
       print('')

       test_image = tf.keras.preprocessing.image.load_img(image_path, target_size=(64, 64))
       test_image = tf.keras.preprocessing.image.img_to_array(test_image)
       test_image = np.expand_dims(test_image, axis = 0)
       result = model.predict(test_image)
       #training_set.class_indices
       print('Predicted Sign is:')
       print('')
       if result[0][0] == 1:
              print('A')
       elif result[0][1] == 1:
              print('B')
       elif result[0][2] == 1:
              print('C')
       elif result[0][3] == 1:
              print('D')
       elif result[0][4] == 1:
              print('E')

