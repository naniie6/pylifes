# coding:utf-8
# This code is in the Public Domain
# -- richard@mechanicalcat.net

# import every damn thing we can find...
import sys, random
import pygame
import pygame.draw
from pygame.locals import *
from utils import *

# 定义地图砖块(tile)
tile_coords = {
    'a': (0,0),
    '.': None,
}

class Map:
    def __init__(self, render, map, tiles, view):
        self.render = render
        self.scrolled = False #记录是否滚动过 留着 也许能对画面渲染优化有点帮助
        self.tiles = tiles    #包括所有 tiles 位图的pygame.image对象
        self.view = view      #将地图画到该 surface 上
        self.tile_width=512   #砖块大小
        self.tile_height=256
        l = [line.strip() for line in open(map).readlines()]
        self.map = [[None]*len(l[0]) for j in range(len(l))]
        self.viewpos = (0,0)  #当前屏幕左上角在地图中的坐标
        self.world_width = len(l[0])*self.tile_width
        self.world_height = len(l)*self.tile_height
        
        for i in range(len(l[0])):
            for j in range(len(l)):
                tile = l[j][i]
                tile = tile_coords[tile]
                if tile is None:
                    continue
                elif isinstance(tile, type([])):
                    tile = random.choice(tile)
                cx, cy = tile
                self.map[j][i] = (cx, cy)

    def set_viewpos(self,pos):
        if self.viewpos!=pos:
            self.scrolled = True
            self.viewpos=pos
        else:
            self.scrolled = False

    def get_viewpos(self):return self.viewpos

    def draw(self,surface=None):
        ' 默认将屏幕上需要显示的部分地图画到 view 上 '
        if surface:temp=surface
        else:temp = self.view
        sx, sy = self.view.get_size()
        for i,j in self.get_range(): 
            try:
                tile = self.map[j][i]
            except IndexError:
                continue
            if not tile:
                continue
            cx, cy = tile
            temp.blit(self.tiles, (i*self.tile_width-self.viewpos[0], j*self.tile_height-self.viewpos[1]), (cx, cy, self.tile_width, self.tile_height))

    def get_range(self):
        '''返回需要在屏幕上显示的tile坐标的列表
        '''
        sw, sh = self.view.get_size()
        tempx = self.viewpos[0]%self.tile_width
        startx = self.viewpos[0]/self.tile_width
        temp = sw-(self.tile_width-tempx)
        stopx = startx+temp/self.tile_width+2

        tempy = self.viewpos[1]%self.tile_height
        starty = self.viewpos[1]/self.tile_height
        temp = sw-(self.tile_height-tempy)
        stopy = starty+temp/self.tile_height+2
        return [(x,y) \
                    for x in range(startx, stopx) \
                    for y in range(starty, stopy)]

    def limit(self, pos):
        '''限制 viewpos 不能到地图外面去'''
        x, y = pos
        # easy
        x = max(x, 0)
        y = max(y, 0)

        return (min(x,self.world_width-self.render.screen_width),min(y,self.world_height-self.render.screen_height))

class MiniMap:
    def __init__(self,engine,render,map,rect):
        self.engine = engine
        self.render = render
        self.image = pygame.Surface([rect.width,rect.height])
        self.image.fill(pygame.color.THECOLORS['green'])
        self.map = map
        self.rect = rect
        self.scalex = self.map.world_width/self.rect.width
        self.scaley = self.map.world_height/self.rect.height
        self.winw = int(render.screen_width/self.scalex)
        self.winh = int(render.screen_height/self.scaley)
    def contain(self,pos):
        return pos[0]<self.rect.right and pos[0]>self.rect.left and pos[1]<self.rect.bottom and pos[1]>self.rect.top
    def mouse(self,pos):
        pos = t_sub(pos,(self.rect.left,self.rect.top))
        self.map.set_viewpos(self.map.limit(t_mul((self.scalex,self.scaley),(pos[0]-self.winw/2,pos[1]-self.winh/2))))
    def draw(self,surface):
        self.image.fill(pygame.color.THECOLORS['green'])
        for life in self.engine._lifes:
            tempcolor = pygame.color.THECOLORS[life.color]
            self.image.fill(tempcolor,[life.position[0]/self.scalex,life.position[1]/self.scaley,1,1])

        pygame.draw.rect(self.image,pygame.color.THECOLORS['blue'],\
                Rect(self.map.viewpos[0]/self.scalex,self.map.viewpos[1]/self.scaley,self.winw,self.winh),1)
        return surface.blit(self.image,self.rect)
        
def main():
    pygame.init()
    win = pygame.display.set_mode((800, 600))

    map = Map('media\\map.txt', 'media\\tiles.bmp', win, None)
    viewpos = (0,0)
    move = False
    clock = pygame.time.Clock()
    sx, sy = win.get_size()
    while 1:
        event = pygame.event.poll()
        while event.type != NOEVENT:
            if event.type in (QUIT, KEYDOWN):
                sys.exit(0)
            elif event.type == MOUSEBUTTONDOWN:
                x, y = viewpos
                dx, dy = event.pos
                x += dx - sx/2
                y += dy - sy/2
                viewpos = (max(x,0), max(y,0))
                #print viewpos
                move = True
            event = pygame.event.poll()
        win.fill((0,0,0))
        map.set_viewpos(viewpos)
        map.draw()
        pygame.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    main()
