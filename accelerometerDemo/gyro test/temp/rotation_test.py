"""
Drawing an arrow and bar depending on on gyro values
"""
import numpy as np
from math import *
import pygame
import sys
import time
 
if sys.platform == 'win32':
    # On Windows, the best timer is time.clock
    default_timer = time.clock
else:
    # On most other platforms the best timer is time.time
    default_timer = time.time

background_color = (255,255,255)
Red = (255,0,0)
Green = (0,255,0)
Blue = (0,0,255)
(width, height) = (500, 250)

def rotate2D(point, center, angledeg):
    """ rotates an (x,y) point around the point center, by given angle """
    M = np.array([[cos(radians(angledeg)), -sin(radians(angledeg))] ,
                  [sin(radians(angledeg)),  cos(radians(angledeg))]])
    return( np.dot(M,(point-center)) + center )
     
def rotate2D_points(points, center, angledeg):
    """ rotates a list of points around the point center, by given angle """
    result=np.empty(points.shape)
    for i in range(len(points)):
        result[i] = rotate2D(points[i],center=center,angledeg=angledeg)
    return result

class Arrow:
    def __init__(self, center, length):
        self.color = (255, 0, 255)
        self.center = center
        self.length = length
        
    def display(self, angle):
        x, y = self.center
        L=self.length
        points = np.array([[x+0, y-0.75*L], [x+0.25*L, y+0.25*L],
                  [x,y], [x-0.25*L, y+0.25*L]])
        newpts = rotate2D_points(points,self.center, angle)                  
        pygame.draw.aalines(screen, self.color, True, 
                            newpts, 0) # closed=True, blend=0

class Speedbar:
    def __init__(self, position=(10,10), width=30, scale=1, color=Blue):
        self.position = position # x,y position of zero on the screen
        self.width = width
        self.scale = scale          # size of bar is value*scale
        self.color = color
        
    def display(self, value):
        x0, y0 = self.position
        rect = (x0-self.width/2, y0, self.width, -value*self.scale)
        pygame.draw.rect(screen, self.color, rect, 0)
        #screen.fill(Red, rect+(100,100,0,0))

class TArc:
    def __init__(self, position=(10,10), size=30, scale=1, color=Blue):
        self.position = position # x,y position of zero on the screen
        self.size=size
        self.scale = scale          # size of bar is value*scale
        self.color = color
        
    def display(self, value):
        x0, y0 = self.position
        rect = (x0-self.size/2, y0-self.size/2, self.size, self.size)
        angle1 = radians(90)
        angle2 = radians(90-value)
        startangle = min(angle1, angle2)
        stopangle = max(angle1, angle2)
        print(startangle, stopangle)
        print(startangle, stopangle)
        pygame.draw.arc(screen, self.color, rect, startangle, stopangle, 10)     # width 5

pygame.init()                      
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Gyro / Accelerometer test')
screen.fill(background_color)

arrow_center = (150,150)
acc_x_pos = (300,150)
acc_y_pos = (340,150)
acc_z_pos = (380,150)
gyro_x_center = (450,60)
gyro_y_center = (450,130)
gyro_z_center = (450,200)
gyro_z_center2 = arrow_center

rotation_arrow = Arrow(center=arrow_center, length=120)
accxbar = Speedbar(position=acc_x_pos)
accybar = Speedbar(position=acc_y_pos)
acczbar = Speedbar(position=acc_z_pos)
tachox = TArc(position=gyro_x_center, size=60, scale=1, color=Red)
tachoy = TArc(position=gyro_y_center, size=60, scale=1, color=Green)
tachoz = TArc(position=gyro_z_center, size=60, scale=1, color=Blue)
tachoz2 = TArc(position=gyro_z_center2, size=200, scale=1, color=Green)
rotation_arrow.display(-90)
accxbar.display(50)
accybar.display(20)
acczbar.display(-40)
tachox.display(360)
tachoy.display(-350)
tachoz.display(350)
tachoz2.display(90)

pygame.display.flip()

running = True
tnow = tlast = default_timer()
angle = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
#    tnow = default_timer()
#    if tnow-tlast>1:
#        angle = fmod(angle + (tnow-tlast)*6, 360)
#        print(angle)
#        screen.fill(background_color)
#        rotation_arrow.display(angle)
#        pygame.display.flip()
#        tlast = tnow
            
pygame.quit()

