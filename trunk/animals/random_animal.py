# coding: utf-8
from lifebase import Animal, engine
from random import randrange

class RandomAni(Animal):
    '''
    move to a random positiom, then move to another random position, and so on ...
    移动到随机位置，到达后移动到新的随机位置，如此反复以至无穷。
    '''
    def initialize(self):
        pass

    def on_idle(self):
        if not self.ismoving:
            temp = (randrange(engine.world_width),randrange(engine.world_height))  
            self.trac('moving from %s to %s speed:%d' % (str(self.position),temp,self.velocity))
            self.begin_moving(temp)

    def on_move_completed(self,sender,args):
        self.trac('arrived target:%s' % (str(sender.position)))


def make_animals():
    return [RandomAni(name='wukong%d' % i,
               position=(randrange(engine.world_width),randrange(engine.world_height)),
               maxv=15)
           for i in range(50)]
