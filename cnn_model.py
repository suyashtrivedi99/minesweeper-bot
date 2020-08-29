#%%
from tensorflow.keras.models import Sequential    #For initialising the model
from tensorflow.keras.layers import Conv2D        #For adding convolutional layer
from tensorflow.keras.layers import MaxPooling2D  #For adding max pooling layer
from tensorflow.keras.layers import Flatten       #For flattening max pooled layer values into a single vector
from tensorflow.keras.layers import Dense         #For adding layers to NN

import glob             #for accessing all the images
import numpy as np      #for handling the images as numpy arrays 
from PIL import Image   #for resizing the images

from sklearn import preprocessing, model_selection as ms  #for splitting data into Training, Cross - Validating, and Testing parts
from tensorflow.keras.preprocessing.image import ImageDataGenerator  #for image augmentation
import h5py                                               #for saving the model
from tensorflow.keras.models import load_model                       #for loading the model

import matplotlib.pyplot as plt  #for plotting training and cross validation accuracies vs epochs

from keras.utils import np_utils  #categorical encoding

#%%
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

#%%
