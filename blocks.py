# Andrew Quintanilla
# Handles blocks
import pygame, random as rnd

white = (255,255,255)
black = (0,0,0)
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

# Draws grid of 15 vertical lines x 9 horizontal lines
class Grid(pygame.sprite.Group):
    def __init__(self):
        pygame.sprite.Group.__init__(self)
        

if __name__ == '__main__':
    x = Block()
    print("{0}".format(x.layout))
    x.RotateCounterclockwise()
    print("{0}".format(x.layout))
    x.RotateClockwise()
    print("{0}".format(x.layout))
