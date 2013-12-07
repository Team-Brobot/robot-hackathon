import rg

class Robot(object):
    def act(self, game):
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
        return['move', rg.toward(self.location, target['location'])]
                
                
