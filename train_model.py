import os
from keras import optimizers
from keras.models import Sequential
from keras.layers import Convolution2D, MaxPooling2D, Flatten, Dense, Dropout

"""
Building a CNN Model using keras library
"""

def train_model(t_path, v_path, model_path):
    # Setting up CNN & Filter
	classifier = Sequential()
	nb_filter = [32, 64]
	dir_amount = len(next(os.walk(t_path))[1])

	# Convolution Layer & Pooling
	classifier.add(Convolution2D(nb_filter[0], 3, 3, input_shape = (64,64,3),
		activation = 'relu'))
	classifier.add(MaxPooling2D(pool_size =(2,2)))

	# Adding 2 convolution layers without input shape
	for i in range(0, 1):
		classifier.add(Convolution2D(nb_filter[i], 3, 3, activation = 'relu'))
		classifier.add(MaxPooling2D(pool_size =(2,2)))

	# Flatterning + Full connection
	classifier.add(Flatten())
	classifier.add(Dense(256, activation = 'relu'))
	classifier.add(Dropout(0.5))
	classifier.add(Dense(dir_amount, activation = 'softmax'))
 
	# Compiling the CNN
	classifier.compile(
		optimizer = optimizers.SGD(lr = 0.01),
		loss = 'categorical_crossentropy',
		metrics = ['accuracy'])

	#Part 2 Fittting the CNN to the image
	from keras.preprocessing.image import ImageDataGenerator
	train_datagen = ImageDataGenerator(
		rescale = 1./255,
		shear_range = 0.2,
		zoom_range = 0.2,
		horizontal_flip = True)

	val_datagen = ImageDataGenerator(rescale=1./255)

	training_set = train_datagen.flow_from_directory(
		t_path,
		target_size = (64,64),
		batch_size = 32,
		class_mode='categorical')

	val_set = val_datagen.flow_from_directory(
    	v_path,
    	target_size=(64, 64),
    	batch_size=32,
    	class_mode='categorical'
	)

	model = classifier.fit_generator(
		training_set,
		steps_per_epoch= len(training_set),
		epochs= dir_amount * 4,
		validation_data = val_set,
		validation_steps = len(val_set)
	)

	print("Length of training set", len(training_set))
	print("Length of val set", len(val_set))

	# Save Model
	classifier.save(model_path)

	# History of accuracy
	print(model.history.keys())
	import matplotlib.pyplot as plt
	plt.plot(model.history['accuracy'])
	plt.plot(model.history['val_accuracy'])
	plt.title('model accuracy')
	plt.ylabel('accuracy')
	plt.xlabel('epoch')
	plt.legend(['train', 'val'], loc = 'upper left')
	plt.savefig('./signs/graphs/acc_plot.jpg')
	plt.clf()
 	#plt.show()
 
 
 	# History of loss
	plt.plot(model.history['loss'])
	plt.plot(model.history['val_loss'])
	plt.title('model loss')
	plt.ylabel('loss')
	plt.xlabel('epoch')
	plt.legend(['train', 'val'], loc = 'upper left')
	plt.savefig('./signs/graphs/loss_plot.jpg')
 	#plt.show()
  
	return True