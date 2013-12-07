import random

import rg


class Brobot(object):

    @property
    def good_locs(self):
        return rg.locs_around(
            self.location,
            filter_out=('invalid', 'obstacle', 'spawn')
        )

    @property
    def any_locs(self):
        return rg.locs_around(
            self.location,
            filter_out=('invalid', 'obstacle')
        )

    @property
    def adjacent_friends(self):
        return [bot for bot in self.adjacent_bots
                if bot.player_id == self.player_id]

    @property
    def adjacent_enemies(self):
        return [bot for bot in self.adjacent_bots
                if bot.player_id != self.player_id]

    @property
    def adjacent_bots(self):
        return [bot for loc, bot in self.game.robots.items()
                if loc in rg.locs_around(self.location)]

    def away_from(self, current_loc, dest_loc):
        x, y = current_loc
        toward_loc = rg.toward(current_loc, dest_loc)
        dx = toward_loc[0] - x
        dy = toward_loc[1] - y
        return (x - dx, y - dy)

    def move_away_from(self, bot):
        return ['move', self.away_from(self.location, bot.location)]

    def in_spawn(self, bot):
        return 'spawn' in rg.loc_types(bot.location)

    def move_out_of_spawn_point(self):
        if not self.good_locs:
            return ['move', random.choice(self.any_locs)]
        else:
            return ['move', random.choice(self.good_locs)]

    def act(self, game):
        self.game = game
        if self.in_spawn(self):
            return self.move_out_of_spawn_point()

        if any([self.in_spawn(friend) for friend in self.adjacent_friends]):
            return self.move_away_from(friend)

        return ['guard']


Robot = Brobot
