"""This is the stage 2 objects file. There's a Player class! EXCITEMENT!
"""
import os

import pyglet

# Obtain the path to this script. This workaround is
# just for importing as a module; it's not needed otherwise.
# We then use this to add the image path to where pyglet searches.
pyglet.resource.path.append(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), 'images'))
pyglet.resource.path.append("/Users/drummondogilvie/Projects/Invaders/images")

class GameObject(object):
    """Basic code for something that has a sprite and
    will check for collisions.

    Image anchor defaults to bottom left.

    Class variables:

    image -- pyglet image for the sprite (default player.png)
    explosion_image -- the same but for post-hit (default explosion.png)
    scale -- the scaling factor that should be applied to the sprite
    explosion_time -- the time in seconds that the explosion sprite lingers

    Instance variables:
    sprite -- the pyglet sprite, made from the image.
              There are also sprite.x and sprite.y, which set the position
              of the object in the window (0, 0 is the bottom left)
    exploded -- has this object exploded? Boolean.
    destroyed -- is this object no longer needed? Boolean.

    Methods:
    has_hit -- Naively checks a collision with another object.
    draw -- draws the sprite
    destroy -- set destroyed to True
    explode -- switch to the explosion sprite and then destroy
    """
    # Default image will be the player.
    image = pyglet.resource.image("player.png")
    explosion_image = pyglet.resource.image("explosion.png")
    scale = 1
    explosion_time = 0.2

    def __init__(self, x_pos, y_pos):
        """Initialise the object, forming a sprite at the given location.

        Arguments:
        x_pos -- The x coordinate of the sprite's anchor point.
        y_pos -- Ditto, but y.
        """
        self.sprite = pyglet.sprite.Sprite(
            self.image,
            x=x_pos,
            y=y_pos)
        self.sprite.scale = self.scale

        # Set state variables to be False
        self.exploded = self.destroyed = False

    def has_hit(self, other_object):
        """Check whether this object has collided with another.

        Simplistic check - we check if our anchor point is within
        their sprite. We can fiddle with the anchor points in our
        subclasses so that this makes the most sense.

        Arguments:
        other_object -- the object we are checking against."""

        # First we check the x direction
        if self.sprite.x > other_object.sprite.x \
                and self.sprite.x < \
                other_object.sprite.x + other_object.sprite.width:

            # Then we check the y.
            if self.sprite.y > other_object.sprite.y \
                    and self.sprite.y < \
                    other_object.sprite.y + other_object.sprite.height:
                return True

        # By default say no.
        return False

    def draw(self):
        """Simply draw the sprite."""
        self.sprite.draw()

    def destroy(self, elapsed_time=None):
        """Mark yourself has destroyed so the game will get rid of you.

        Arguments:
        elapsed_time -- not used, but required by the clock system in pyglet
        """
        self.destroyed = True

    def explode(self):
        """Make yourself explode, and then destroy yourself after a delay!

        This swaps the sprite in place to be the explosion image, and uses
        the pyglet clock to schedule calling self.destroy after a delay that
        is set in the class variable explosion_time."""
        self.exploded = True
        self.sprite = pyglet.sprite.Sprite(
            self.explosion_image,
            x=self.sprite.x,
            y=self.sprite.y)
        pyglet.clock.schedule_once(self.destroy, self.explosion_time)


class Player(GameObject):
    """Handles the details of the player's tank. Extends GameObject.

    Contains a pyglet KeyStateHandler for tracking the keyboard.

    Changed Class Variables:
    image -- now set to player.png

    New Class Variables:
    speed -- pixels per second, like the bullet. (default 150)
    left_key -- the keyboard key for moving left (default left arrow)
    right_key -- ditto, but for moving right (default right arrow)

    Instance Variables:
    key_handler -- The KeyStateHandler for tracking buttons

    Methods:
    update -- Call move based on keyboard
    move -- Called by update to move along the x direction appropriately
    """

    image = pyglet.resource.image("player.png")
    speed = 150

    left_key = pyglet.window.key.LEFT
    right_key = pyglet.window.key.RIGHT

    def __init__(self):
        """Create a new Player instance.

        Starts player off at standard location, and makes a KeyStateHandler.
        """
        super(Player, self).__init__(x_pos=20, y_pos=20)
        self.key_handler = pyglet.window.key.KeyStateHandler()

    def update(self, elapsed_time=0):
        """Move and fire if appropriate.

        Uses the key_handler to see what buttons are active.
        Will only fire if not on cooldown, and only move if just
        one of the movement buttons is being pressed. Uses the speed
        class variable, negating it for moving left.

        Arguments:
        elapsed_time -- Time in seconds since last update. Passed to move.
        """
        # Check player holding left ONLY
        if self.key_handler[Player.left_key] and \
                not self.key_handler[Player.right_key]:
            self.move(-Player.speed, elapsed_time)
        # Alternatively holding right ONLY
        elif self.key_handler[Player.right_key] and \
                not self.key_handler[Player.left_key]:
            self.move(Player.speed, elapsed_time)

    def move(self, speed, elapsed_time):
        """Simply do speed * time to get a movement distance.

        Arguments:
        speed -- The horizontal speed.
        elapsed_time -- Time the tank has been travelling at that speed.
        """
        self.sprite.x += speed * elapsed_time