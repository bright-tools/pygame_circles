#  Copyright 2017 John Bailey
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0

#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import pygame, sys, math, time, colorsys
from pygame.locals import *

# Colours, defined in RGB triplets
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (32, 32, 32)
BLUE = (0, 0, 255)

LINES = 12
LINE_COLOUR = GREY 
INNER_CIRCLE_DIAMETER = 10
INNER_CIRCLE_THICKNESS = 2
INNER_CIRCLE_COLOUR = BLUE
DEGREES_IN_ROTATION = 360
EFFECT = 2
MAX_EFFECT = 2
TIME_STEP = 0.02

enableColour = False

class Circle:
    def __init__(self,center,diameter):
        self.center = center
        self.diameter = diameter

    def draw(self,windowSurface, colour, thickness):
        pygame.draw.circle(windowSurface, colour, self.center, self.diameter, thickness)

class Anim:

    def __init__(self,windowSurface):
        self.windowSurface = windowSurface
        self.step = 0

    def drawLine(self,angle):
        rads = math.radians(angle)
        startx = self.outerCircle.center[0] - math.sin(rads)*self.outerCircle.diameter
        starty = self.outerCircle.center[1] - math.cos(rads)*self.outerCircle.diameter
        endx = self.outerCircle.center[0] + math.sin(rads)*self.outerCircle.diameter
        endy = self.outerCircle.center[1] + math.cos(rads)*self.outerCircle.diameter
        pygame.draw.line(self.windowSurface, LINE_COLOUR, (startx,starty), (endx,endy), 1)

    def drawLines(self):
        for lineCount in range(0,LINES):
            self.drawLine( lineCount * self.spacing )

    def drawInnerCircle(self,angle,offset):
        global enableColour

        rads = math.radians(angle)
        diam = (self.outerCircle.diameter / DEGREES_IN_ROTATION) * (offset)
        startx = (int)(self.outerCircle.center[0] + math.sin(rads)*diam)
        starty = (int)(self.outerCircle.center[1] + math.cos(rads)*diam)
        circle = Circle( [startx, starty], INNER_CIRCLE_DIAMETER )
        if enableColour:
            col = tuple([255*x for x in colorsys.hsv_to_rgb(angle/180, 1, 1)])
        else:
            col = INNER_CIRCLE_COLOUR
        circle.draw( self.windowSurface, col, INNER_CIRCLE_THICKNESS )

    def drawCircleEffect1(self,angle):
        offset = (angle + self.step ) % DEGREES_IN_ROTATION
        self.drawInnerCircle( angle, offset )

    def drawCircleEffect2(self,angle):
        offset = math.sin(math.radians((angle + self.step ) % DEGREES_IN_ROTATION))*DEGREES_IN_ROTATION
        self.drawInnerCircle( angle,offset )

    def drawCircle(self,angle):
        if EFFECT == 1:
            self.drawCircleEffect1(angle)
        else:
            self.drawCircleEffect2(angle)

    def drawInnerCircles(self):
        self.step = (self.step + 1) % DEGREES_IN_ROTATION
        for lineCount in range(0,LINES):
            self.drawCircle( lineCount * self.spacing )

    def drawOuterCircle(self):
        windowMargin = 5
        winWidth, winHeight = pygame.display.get_surface().get_size()
        halfWinWidth = (int)(winWidth/2)
        circleDiameter = ((int)(min(winWidth,winHeight)/2))-windowMargin
        self.outerCircle = Circle( [halfWinWidth, (int)(winHeight/2)], circleDiameter )
        self.outerCircle.draw( self.windowSurface, WHITE, 2 )

    def updateWindow(self):
        self.spacing = DEGREES_IN_ROTATION / LINES

        if( EFFECT == 2 ):
            self.spacing /= 2

        self.windowSurface.fill(BLACK)

        self.drawOuterCircle()
        self.drawLines()
        self.drawInnerCircles()

        pygame.display.update()

def main():
    global LINES, EFFECT, enableColour
    pygame.init()
    windowSurface = pygame.display.set_mode((500, 500), 0, 32)
    pygame.display.set_caption('Keep your eyes on the circles ...')

    anim = Anim(windowSurface)

    while True:
        anim.updateWindow()
        sys.stdout.flush()
        time.sleep( TIME_STEP )
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if( LINES > 1 ):
                        LINES = LINES - 1 
                if event.key == pygame.K_RIGHT:
                    LINES = LINES + 1
                if event.key == pygame.K_DOWN:
                    if( EFFECT > 1 ):
                        EFFECT = EFFECT - 1 
                if event.key == pygame.K_UP:
                    if( EFFECT < MAX_EFFECT ):
                        EFFECT = EFFECT + 1
                if event.key == pygame.K_c:
                    enableColour = not enableColour
            elif event.type == QUIT:
                pygame.quit()
                sys.exit()


if __name__ == "__main__":
    main()

# vim: set noai tabstop=4 expandtab:
