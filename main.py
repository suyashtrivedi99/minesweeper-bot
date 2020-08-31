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

def initialize():
    global buttons
    global mat
    global n
    
    first = pg.locateCenterOnScreen('tab.png')
    
    #click on first tile to start
    pg.click(first)
    
    #coordinates of the grid
    gstartx = first.x - (bsize/2)
    gstarty = first.y - (bsize/2)
    gendx = first.x + ((n - 0.5)*bsize)
    gendy = first.y + ((n - 0.5)*bsize)
    
    #creating a matrix
    mat = grid(n,n,gstartx,gstarty,gendx,gendy)    
    
    for i in range(n):
        curbuttons = []
        for j in range(n):
            b = button(first.x + (j*bsize),first.y + (i*bsize),9)
            curbuttons.append(b)
        buttons.append(curbuttons)
    """    
    for b in buttons:
        pg.click(b.x,b.y)
        
        if kbd.is_pressed('s'):
            break
   
    temp = scan(n, mat.startx, mat.starty, mat.endx, mat.endy, 8)
    """

#update the status of all tiles
def update_tiles():
    global buttons
    global mat
    global n
    
    temp_list = scan(n, mat.startx, mat.starty, mat.endx, mat.endy, 8)
    
    for i in range(n):
        for j in range(n):
           buttons[i][j].status = temp_list[i][j]

#check if end has been reached
def check_run():
    global buttons
    global mat
    
    for button in buttons:
        #bomb detection
        if button.status == 11:
            return False
    return True     

#solve
def solve():
    global buttons
    global mat
    global n
    
    for i in range(n):
        for j in range(n):
            curs = buttons[i][j].status
            
            if 1 <= curs <= 8:
                flag = []
                risk = []
                
                #top-left tile
                curi = i-1
                curj = j-1
                
                if 0 <= curi <= n-1 and 0 <= curj <= n-1:
                    if buttons[curi][curj].status == 9:
                        risk.append((curi,curj))
                    elif buttons[curi][curj].status == 10:
                        flag.append((curi,curj))
                
                #top-middle tile
                curi = i-1
                curj = j
                
                if 0 <= curi <= n-1 and 0 <= curj <= n-1:
                    if buttons[curi][curj].status == 9:
                        risk.append((curi,curj))
                    elif buttons[curi][curj].status == 10:
                        flag.append((curi,curj))
                
                #top-right tile
                curi = i-1
                curj = j+1
                
                if 0 <= curi <= n-1 and 0 <= curj <= n-1:
                    if buttons[curi][curj].status == 9:
                        risk.append((curi,curj))
                    elif buttons[curi][curj].status == 10:
                        flag.append((curi,curj))
    
                #middle-left tile
                curi = i
                curj = j-1
                
                if 0 <= curi <= n-1 and 0 <= curj <= n-1:
                    if buttons[curi][curj].status == 9:
                        risk.append((curi,curj))
                    elif buttons[curi][curj].status == 10:
                        flag.append((curi,curj))
                
                #middle-right tile
                curi = i
                curj = j+1
                
                if 0 <= curi <= n-1 and 0 <= curj <= n-1:
                    if buttons[curi][curj].status == 9:
                        risk.append((curi,curj))
                    elif buttons[curi][curj].status == 10:
                        flag.append((curi,curj))

                #bottom-left tile
                curi = i+1
                curj = j-1
                
                if 0 <= curi <= n-1 and 0 <= curj <= n-1:
                    if buttons[curi][curj].status == 9:
                        risk.append((curi,curj))
                    elif buttons[curi][curj].status == 10:
                        flag.append((curi,curj))
                
                #bottom-middle tile
                curi = i+1
                curj = j
                
                if 0 <= curi <= n-1 and 0 <= curj <= n-1:
                    if buttons[curi][curj].status == 9:
                        risk.append((curi,curj))
                    elif buttons[curi][curj].status == 10:
                        flag.append((curi,curj))
                
                #bottom-right tile
                curi = i+1
                curj = j+1
                
                if 0 <= curi <= n-1 and 0 <= curj <= n-1:
                    if buttons[curi][curj].status == 9:
                        risk.append((curi,curj))
                    elif buttons[curi][curj].status == 10:
                        flag.append((curi,curj))

                #what action to take?
                clickside = ""
                
                #if only the bombs remain unmarked
                if curs - len(flag) == risk:
                    clickside = "right"
                    
                #if all the bombs have already been marked    
                elif curs == len(flag):
                    clickside = "left"
                
                for coord in risk:
                    clickcoord = (buttons[coord[0]][coord[1]].x, buttons[coord[0]][coord[1]].y)    
                    pg.click(x=clickcoord[0],y=clickcoord[1],button=clickside)
                        

#start execution 
initialize()

while check_run():
        
    #update board
    update_tiles()
    
    #solve the board
    solve()
                    
