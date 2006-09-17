# coding: utf-8
import pygame
from pygame import sprite
from pygame.locals import *
import os
import sys
import math
import stackless
from tilemap import Map,MiniMap

def load_image(name):
    path = os.path.join('media', name)
    return pygame.image.load(path).convert()

images = {}
def preload():
    images['world'] = load_image('world.png')
    images['normal'] = load_image('normal.gif')
    images['light'] = load_image('light.gif')
    images['tiles'] = load_image('tiles.bmp')

window_size = (800,600)

class Render:
    def __init__(self,engine):
        self.engine = engine

    def initialize(self):
        pygame.init()
        self.screen = pygame.display.set_mode(window_size)
        self.screen_width=self.screen.get_rect().width
        self.screen_height=self.screen.get_rect().height
        preload()
        self.map = Map(self,'media/map.txt', images['tiles'],self.screen) 
        temp_width = 150
        temp_height = 150
        self.minimap = MiniMap(self.engine,self,self.map,Rect([self.screen.get_rect().width-temp_width,0,temp_width,temp_height]))
        self.world = images['world']
        self.screen.blit(self.world,(0,0))
        #self.clock = pygame.time.Clock()
        pygame.time.set_timer(USEREVENT, 1000)
        self.font = pygame.font.Font('media/freesansbold.ttf', 40)
        self.timer = pygame.time.Clock()

        self.engine.screen_width = self.screen.get_rect().width
        self.engine.screen_height = self.screen.get_rect().height
        self.engine.world_width = self.map.world_width
        self.engine.world_height = self.map.world_height
        self.engine.tile_width = self.map.tile_width
        self.engine.tile_height = self.map.tile_height

        for l in self.engine._lifes:
            l.sprite = get_sprite(l.sprite_name) (l)

    def loop(self):
        fps = 0
        message = None
        viewpos = (0,0)
        sx, sy = self.screen.get_size()
        mapsurf = pygame.Surface(self.screen.get_size())
        fresh = True
        group = pygame.sprite.RenderUpdates()
        while True:
            self.timer.tick()
            mousex,mousey = pygame.mouse.get_pos()
            mouse_in_minimap = self.minimap.contain((mousex,mousey))
            border = 100
            cond1 = mousex<border
            cond2 = mousey<border and not mouse_in_minimap
            cond3 = mousex>self.screen.get_rect().width-border and not mouse_in_minimap
            cond4 = mousey>self.screen.get_rect().height-border
            moveunit = 20
            x,y = self.map.get_viewpos()
            if cond1:
                x-=moveunit
            elif cond2:
                y-=moveunit
            elif cond3:
                x+=moveunit
            elif cond4:
                y+=moveunit
            self.map.set_viewpos(self.map.limit((x,y)))
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN and event.key==K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    if mouse_in_minimap:
                        self.minimap.mouse(event.pos)
                    else:
                        x, y = self.map.get_viewpos()
                        dx, dy = event.pos
                        x += dx - sx/2
                        y += dy - sy/2
                        viewpos = self.map.limit((x,y))
                        self.map.set_viewpos(viewpos)
                elif event.type == USEREVENT:
                    fps = self.timer.get_fps()
            s = " fps: %.2f pos: %s" % (fps,str(self.map.get_viewpos()))
            message = self.font.render(s, 0, (255,255,255)).convert()      

            self.map.draw()
             
            for pos in self.map.get_range():
                if self.engine._tile_lifes.has_key(pos):
                    for life in self.engine._tile_lifes[pos]:
                        sprite = life.sprite
                        img = sprite.image
                        temp = img.get_rect().move(life.position[0]-self.map.viewpos[0],life.position[1]-self.map.viewpos[1])
                        if math.cos(life.direction) < 0:
                            img = pygame.transform.flip(img, 1, 0)
                        self.screen.blit(img,temp)
            self.screen.blit(message,(0,0))
            self.minimap.draw(self.screen)
            pygame.display.update()

            stackless.schedule()

class Style(sprite.Sprite):
    def __init__(self,life):
        sprite.Sprite.__init__(self)
        self.life = life
        self.image = images[self.imagename]
        self.rect = self.image.get_rect()
    def update(self,screen,viewpos):
        self.rect = self.rect.move(self.life.position[0]-viewpos[0],self.life.position[1]-viewpos[1])

class Normal(Style):
    def __init__(self,life):
        self.imagename = 'normal'
        Style.__init__(self,life)

class Light(Style):
    def __init__(self,life):
        self.imagename = 'light'
        Style.__init__(self,life)


SPRITES = {'normal':Normal,'light':Light}
def get_sprite(sprite_name):
    if sprite_name:
        return SPRITES[sprite_name]
    else:
        return Normal
