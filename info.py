# Andrew Quintanilla
# Displays the score
import pygame

white = (255,255,255)
black = (0,0,0)

class Info(pygame.sprite.Group):
    def __init__(self, xborder, yborder):
        pygame.sprite.Group.__init__(self)
        self.scoreval = 0
        self.font = pygame.font.SysFont("quartzms",20)
        gameoverfont = pygame.font.SysFont("quartzms",100)
        self.scoretext = pygame.sprite.Sprite()
        self.scoretext.image = self.font.render('Score:',True,white)
        self.scoretext.rect = self.scoretext.image.get_rect()
        self.scoretext.rect.top = 130
        self.scoretext.rect.left = xborder-self.scoretext.rect.width-20
        self.add(self.scoretext)
        self.score = pygame.sprite.Sprite()
        self.score.image = self.font.render('{0}'.format(self.scoreval),True,white)
        self.score.rect = self.score.image.get_rect()
        self.score.rect.top = 130+self.scoretext.rect.height
        self.score.rect.left = xborder-self.score.rect.width-20
        self.add(self.score)
        self.xborder = xborder
        self.gameover = pygame.sprite.Sprite()
        self.gameover.image = gameoverfont.render('- Game Over -',True,black)
        self.gameover.rect = self.gameover.image.get_rect()
        self.gameover.rect.centerx = xborder/2
        self.gameover.rect.centery = yborder/2
        

    def reset(self):
        self.scoreval = 0
        self.gameover.kill()

    def update(self, scoreval):
        if self.scoreval != scoreval:
            self.scoreval = scoreval
            self.score.image = self.font.render('{0}'.format(self.scoreval),True,white)
            self.score.rect = self.score.image.get_rect()
            self.score.rect.top = 130+self.scoretext.rect.height
            self.score.rect.left = self.xborder-self.score.rect.width-20
        elif scoreval < 0:
            self.GameOver()

    def GameOver(self):
        print('gameover')
        self.add(self.gameover)

    def IsGameOver(self):
        return self.gameover in self.sprites()
