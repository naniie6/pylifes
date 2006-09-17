# coding:utf-8
from lifebase import *
from random import randrange

'''
可以使用的API：

    begin_moving(target)
    移动到指定位置,target为tuple
    stop_moving()
    停止移动
    scan()->list
    搜索视野范围内的动物，返回动物状态列表，视野半径由sight指定
    scanfor(animal_state)->animal_state
    返回指定animal最新状态，如果该animal消失(比如离开视野范围、死亡等)则返回None
'''

class TestAni(Animal):
    '''
    移动到随机位置，到达后移动到新的随机位置，如此反复以至无穷。
    '''
    def initialize(self):
        temp = (2000,2000)  
        self.begin_moving(temp)
    def on_idle(self):
        pass
    def on_move_completed(self,sender,args):
        self.trac('arrived target:%s' % (str(sender.position)))

class MyAni(Animal):
    '''
    移动到随机位置，到达后移动到新的随机位置，如此反复以至无穷。
    '''
    def initialize(self):
        pass
    def on_idle(self):
        if not self.ismoving:
            temp = (randrange(world_width),randrange(world_height))  
            self.trac('moving from %s to %s speed:%d' % (str(self.position),temp,self.velocity))
            self.begin_moving(temp)
    def on_move_completed(self,sender,args):
        self.trac('arrived target:%s' % (str(sender.position)))

class Animal1(Animal):
    '''
    从某个点出发，移动到随机位置然后返回出发点，再移动到新的随机位置，反复至无穷
    '''
    def initialize(self):
        self.trac('initializing %s,%s,%f,%f'%(self.sprite_name,self.color,self.maxv,self.sight))
        self.start = self.position
        self.flag = True
    def on_idle(self):
        if not self.ismoving:
            if self.flag:
                self.end = (randrange(world_width),randrange(world_height))
                self.begin_moving(self.end)
                self.trac('moving to %s speed:%d' % (str(self.end),self.velocity))
            else:
                self.begin_moving(self.start)
                self.trac('moving back %s speed:%d' % (self.start,self.velocity))
    def on_move_completed(self,sender,args):
        if self.flag:self.flag=False
        else:self.flag=True
        self.trac('arrived target:%s' % str(sender.position))

class LazyAnimal(Animal):
    '''
    不动。不停监视自己视野范围，一旦有动物进入视野范围立即跟上去，直到跟丢为止。
    '''
    def initialize(self):
        self.color = 'blue'
        self.animal = None #当前正在跟踪的动物
        self.trac('initializing')
        self.sprite_name = 'light'
    def on_idle(self):
        if not self.ismoving:
            if self.animal:
                self.follow()
            else:
                self.follow_another()
        else:
            temp = self.scanfor(self.follow)
            if not temp:
                self.trac('lost %s' % str(self.follow.name))
                self.stop_moving('lost target')
            else:
                pos = temp.position
                pos += (temp.v[0],temp.v[1])
                self.trac('target:%s;distance:%d;speed:(%d, %d)' % (temp.name, self.distance, self.velocity, temp.velocity))
                self.reset_target(pos)
    def on_move_completed(self,sender,args):
        self.trac('stopped for %s' % args.reason)
    def follow_another(self):
        '监视，如果有动物进入视野立即更上去，不跟自己人'
        lifes = [ l for l in self.scan() if not isinstance(i, LazyAnimal) ]
        #print 'lazy scaned',len(lifes)
        if lifes:
            self.trac('scaned %d lifes ' % len(lifes))
            self.follow = lifes[0]
            self.trac('follow the first one %s (%d, %d)' % (self.follow.name,self.follow.position[0],self.follow.position[1]))
            self.begin_moving(self.follow.position)
    def follow(self):
        '尝试跟踪当前动物，如果已跟丢，则寻找其他动物'
        temp = self.scanfor(self.follow)
        if not temp:
            self.follow_another()
        else:
            pos = temp.position
            pos += (temp.v.x,temp.v.y)
            self.begin_moving(pos)

class AttackAnimal(Animal):
    def initialize(self):
        self.trac('initializing')
    def on_idle(self):
        ani = self.scan()
    def on_move_completed(self):
        pass

if __name__ == '__main__':
    import sys,kernel
    engine = kernel.engine
    if len(sys.argv)>1 and sys.args[1]=='-q':
        engine.init_logs() # no pygame interface and use log instead.
    else:
        engine.init_pygame((800,600))
    world_width = engine.world_width
    world_height = engine.world_height
    for i in range(100):
       engine.add_life(MyAni(name='wukong%d' % i,position=(randrange(world_width),randrange(world_height)),maxv=15))
    for i in range(100):
       engine.add_life(Animal1(name='bajie%d' % i,x=randrange(world_width),y=randrange(world_height),maxv=randrange(1,40)))
    for i in range(100):
       engine.add_life(LazyAnimal(name='lazy%d' % i,position=(randrange(world_width),randrange(world_height)),maxv=7,sight=60))

    engine.run()
