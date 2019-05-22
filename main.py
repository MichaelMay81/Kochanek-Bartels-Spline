import sys
import os
import random
from typing import Tuple

import pygame
from pygame.locals import *

import spline

TEXT_FONT = "Arial"
TEXT_COLOR = 255, 255, 255
BACKGROUND = 0, 0, 0

tension = 0.0
bias = 0.0
continuity = 0.0
pressing = False
selected = None


def GetInput(my_spline):
	global pressing, selected
	global tension, bias, continuity
	key = pygame.key.get_pressed()
	mpress = pygame.mouse.get_pressed()
	mpos = pygame.mouse.get_pos()

	for event in pygame.event.get():
		if event.type == QUIT or key[K_ESCAPE]:
			pygame.quit()
			sys.exit()
		elif key[K_t]:
			tension += 0.1
			if tension > 1:
				tension = 0.0
		elif key[K_b]:
			bias += 0.1
			if bias > 1:
				bias = 0.0
		elif key[K_c]:
			continuity += 0.1
			if continuity > 1:
				continuity = 0.0


	if mpress[0]:
		if not pressing:
			selected = None
			pressing = True
			nearest, dist = my_spline.nearestPoint((mpos[0], mpos[1]))
			nindex = my_spline.ControlPoints.index(nearest)

			if dist < 100:
				selected = nindex
			else:
				snearest, sdist = my_spline.nearestSubPoint((mpos[0], mpos[1]))
				snindex = my_spline.subpoints.index(snearest) - nindex
				nsindex = snindex/5.0
				print(nsindex, nindex)

				test = nsindex - nindex
				print(test)
				if test>=0 and test < 2:
					nindex+=1

				my_spline.ControlPoints.insert(nindex, (mpos[0], mpos[1]))
				selected = nindex
		else:
			my_spline.ControlPoints[selected] = (mpos[0], mpos[1])

	else:
		pressing = False


def DrawText(txt: str, surface: pygame.Surface, position: Tuple[int, int]):
	font = pygame.font.SysFont(TEXT_FONT, 15)
	tex_surf = font.render(txt, False, TEXT_COLOR, BACKGROUND)
	surface.blit(tex_surf, position)


def Draw(my_spline: spline.Spline, surface: pygame.Surface):
	global tension, bias, continuity

	surface.fill(BACKGROUND)
	DrawText("[t] tension       {:.1f}".format(tension), surface, (10, 10))
	DrawText("[b] bias            {:.1f}".format(bias), surface, (10, 30))
	DrawText("[c] continuity   {:.1f}".format(continuity), surface, (10, 50))
	DrawText("[ESC] quit", surface, (10, 70))

	for cp in my_spline.ControlPoints:
		pygame.draw.circle(surface, (255, 0, 0), (int(cp[0]), int(cp[1])), 2)

	finalpoints = my_spline.interpolate_curve(tension, bias, continuity)
	pygame.draw.aalines(surface, (255, 255, 255), False, finalpoints)

	pygame.display.flip()


def main():
	if sys.platform == 'win32' or sys.platform == 'win64':
		os.environ['SDL_VIDEO_CENTERED'] = '1'
	pygame.init()

	Screen = (800, 600)
	icon = pygame.Surface((1, 1))
	icon.set_alpha(0)
	pygame.display.set_icon(icon)

	pygame.display.set_caption("Kochanek-Bartels Spline - Ian Mallett - 1.0.0 - May 2008")
	Surface = pygame.display.set_mode(Screen)
	myspline = spline.Spline()

	for i in range(3):
		myspline.ControlPoints.append((random.random() * 800, random.random() * 600))

	while True:
		GetInput(myspline)
		Draw(myspline, Surface)


if __name__ == '__main__': main()
