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

class BlockManager(pygame.sprite.Group):
    def __init__(self, color1, color2, wiperspeed, dropspeed, xoffset=0,
                 yoffset=0):
        pygame.sprite.Group.__init__(self)
        self.color1 = color1
        self.color2 = color2
        self.waitingcount = -1
        self.fallingblock = False
        self.grid = [[0 for y in range(10)] for x in range(16)]
        self.xoffset = xoffset
        self.yoffset = yoffset
        self.wiper = Wiper(wiperspeed,self.xoffset,self.yoffset)
        self.dropspeed = dropspeed
        self.grid = Gridlines(self.xoffset,self.yoffset)

    def update(self, time):
        self.wiper.update(time)
        if (self.waitingblock == -1):
            
        else:
            self.block = Block(self.color1,self.color2)
            self.add(self.block)
            self.fallingblock = False

    def draw(self, Surface):
        self.grid.draw(Surface)
        self.wiper.draw(Surface)

class Tile(pygame.sprite.Sprite):
    def __init__(self, color1, color2):
        pygame.sprite.Sprite.__init__(self)
        self.border = pygame.Surface
        self.image = pygame.Surface(tilesize)
        self.image.fill(color1)
        self.lining = pygame.Surface(liningsize)
        self.lining.fill(color2)
        self.inner = pygame.Surface(innersize)
        self.inner.fill(color1)
        self.image.blit(self.lining,(2,2))
        self.image.blit(self.inner,(4,4))

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

class Line(pygame.sprite.Sprite):
    def __init__(self, size, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(size)
        self.image.fill(grey_lite)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        
# Draws grid of 15 vertical lines x 9 horizontal lines
class Gridlines(pygame.sprite.Group):
    def __init__(self, xoffset=0, yoffset=0):
        pygame.sprite.Group.__init__(self)
        for i in range(0,11):
            self.add(Line((720,2),(xoffset,45*i-1+yoffset)))
        for i in range(0,17):
            self.add(Line((2,450),(45*i-1+xoffset,yoffset)))

# The line that wipes out blocks
class Wiper(pygame.sprite.GroupSingle):
    def __init__(self, speed, xoffset=0, yoffset=0):
        pygame.sprite.GroupSingle.__init__(self)
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = pygame.Surface((2,450))
        self.sprite.image.fill(yellow)
        self.sprite.rect = self.sprite.image.get_rect()
        self.xoffset = xoffset
        self.sprite.rect.topleft = (xoffset,yoffset)
        
        # Velocity is measured in pixels per second
        self.speed = speed
        self.left_float = 0.0+self.sprite.rect.left

    def update(self, time):
        self.left_float = self.left_float + self.speed*time
        if (self.left_float > 719+self.xoffset):
            self.left_float = 0.0+self.xoffset
        self.sprite.rect.left = self.left_float
        
