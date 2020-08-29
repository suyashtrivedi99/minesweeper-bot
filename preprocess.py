import glob
import numpy as np
import cv2
from keras.utils import np_utils  #categorical encoding

X_data = [] #list for holding all images as numpy arrays
y_data = [] #list for holding the labels corresponding to the respective images

#list of all folders where images of different categories reside
imgPathList = [ 
             {"path": glob.glob(r'img\white\*.*'), "label": 0},
             {"path": glob.glob(r'img\1\*.*'), "label": 1},
             {"path": glob.glob(r'img\2\*.*'), "label": 2},
             {"path": glob.glob(r'img\3\*.*'), "label": 3},
             {"path": glob.glob(r'img\4\*.*'), "label": 4},
             {"path": glob.glob(r'img\5\*.*'), "label": 5},
             {"path": glob.glob(r'img\6\*.*'), "label": 6},
             {"path": glob.glob(r'img\7\*.*'), "label": 7},
             {"path": glob.glob(r'img\8\*.*'), "label": 8},
             {"path": glob.glob(r'img\blue\*.*'), "label": 9},
             {"path": glob.glob(r'img\flag\*.*'), "label": 10},
             {"path": glob.glob(r'img\bomb\*.*'), "label": 11}] 
               
#resizing all the images to the same size, and storing images alongwith their labels
for path in imgPathList:
    label = path["label"]
    
    for image in path["path"]:
        img = cv2.imread(image)
        img_resized = cv2.resize(img, (36, 36))
        cv2.imwrite(image, img_resized)
        
        img_array = np.asarray(img_resized)
        X_data.append(img_array)
        y_data.append(label)
        
#converting the lists to numpy arrays(for flow method)
X_data = np.array(X_data)  
y_data = np.array(y_data)

m = X_data.shape[0]  #no. of samples

rand_idx = np.arange(m)     #generating indices
np.random.shuffle(rand_idx) #randomising indices

#randomly shuffling all the samples
X_data = X_data[rand_idx]   
y_data = y_data[rand_idx]

#categorical encoding of labels
y_data = np_utils.to_categorical(y_data)

#saving all the sample data
np.save(r'Data\X_data.npy', X_data)
np.save(r'Data\y_data.npy', y_data)