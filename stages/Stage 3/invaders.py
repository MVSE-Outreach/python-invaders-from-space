#!env python
"""This is the Stage 3 invaders file. You can move and fire bullets!"""
import pyglet

from objects import Player

class InvadersWindow(pyglet.window.Window):
    """This class does all managing: it draws to the screen, and
    updates all the bits and pieces flying around the screen!

    Extends pyglet.window.Window, overwriting the on_draw method.
    """

    def __init__(self):
        """This sets everything up. Factoid: Init is short for 'initialise'.

        We call up to pyglets Window init to do the heavy lifting,
        specifying a width, height and caption (title).
        """
        # Create pyglet window - the caption is the window title
        pyglet.window.Window.__init__(
            self,
            caption="Invaders From Space!",
            width=640,
            height=480)

        # A list of bullets!
        self.bullets = []

        # Our fearless tank, with a reference to ourselves being passed in.
        self.player = Player(window=self)
        # We make sure that the keyboard events are sent to the key handler.
        self.push_handlers(self.player.key_handler)

    def on_draw(self):
        """Overrides Window.on_draw.
        """
        # First off we wipe the slate clean.
        self.clear()

        # We draw our player
        self.player.draw()

        # We draw our bullets
        for bullet in self.bullets:
            bullet.draw()

    def update(self, elapsed_time):
        """Perform frame-rate indepent updates of game objects.
        """
        # Update the player
        self.player.update(elapsed_time=elapsed_time)

        # We update all our bullets!
        for bullet in self.bullets:
            bullet.update(elapsed_time=elapsed_time)
            # Check if it has gone off the screen
            if bullet.sprite.y > self.height:
                # It has, so destroy it.
                bullet.destroy()

        # Keep only the bullets that aren't 'destroyed'
        # This is a super cool and useful Python feature
        # called a 'list comprehension'. Make a list from a loop!
        self.bullets = [b for b in self.bullets if not b.destroyed]


def run_game():
    """Creates an InvadersWindow, schedules the update function
    and starts the main pyglet loop.

    This is in a function so that we can run the game from a python
    instance as well as in a script."""
    # Make a new game window
    game_window = InvadersWindow()

    # Run the update function as close to 120 times a second as possible
    pyglet.clock.schedule_interval(game_window.update, 1/120.0)

    # And LOOP!
    pyglet.app.run()

if __name__ == "__main__":
    # This is triggered if being run as a script.
    run_game()