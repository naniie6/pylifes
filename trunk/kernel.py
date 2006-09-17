# coding:utf-8
import stackless
from stackless import tasklet as Tasklet
from stackless import channel as Channel
from threading import Timer
from time import clock
from utils import *
import math

debug = 0  
TimeUnit = 8.0 #用来统一控制世界运行速度

class GameEngine:
    def __init__(self):
        self._lifes = []     # 所有动物列表     方便对动物进行遍历
        self._lifes_dict = {}     # 动物名:动物  方便根据名称查找动物
        self._tile_lifes = {} # (tile_x,tile_y):[动物列表]  方便根据tile坐标查找动物
        self.timepass = 0.0  # 和 TimeUnit 一起使世界以一致的速度运行(不管机器速度如何)
        self.now = clock()   # 获取当前时间 用来计算 self.timepass

        self.log = False
        
        self.screen_width = 1024
        self.screen_height= 768
        self.world_width = 10*512
        self.world_height = 10*256
        self.tile_width = 512
        self.tile_height = 256

        # kernel "processes":
        Tasklet(self._do_actions)()

    def init_pygame(self, window_size=()):
        import render
        if window_size:
            render.window_size = window_size
        self.render = render.Render(self)
        Tasklet(self.render.initialize)()
        Tasklet(self.render.loop)()

	def init_logs(self, dirname='logs'):
		import os
		self.log = True
		self.logdir = 'logs'
		if os.path.exists(self.logdir):
			os.mkdir(self.logdir)

    def add_life(self,life):
        if debug:print 'add life',life.name
        self._lifes.append(life)
        self._lifes_dict[life.name]=life
        if not self._tile_lifes.has_key(life.tilepos):
            self._tile_lifes[life.tilepos]=[life]
        else:
            self._tile_lifes[life.tilepos].append(life)
        Tasklet(life._main)()

    def get_life(self,name):
        if self._lifes_dict.has_key(name) and self._lifes_dict[name]:
            return self._lifes_dict[name]

    def _do_actions(self):
        while True:
            temp = clock()
            self.timepass = temp-self.now
            self.now = temp
            print self.timepass

            for l in self._lifes:
                if l.ac_move:
                    if l.ac_move.update():
                        l.ac_move = None
                if l.ac_eat:
                    if l.ac_eat.update():
                        l.ac_eat= None
                if l.ac_attack:
                    if l.ac_attack.update():
                        l.ac_attack= None
            stackless.schedule()

    def update_tilepos(self,who,oldpos):
        '修改 _tile_lifes 中对动物所在 tile 位置的记录'
        if who.tilepos!=oldpos:
            if oldpos in self._tile_lifes:
                self._tile_lifes[oldpos].remove(who)
            if who.tilepos in self._tile_lifes:
                self._tile_lifes[who.tilepos].append(who)
            else:
                self._tile_lifes[who.tilepos]=[who]

    def run(self):
        stackless.run()

    def scan(self,life):
        '搜索动物视野范围内动物列表'
        left = max( int( ( life.position[0] - life.sight ) / self.tile_width ), 0)
        right = max( int( ( life.position[0] + life.sight) / self.tile_width ), 0)
        top = max( int( ( life.position[1] - life.sight ) / self.tile_height ), 0)
        bottom = max( int( ( life.position[1] + life.sight ) / self.tile_height ), 0)
        all = []
        for i in range(left,right+1):
            for j in range(top,bottom+1):
                if (i,j) in self._tile_lifes:
                    all += self._tile_lifes[(i,j)]
        list = []
        for l in all:
            if within_sight(life,l):
                if debug:print l.name,'is scanned',l.gridpos
                list.append(l.copy_state())
        return list

    def scan_plants(self, life):
        pass

    def scanfor(self,who,lifestate):
        life = self.get_life(lifestate.name)
        if within_sight(who,life):
            return life.copy_state()

engine = GameEngine()
