import tensorflow as tf
from keras_preprocessing.image import ImageDataGenerator

# Load the trained model
model = tf.keras.models.load_model('Trained_model.h5')

# Create an ImageDataGenerator instance for the test data
test_datagen = ImageDataGenerator(rescale=1./255)
test_generator = test_datagen.flow_from_directory(
        'signs/training',
        target_size=(64, 64),
        batch_size=32,
        class_mode='categorical')

# Make predictions on the test data
predictions = model.predict(test_generator, verbose=0)[:32]

# Print the predictions
print(predictions)