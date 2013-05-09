# Andrew Quintanilla
# Handles blocks
import pygame, random as rnd
from pygame.locals import *

white = (255,255,255)
black = (0,0,0)
grey_lite = (128,128,128)
yellow = (255,255,0)
layouts = dict([(1,(0,0,0,0)), (2,(0,0,0,1)), (3,(0,0,1,1)), (4, (1,0,1,1)),
               (5, (1,1,1,1)), (6, (0,1,0,1))])
tilesize = (45,45)
liningsize = (tilesize[0]-4,tilesize[1]-4)
innersize = (liningsize[0]-4,liningsize[1]-4)
flagliningsize = (tilesize[0]-2,tilesize[1]-2)
flaginnersize = (flagliningsize[0]-2,flagliningsize[1]-2)
griddimensions = (720,450)
tiledropwait = 0.05

class BlockManager(pygame.sprite.Group):
    def __init__(self, color1, color2, wiperspeed, fallwait, xoffset=0,
                 yoffset=0):
        pygame.sprite.Group.__init__(self)
        self.color1 = color1
        self.color2 = color2
        self.waitcount = 0.0
        self.tilewait = 0.0
        self.fallingblock = False
        self.droppingblocktiles = False
        # y = 0,1 are above the gridlines, blocks wait here
        self.grid = [[0 for y in range(12)] for x in range(16)]
        self.xoffset = xoffset
        self.yoffset = yoffset
        self.wiper = Wiper(wiperspeed,self.xoffset,self.yoffset)
        self.fallwait = fallwait
        self.grid = Gridlines(self.xoffset,self.yoffset)

    def KeydownHandler(self, key):
        if key == K_x:
            self.block.RotateClockwise()
        elif key == K_z:
            self.block.RotateCounterclockwise()
        elif key == K_RIGHT:
            self.block.MoveRight()
            if self.CheckBlockCollision():
                self.block.MoveLeft()
        elif key == K_LEFT:
            self.block.MoveLeft()
            if self.CheckBlockCollision():
                self.block.MoveRight()
        elif key == K_DOWN:
            self.oldfallwait = self.fallwait
            self.fallwait = 0.08

    def KeyupHandler(self, key):
        if key == K_DOWN:
            self.fallwait = self.oldfallwait

    def CheckBlockCollision(self):
        if pygame.sprite.groupcollide(self.block,self,False,False):
            print('collide self')
            return True
        elif self.block.x < self.xoffset:
            print('collide left side')
            return True
        elif self.block.x > self.xoffset+griddimensions[0]-2*tilesize[0]:
            print('collide right side')
            return True
        elif self.block.y > self.yoffset+griddimensions[1]-2*tilesize[1]:
            print('collide bottom')
            return True
        else:
            return False

    def CheckTileCollision(self,tile):
        if pygame.sprite.spritecollide(tile,self,False):
            print('collide self')
            return True
        elif tile.rect.bottom > griddimensions[1]+self.yoffset:
            print('collide bottom')
            return True
        else:
            return False

    # If 2x2 is found, tiles in 2x2 are flagged
    def Check2x2(self,tile):
        pass

    def update(self, time):        
        self.wiper.update(time)
        if self.fallingblock:
            if self.waitcount < self.fallwait:
                self.waitcount += time
            else:
                self.block.DropOne()
                self.waitcount = 0.0
                # Triggers when a block lands
                if self.CheckBlockCollision():
                    self.block.RaiseOne()
                    self.fallingblock = False
                    self.droppingblocktiles = True
        # Handles block tiles dropping into gaps
        elif self.droppingblocktiles:
            if self.tilewait < tiledropwait:
                self.tilewait += time
            else:
                self.block.tiledict[3].DropOne()
                while not self.CheckTileCollision(self.block.tiledict[3]):
                    self.block.tiledict[3].DropOne()
                self.block.tiledict[3].RaiseOne()
                self.add(self.block.tiledict[3])
                
                self.block.tiledict[0].DropOne()
                while not self.CheckTileCollision(self.block.tiledict[0]):
                    self.block.tiledict[0].DropOne()
                self.block.tiledict[0].RaiseOne()
                self.add(self.block.tiledict[0])
                
                self.block.tiledict[2].DropOne()
                while not self.CheckTileCollision(self.block.tiledict[2]):
                    self.block.tiledict[2].DropOne()
                self.block.tiledict[2].RaiseOne()
                self.add(self.block.tiledict[2])
                
                self.block.tiledict[1].DropOne()
                while not self.CheckTileCollision(self.block.tiledict[1]):
                    self.block.tiledict[1].DropOne()
                self.block.tiledict[1].RaiseOne()
                self.add(self.block.tiledict[1])
                
                self.block.empty()
                self.droppingblocktiles = False
                    
        else:
            self.block = Block(self.color1,self.color2,
                               griddimensions[0]/2-tilesize[0]+self.xoffset,
                               self.yoffset-tilesize[1]*2)
            self.fallingblock = True
        pygame.sprite.Group.update(self)

    def draw(self, Surface):
        self.grid.draw(Surface)
        pygame.sprite.Group.draw(self,Surface)
        self.block.draw(Surface)
        self.wiper.draw(Surface)

