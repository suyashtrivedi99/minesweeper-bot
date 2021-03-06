import os  
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import pyautogui as pg
from PIL import Image
from tensorflow.keras.models import load_model
import numpy as np
import time
import matplotlib.pyplot as plt
import cv2
import secrets
import string

def scan(n, sx, sy, ex, ey, off):
    tiles = []
    
    #loading the model
    model = load_model('model.h5')
    
    #take a screen shot of the grid
    img = pg.screenshot(region=(sx,sy,ex-sx,ey-sy))
    img = np.asarray(img)
        
    ih = img.shape[0]
    iw = img.shape[1]
    ih = ih // n
    iw = iw // n
    
    for i in range(n):
        curtiles = []
        
        for j in range(n):
            #off = 8    
            #select the current tile from the whole image
            cur = img[i*ih + off:(i+1)*ih - off,j*iw + off:(j+1)*iw - off]
            
    
            #path to save tile image
            res = ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(10)) 
            path = r"./tempimg/" + str(res) + ".png"
            
            #convert this snap of a tile into an image and save it
            cur = cv2.cvtColor(cur, cv2.COLOR_BGR2RGB)
            cv2.imwrite(path, cur)
            cur = cv2.imread(path)
            
            cur = np.asarray(cur)
            
            #scanning the tile image by using the CNN model
            predArr = model.predict(np.expand_dims(cur, axis=0))[0]
            num = np.where(predArr == np.amax(predArr))
            
            #adding to the current row of tiles
            curtiles.append(num[0][0])
            
            #remove image after use
            os.remove(path)
        tiles.append(curtiles)
    
    return tiles
        