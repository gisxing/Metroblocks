#!/usr/bin/python
#coding=utf-8
# Andrew Quintanilla
# Handles blocks
import pygame, random as rnd
from pygame.locals import *

white = (255,255,255)
black = (0,0,0)
grey_lite = (128,128,128)
yellow = (255,255,0)
# 6种砖块的组合 0 ， 1 代表两种不同颜色
layouts = dict([(1,[0,0,0,0]), (2,[0,0,0,1]), (3,[0,0,1,1]), (4, [1,0,1,1]),
               (5, [1,1,1,1]), (6, [0,1,0,1])])
tilesize = (45,45)     # 每个小格子的大小
liningsize = (tilesize[0]-4,tilesize[1]-4)
innersize = (liningsize[0]-4,liningsize[1]-4)
flagliningsize = (tilesize[0]-2,tilesize[1]-2)
flaginnersize = (flagliningsize[0]-2,flagliningsize[1]-2)
griddimensions = (720,450)
gridsize = (16,12)
fastfall = 0.01

class BlockManager(pygame.sprite.Group):
    def __init__(self, color1, color2, wiperspeed, waitcount, xoffset=0,
                 yoffset=0):
        pygame.sprite.Group.__init__(self)
        self.color1 = color1
        self.color2 = color2
        self.waitcount = waitcount
        self.oldwaitcount = waitcount
        self.wiperspeed = wiperspeed
        self.xoffset = xoffset
        self.yoffset = yoffset      
        self.gridlines = Gridlines(self.xoffset,self.yoffset)
        self.NewGame()

    def NewGame(self):
        for sp in self.sprites():
            sp.kill()
        self.fallwait = 0.0
        self.tilewait = 0.0
        self.fallingblock = False
        self.droppingtiles = False
        self.grid = {}
        # Grid is initialized with the tuple of topleft corner of each cell
        # Points to tiles at locations
        for i in range(16):
            for j in range(12):
                self.grid[(i,j)] = (self.xoffset+tilesize[0]*i,self.yoffset+tilesize[1]*(j-2))
        self.wiper = Wiper(self.wiperspeed,self.xoffset,self.yoffset)
        self.dmanager = DestructionManager()
        self.layoutqueue = LayoutQueue(self.xoffset,self.yoffset,self.color1,self.color2)
        self.score = 0
        self.block = False

    def KeydownHandler(self, key):
        if self.block:
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
                self.oldwaitcount = self.waitcount
                self.waitcount = fastfall

    def KeyupHandler(self, key):
        if key == K_DOWN:
            self.waitcount = self.oldwaitcount

    def CheckBlockCollision(self):
        if pygame.sprite.groupcollide(self.block,self,False,False):
            return True
        elif self.block.x < self.xoffset:
            return True
        elif self.block.x > self.xoffset+griddimensions[0]-2*tilesize[0]:
            return True
        elif self.block.y > self.yoffset+griddimensions[1]-2*tilesize[1]:
            return True
        else:
            return False

    def CheckTileCollision(self,tile):
        if pygame.sprite.spritecollide(tile,self,False):
            return True
        elif tile.rect.bottom > griddimensions[1]+self.yoffset:
            return True
        else:
            return False
        
    # If 2x2 is found, tiles in 2x2 are flagged
    def Check2x2(self,tile):
        loc = tile.grid
        locbelow = (loc[0],loc[1]+1)
        locleft = (loc[0]-1,loc[1])
        locright = (loc[0]+1,loc[1])
        locbelowleft = (loc[0]-1,loc[1]+1)
        locbelowright = (loc[0]+1,loc[1]+1)
        if loc[1] < gridsize[1]-1:
            if not isinstance(self.grid[locbelow],tuple) and \
               self.grid[locbelow].color1 == tile.color1:
                # Check tiles to the left
                if loc[0] > 0 and \
                   not (isinstance(self.grid[locleft],tuple) or \
                        isinstance(self.grid[locbelowleft],tuple)) and \
                        not self.grid[locleft].moved and \
                        not self.grid[locbelowleft].moved and \
                        self.grid[locleft].color1 == tile.color1 and \
                        self.grid[locbelowleft].color1 == tile.color1:
                    tile.Flag(1)
                    self.grid[locleft].Flag(0)
                    self.grid[locbelow].Flag(2)
                    self.grid[locbelowleft].Flag(3)
                    templist = [tile, self.grid[locleft], self.grid[locbelow],\
                                self.grid[locbelowleft]]
                    
                    self.dmanager.add(templist)  # 把标志好的tile加入dmanager
                # Check tiles to the right
                if loc[0] < gridsize[0]-1 and \
                   not (isinstance(self.grid[locright],tuple) or \
                        isinstance(self.grid[locbelowright],tuple)) and \
                        not self.grid[locright].moved and \
                        not self.grid[locbelowright].moved and \
                        self.grid[locright].color1 == tile.color1 and \
                        self.grid[locbelowright].color1 == tile.color1:
                    tile.Flag(0)
                    self.grid[locright].Flag(1)
                    self.grid[locbelow].Flag(3)
                    self.grid[locbelowright].Flag(2)
                    templist = [tile,self.grid[locright],self.grid[locbelow],\
                                self.grid[locbelowright]]
                    self.dmanager.add(templist)    # 把标志好的tile加入dmanager

    def update(self, time):        
        if self.fallingblock:
            if self.fallwait < self.waitcount:
                self.fallwait += time
            else:
                self.block.MoveDown()
                self.fallwait = 0.0
                # Triggers when a block lands
                if self.CheckBlockCollision():
                    # 这块block下降时发生了碰撞，向上返回一层，并且尝试进行 block 中的 tile的下降                
                    self.block.MoveUp()
                    self.fallingblock = False
                    for sp in self.block.sprites():
                        #sp.grid 是一个 (0,0) 的表示位置的元组     
                        if sp.grid[1] <2:
                            self.score = -1   # game over !
                            return
                        self.grid[sp.grid] = sp    # 从一个tuple 改成 一个sprite(tile)
                        self.add(sp)
                        self.droppingtiles = True
                    self.block.empty()    #删除这个sprite group中的所有 sprite
        else:
            # self.fallingblck 为 False , 则从队列中获得一块 block                        
            self.block = Block(self.color1,self.color2, self.layoutqueue.GetNext()\
                               ,griddimensions[0]/2-tilesize[0]+self.xoffset,
                               self.yoffset-tilesize[1]*2, (7,0))
            self.waitcount = self.oldwaitcount
            self.fallingblock = True
                        
        # Animates tiles dropping into gaps
        if self.droppingtiles:
            self.droppingtiles = False
            tocheck = []
            for sp in self.sprites():
                gridbelow = (sp.grid[0],sp.grid[1]+1)
                if gridbelow[1] < gridsize[1] and \
                    isinstance(self.grid[gridbelow],tuple):
                    # 还没到最底层，并且下一层是空格时                    
                    self.swap(sp, gridbelow)     #对调两者
                    sp.moved = True
                    self.droppingtiles = True
                    if sp.flagged:
                        tocheck.extend(self.dmanager.Pardon(sp))
                elif sp.moved:
                    # 刚移动到当前位置，并且已经不能再向下跌落 （停止跌落的tile)
                    tocheck.append(sp)    # 添加到等待检查的 list 中
                    sp.moved = False
            for sp in tocheck:
                self.Check2x2(sp)
        
        self.wiper.update(time)
        scorechange = self.dmanager.update(self.wiper.sprite,self.grid)
        if scorechange:
            self.score += scorechange
            self.droppingtiles = True    # 发生得分，标志 dropingtiles 为 true  继续下降其他可能的 tiles

    def swap(self, tile, loc):
        self.grid[tile.grid] = tile.rect.topleft
        tile.rect.topleft = self.grid[loc]
        tile.grid = loc
        self.grid[loc] = tile

    def draw(self, Surface):
        self.gridlines.draw(Surface)
        pygame.sprite.Group.draw(self,Surface)
        self.block.draw(Surface)
        self.wiper.draw(Surface)
        self.layoutqueue.draw(Surface)

