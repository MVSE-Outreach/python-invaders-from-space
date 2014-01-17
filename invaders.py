"""Invaders From Space! A Totally Original Game For Digimakers"""

import pyglet


class InvadersWindow(pyglet.window.Window):
    """This class does all managing: it draws to the screen, and
    runs the main game loop"""

    def __init__(self):
        """Assumes options have been parsed from the command line."""
        # Create pyglet window
        super(InvadersWindow, self).__init__()

        self.hello = pyglet.text.Label(
            "HELLO WORLD!",
            anchor_x="center",
            anchor_y="center",
            x=self.width/2,
            y=self.height/2,
            font_size=40)

    def on_draw(self):
        """Main draw loop. Here is where things actually get
        written to the screen"""
        super(InvadersWindow, self).clear()
        self.hello.draw()
