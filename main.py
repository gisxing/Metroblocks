# Andrew Quintanilla
# Lumines clone
import os, sys, pygame, blocks
from pygame.locals import *

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
charcoal = (37,37,38)

def main():
    screendimensions = (720,450)
    pygame.init()
    screen = pygame.display.set_mode(screendimensions)
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(True)

    tile = blocks.Tile(red,white)
    grid = blocks.Grid()

    while 1:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                return

        screen.fill(charcoal)
        grid.draw(screen)
        screen.blit(tile.image,pygame.mouse.get_pos())
        pygame.display.flip()

if __name__ == '__main__':
    main()