class DestructionManager():
    def __init__(self):
        self.destroyers = []
        self.tilewiper = pygame.Surface((2,tilesize[1]))

    def add(self, sprites):
        added = False
        count = 0
        if self.destroyers:
            for dst in self.destroyers:
                for sp in sprites:
                    if sp in dst:
                        dst.addtiles(sprites)
                        added = True
                        return
                count += 1
        if not added:
            # 没有添加的情况
            self.destroyers.append(TileDestroyer())
            self.destroyers[-1].addtiles(sprites)

    def update(self, wiper, grid):
        score = 0
        for dst in self.destroyers:
            dstscore = dst.update(wiper,grid)
            if dstscore:
                score += dstscore
            if not dst:
                self.destroyers.remove(dst)
        return score

    # Removes tile from its TileDestroyer, along with all other condemned tiles
    # Returns a list of all pardoned tiles
    # 如果tile 存在于某一个 destroyers中 ， 则把它里面的tiles 全部移出来，并且清空这个destroyers，
    # 重新标记成 unfalg 
    def Pardon(self, tile):
        pardoned = []
        for dst in self.destroyers:
            if tile in dst:
                pardoned.extend(dst.sprites())
                self.destroyers.remove(dst)
                for lucky in pardoned:
                    lucky.Unflag()
                return pardoned

    def clear(self):
        self.destroyers[:] = []
                
