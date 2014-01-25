"""Contains code for all the game objects."""

import pyglet
from random import random


class Bullet(object):
    """Deal with collisions, and bullets pathing and stuff."""
    image = pyglet.resource.image("images/bullet.png")
    image.anchor_x = image.width / 2
    speed = 180
    scale = 0.2

    def __init__(self, x_pos):
        """Initialise a newly created bullet"""
        self.sprite = pyglet.sprite.Sprite(
            self.image,
            x=x_pos,
            y=Player.image.height)
        self.sprite.scale = Bullet.scale
        self.destroyed = False

    def update(self, delta_time):
        """Move the bullet up"""
        self.sprite.y += self.speed * delta_time

    def draw(self):
        """Draw the bullet sprite"""
        self.sprite.draw()


class Laser(Bullet):
    """Like bullets, but green and they travel downwards!"""
    image = pyglet.resource.image("images/laser.png")
    speed = -180

    def __init__(self, x_pos, y_pos):
        """Initialise a newly created bullet"""
        super(Laser, self).__init__(x_pos)
        self.sprite.y = y_pos


class Player(object):
    """Handles the details of the player's avatar."""

    image = pyglet.resource.image("images/player.png")
    speed = 150
    cooldown_time = 0.5

    left_key = pyglet.window.key.LEFT
    right_key = pyglet.window.key.RIGHT
    fire_key = pyglet.window.key.SPACE

    def __init__(self, window):
        """Create a new Player instance"""
        self.sprite = pyglet.sprite.Sprite(Player.image, x=20, y=20)
        self.key_handler = pyglet.window.key.KeyStateHandler()
        self.window = window
        self.cooldown = False

    def draw(self):
        """Draw the sprite"""
        self.sprite.draw()

    def update(self, delta_time):
        """Move the sprite if appropriate.
        Use the speed and the delta_time provided"""
        if self.key_handler[Player.left_key] and \
                not self.key_handler[Player.right_key]:
            self.move(-Player.speed, delta_time)
        elif self.key_handler[Player.right_key] and \
                not self.key_handler[Player.left_key]:
            self.move(Player.speed, delta_time)

        if self.key_handler[self.fire_key] and not self.cooldown:
            self.fire()
            self.cooldown = True
            pyglet.clock.schedule_once(self.end_cooldown, Player.cooldown_time)

    def move(self, speed, elapsed_time):
        """Simply do speed * time to get a movement distance"""
        self.sprite.x += speed * elapsed_time

    def end_cooldown(self, delta_time=None):
        """Set cooldown to false, enabling you to fire again"""
        self.cooldown = False

    def fire(self):
        """Fire a bullet!"""
        self.window.bullets.append(
            Bullet(self.sprite.x + self.sprite.width / 2))

    def explode(self):
        """Turn into a nice explosion!"""
        self.sprite = pyglet.sprite.Sprite(
            Alien.explosion_image,
            x=self.sprite.x,
            y=self.sprite.y)
        self.sprite.draw()


class Alien(object):
    """Handles all of the joys of being an alien"""

    image = pyglet.resource.image("images/invader.png")
    explosion_image = pyglet.resource.image("images/explosion.png")
    strafe_step = 50
    strafe_delay = 1
    lurch_delay = 5
    victory_threshold = 50
    likelihood_to_fire = 0.001

    def __init__(self, window, x_pos):
        """Set up a new alien"""
        self.sprite = pyglet.sprite.Sprite(
            Alien.image,
            x=x_pos,
            y=window.height - Alien.image.height)

        self.head_right = True

        pyglet.clock.schedule_interval(self.strafe, Alien.strafe_delay)

        self.exploded = False
        self.destroyed = False

        self.window = window

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
        """Lurch forward, towards the player.
        Returns false if the alien has reached the victory threshold"""
        self.sprite.y -= self.sprite.height + 5
        return self.sprite.y > Alien.victory_threshold

    def explode(self):
        """Turn into a nice explosion!"""
        self.exploded = True
        self.sprite = pyglet.sprite.Sprite(
            Alien.explosion_image,
            x=self.sprite.x,
            y=self.sprite.y)
        pyglet.clock.schedule_once(self.destroy, 0.2)

    def destroy(self, delta_time):
        """Make this alien destroyed so it gets removed"""
        self.destroyed = True

    def fire(self):
        """Fire the LASERS! Maybe."""
        if random() < Alien.likelihood_to_fire:
            self.window.lasers.append(
                Laser(
                    self.sprite.x + self.sprite.width / 2,
                    self.sprite.y))
