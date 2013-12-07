
import random

THE_SEAL = 10

class Robot(object):
    'Drunkenly performs a random action.'
    
    def __init__(self):
        self.age = 0
    
    @property
    def up(self):
        return self.x, self.y+1
    
    @property    
    def down(self):
        return self.x, self.y-1
    
    @property
    def left(self):
        return self.x-1, self.y
    
    @property
    def right(self):
        return self.x+1, self.y
    
    @property
    def x(self):
        return self.location[0]
    
    @property
    def y(self):
        return self.location[1]
    
    def stagger(self, game):
        x,y = [self.up, self.down, self.right, self.left][random.randint(0,4)]
        return ['move', (x,y)]
    
    def fall_down(self, game):
        return ['guard']
    
    def brawl(self, game):
        targets = []
        for location in (self.up, self.down, self.left, self.right):
            bot = game['robots'].get(location)
            if bot and bot.player_id != self.player_id:
                targets.append(bot)
        if not targets:
            return stagger(game)
        target = min(targets, key=lambda x: x['hp'])
        return ['attack', target['location']]
        
    def piss_myself(self, game):
        return ['suicide']
    
    def act(self, game):
        self.age += 1

        # check if we have pissed ourselves
        if random.randint(THE_SEAL,1000) < self.age:
            return self.piss_myself(game)
        
        return random.choice([self.stagger, 
                            self.stagger, self.stagger, 
                            self.brawl, self.brawl, self.fall_down])(game)
        
        
        