"""Invaders From Space! A Totally Original Game For Digimakers"""

import pyglet
from player import Player
from alien import Alien


class InvadersWindow(pyglet.window.Window):
    """This class does all managing: it draws to the screen, and
    runs the main game loop"""

    def __init__(self):
        """Assumes options have been parsed from the command line."""
        # Create pyglet window
        super(InvadersWindow, self).__init__()

        #  Add the alien tracker
        self.aliens = []
        self.spawn_alien_row(4)

        # Add the timed functions to make them jump about
        pyglet.clock.schedule_interval(self.lurch_aliens_forward, 5)
        pyglet.clock.schedule_interval(self.change_alien_direction, 5)

        # Add the player and bullet tracker
        self.player = Player(window=self)
        self.push_handlers(self.player.key_handler)
        self.push_handlers(self.player)

        self.bullets = []

    def on_draw(self):
        """Main draw loop. Here is where things actually get
        written to the screen"""
        super(InvadersWindow, self).clear()
        self.player.draw()
        for bullet in self.bullets:
            bullet.draw()

        for alien in self.aliens:
            alien.draw()

    def update(self, delta_time):
        """Perform frame-rate indepent updates of game objects"""
        have_collided = InvadersWindow.have_collided
        self.player.update(delta_time=delta_time)

        # Update all the bullets
        for bullet in self.bullets:
            bullet.update(delta_time=delta_time)
            # Check collisions
            for alien in self.aliens:
                if have_collided(bullet, alien):
                    bullet.destroyed = True
                    alien.explode()

        # Remove bullets that have gone off the screen
        self.bullets = [b for b in self.bullets if b.sprite.y < self.height and not bullet.destroyed]
        self.aliens = [a for a in self.aliens if not a.destroyed]

    def change_alien_direction(self, delta_time):
        """Make aliens strafe in a different direction"""
        for alien in self.aliens:
            alien.head_right = not alien.head_right

    def lurch_aliens_forward(self, delta_time):
        """Make aliens lurch forward"""
        for alien in self.aliens:
            alien.lurch()

    def spawn_alien_row(self, number_of_aliens):
        """Make a row of aliens at the top of the screen"""
        spacing = Alien.image.width + 10
        self.aliens += [
            Alien(window=self, x_pos=(spacing*number))
            for number in xrange(1, number_of_aliens + 1)]

    @staticmethod
    def have_collided(bullet, alien):
        if bullet.sprite.x > alien.sprite.x \
                and bullet.sprite.x < alien.sprite.x + alien.sprite.width:
            bullet_tip = bullet.sprite.y + bullet.sprite.height
            if bullet_tip > alien.sprite.y \
                    and bullet_tip < alien.sprite.y + alien.sprite.height:
                return True

        # By default say no.
        return False

def run_game():
    # Make a new game window
    game_window = InvadersWindow()

    # Run the update function as close to 120 times a second as possible
    pyglet.clock.schedule_interval(game_window.update, 1/120.0)

    # And LOOP!
    pyglet.app.run()

if __name__ == "__main__":
    run_game()
