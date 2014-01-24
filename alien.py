"""Contains code for making the aliens work"""

import pyglet


class Alien(object):
    """Handles all of the joys of being an alien"""

    image = pyglet.resource.image("images/invader.png")
    explosion = pyglet.resource.image("images/explosion.png")
    strafe_step = 50
    strafe_delay = 1
    lurch_delay = 5

    def __init__(self, window, x_pos):
        """Set up a new alien"""
        self.sprite = pyglet.sprite.Sprite(
            Alien.image,
            x=x_pos,
            y=window.height - 20)

        self.head_right = True

        pyglet.clock.schedule_interval(self.strafe, Alien.strafe_delay)

        self.destroyed = False

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

    def explode(self):
        """Turn into a nice explosion!"""
        self.sprite = pyglet.sprite.Sprite(
            Alien.explosion,
            x=self.sprite.x,
            y=self.sprite.y)
        pyglet.clock.schedule_once(self.destroy, 0.2)

    def destroy(self, delta_time):
        """Make this alien destroyed so it gets removed"""
        self.destroyed = True
