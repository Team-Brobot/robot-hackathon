import rg


class Robot(object):
    "Cowardly runs away from enemies and spawn points"
    def act(self, game):
        
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