import time
import numpy
import os
import keyboard
import pygame
from tkinter import *
from tkinter import messagebox

pygame.init()

#python Documents\Projects\Programming\Python\ConwaysGameOfLife\ConwaysRules.py

WIDTH = 1500
HEIGHT = 700
GRID_WIDTH = int(WIDTH/10)
GRID_HEIGHT = int(HEIGHT/10)
gridBool = numpy.full((GRID_WIDTH, GRID_HEIGHT), False)
tempGridBool = numpy.copy(gridBool)
row, column = gridBool.shape
drawerCellPos = [0, 0]
is_running = True

WIN = pygame.display.set_mode((WIDTH, HEIGHT)) 
pygame.display.set_caption ("Conways Game Of Life")
MAX_FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (155, 155, 155)

FIELD_SPACING = WIDTH / GRID_WIDTH


def DrawCell(): 
    global drawerCellPos, key_is_pressed, is_running
    key_is_pressed = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                return
        currently_pressed_key = pygame.key.get_pressed()
        print(GRID_WIDTH, drawerCellPos[0], 0)
        if currently_pressed_key[pygame.K_UP] and drawerCellPos[1] > 0:
            drawerCellPos[1] -= 1
            key_is_pressed = True
        if currently_pressed_key[pygame.K_DOWN] and drawerCellPos[1] < GRID_HEIGHT-1:
            drawerCellPos[1] += 1
            key_is_pressed = True
        if currently_pressed_key[pygame.K_LEFT] and drawerCellPos[0] > 0:
            drawerCellPos[0] -= 1
            key_is_pressed = True
        if currently_pressed_key[pygame.K_RIGHT] and drawerCellPos[0] < GRID_WIDTH-1:
                drawerCellPos[0] += 1
                key_is_pressed = True
        if currently_pressed_key[pygame.K_RETURN]:
            return
        if currently_pressed_key[pygame.K_d]:
            gridBool[drawerCellPos[0], drawerCellPos[1]] = False
            tempGridBool[drawerCellPos[0], drawerCellPos[1]] = False
            key_is_pressed = True
        if currently_pressed_key[pygame.K_f]:
            gridBool[drawerCellPos[0], drawerCellPos[1]] = True
            tempGridBool[drawerCellPos[0], drawerCellPos[1]] = True                
            key_is_pressed = True
        if currently_pressed_key[pygame.K_r]:
            for i in range(column):
                for j in range(row):
                    tempGridBool[j][i] = False
                    gridBool[j][i] = False
        if currently_pressed_key[pygame.K_LCTRL] or currently_pressed_key[pygame.K_RCTRL]:
            second_pressed_key = pygame.key.get_pressed()
            if second_pressed_key[pygame.K_s]:
                save_file = open('save.txt', 'w')
                save_file.close()
                save_file = open('save.txt', 'a')
                for i in range(column):
                    for j in range(row):
                        if tempGridBool[j][i] == True:
                            temp_text = str(j) + ' ' + str(i)
                            save_file.write(temp_text)
                            save_file.write("\n") 
                save_file.close()
                time.sleep(0.3)
            if second_pressed_key[pygame.K_l]:
                Handle_Save_File()


        DrawField()
        if(key_is_pressed):
            # print(drawerCellPos[0], drawerCellPos[1])
            WIN.fill(WHITE)
            DrawField()
            key_is_pressed = False
            # time.sleep(0.03)

def Handle_Save_File():
    save_file = open('save.txt', 'r')
    for line in save_file:
        temp_word = []
        # print(line)
        words = line.rstrip().split()
        for word in words:
            temp_word.append(word)
        tempGridBool[int(temp_word[0])][int(temp_word[1])] = True
        gridBool[int(temp_word[0])][int(temp_word[1])] = True
    save_file.close()

def DrawField():
    global drawerCellPos
    WIN.fill(WHITE)
    for i in range(column):
        for j in range(row):
            if tempGridBool[j, i]:
                pygame.draw.rect(WIN, BLACK, pygame.Rect(FIELD_SPACING*j, FIELD_SPACING*i, FIELD_SPACING, FIELD_SPACING))
            elif j == drawerCellPos[0] and i == drawerCellPos[1]:
                pygame.draw.rect(WIN, (255, 0, 0), pygame.Rect(FIELD_SPACING*j, FIELD_SPACING*i, FIELD_SPACING, FIELD_SPACING))
            else:
                pygame.draw.rect(WIN, WHITE, pygame.Rect(FIELD_SPACING*j, FIELD_SPACING*i, FIELD_SPACING, FIELD_SPACING))
    pygame.display.update()

def CountNeighbours(xPos, yPos):
    neighbours = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if xPos + j <= row - 1 and yPos + i <= column - 1 and xPos + j >= 0 and yPos + i >= 0:
                if tempGridBool[xPos + j, yPos + i]:
                    neighbours += 1
    return neighbours

def OverUnderPopulation(xPos, yPos):
    if (CountNeighbours(xPos, yPos) > 4 or CountNeighbours(xPos, yPos) < 3) and tempGridBool[xPos, yPos]:
        gridBool[xPos, yPos] = False

def Alive3Neighbours(xPos, yPos):
    if CountNeighbours(xPos, yPos) == 3 and tempGridBool[xPos, yPos] == False:
        gridBool[xPos, yPos] = True

def Main():
    global tempGridBool, is_running
    DrawField()
    messagebox.showinfo('Conways Game Of Life',
'''
F = Place Block
D = Delete Block
CTRL + S = Save Blocks
CTRL + L = Load Blocks
ENTER = New Generation''')
    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
        currently_pressed_key = pygame.key.get_pressed()
        if currently_pressed_key[pygame.K_RETURN]:
            WIN.fill(WHITE)
            tempGridBool = numpy.copy(gridBool)
            DrawField()
            for i in range(column):
                for j in range(row):
                    OverUnderPopulation(j, i)
                    Alive3Neighbours(j, i)
            # time.sleep(0.1)
        DrawCell()

    pygame.quit()

Main()

# Glider Gun:
#  5 1
#  6 1
#  5 2
#  6 2
#  5 11
#  6 11
#  7 11
#  4 12
#  8 12
#  3 13
#  9 13
#  3 14
#  9 14
#  6 15
#  4 16
#  8 16
#  5 17
#  6 17
#  7 17
#  6 18
#  3 21
#  4 21
#  5 21
#  3 22
#  4 22
#  5 22
#  2 23
#  6 23
#  1 25
#  2 25
#  6 25
#  7 25
#  3 35
#  4 35
#  3 36
#  4 36