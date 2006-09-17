# coding:utf-8
from kernel import *
import stackless
#from render import Normal,Light
import math
import os


def update_move(who,target):
    '''每一次轮转更新正在移动的动物的坐标 并判断已经是否到达目的地
     返回True可以使当前action被删除'''
    if not who.ismoving:
        '调用了stop_moving函数终止'
        who.ev_move = MoveCompletedArg(None,who.velocity,'stopped') 
        return True
    temp = engine.timepass*TimeUnit #timepass为一次轮转花费的时间，配合TimeUnit使用 不管机器速度如何都可使世界以一致的速度进行
    oldpos = who.tilepos
    who.position = t_add(who.position,t_mul(who.v,(temp,temp)))
    #who.gridpos = t_div(who.position,(tile_width,tile_height))  #更新方块坐标
    who.tilepos = t_div(who.position,(engine.tile_width,engine.tile_height))
    engine.update_tilepos(who,oldpos)  #
    divpos = t_sub(who.position,target)
    who.distance = math.sqrt(divpos[0]**2+divpos[1]**2)
    if who.distance<who.velocity:
        who.position = target
        who.ev_move = MoveCompletedArg(target,who.velocity,'arrived')
        if debug:print 'move complete',target,who.velocity
        return True
    else:return False
def update_eat(who,target):
    pass
def update_attack(who,target):
    pass

UPDATE_DICT = {'move':update_move,'eat':update_eat,'attack':update_attack}

class ResultEvent(object):
    'engine通过这个来通知animal一些事件 animal不停查询此对象状态'
    __slots__=('MoveCompleted','EatCompleted','AttackCompleted')
    def __init__(self):
        self.MoveCompleted = None
        self.EatCompleted=None
        self.AttackCompleted=None

class Action:
    def __init__(self,who,ac_name,*args):
        self.who = who
        self.name = ac_name
        self.action = UPDATE_DICT[ac_name]
        self.args = args
    def update(self):
        return self.action(self.who,*self.args)
    def __repr__(self):
        return '%s %s %s' % (self.who.name,self.name,self.args)

class ActionCompletedArg(object):
    __slots__=('reason')
    def __init__(self,reason):
        self.reason=reason

class MoveCompletedArg(ActionCompletedArg):
    __slots__=('pos','speed')
    def __init__(self,pos,speed,reason):
        ActionCompletedArg.__init__(self,reason)
        self.pos=pos
        self.speed = speed

class Animal(object):
    def __init__(self,**kw):
        self.color = 'red'
        self.position = (0.0,0.0)
        self.maxv = 0.0
        self.direction = 0.0
        self.sight = 0
        self.__dict__.update(kw)

        self.velocity = 0.0
        self.v = (0.0,0.0)
        self.tilepos = t_div(self.position,(engine.tile_width,engine.tile_height))
        self.age = 0
        self.ev_move, self.ev_eat, self.ev_attack = None,None,None
    #self.events= [self.ev_move, self.ev_eat, self.ev_attack]
        self.ac_move,self.ac_eat,self.ac_attack = None,None,None
    #self.actions = [self.ac_move, self.ac_eat, self.ac_attack]
        self.sprite_name = 'normal'
        if engine.log:
            self.logfile = open(os.path.join(engine.logdir,'%s.txt' % self.name),'w')
        else:
            self.logfile = None

        self.initialize()
        
    ismoving = property(lambda self:self.ac_move!=None)
    iseating = property(lambda self:self.ac_eat!=None)

    def _main(self):
        '''main loop'''
        while True:
            self.onLoad()
            if self.ev_move:
                self.onMoveCompleted(self.ev_move)
            self.onIdle()
            stackless.schedule()

    def begin_moving(self,target):
        '''calculate the speed, direction,etc.
        进行一些几何运算 计算运动速度、方向 
        '''
        if self.ismoving:
            self.trac('is already moving')
            return
        divpos = t_sub(target,self.position)
        self.distance = math.sqrt(divpos[0]**2+divpos[1]**2)
        if self.distance>0:
            self.direction = math.acos(divpos[0] / self.distance)
            if divpos[1] < 0.:
                self.direction *= -1
            self.velocity = min(self.distance,self.maxv)
        if self.velocity>0:
            self.v = (self.velocity*math.cos(self.direction), self.velocity*math.sin(self.direction))
            #self.moving = True
            ac = Action(self,'move',target)
            self.ac_move = ac
            return ac

    def stop_moving(self, reason):
        self.ac_move = None
        arg = MoveCompletedArg(self.position, self.velocity, reason)
        self.onMoveCompleted(arg)
    def reset_target(self,target):
        '''
        recalculate the speed, direction ,etc.
        调整方向 重新计算方向距离速度等参数
        '''
        if not self.ismoving:return
        divpos = t_sub(target,self.position)
        self.distance = math.sqrt(divpos[0]**2+divpos[1]**2)
        if self.distance>0:
            self.direction = math.acos(divpos[0] / self.distance)
            if divpos[1] < 0.:
                self.direction *= -1
            self.velocity = min(self.distance,self.maxv)
        if self.velocity>0:
            self.v = (self.velocity*math.cos(self.direction),self.velocity*math.sin(self.direction))
        self.ac_move.target=target

    def begin_attack(self,target):
        pass
    def stop_attack(self):
        pass

    def begin_eat(self,target):
        pass
    def stop_eat(self):
        pass
    
    def scan(self):
        '搜索视野范围内其他生物'
        return engine.scan(self)
    def scanfor(self,life):
        '在视野范围内搜索指定生物'
        return engine.scanfor(self,life)

    def copy_state(self):
        '返回动物当前可被其他动物观察到的状态'
        return AnimalState(self.name,self.position,self.direction,self.velocity,self.v)

    def trac(self,*msgs):
        if self.logfile:
       	    self.logfile.write('%s\n' % ' '.join(msgs))
        #print self.name,msg

    def onLoad(self):
        if debug:print self.name,'onLoad'
        self.on_load()
    def onIdle(self):
        if debug:print self.name,'onIdle'
        self.on_idle()
    def onMoveCompleted(self,arg=None):
        if debug:print self.name,'onMoveCompleted'
        #self.moving = False
        self.velocity=0
        self.move_action = None
        self.ev_move = None
        self.on_move_completed(self,arg)
    def onEatCompleted(self,arg=None):
        pass
    def onAttackCompleted(self,arg=None):
        pass

    def on_load(self):pass
    def on_idle(self):pass
    def on_move_completed(self, sender, arg=None):pass
    def on_eat_completed(self):pass
    def on_attack_completed(self):
        pass

class Plant:
    def __init__(self,**kw):
        self.sprite_name = ''
        self.enegry = 0
        self.__dict__.update(kw)

class AnimalState(object):
    'properties of animals exposed to other animals'
    __slots__=('_name','_position','_direction','_velocity','_v')
    def __init__(self,name,pos,dir,vel,v):
        self._name = name
        self._position = pos
        self._direction = dir
        self._velocity = vel
        self._v = v
    name=property(lambda self:self._name)
    position=property(lambda self:self._position)   
    direction=property(lambda self:self._direction) 
    velocity=property(lambda self:self._velocity)
    v=property(lambda self:self._v) 

