# DodgerObject - base class for Baddie and Goodie
# Removes duplication of MIN_SIZE/MAX_SIZE/MIN_SPEED/MAX_SPEED constants
# and provides circle-based collision detection

import random

class DodgerObject:
    MIN_SIZE = 10
    MAX_SIZE = 40
    MIN_SPEED = 1
    MAX_SPEED = 8

    def _init_size(self):
        """Initialize random size and derived radius. Call from subclass __init__."""
        self.size = random.randrange(DodgerObject.MIN_SIZE, DodgerObject.MAX_SIZE + 1)
        self.radius = self.size / 2

    def _get_center(self):
        """Return (cx, cy) — center of this object based on current x, y."""
        return self.x + self.radius, self.y + self.radius

    def collide(self, player_cx, player_cy, player_radius):
        """Circle-based collision: True if this object overlaps with the player circle."""
        cx, cy = self._get_center()
        dist_sq = (cx - player_cx) ** 2 + (cy - player_cy) ** 2
        return dist_sq < (self.radius + player_radius) ** 2

    def draw(self):
        self.image.draw()
