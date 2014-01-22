"""Contains code for making the player character all sorted and stuff"""

import pyglet


class Bullet(object):
    """Deal with collisions, and bullets pathing and stuff."""

    def __init__(self):
        """Initialise a newly created bullet"""
        pass


class Player(object):
    """Handles the details of the player's avatar."""

    tank_image = pyglet.resource.image("images/player.png")

    def __init__(self):
        """Create a new Player instance"""
        self.sprite = pyglet.sprite.Sprite(Player.tank_image, x=20, y=20)

    def draw(self):
        """Draw the sprite"""
        self.sprite.draw()
