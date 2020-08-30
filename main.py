import os  
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import pyautogui as pg
import keyboard as kbd
import time

import numpy as np

from tensorflow.keras.models import load_model

from capture import scan
import matplotlib.pyplot as plt

bsize = 52.5

#no of rows and columns, and tiles
n = 9
tiles = n * n

#list to hold status of all buttons
buttons = []

#class for buttons
class button:
    def __init__(self,x=0,y=0,status=0):
        self.size = bsize
        self.x = x
        self.y = y
        self.status = status

#class for the grid        
class grid:
    def __init__(self,row=0,col=0,startx=0,starty=0,endx=0,endy=0):
        self.row = row
        self.col = col
        self.startx = startx
        self.starty = starty
        self.endx = endx
        self.endy = endy
        self.w = endx - startx
        self.h = endy - starty

mat = grid()
temp = []

def initialize():
    global buttons
    global mat
    global temp
    
    first = pg.locateCenterOnScreen('tab.png')
    
    #coordinates of the grid
    gstartx = first.x - (bsize/2)
    gstarty = first.y - (bsize/2)
    gendx = first.x + ((n - 0.5)*bsize)
    gendy = first.y + ((n - 0.5)*bsize)
    
    #creating a matrix
    mat = grid(n,n,gstartx,gstarty,gendx,gendy)    
    
    for i in range(n):
        for j in range(n):
            b = button(first.x + (j*bsize),first.y + (i*bsize),0)
            buttons.append(b)
            
    for b in buttons:
        pg.click(b.x,b.y)
        
        if kbd.is_pressed('s'):
            break
   
    temp = scan(n, mat.startx, mat.starty, mat.endx, mat.endy, 8)
             
initialize()

#%%

print(np.matrix(temp))
