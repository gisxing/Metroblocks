# Andrew Quintanilla
# Menu
import pygame

white = (255,255,255)
black = (0,0,0)
yellow = (255,255,0)
opacity = 0.5
backgroundpos = (0,0)
resumepos = (0,0)
newgamepos = (0,0)
resumetext = 'Resume'
newgametext = 'New Game'
quittext = 'Quit'

class Menu(pygame.sprite.OrderedUpdates):
    def __init__(self,screendimensions):
        xborder = screendimensions[0]
        yborder = screendimensions[1]
        pygame.sprite.OrderedUpdates.__init__(self)
        self.background = pygame.sprite.Sprite()
        self.background.image = pygame.Surface((600,400))
        self.background.image.fill(black)
        self.background.image.set_alpha(255*opacity)
        self.background.rect = self.background.image.get_rect()
        self.background.rect.centerx = xborder/2
        self.background.rect.centery = yborder/2
        self.font = pygame.font.SysFont("quartzms",40)
        self.resume = pygame.sprite.Sprite()
        self.resume.image = self.font.render(resumetext,True,white)
        self.resume.rect = self.resume.image.get_rect()
        self.resume.rect.top = self.background.rect.top + 20
        self.resume.rect.centerx = self.background.rect.centerx
        self.resume.highlighted = False
        self.newgame = pygame.sprite.Sprite()
        self.newgame.image = self.font.render(newgametext,True,white)
        self.newgame.rect = self.newgame.image.get_rect()
        self.newgame.rect.top = self.resume.rect.bottom + 20
        self.newgame.rect.centerx = self.resume.rect.centerx
        self.newgame.highlighted = False
        self.quit = pygame.sprite.Sprite()
        self.quit.image = self.font.render(quittext,True,white)
        self.quit.rect = self.quit.image.get_rect()
        self.quit.rect.top = self.newgame.rect.bottom + 20
        self.quit.rect.centerx = self.newgame.rect.centerx
        self.quit.highlighted = False
        self.mouse = pygame.sprite.Sprite()
        self.mouse.image = pygame.Surface((1,1))
        self.mouse.rect = self.mouse.image.get_rect()
        self.enabled = False
        self.option = -1

    def ToggleMenu(self):
        if self.enabled:
            self.HideMenu()
        else:
            self.ShowMenu()

    def ShowMenu(self):
        self.add(self.background)
        self.add(self.resume)
        self.add(self.newgame)
        self.add(self.quit)
        self.enabled = True

    def HideMenu(self):
        for sp in self.sprites():
            sp.kill()
        self.enabled = False

    def update(self,mousepos):
        if self.enabled:
            self.mouse.rect.topleft = mousepos
            if pygame.sprite.collide_rect(self.mouse,self.resume):
                if not self.resume.highlighted:
                    self.resume.image = self.font.render(resumetext,True,yellow)
                    self.resume.highlighted = True
                    self.option = 0
            else:
                if self.resume.highlighted:
                    self.resume.image = self.font.render(resumetext,True,white)
                    self.resume.highlighted = False
                    self.option = -1
            if pygame.sprite.collide_rect(self.mouse,self.newgame):
                if not self.newgame.highlighted:
                    self.newgame.image = self.font.render(newgametext,True,yellow)
                    self.newgame.highlighted = True
                    self.option = 1
            else:
                if self.newgame.highlighted:
                    self.newgame.image = self.font.render(newgametext,True,white)
                    self.newgame.highlighted = False
                    self.option = -1
            if pygame.sprite.collide_rect(self.mouse,self.quit):
                if not self.quit.highlighted:
                    self.quit.image = self.font.render(quittext,True,yellow)
                    self.quit.highlighted = True
                    self.option = -2
            else:
                if self.quit.highlighted:
                    self.quit.image = self.font.render(quittext,True,white)
                    self.quit.highlighted = False
                    self.option = -1
