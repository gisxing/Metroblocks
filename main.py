# Andrew Quintanilla
# Lumines clone
import os, sys, pygame, blocks, info
from menu import Menu
from pygame.locals import *
from glob import glob
from random import shuffle

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
    mousevisible = False
    pygame.mouse.set_visible(mousevisible)

    color1 = red
    color2 = white
    manager = blocks.BlockManager(red,white,125,1.5,
                                  (screendimensions[0]-griddimensions[0])/2,
                                  screendimensions[1]-griddimensions[1]-20)
    inf = info.Info(screendimensions[0],screendimensions[1])
    menu = Menu(screendimensions)
    scorechange = 0
    songs = glob('*.ogg')
    shuffle(songs)
    for i in range(len(songs)):
        if i == 0:
            pygame.mixer.music.load(songs[i])
        else:
            pygame.mixer.music.queue(songs[i])
    if songs:
        pygame.mixer.music.play()

    while 1:
        time = clock.tick(60)/1000
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.mixer.music.stop()
                return
            elif event.type == MOUSEBUTTONDOWN:
                if menu.enabled:
                    if menu.option == -2:
                        pygame.mixer.music.stop()
                        return
                    elif menu.option == 0:
                        mousevisible = False
                        pygame.mouse.set_visible(mousevisible)
                        menu.HideMenu()
                    elif menu.option == 1:
                        manager.NewGame()
                        inf.reset()
                        scorechange = 0
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    mousevisible = not mousevisible
                    pygame.mouse.set_visible(mousevisible)
                    menu.ToggleMenu()
                # Send keyboard input to manager to be handled
                if not menu.enabled and scorechange != -1:
                    manager.KeydownHandler(event.key)
            elif event.type == KEYUP and scorechange != -1:
                if not menu.enabled:
                    manager.KeyupHandler(event.key)

        if menu.enabled:
            choice = menu.update(pygame.mouse.get_pos())
        elif scorechange != -1:
            scorechange = manager.update(time)
        if scorechange:
            inf.update(scorechange)
        screen.fill(charcoal)
        manager.draw(screen)
        menu.draw(screen)
        inf.draw(screen)
        pygame.display.flip()

if __name__ == '__main__':
    main()
