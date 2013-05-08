# Andrew Quintanilla
# Handles blocks
import pygame, random as rnd

white = (255,255,255)
black = (0,0,0)
grey_lite = (128,128,128)
yellow = (255,255,0)
layouts = dict([(1,(0,0,0,0)), (2,(0,0,0,1)), (3,(0,0,1,1)), (4, (1,0,1,1)),
               (5, (1,1,1,1)), (6, (0,1,0,1))])
blocksize = (80,80)
tilesize = (45,45)
liningsize = (tilesize[0]-4,tilesize[1]-4)
innersize = (liningsize[0]-4,liningsize[1]-4)

class Tile(pygame.sprite.Sprite):
    def __init__(self, color1, color2):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(tilesize)
        self.image.fill(color1)
        lining = pygame.Surface(liningsize)
        lining.fill(color2)
        inner = pygame.Surface(innersize)
        inner.fill(color1)
        self.image.blit(lining,(2,2))
        self.image.blit(inner,(4,4))

# Returns a random block
class Block(pygame.sprite.Group):
    def __init__(self, color1, color2):
        pygame.sprite.Group.__init__(self)
        self.layout = layouts[rnd.randint(1,6)]
        for i in self.layout:
            if i == 0:
                self.add(Tile(color1,color2))
            else:
                self.add(Tile(color2,color1))
        self.pos = (0,0)

    def RotateCounterclockwise(self):
        x0 = self.layout[0]
        x1 = self.layout[1]
        x2 = self.layout[2]
        x3 = self.layout[3]
        self.layout = (x3,x0,x1,x2)

    def RotateClockwise(self):
        x0 = self.layout[0]
        x1 = self.layout[1]
        x2 = self.layout[2]
        x3 = self.layout[3]
        self.layout = (x1,x2,x3,x0)

    #def update(self):

class Line(pygame.sprite.Sprite):
    def __init__(self, size, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(size)
        self.image.fill(grey_lite)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        
# Draws grid of 15 vertical lines x 9 horizontal lines
class Grid(pygame.sprite.Group):
    def __init__(self):
        pygame.sprite.Group.__init__(self)
        for i in range(1,10):
            self.add(Line((720,2),(0,45*i)))
        for i in range(1,16):
            self.add(Line((2,450),(45*i,0)))

# The line that wipes out blocks
class Wiper(pygame.sprite.GroupSingle):
    def __init__(self, speed):
        pygame.sprite.GroupSingle.__init__(self)
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = pygame.Surface((2,450))
        self.sprite.image.fill(yellow)
        self.sprite.rect = self.sprite.image.get_rect()
        self.sprite.rect.topleft = (0,0)
        # Velocity is measured in pixels per second
        self.speed = speed
        self.left_float = 0.0

    def update(self, time):
        self.left_float = self.left_float + self.speed*time
        if (self.left_float > 748):
            self.left_float = 0.0
        self.sprite.rect.left = self.left_float
        
