import pyautogui as pg
import keyboard as kbd
import time
import numpy as np
import cv2

bsize = 52.5
fnamelen = 50

#no of rows and columns, and tiles
n = 9
tiles = n * n

#list to hold status of all buttons
buttons = []
mat

#class for buttons
class button:
    def __init__(self,x,y,status):
        self.size = bsize
        self.x = x
        self.y = y
        self.status = status

#class for the grid        
class grid:
    def __init__(self,row,col,startx,starty,endx,endy):
        self.row = row
        self.col = col
        self.startx = startx
        self.starty = starty
        self.endx = endx
        self.endy = endy
        self.w = endx - startx
        self.h = endy - starty
        
def initialize():
    global buttons
    global mat
    
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
    i = 0
    for b in buttons:
        pg.click(b.x,b.y)
        time.sleep(0.5)
        
        if kbd.is_pressed('s'):
            break
                
initialize()
