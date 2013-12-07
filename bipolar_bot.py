
import rg

class Robot(object):
    def act(self, game):
        if self.hp < (rg.settings.robot_hp * 0.5):
            return self.coward(game)
        else:
            return self.bully(game)
    
    def bully(self, game):
        all_bots = [bot for bot in game['robots'].values() if bot['player_id'] != self.player_id]
        
        min_dist = rg.dist(self.location, all_bots[0]['location'])
        close_bots = [all_bots[0]]
        
        for bot in all_bots[1:]:
            distance = rg.dist(self.location, bot['location'])
            if distance == min_dist:
                # this bot is the same distance as the (known) closest bot
                close_bots.append(bot)
            elif distance < min_dist:
                # this bot is closer than the (known) closest bots, make it
                # the closest bot
                min_dist = distance
                close_bots = [bot]
        
        # by this point, we should have a list of the closest robot(s)
        target = min(close_bots, key=lambda x: x['hp'])
        if min_dist <= 1:
            return ['attack', target['location']]
        return ['move', rg.toward(self.location, target['location'])]
        
    def coward(self, game):
        # First, make sure you are not in a spawn point
        if 'spawn' in rg.loc_types(self.location):
            #Move out of spawn point!
            return ['move', rg.toward(self.location, rg.CENTER_POINT)]
        
        # second, make sure you are not next to an enemy
        locations = rg.locs_around(self.location, filter_out=('invalid', 'obstacle'))
        enemies = []
        for l in locations:
            bot = game['robots'].get(l)
            if bot and bot['player_id'] != self.player_id:
                enemies.append(bot)
        if enemies:
            #Find a safe place!
            for l in locations:
                if not game['robots'].get(l):
                    # unoccupied spot!
                        return ['move', l]
            else:
                # surrounded!
                if self.hp < rg.settings.attack_range[1] * len(enemies):
                    return ['suicide']
                else:
                    target = min(enemies, key=lambda x: x['hp'])
                    return ['attack', target['location']]
        # finally, just chill out.
        return ['guard']