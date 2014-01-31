#!env python
"""Invaders From Space! A Totally Original Game For Digimakers"""
from itertools import chain

import pyglet

from objects import Player, Alien


class InvadersWindow(object):
    """This class does all managing: it draws to the screen, and
    runs the main game loop.

    Class variables:
    seconds_till_lurch -- the seconds between aliens lurching (default 5)
    aliens_per_row -- how many new aliens per row created (default 5)

    Instance Variables:
    game_over_label -- Initially None, set to a pyglet label by game_over
    aliens -- List of all Alien objects in the game.
    lasers -- List of all laser blasts in the game.
    player -- The Player object.
    bullets -- The list of bullets in the game.
    window -- The pyglet window

    Methods:
    on_draw -- Assigned to the window as a draw function
    update -- Calls the update functions for all game objects.
    change_alien_direction -- Makes all aliens swap strafe direction.
    lurch_aliens_forward -- Makes all aliens jump forward.
    spawn_alien_row -- Spawns a new row of aliens at the top of the screen.
    game_over -- Sets the game over text based on a boolean argument.
    """

    seconds_till_lurch = 5
    aliens_per_row = 5

    def __init__(self):
        """This sets everything up. Factoid: Init is short for 'initialise'.

        We call up to pyglets Window init to do the heavy lifting, and we
        give it a caption for the window title.
        """
        # Create pyglet window - the caption is the window title
        self.window = pyglet.window.Window(
            caption="Invaders From Space!",
            width=640,
            height=480)

        # Game over label. We also use it as a flag for when
        # the game is finished.
        self.game_over_label = None

        #  Add the alien and laser lists
        self.aliens = []
        self.lasers = []

        # Start the game with three loads of aliens
        self.lurch_aliens_forward()
        self.lurch_aliens_forward()
        self.lurch_aliens_forward()

        # We add two timed functions here to control the flow of aliens
        pyglet.clock.schedule_interval(
            self.change_alien_direction,
            self.seconds_till_lurch)
        pyglet.clock.schedule_interval(
            self.lurch_aliens_forward,
            self.seconds_till_lurch)

        # Add the player and bullet tracker
        self.player = Player(window=self)
        self.bullets = []
        # And let the window know to send keyboard events to the Player's
        # key_handler object.
        self.window.push_handlers(self.player.key_handler)

    def on_draw(self):
        """Overrides Window.on_draw, and draws all our sprites to the screen.

        Draw order is:
        1. Player
        2. Bullets
        3. Aliens
        4. Lasers

        Things drawn later go on top of things drawn earlier.
        """
        # First off we wipe the slate clean.
        self.window.clear()

        # Then we draw our tank
        self.player.draw()

        # Now we go through the bullets, aliens and lasers and draw them
        for drawable in chain(self.bullets, self.aliens, self.lasers):
            drawable.draw()

        # Lastly we draw the game over text on the screen if it has been set
        if self.game_over_label is not None:
            self.game_over_label.draw()

    def update(self, elapsed_time):
        """Perform frame-rate indepent updates of game objects.

        This method just tells each game object to update themselves, Then it
        checks for collions, removes destroyed objects and tests for Player
        victory.

        Arguments:
        elapsed_time -- Time in seconds since the last update."""

        # First off we make sure the player gets updated.
        self.player.update(elapsed_time=elapsed_time)

        # Update all the bullets...
        for bullet in self.bullets:
            bullet.update(elapsed_time=elapsed_time)
            # .. and now check for collisions
            for alien in self.aliens:
                if bullet.has_hit(alien):
                    bullet.destroy()
                    alien.explode()

        # Update all the lasers...
        for laser in self.lasers:
            laser.update(elapsed_time=elapsed_time)
            # and check for collisions there too!
            if laser.has_hit(self.player):
                laser.destroy()
                self.player.explode()
                self.game_over(you_won=False)

        # Remove bullets that have gone off the screen or have
        # been marked as 'destroyed'. This kind of line here is
        # a 'list comprehension'. They are really nifty.
        self.bullets = [
            b for b in self.bullets if b.sprite.y < self.window.height
            and not b.destroyed]

        # Remove the aliens that are destroyed, like above, with
        # another list comprehension
        self.aliens = [a for a in self.aliens if not a.destroyed]

        # Remove lasers that have gone off the screen.
        self.lasers = [
            l for l in self.lasers if l.sprite.y > 0
            and not l.destroyed]

        # Make the aliens fire! Maybe. It's a bit random.
        for alien in self.aliens:
            alien.fire()

        # Do the end game victory check
        if len(self.aliens) == 0:
            self.game_over(you_won=True)

    def change_alien_direction(self, elapsed_time=None):
        """Make aliens strafe in a different direction.

        Simply sets each aliens head_right variable to the opposite
        value.

        Arguments:
        elapsed_time -- Ignored. Required by pyglet clock.
        """
        for alien in self.aliens:
            alien.head_right = not alien.head_right

    def lurch_aliens_forward(self, elapsed_time=None):
        """Make aliens lurch forward.

        Simply calls each aliens lurch function, checking for the
        return value of false that means the Alien has won. If it
        finds it, it calls game_over.

        After each lurch, it spawns a new row of aliens.

        Arguments:
        elapsed_time -- Ignored, required by pyglet's clock.
        """
        if self.game_over_label is None:
            for alien in self.aliens:
                if not alien.lurch():
                    # lurch() returns false if the alien has reached you!
                    # This is a nice way of checking that.
                    self.game_over(you_won=False)

            # After all the aliens have moved forward, we add a new row in
            self.spawn_alien_row()

    def spawn_alien_row(
            self,
            elapsed_time=None,
            number_of_aliens=None):
        """Make a row of aliens at the top of the screen.

        Does some rather hacky spacing calculations to determine
        Alien x coordinates.

        Arguments:
        elapsed_time -- Ignored, required by pyglet's clock.
        number_of_aliens -- How many aliens do we want?
        """
        # Check if we should use the default number of aliens
        if not number_of_aliens:
            number_of_aliens = self.aliens_per_row

        # This maths figures out how much space we need to leave for
        # the aliens to strafe across the whole screen.
        number_of_strafes = self.seconds_till_lurch / Alien.strafe_delay
        strafe_distance = number_of_strafes * Alien.strafe_step
        rightmost_start = self.window.width - strafe_distance

        # Now we figure out if we can fit the number of aliens requested
        # into that space. If we can't, we try with one less, then two less...
        spacing = None

        while not spacing:
            space_per_alien = rightmost_start / number_of_aliens
            if space_per_alien < Alien.image.width:
                # Won't fit! Try one less!
                number_of_aliens -= 1
            else:
                # Great! Let's make these aliens!
                spacing = space_per_alien

        # Add some new aliens to the list.
        self.aliens += [
            Alien(window=self, x_pos=(spacing*number + Alien.strafe_step))
            for number in range(number_of_aliens)]

    def game_over(self, you_won=False):
        """Game over! Set the game_over_label.

        The text is determined by the boolean you_won argument.

        Arguments:
        you_won -- True for a player win, false for an Alien victory.
        """
        if you_won:
            text = "You Win!"
        else:
            text = "Game Over"

        self.game_over_label = pyglet.text.Label(
            text,
            font_size=30,
            anchor_x="center",
            x=self.window.width / 2,
            y=self.window.height / 2)


def run_game():
    """Creates an InvadersWindow, schedules the update function
    and starts the main pyglet loop.

    This is in a function so that we can run the game from a python
    instance as well as in a script."""
    # Make a new game window
    game_window = InvadersWindow()

    @game_window.window.event
    def on_draw():
        game_window.on_draw()

    # Run the update function as close to 120 times a second as possible
    pyglet.clock.schedule_interval(game_window.update, 1/120.0)

    # And LOOP!
    pyglet.app.run()



if __name__ == "__main__":
    # This is triggered if being run as a script.
    run_game()
