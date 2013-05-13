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
royalblue = (65,105,225)
deepskyblue = (0,191,255)
gold = (255,215,0)
yellow = (255,255,0)

def main():
    screendimensions = (1000,600)
    griddimensions = (720,450)
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (50,50)
    pygame.init()
    screen = pygame.display.set_mode(screendimensions)
    font = pygame.font.SysFont("quartzms",50)
    loading = pygame.sprite.Sprite()
    loading.image = font.render('- LOADING-',True,white)
    loading.rect = loading.image.get_rect()
    loading.rect.centerx = screendimensions[0]/2
    loading.rect.centery = screendimensions[1]/2
    screen.blit(loading.image,loading.rect)
    pygame.display.flip()
    clock = pygame.time.Clock()
    mousevisible = False
    pygame.mouse.set_visible(mousevisible)    
    color1 = red
    color2 = white
    manager = blocks.BlockManager(color1,color2,125,1.5,
                                  (screendimensions[0]-griddimensions[0])/2,
                                  screendimensions[1]-griddimensions[1]-20)
    inf = info.Info(screendimensions[0],screendimensions[1])
    menu = Menu(screendimensions)
    songs = glob('*.ogg')
    shuffle(songs)
    print(songs)
    if songs:
        pygame.mixer.music.load(songs[0])
        pygame.mixer.music.play()
        currentsong = 0
        songlengths = []
        for song in songs:
            songlengths.append(pygame.mixer.Sound(song).get_length())

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
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    mousevisible = not mousevisible
                    pygame.mouse.set_visible(mousevisible)
                    menu.ToggleMenu()
                # Send keyboard input to manager to be handled
                if not menu.enabled and not inf.IsGameOver():
                    manager.KeydownHandler(event.key)
            elif event.type == KEYUP and not inf.IsGameOver():
                if not menu.enabled:
                    manager.KeyupHandler(event.key)

        if songs and pygame.mixer.music.get_pos()/1000+1 > songlengths[currentsong]:
            currentsong = (currentsong+1)%len(songs)
            pygame.mixer.music.load(songs[currentsong])
            pygame.mixer.music.play()
        if menu.enabled:
            choice = menu.update(pygame.mouse.get_pos())
        else:
            if not inf.IsGameOver():
                if manager.score == -1:
                    print('main gameover')
                    inf.GameOver()
                else:
                    manager.update(time)
                    inf.update(manager.score)
            
        screen.fill(charcoal)
        manager.draw(screen)
        inf.draw(screen)
        menu.draw(screen)
        pygame.display.flip()

if __name__ == '__main__':
    main()
