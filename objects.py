"""Contains code for all the game objects."""

import pyglet
from random import random


class GameObject(object):
    """Basic code for something that has a sprite and
    will check for collisions"""
    # Default image will be the player.
    image = pyglet.resource.image("images/player.png")
    explosion_image = pyglet.resource.image("images/explosion.png")
    scale = 1

    def __init__(self, x_pos, y_pos):
        """Create the sprite"""
        self.sprite = pyglet.sprite.Sprite(
            self.image,
            x=x_pos,
            y=y_pos)
        self.sprite.scale = self.scale

        # State Variables
        self.exploded = False
        self.destroyed = False

    def has_hit(self, other_object):
        """Check whether this object has collided with another.

        Simplistic check - we check if our anchor point is within
        their sprite. We can fiddle with the anchor points in our
        subclasses so that this makes the most sense."""

        if self.sprite.x > other_object.sprite.x \
                and self.sprite.x < \
                other_object.sprite.x + other_object.sprite.width:

            if self.sprite.y > other_object.sprite.y \
                    and self.sprite.y < \
                    other_object.sprite.y + other_object.sprite.height:
                return True

        # By default say no.
        return False

    def draw(self):
        """Simply draw the sprite"""
        self.sprite.draw()

    def destroy(self, delta_time=None):
        """Mark yourself has destroyed so the game will get rid of you."""
        self.destroyed = True

    def explode(self):
        """Make yourself explode, and then destroy yourself!"""
        self.exploded = True
        self.sprite = pyglet.sprite.Sprite(
            self.explosion_image,
            x=self.sprite.x,
            y=self.sprite.y)
        pyglet.clock.schedule_once(self.destroy, 0.2)


class Bullet(GameObject):
    """Deal with collisions, and bullets pathing and stuff."""
    image = pyglet.resource.image("images/bullet.png")
    image.anchor_x = image.width / 2
    image.anchor_y = image.height
    speed = 180
    scale = 0.2

    def __init__(self, x_pos):
        """Initialise a newly created bullet"""
        super(Bullet, self).__init__(
            x_pos=x_pos,
            y_pos=Player.image.height + self.image.height)
        self.destroyed = False

    def update(self, delta_time):
        """Move the bullet up"""
        self.sprite.y += self.speed * delta_time


class Laser(Bullet):
    """Like bullets, but green and they travel downwards!"""
    image = pyglet.resource.image("images/laser.png")
    image.anchor_y = 0
    speed = -180

    def __init__(self, x_pos, y_pos):
        """Initialise a newly created bullet"""
        super(Laser, self).__init__(x_pos)
        self.sprite.y = y_pos


class Player(GameObject):
    """Handles the details of the player's avatar."""

    image = pyglet.resource.image("images/player.png")
    speed = 150
    cooldown_time = 0.5

    left_key = pyglet.window.key.LEFT
    right_key = pyglet.window.key.RIGHT
    fire_key = pyglet.window.key.SPACE

    def __init__(self, window):
        """Create a new Player instance"""
        super(Player, self).__init__(x_pos=20, y_pos=20)
        self.key_handler = pyglet.window.key.KeyStateHandler()
        self.window = window
        self.cooldown = False

    def update(self, delta_time):
        """Move the sprite if appropriate.
        Use the speed and the delta_time provided"""
        if self.key_handler[Player.left_key] and \
                not self.key_handler[Player.right_key]:
            self.move(-Player.speed, delta_time)
        elif self.key_handler[Player.right_key] and \
                not self.key_handler[Player.left_key]:
            self.move(Player.speed, delta_time)

        # Prevent a swarm of bullets by only firing if cooldown is false
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


class Alien(GameObject):
    """Handles all of the joys of being an alien"""
    image = pyglet.resource.image("images/invader.png")
    strafe_step = 50
    strafe_delay = 1
    lurch_delay = 5
    victory_threshold = 50
    likelihood_to_fire = 0.001

    def __init__(self, window, x_pos):
        """Set up a new alien"""
        super(Alien, self).__init__(
            x_pos=x_pos,
            y_pos=window.height - Alien.image.height)

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

    def lurch(self):
        """Lurch forward, towards the player.
        Returns false if the alien has reached the victory threshold"""
        self.sprite.y -= self.sprite.height + 5
        return self.sprite.y > Alien.victory_threshold

    def fire(self):
        """Fire the LASERS! Maybe."""
        if random() < Alien.likelihood_to_fire:
            self.window.lasers.append(
                Laser(
                    self.sprite.x + self.sprite.width / 2,
                    self.sprite.y))
