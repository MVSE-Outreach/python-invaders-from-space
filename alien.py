"""Contains code for making the aliens work.

Explosion sound effect courtesy of Mike Koenig via soundbible.com"""

import pyglet


class Alien(object):
    """Handles all of the joys of being an alien"""

    image = pyglet.resource.image("images/invader.png")
    explosion_image = pyglet.resource.image("images/explosion.png")
    explosion_sound = pyglet.media.StaticSource(
        pyglet.media.load("sounds/explosion.wav"))
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

        self.exploded = False
        self.destroyed = False

        self.sfx_player = pyglet.media.Player()

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
        self.sprite.y -= self.sprite.height + 5

    def explode(self):
        """Turn into a nice explosion!"""
        self.exploded = True
        self.sfx_player.queue(Alien.explosion_sound)
        self.sfx_player.play()
        self.sprite = pyglet.sprite.Sprite(
            Alien.explosion_image,
            x=self.sprite.x,
            y=self.sprite.y)
        pyglet.clock.schedule_once(self.destroy, 0.2)

    def destroy(self, delta_time):
        """Make this alien destroyed so it gets removed"""
        self.destroyed = True
