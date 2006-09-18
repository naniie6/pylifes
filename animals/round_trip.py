# coding: utf-8
from lifebase import Animal, engine
from random import randrange

class RoundTripAni(Animal):
    '''
    set out from some position, then move to a random position, 
    then back to the start position, then another random position, and so on...
    从某个点出发，移动到随机位置然后返回出发点，再移动到新的随机位置，反复至无穷
    '''
    def initialize(self):
        self.trac('initializing %s,%s,%f,%f'%(self.sprite_name,self.color,self.maxv,self.sight))
        self.start = self.position
        self.flag = True

    def on_idle(self):
        if not self.ismoving:
            if self.flag:
                self.end = (randrange(engine.world_width),randrange(engine.world_height))
                self.begin_moving(self.end)
                self.trac('moving to %s speed:%d' % (str(self.end),self.velocity))
            else:
                self.begin_moving(self.start)
                self.trac('moving back %s speed:%d' % (self.start,self.velocity))

    def on_move_completed(self,sender,args):
        if self.flag:self.flag=False
        else:self.flag=True
        self.trac('arrived target:%s' % str(sender.position))


def make_animals():
    return [RoundTripAni(name = 'bajie%d' % i,
                    position = (randrange(engine.world_width), randrange(engine.world_height)),
                    maxv=randrange(1,40))
           for i in range(50)]
