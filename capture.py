import pyautogui as pg
import time
import numpy as np
import cv2
import secrets 
import string 
from PIL import Image

#size of each tile
bsize = 52.5

#name length of image files
fnamelen = 50

#no of rows and columns, and tiles
n = 9
tiles = n * n

first = pg.locateCenterOnScreen('tab.png')

#coordinates of the grid
sx = first.x - (bsize/2)
sy = first.y - (bsize/2)
ex = first.x + ((n - 0.5)*bsize)
ey = first.y + ((n - 0.5)*bsize)

#wait for 120 secs to click all 4 corners    
time.sleep(120)

#take a screen shot of the grid
img = pg.screenshot(region=(sx,sy,ex-sx,ey-sy))
img = np.asarray(img)
    
ih = img.shape[0]
iw = img.shape[1]
ih = ih // n
iw = iw // n

for i in range(n):
    for j in range(n):
        off = 8    
        #select the current tile from the whole image
        cur = img[i*ih + off:(i+1)*ih - off,j*iw + off:(j+1)*iw - off]
       
        #path to save tile image
        res = ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(fnamelen)) 
        path = r"./img/" + str(res) + ".png"
        
        #convert this snap of a tile into an image and save it
        cur = Image.fromarray(cur).convert('RGB')
        cur.save(path)
        
        #cv2.imshow("frame",cur)
        #cv2.waitKey(0)

cv2.destroyAllWindows()       