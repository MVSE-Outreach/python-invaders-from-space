"""Invaders From Space! A Totally Original Game For Digimakers"""
from itertools import chain

import pyglet

from objects import Player, Alien


class InvadersWindow(pyglet.window.Window):
    """This class does all managing: it draws to the screen, and
    runs the main game loop"""

    def __init__(self):
        """Assumes options have been parsed from the command line."""
        # Create pyglet window - the caption is the window title
        super(InvadersWindow, self).__init__(caption="Invaders From Space!")

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
        pyglet.clock.schedule_interval(self.change_alien_direction, 5)
        pyglet.clock.schedule_interval(self.lurch_aliens_forward, 5)

        # Add the player and bullet tracker
        self.player = Player(window=self)
        self.push_handlers(self.player.key_handler)
        self.bullets = []

    def on_draw(self):
        """Main draw loop. Here is where things actually get
        written to the screen"""
        self.clear()
        self.player.draw()

        for drawable in chain(self.bullets, self.aliens, self.lasers):
            drawable.draw()

        if self.game_over_label is not None:
            self.game_over_label.draw()

    def update(self, delta_time):
        """Perform frame-rate indepent updates of game objects"""

        # have_collided = InvadersWindow.have_collided
        self.player.update(delta_time=delta_time)

        # Update all the bullets
        for bullet in self.bullets:
            bullet.update(delta_time=delta_time)
            # Check collisions
            for alien in self.aliens:
                if bullet.has_hit(alien):
                    bullet.destroy()
                    alien.explode()

        # Update all the lasers
        for laser in self.lasers:
            laser.update(delta_time=delta_time)
            # Check collisions
            if laser.has_hit(self.player):
                laser.destroy()
                self.player.explode()
                self.game_over(you_won=False)

        # Remove bullets that have gone off the screen
        self.bullets = [
            b for b in self.bullets if b.sprite.y < self.height
            and not b.destroyed]

        # Remove the aliens that are destroyed
        self.aliens = [a for a in self.aliens if not a.destroyed]

        # Remove lasers that have gone off the screen
        self.lasers = [
            l for l in self.lasers if l.sprite.y > 0
            and not l.destroyed]

        # Make the aliens fire!
        for alien in self.aliens:
            alien.fire()

        # Do the end game victory check
        if len(self.aliens) == 0:
            self.game_over(you_won=True)

    def change_alien_direction(self, delta_time):
        """Make aliens strafe in a different direction"""
        for alien in self.aliens:
            alien.head_right = not alien.head_right

    def lurch_aliens_forward(self, delta_time=None):
        """Make aliens lurch forward"""
        if self.game_over_label is None:
            for alien in self.aliens:
                if not alien.lurch():
                    # lurch() returns false if the alien
                    # has reached you
                    self.game_over(you_won=False)
                    return
            self.spawn_alien_row(number_of_aliens=4)

    def spawn_alien_row(self, delta_time=None, number_of_aliens=4):
        """Make a row of aliens at the top of the screen"""
        spacing = Alien.image.width + 10
        self.aliens += [
            Alien(window=self, x_pos=(spacing*number))
            for number in xrange(1, number_of_aliens + 1)]

    def game_over(self, you_won=False):
        """Game over!"""
        if you_won:
            text = "You Win!"
        else:
            text = "Game Over"

        self.game_over_label = pyglet.text.Label(
            text,
            font_size=30,
            anchor_x="center",
            x=self.width/2,
            y=self.height/2)


def run_game():
    """Runs the game."""
    # Make a new game window
    game_window = InvadersWindow()

    # Run the update function as close to 120 times a second as possible
    pyglet.clock.schedule_interval(game_window.update, 1/120.0)

    # And LOOP!
    pyglet.app.run()

if __name__ == "__main__":
    run_game()
