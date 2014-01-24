"""Invaders From Space! A Totally Original Game For Digimakers"""

import pyglet
from player import Player


class InvadersWindow(pyglet.window.Window):
    """This class does all managing: it draws to the screen, and
    runs the main game loop"""

    def __init__(self):
        """Assumes options have been parsed from the command line."""
        # Create pyglet window
        super(InvadersWindow, self).__init__()

        self.aliens = []
        self.bullets = []
        self.player = Player(window=self)
        self.push_handlers(self.player.key_handler)
        self.push_handlers(self.player)

    def on_draw(self):
        """Main draw loop. Here is where things actually get
        written to the screen"""
        super(InvadersWindow, self).clear()
        self.player.draw()
        for bullet in self.bullets:
            bullet.draw()

    def update(self, delta_time):
        """Perform frame-rate indepent updates of game objects"""
        self.player.update(delta_time=delta_time)

        # Update all the bullets
        for bullet in self.bullets:
            bullet.update(delta_time=delta_time)

        # Remove bullets that have gone off the screen
        self.bullets = [b for b in self.bullets if b.sprite.y < self.height]


def run_game():
    # Make a new game window
    game_window = InvadersWindow()

    # Run the update function as close to 120 times a second as possible
    pyglet.clock.schedule_interval(game_window.update, 1/120.0)

    # And LOOP!
    pyglet.app.run()

if __name__ == "__main__":
    run_game()