class TileDestroyer(pygame.sprite.Group):
    def __init__(self):
        pygame.sprite.Group.__init__(self)
        self.maxX = 0
        self.killready = False
        self.kill = False
        self.tilewiper = pygame.Surface((2,tilesize[1]))
        self.score = 0

    def addtiles(self, sprites):
        self.score *= 2
        if sprites:
            self.tilewiper.fill(sprites[0].color1)
        for sprite in sprites:
            self.add(sprite)
            if sprite.rect.right > self.maxX:
                self.maxX = sprite.rect.right
        self.score += len(sprites)

    def update(self, wiper, grid):
        if pygame.sprite.spritecollideany(wiper,self):
            if self.killready:
                self.kill = True
                for sp in self.sprites():
                    sp.image.blit(self.tilewiper,(wiper.rect.left-sp.rect.left,0))
        else:
            if self.kill:
                for sp in self.sprites():
                    grid[(sp.grid)] = sp.rect.topleft
                    sp.kill()
                return self.score
            else:
                self.killready = True
        return 0

# Queue of layouts to use in new blocks
class LayoutQueue():
    def __init__(self,xoffset,yoffset,color1,color2):
        self.xoffset = xoffset
        self.yoffset = yoffset
        self.color1 = color1
        self.color2 = color2
        self.length = 4        
        self.FillQueue()
        self.blocks = []
        for i in range(self.length):
            self.blocks.append(Block(color1,color2,self.layouts[i], \
                                     xoffset-2*tilesize[0]-15, \
                                  yoffset-tilesize[1]+3*tilesize[1]*i))
            for i in range(rnd.randint(0,3)):
                self.blocks[-1].RotateClockwise()

    # Fills Queue
    def FillQueue(self):
        self.layouts = []
        for i in range(self.length):
            self.layouts.append(rnd.randint(1,6))

    # Fills queue with predetermined layouts for testing purposes
    def FillQueueTest(self):
        self.layouts = [1,3,5,1]

    def GetNext(self):
        self.layouts.pop(0)
        choices = [1,2,3,4,5,6]
        for l in self.layouts:
            if l in choices:
                choices.remove(l)
        self.layouts.append(choices[rnd.randint(0,len(choices)-1)])
        layout = self.blocks[0].layout
        self.blocks.pop(0)
        for b in self.blocks:
            b.MoveUp()
            b.MoveUp()
            b.MoveUp()
        self.blocks.append(Block(self.color1,self.color2,self.layouts[-1],\
                              self.xoffset-2*tilesize[0]-15, \
                                 self.yoffset-tilesize[1]+3*tilesize[1]*3))
        for i in range(rnd.randint(0,3)):
            self.blocks[-1].RotateClockwise()
        return layout

    def draw(self,surface):
        for b in self.blocks:
            b.draw(surface)

class Tile(pygame.sprite.Sprite):
    # 一个block由4个tile构成
    #   0    1
    #   3    2
    
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
        self.grid = (0,0)
        self.flagged = False
        self.moved = True

    def MoveLeft(self):
        self.rect.left -= tilesize[0]
        self.grid = (self.grid[0]-1,self.grid[1])

    def MoveRight(self):
        self.rect.left += tilesize[0]
        self.grid = (self.grid[0]+1,self.grid[1])
        
    def MoveDown(self):
        self.rect.top += tilesize[1]
        self.grid = (self.grid[0],self.grid[1]+1)

    def MoveUp(self):
        self.rect.top -= tilesize[1]
        self.grid = (self.grid[0],self.grid[1]-1)

    # Flags tiles according to position in 2x2
    # 0: Top left
    # 1: Top right
    # 2: Bottom right
    # 3: Bottom left
    def Flag(self,pos):
        self.flagged = True
        self.image.fill(self.color1)
        lining = pygame.Surface(flagliningsize)
        inner = pygame.Surface(flaginnersize)
        lining.fill(self.color2)
        inner.fill(self.color1)
        if pos == 0:
            self.image.blit(lining,(2,2))
            self.image.blit(inner,(4,4))
        elif pos == 1:
            self.image.blit(lining,(0,2))
            self.image.blit(inner,(0,4))
        elif pos == 2:
            self.image.blit(lining,(0,0))
            self.image.blit(inner,(0,0))
        else:
            self.image.blit(lining,(2,0))
            self.image.blit(inner,(4,0))

    def Unflag(self):
        self.image = pygame.Surface(tilesize)
        self.image.fill(self.color1)
        lining = pygame.Surface(liningsize)
        lining.fill(self.color2)
        inner = pygame.Surface(innersize)
        inner.fill(self.color1)
        self.image.blit(lining,(2,2))
        self.image.blit(inner,(4,4))
        self.flagged = False