class Tile(pygame.sprite.Sprite):
    def __init__(self, color1, color2):
        pygame.sprite.Sprite.__init__(self)
        self.color1 = color1
        self.color2 = color2
        self.image = pygame.Surface(tilesize)
        self.image.fill(color1)
        lining = pygame.Surface(liningsize)
        lining.fill(color2)
        inner = pygame.Surface(innersize)
        inner.fill(color1)
        self.image.blit(lining,(2,2))
        self.image.blit(inner,(4,4))
        self.rect = self.image.get_rect()

    def DropOne(self):
        self.rect.top += tilesize[1]

    def RaiseOne(self):
        self.rect.top -= tilesize[1]

    # Flags tiles according to position in 2x2
    # 0: Topright
    # 1: Topleft
    # 2: Bottomleft
    # 3: Bottomright
    def FlagTile(self,pos):
        self.image.fill(self.color1)
        lining = pygame.Surface(flagliningsize)
        inner = pygame.Surface(flaginnersize)
        lining.fill(color2)
        inner.fill(color1)
        if pos == 0:
            self.image.blit(lining,(2,2))
            self.image.blit(inner,(4,4))
        elif pos == 1:
            self.image.blit(lining,(0,2))
            self.image.blit(inner,(0,4))
        elif pos == 2:
            self.image.blit(lining,(2,0))
            self.image.blit(inner,(4,0))
        else:
            self.image.blit(lining,(0,0))
            self.image.blit(inner,(0,0))

# Returns a random block, tiles arraged
# 0 1
# 3 2
class Block(pygame.sprite.Group):
    def __init__(self, color1, color2, x=0, y=0):
        pygame.sprite.Group.__init__(self)
        layout = layouts[rnd.randint(1,6)]        
        # x and y are the coordinates of the top left corner of block
        for i in layout:
            if i == 0:
                self.add(Tile(color1,color2))
            else:
                self.add(Tile(color2,color1))
        self.tiledict = {}        
        for i in range(4):
            if i == 0:
                self.sprites()[i].rect.left = x
                self.sprites()[i].rect.top = y
            elif i == 1:
                self.sprites()[i].rect.left = x + tilesize[0]
                self.sprites()[i].rect.top = y
            elif i == 2:
                self.sprites()[i].rect.left = x + tilesize[0]
                self.sprites()[i].rect.top = y + tilesize[1]
            else:
                self.sprites()[i].rect.left = x
                self.sprites()[i].rect.top = y + tilesize[1]
            self.tiledict[i]=self.sprites()[i]
        self.x = self.sprites()[0].rect.left
        self.y = self.sprites()[0].rect.top

    def RotateCounterclockwise(self):
        x0 = self.sprites()[0].rect.topleft
        x1 = self.sprites()[1].rect.topleft
        x2 = self.sprites()[2].rect.topleft
        x3 = self.sprites()[3].rect.topleft
        self.sprites()[0].rect.topleft = x3
        self.sprites()[1].rect.topleft = x0
        self.sprites()[2].rect.topleft = x1
        self.sprites()[3].rect.topleft = x2        
        s0 = self.tiledict[0]
        s1 = self.tiledict[1]
        s2 = self.tiledict[2]
        s3 = self.tiledict[3]
        self.tiledict[0] = s1
        self.tiledict[1] = s2
        self.tiledict[2] = s3
        self.tiledict[3] = s0

    def RotateClockwise(self):
        x0 = self.sprites()[0].rect.topleft
        x1 = self.sprites()[1].rect.topleft
        x2 = self.sprites()[2].rect.topleft
        x3 = self.sprites()[3].rect.topleft
        self.sprites()[0].rect.topleft = x1
        self.sprites()[1].rect.topleft = x2
        self.sprites()[2].rect.topleft = x3
        self.sprites()[3].rect.topleft = x0
        s0 = self.tiledict[0]
        s1 = self.tiledict[1]
        s2 = self.tiledict[2]
        s3 = self.tiledict[3]
        self.tiledict[0] = s3
        self.tiledict[1] = s0
        self.tiledict[2] = s1
        self.tiledict[3] = s2

    def MoveRight(self):
        x_list = []
        for sp in self.sprites():
            sp.rect.left += tilesize[0]
            x_list.append(sp.rect.left)
        if x_list:
            self.x = min(x_list)

    def MoveLeft(self):
        x_list = []
        for sp in self.sprites():
            sp.rect.left -= tilesize[0]
            x_list.append(sp.rect.left)
        if x_list:
            self.x = min(x_list)

    def DropOne(self):
        y_list = []
        for sp in self.sprites():
            sp.DropOne()
            y_list.append(sp.rect.top)
        if y_list:
            self.y = min(y_list)

    def RaiseOne(self):
        y_list = []
        for sp in self.sprites():
            sp.RaiseOne()
            y_list.append(sp.rect.top)
        if y_list:
            self.y = min(y_list)
        

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
            self.add(Line((griddimensions[0]+2,2),(xoffset-1,45*i-1+yoffset)))
        for i in range(0,17):
            self.add(Line((2,griddimensions[1]+1),(45*i-1+xoffset,yoffset)))

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
        
