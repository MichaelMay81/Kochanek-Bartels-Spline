import pygame

from pygame.locals import *

import sys, os
import random

import spline

if sys.platform == 'win32' or sys.platform == 'win64':

    os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()



Screen = (800,600)

icon = pygame.Surface((1,1)); icon.set_alpha(0); pygame.display.set_icon(icon)

pygame.display.set_caption("Kochanek-Bartels Spline - Ian Mallett - 1.0.0 - May 2008")

Surface = pygame.display.set_mode(Screen)




for i in range(5):
            spline.ControlPoints.append((random.random()*800, random.random()*600))



pressing = False

def GetInput():

    global pressing

    key = pygame.key.get_pressed()

    mpress = pygame.mouse.get_pressed()

    mpos = pygame.mouse.get_pos()

    for event in pygame.event.get():

        if event.type == QUIT or key[K_ESCAPE]:

            pygame.quit(); sys.exit()

    if mpress[0]:

        if not pressing:

            pressing = True

            spline.ControlPoints.append((mpos[0],mpos[1]))

    else:

        pressing = False



def Draw():

    Surface.fill((0,0,0))

    for cp in spline.ControlPoints:

        pygame.draw.circle(Surface,(255,0,0),(int(cp[0]),int(cp[1])),2)

    if len(spline.ControlPoints) >= 4:

        finalpoints = spline.DrawCurve()
        
        #for pset in finalpoints:
        pygame.draw.aalines(Surface,(255,255,255),False,finalpoints)

    pygame.display.flip()

def main():

    while True:

        GetInput()

        Draw()

if __name__ == '__main__': main()