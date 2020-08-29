from tensorflow.keras.models import Sequential    #For initialising the model
from tensorflow.keras.layers import Conv2D        #For adding convolutional layer
from tensorflow.keras.layers import MaxPooling2D  #For adding max pooling layer
from tensorflow.keras.layers import Flatten       #For flattening max pooled layer values into a single vector
from tensorflow.keras.layers import Dense         #For adding layers to NN

import glob             #for accessing all the images
import numpy as np      #for handling the images as numpy arrays 

from sklearn import preprocessing, model_selection as ms  #for splitting data into Training, Cross - Validating, and Testing parts
from tensorflow.keras.preprocessing.image import ImageDataGenerator  #for image augmentation
import h5py                                               #for saving the model
from tensorflow.keras.models import load_model                       #for loading the model

import matplotlib.pyplot as plt  #for plotting training and cross validation accuracies vs epochs

def cnn_model(h_layers, features, neurons):        #returns the model with desired parameters
    model = Sequential() #initialise the model

    model.add( Conv2D( features, (3, 3),input_shape = (36, 36, 3), activation = 'relu' )) #Kernel size = 3*3, accepting 36*36 pixels 
    model.add( MaxPooling2D( pool_size = (2, 2) )) #add max pooling layer, with dims of each pool = 2*2
    model.add( Flatten() ) #add flattening layer 
    
    for i in range( h_layers ):  #add all hidden layers
        model.add( Dense( units = neurons, activation = 'relu' ))
        
    model.add( Dense( units = 12, activation = 'softmax' ))  #add an output layer

    model.compile( optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])  #define optimizer and loss functions as well as required metrics

    return model

#loading the sample data
X_data = np.load(r'Data\X_data.npy')
y_data = np.load(r'Data\y_data.npy')

#creating training, cross-validation, and testing sets
X_train, X_new, y_train, y_new = ms.train_test_split(X_data, y_data, test_size = 0.1, random_state = 0)
X_crossval, X_test, y_crossval, y_test = ms.train_test_split(X_new, y_new, test_size = 0.5, random_state = 0)

val_size = X_crossval.shape[0] #cross-validation set size

#training and testing data generators
train_datagen = ImageDataGenerator(rescale = 1./255)
test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow(X_train,
                                     y_train,
                                     batch_size = 10)

val_generator = test_datagen.flow(X_crossval,
                                  y_crossval,
                                  batch_size = 1)

test_generator = test_datagen.flow(X_test,
                                   y_test,
                                   batch_size = 1)

#creating model
h_layers = 1   #no. of hidden layers
features = 32  #no. of feature maps 
neurons = 128  #no. of neurons in each hidden layer

model = cnn_model(h_layers, features, neurons)

#training the model
history = model.fit_generator(train_generator,
                              steps_per_epoch = len(X_train) / 10,
                              epochs = 20,
                              validation_data = val_generator,
                              validation_steps = val_size)
#saving the model
model.save('model.h5')

#loading the model
model = load_model('model.h5')

#obtaining accuracy on test set 
test_acc = model.evaluate_generator(test_generator, steps = len(test_generator))

print(model.metrics_names)
print('Test Accuracy Obtained: ')
print(test_acc[1] * 100, ' %')

#Plotting Training and Testing accuracies
plt.plot(history.history['accuracy'])
plt.plot(history.history['loss'])
plt.title('model accuracy')
plt.ylabel('accuracy/loss')
plt.xlabel('epoch')
plt.legend(['accuracy', 'loss'], loc='best')
plt.show()