# Returns a random block, tiles arraged
# 0 1
# 3 2
# 一个block 包含4个tile
class Block(pygame.sprite.Group):
    def __init__(self, color1, color2, lay, x, y, grid=(0,0)):
        pygame.sprite.Group.__init__(self)
        if isinstance(lay,int):
            # 6 种砖块中的其中一种                       
            if lay >= 0 and lay <= 6:
                self.layout = layouts[lay]
            else:
                self.layout = layouts[rnd.randint(1,6)]
        elif isinstance(lay,list):
            self.layout = lay
        # x and y are the coordinates of the top left corner of block
##        for i in self.layout:
##            if i == 0:
##                self.add(Tile(color1,color2))
##            else:
##                self.add(Tile(color2,color1))
        self.tiledict = {}   # 0 , 1 , 2 , 3 分别作为key
        # 构造 4 个tile 
        for i in range(4):
            if self.layout[i] == 0:
                temp = Tile(color1,color2)
                self.add(temp)
            else:
                temp = Tile(color2,color1)
                self.add(temp)
            if i == 0:
                temp.rect.left = x
                temp.rect.top = y
                temp.grid = grid
            elif i == 1:
                temp.rect.left = x + tilesize[0]
                temp.rect.top = y
                temp.grid = (grid[0]+1,grid[1])
            elif i == 2:
                temp.rect.left = x + tilesize[0]
                temp.rect.top = y + tilesize[1]
                temp.grid = (grid[0]+1,grid[1]+1)
            else:
                temp.rect.left = x
                temp.rect.top = y + tilesize[1]
                temp.grid = (grid[0],grid[1]+1)
            self.tiledict[i]=temp
        self.x = self.sprites()[0].rect.left
        self.y = self.sprites()[0].rect.top

    def RotateCounterclockwise(self):
        self.tiledict[0].MoveDown()
        self.tiledict[1].MoveLeft()
        self.tiledict[2].MoveUp()
        self.tiledict[3].MoveRight()
        s0 = self.tiledict[0]
        s1 = self.tiledict[1]
        s2 = self.tiledict[2]
        s3 = self.tiledict[3]
        self.tiledict[0] = s1
        self.tiledict[1] = s2
        self.tiledict[2] = s3
        self.tiledict[3] = s0
        temp = self.layout.pop(0)
        self.layout.append(temp)

    def RotateClockwise(self):
        self.tiledict[0].MoveRight()
        self.tiledict[1].MoveDown()
        self.tiledict[2].MoveLeft()
        self.tiledict[3].MoveUp()
        s0 = self.tiledict[0]
        s1 = self.tiledict[1]
        s2 = self.tiledict[2]
        s3 = self.tiledict[3]
        self.tiledict[0] = s3
        self.tiledict[1] = s0
        self.tiledict[2] = s1
        self.tiledict[3] = s2
        temp = self.layout.pop()
        self.layout.insert(0,temp)

    def MoveRight(self):
        x_list = []
        for sp in self.sprites():
            sp.MoveRight()
            x_list.append(sp.rect.left)
        if x_list:
            self.x = min(x_list)

    def MoveLeft(self):
        x_list = []
        for sp in self.sprites():
            sp.MoveLeft()
            x_list.append(sp.rect.left)
        if x_list:
            self.x = min(x_list)

    def MoveDown(self):
        y_list = []
        for sp in self.sprites():
            sp.MoveDown()
            y_list.append(sp.rect.top)
        if y_list:
            self.y = min(y_list)

    def MoveUp(self):
        y_list = []
        for sp in self.sprites():
            sp.MoveUp()
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
        
