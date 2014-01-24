"""Contains code for making the player character all sorted and stuff"""

import pyglet


class Bullet(object):
    """Deal with collisions, and bullets pathing and stuff."""
    image = pyglet.resource.image("images/bullet.png")
    image.anchor_x = image.width / 2
    speed = 180
    scale = 0.2

    def __init__(self, x_pos):
        """Initialise a newly created bullet"""
        self.sprite = pyglet.sprite.Sprite(
            Bullet.image,
            x=x_pos,
            y=Player.image.height)
        self.sprite.scale = Bullet.scale

    def update(self, delta_time):
        """Move the bullet up"""
        self.sprite.y += Bullet.speed * delta_time

    def draw(self):
        """Draw the bullet sprite"""
        self.sprite.draw()


class Player(object):
    """Handles the details of the player's avatar."""

    image = pyglet.resource.image("images/player.png")
    speed = 150
    left_key = pyglet.window.key.LEFT
    right_key = pyglet.window.key.RIGHT
    fire_key = pyglet.window.key.SPACE

    def __init__(self, window):
        """Create a new Player instance"""
        self.sprite = pyglet.sprite.Sprite(Player.image, x=20, y=20)
        self.key_handler = pyglet.window.key.KeyStateHandler()
        self.window = window

    def draw(self):
        """Draw the sprite"""
        self.sprite.draw()

    def update(self, delta_time):
        """Move the sprite if appropriate.
        Use the speed and the delta_time provided"""
        if self.key_handler[Player.left_key] and \
                not self.key_handler[Player.right_key]:
            self.move(0-Player.speed, delta_time)
        elif self.key_handler[Player.right_key] and \
                not self.key_handler[Player.left_key]:
            self.move(Player.speed, delta_time)

    def move(self, speed, elapsed_time):
        """Simply do speed * time to get a movement distance"""
        self.sprite.x += speed * elapsed_time

    def on_key_press(self, symbol, modifiers):
        """Used for the less frequent key: firing!"""
        if symbol == pyglet.window.key.SPACE:
            self.fire()

    def fire(self):
        """Fire a bullet!"""
        self.window.bullets.append(
            Bullet(self.sprite.x + self.sprite.width / 2))
