"""Contains code for making the aliens work"""

import pyglet


class Alien(object):
    """Handles all of the joys of being an alien"""

    image = pyglet.resource.image("images/invader.png")
    strafe_step = 50
    strafe_delay = 1

    def __init__(self, window, x_pos):
        """Set up a new alien"""
        self.sprite = pyglet.sprite.Sprite(
            Alien.image,
            x=x_pos,
            y=window.height - 20)

        self.head_right = True

        pyglet.clock.schedule_interval(self.strafe, Alien.strafe_delay)

    def strafe(self, delta_time):
        """Do that characteristic lurch across the screen"""
        if self.head_right:
            self.sprite.x += Alien.strafe_step * delta_time
        else:
            self.sprite.x -= Alien.strafe_step * delta_time

    def draw(self):
        """Draw the sprite"""
        self.sprite.draw()

    def lurch(self):
        """Lurch forward, towards the player"""
        self.sprite.y -= self.sprite.height / 2
