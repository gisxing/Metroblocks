Metroblocks
by
Andrew Quintanilla
Makoa Fautua
Ray Liang

Python 3.2.3, pygame

Gameplay:
Form 2x2s of one solid color to be cleared by the wiper.
Game over if the block can't land in the grid.

Controls:
x - Rotate block clockwise
z - Rotate block counterclockwise
Left arrow - Move block left
Right arrow - Move block right
Down arrow - Accelerate block down
Esc - Toggle Menu

Any .ogg files you have in the same directory will be played in a random order.

------------------------------------------------------
整理学习笔记

可以作为一个消除类游戏的模板进行学习。 

class Tile 是一个基本的sprites类，作为一个方格的最基本方块
class Block 则是包含4个 tile 的类 。
通过一个blockmanager的类的实例，管理一个包含tileDestroyers的实例的数组。每一个tileDestroyers都是独立的一组已经‘连接’在
一起的准备被消除的tile集合。 
通过判断wiper是否和某destroyers中的sprites发生碰撞，触发予以消除。

作为整个版图，用grid{} 记录，用座标作为key , 初始时存放座标信息的元祖， 被tile占据的时候，则存放这个tile的实例。所以会
看到不少isinstance的判断。 

Check2X2 那个函数就是检查是否构成一整块2X2的单元，是的话则添加入一个destroyer中。 

blockqueue是管理4块队列中的方块 。 放于左侧。 

方块的下落有一个小的counter计数，和delta timer累计作比较，看是否需要降落。 而tile是否会产生下落，则是遍历tiles， 看是否
满足下落的条件，下落时候准星相应的判断逻辑。 
