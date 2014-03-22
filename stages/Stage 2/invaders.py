#!env python
"""
This is the stage 2 invaders file. There's a player tank!
"""
import pyglet


class InvadersWindow(pyglet.window.Window):
    """
    This class does all managing: it draws to the screen, and
    updates all the bits and pieces flying around the screen!

    Extends pyglet.window.Window, overwriting the on_draw method.
    """

    def __init__(self):
        """
        This sets everything up. Factoid: Init is short for 'initialise'.

        We call up to pyglets Window init to do the heavy lifting,
        specifying a width, height and caption (title).
        """
        # Create pyglet window - the caption is the window title
        pyglet.window.Window.__init__(
            self,
            caption="Invaders From Space!",
            width=640,
            height=480)
        from objects import Player
        self.player = Player()
        self.push_handlers(self.player.key_handler)

    def on_draw(self):
        """
        Overrides Window.on_draw.
        """
        # First off we wipe the slate clean.
        self.clear()
        self.player.draw()

    def update(self, elapsed_time):
        """
        Perform frame-rate indepent updates of game objects.
        """
        self.player.update(elapsed_time=elapsed_time)
        pass


def run_game():
    """
    Creates an InvadersWindow, schedules the update function
    and starts the main pyglet loop.

    This is in a function so that we can run the game from a python
    instance as well as in a script.
    """
    # Make a new game window
    game_window = InvadersWindow()

    # Run the update function as close to 120 times a second as possible
    pyglet.clock.schedule_interval(game_window.update, 1/120.0)

    # And LOOP!
    pyglet.app.run()

if __name__ == "__main__":
    # This is triggered if being run as a script.
    run_game()
