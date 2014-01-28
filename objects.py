"""Contains code for all the game objects."""

import pyglet
from random import random

# Add the image path to where pyglet searches.
pyglet.resource.path.append("images")


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


class Bullet(GameObject):
    """This class specifies the behaviour for the projectiles that we will fire,
    and inherits from GameObject

    Changed Class Variables:
    image -- Now set to the bullet image with the anchor at the top centre.
    scale -- Set to 0.2 to make the bullets smaller.

    New Class Variables:
    speed: Bullet speed in pixels per second. (Default 180)

    Methods:
    update -- Moves the bullet along the y axis.
    """
    image = pyglet.resource.image("bullet.png")
    image.anchor_x = image.width / 2
    image.anchor_y = image.height
    speed = 180
    scale = 0.2

    def __init__(self, x_pos):
        """Initialise a newly created bullet.

        Assumes that the starting y coordinate is the height of the Player
        plus the scaled height of a bullet (because the anchor is at the top).

        Arguments:
        x_pos -- the x coordinate, intended to be the middle of the Player
        """
        super(Bullet, self).__init__(
            x_pos=x_pos,
            y_pos=Player.image.height + self.image.height * self.scale)

    def update(self, elapsed_time):
        """Move the bullet up, according to the speed and elapsed time.

        Arguments:
        elapsed_time -- The time since we last moved.
        """
        self.sprite.y += self.speed * elapsed_time


class Laser(Bullet):
    """Like bullets, but green and they travel downwards! Extends Bullet.

    Changed Class Variables:
    image -- Set to laser.png, and the anchor point at middle bottom
    speed -- Set to -180, as lasers travel downwards.
    """
    image = pyglet.resource.image("laser.png")
    image.anchor_y = 0
    speed = -180

    def __init__(self, x_pos, y_pos):
        """Initialise a newly created laser.

        Takes both x and y as alien could be anywhere on screen.
        We adjust the y-coordinate so that the laser looks like it
        comes from the middle of the alien.
        """
        super(Laser, self).__init__(x_pos)
        self.sprite.y = y_pos + self.sprite.height / 2


class Player(GameObject):
    """Handles the details of the player's tank. Extends GameObject.

    Contains a pyglet KeyStateHandler for tracking the keyboard.

    Changed Class Variables:
    image -- now set to player.png

    New Class Variables:
    speed -- pixels per second, like the bullet. (default 150)
    cooldown_time -- minimum time between shots, in seconds. (default 0.5)
    left_key -- the keyboard key for moving left (default left arrow)
    right_key -- ditto, but for moving right (default right arrow)
    fire_key -- Again, but for firing! (default space)

    Instance Variables:
    cooldown -- Boolean for whether you are on cooldown. Reset by end_cooldown.
    window -- The window where everything is being drawn. Used to add bullets.
    key_handler -- The KeyStateHandler for tracking buttons

    Methods:
    update -- Call move and fire based on keyboard and cooldown.
    move -- Called by update to move along the x direction appropriately
    end_cooldown -- Called when it is ok to fire again.
    fire -- Fires a bullet!
    """

    image = pyglet.resource.image("player.png")
    speed = 150
    cooldown_time = 0.5

    left_key = pyglet.window.key.LEFT
    right_key = pyglet.window.key.RIGHT
    fire_key = pyglet.window.key.SPACE

    def __init__(self, window):
        """Create a new Player instance.

        Starts player off at standard location, and makes a KeyStateHandler.
        Sets the cooldown to false, so we can fire immediately.

        Arguments:
        window -- the main game window. Used for referring to bullet list.
        """
        super(Player, self).__init__(x_pos=20, y_pos=20)
        self.key_handler = pyglet.window.key.KeyStateHandler()
        self.window = window
        self.cooldown = False

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

        # Prevent a swarm of bullets by only firing if cooldown is false
        if self.key_handler[self.fire_key] and not self.cooldown:
            self.fire()
            self.cooldown = True
            pyglet.clock.schedule_once(self.end_cooldown, Player.cooldown_time)

    def move(self, speed, elapsed_time):
        """Simply do speed * time to get a movement distance.

        Arguments:
        speed -- The horizontal speed.
        elapsed_time -- Time the tank has been travelling at that speed.
        """
        self.sprite.x += speed * elapsed_time

    def end_cooldown(self, elapsed_time=None):
        """Set cooldown to false, enabling you to fire again

        Arguments:
        elapsed_time -- Ignored. Required by pyglet scheduling system."""
        self.cooldown = False

    def fire(self):
        """Fire a bullet!

        Uses the window variable to add a bullet into the list
        managed by the main game window.
        """
        self.window.bullets.append(
            Bullet(self.sprite.x + self.sprite.width / 2))


class Alien(GameObject):
    """Handles all of the joys of being an alien. Extends GameObject.

    Changed Class Variables:
    image -- Now invader.png. Anchor point unchanged.

    New Class Variables:
    strafe_step -- The number of pixels aliens should move sideways at a time (default 50)
    strafe_delay -- The time in seconds between sideways movements. (default 1)
    lurch_delay -- The time in seconds between downwards jumps. (default 5)
    victory_threshold -- The height that an alien needs to reach to win (default Player height)
    likelihood_to_fire -- Between 0 and 1. Percentage chance of firing on update (default 0.001)
    row_size -- How many aliens to a row (default 4)

    Instance variables:
    head_right -- Boolean. True for strafing right, false for left.

    Methods:
    strafe -- Jump right or left depending on head_right's value.
    lurch -- Jump downwards, towards player. Return false if victory_threshold reached.
    fire -- Pick a random percentage. Fire if it is less than likelihood_to_fire.
    """
    image = pyglet.resource.image("invader.png")
    strafe_step = 50
    strafe_delay = 1
    lurch_delay = 5
    victory_threshold = Player.image.height
    likelihood_to_fire = 0.001
    row_size = 4

    def __init__(self, window, x_pos):
        """Set up a new alien.

        Assumes the y coordinate is at the top of the screen.

        Arguments:
        window -- The window. Used for firing lasers.
        x_pos -- The x coordinate."""
        super(Alien, self).__init__(
            x_pos=x_pos,
            y_pos=window.height - Alien.image.height)

        self.head_right = True

        pyglet.clock.schedule_interval(self.strafe, Alien.strafe_delay)

        self.window = window

    def strafe(self, elapsed_time=None):
        """Do that characteristic strafe across the screen.

        Arguments:
        elapsed_time -- ignored, as aliens jump same distance each time.
        """
        if self.head_right:
            self.sprite.x += Alien.strafe_step
        else:
            self.sprite.x -= Alien.strafe_step

    def lurch(self):
        """Lurch forward, towards the player.
        Returns false if the alien has reached the victory threshold

        Moves a distance of 1 alien plus 5 pixels.
        """
        self.sprite.y -= self.sprite.height + 5
        return self.sprite.y > Alien.victory_threshold

    def fire(self):
        """Fire the LASERS! Maybe.

        Percentages are represented as decimal numbers between 0 and 1.
        We choose a random percentage, and fire if it is below the
        likelihood_to_fire value.

        The laser is spawned from the centre bottom of the aliens.
        """
        if random() < Alien.likelihood_to_fire:
            self.window.lasers.append(
                Laser(
                    self.sprite.x + self.sprite.width / 2,
                    self.sprite.y + self.sprite.height))
