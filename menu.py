# Andrew Quintanilla
# Menu
import pygame

white = (255,255,255)
black = (0,0,0)
yellow = (255,255,255)

class Menu(pygame.sprite.Group):
    def __init__(self,xborder,yborder):
        pygame.sprite.Group.__init__(self)
        self.font = pygame.font.SysFont("quartzms",40)
        self.resumetext = pygame.sprite.Sprite()
        self.resumetext.image = self.font.render('Resume',True,white)
        self.resumetext.rect = self.scoretext.image.get_rect()
        self.newgametext = pygame.sprite.Sprite()
        self.newgametext.image = self.font.render('New Game',True,white)
        self.newgametext.rect = self.newgametext.image.get_rect()
        
