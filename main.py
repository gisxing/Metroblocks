# Andrew Quintanilla
# Lumines clone
import os, sys, pygame, blocks, info
from pygame.locals import *

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
charcoal = (37,37,38)

def main():
    screendimensions = (1000,600)
    griddimensions = (720,450)
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (50,50)
    pygame.init()
    screen = pygame.display.set_mode(screendimensions)
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)

    color1 = red
    color2 = white
    manager = blocks.BlockManager(red,white,125,1.5,
                                  (screendimensions[0]-griddimensions[0])/2,
                                  screendimensions[1]-griddimensions[1]-20)
    inf = info.Info(screendimensions[0],screendimensions[1])
    paused = False
    scorechange = 0

    while 1:
        time = clock.tick(60)/1000
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    paused = not paused
                # Send keyboard input to manager to be handled
                if not paused and scorechange != -1:
                    manager.KeydownHandler(event.key)
            elif event.type == KEYUP and scorechange != -1:
                if not paused:
                    manager.KeyupHandler(event.key)
                    
        if not paused and scorechange != -1:
            scorechange = manager.update(time)
        if scorechange:
            inf.update(scorechange)
        screen.fill(charcoal)
        manager.draw(screen)
        inf.draw(screen)
        pygame.display.flip()

if __name__ == '__main__':
    main()
