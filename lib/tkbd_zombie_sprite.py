#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    tkBoulderDash - Python3-Tkinter port of 'Boulder Dash' game

    Python3-Tkinter port by Raphaël Seban <motus@laposte.net>

    Copyright (c) 2014+ Raphaël Seban for the present code

    This program is free software: you can redistribute it and/or
    modify it under the terms of the GNU General Public License as
    published by the Free Software Foundation, either version 3 of
    the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
    General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.

    If not, see http://www.gnu.org/licenses/
"""

# lib imports
import random
from . import tkbd_base_sprite as S


class TkBDZombieSprite (S.TkBDBaseSprite):
    """
        Zombie sprite in the mine;
    """

    # class constants
    STATUS = {

        # idle right
        "default": {
            "loop": True,
            "sequence": True,
            "delay": 200,
        },

        "idle_left": {
            "loop": True,
            "sequence": True,
            "delay": 200,
        },

        "walk_left": {
            "loop": True,
            "sequence": True,
            "delay": 100,
        },

        "walk_right": {
            "loop": True,
            "sequence": True,
            "delay": 100,
        },

        "attack_left": {
            "loop": True,
            "sequence": True,
            "delay": 100,
        },

        "attack_right": {
            "loop": True,
            "sequence": True,
            "delay": 100,
        },

        "die_left": {
            "loop": False,
            "sequence": True,
            "delay": 200,
        },

        "die_right": {
            "loop": False,
            "sequence": True,
            "delay": 200,
        },
    }


    def ai_loop (self):
        """
            player tracking AI logics;
        """
        # game paused?
        if self.game_paused:
            # wait
            self.state_idle()
        # game resumed
        else:
            # inits
            cs = self.matrix.cellsize
            px, py = self.player_xy
            x, y = self.xy
            dx, dy = (px - x, py - y)
            # moving inits
            moved = False
            # moving horizontally
            if dx < 0:
                moved = self.move_left()
            elif dx > 0:
                moved = self.move_right()
            # end if
            # moving vertically
            if dy < 0:
                moved = moved or self.move_up()
            elif dy > 0:
                moved = moved or self.move_down()
            # end if
            if random.randint(1, 3) == 3 and \
                                not dy and abs(dx) < 4 * cs:
                self.state_attack()
            elif not moved:
                self.state_idle()
            # end if
        # end if
        # loop again
        self.animations.run_after(800, self.ai_loop)
    # end def


    def filter_collisions (self, c_dict):
        """
            controls whether collisions with other sprites should
            allow to move or not;
        """
        # collided sprite inits
        sprite = c_dict["sprite"]
        # got something?
        if sprite:
            # touched player?
            if "player" in sprite.role:
                # freeze!
                sprite.freeze()
            # got some earth?
            elif "earth" in sprite.role and sprite.is_overable:
                # dig it!
                sprite.destroy()
            else:
                # denied movement
                return False
            # end if
        # end if
        # allowed movement
        return True
    # end def


    def game_started (self, player_sprite, *args, **kw):
        """
            event handler;
            hook method to be reimplemented in subclass;
            game has started;
        """
        # player pos
        self.player_xy = player_sprite.xy
        # start AI loop
        self.animations.run_after(
            2000 + 100 * random.randint(0, 10), self.ai_loop
        )
    # end def


    def init_sprite (self, **kw):
        """
            hook method to be reimplemented in subclass;
            this avoids re-declaring __init__ signatures all the time;
        """
        # super class inits
        super().init_sprite(**kw)
        # member inits
        self.direction = "right"
        self.player_xy = None
        # event bindings
        self.events_dict.update(
            {
                "Game:Player:Moved": self.player_moved,
                "Main:Game:Over": self.game_over,
                "Main:Game:Paused": self.game_suspended,
                "Main:Game:Resumed": self.game_resumed,
                "Main:Game:Started": self.game_started,
            }
        )
    # end def


    def killed (self, *args, **kw):
        """
            zombie has been killed by some sprite;
        """
        # stop animations
        self.animations.lock(
            self.ai_loop,
            self.state_idle,
            self.state_attack,
            self.state_walk,
            self.state_die,
        )
        # zombie dies now
        self.state_die()
    # end def


    def move_down (self, *args, **kw):
        """
            moves down;
        """
        moved = self.move_sprite(0, +1, callback=self.filter_collisions)
        if moved:
            self.state_walk()
        # end if
        return moved
    # end def


    def move_left (self, *args, **kw):
        """
            moves left;
        """
        moved = self.move_sprite(-1, 0, callback=self.filter_collisions)
        if moved:
            self.state_walk("left")
        # end if
        return moved
    # end def


    def move_right (self, *args, **kw):
        """
            moves right;
        """
        moved = self.move_sprite(+1, 0, callback=self.filter_collisions)
        if moved:
            self.state_walk("right")
        # end if
        return moved
    # end def


    def move_up (self, *args, **kw):
        """
            moves up;
        """
        moved = self.move_sprite(0, -1, callback=self.filter_collisions)
        if moved:
            self.state_walk()
        # end if
        return moved
    # end def


    def on_sequence_end (self, *args, **kw):
        """
            on image animation sequence end;
        """
        # zombie is dead
        self.destroy(*args, **kw)
    # end def


    def player_moved (self, sprite, *args, **kw):
        """
            event handler;
            player moved: update target position;
        """
        self.player_xy = sprite.xy
    # end def


    def state_attack (self, *args, **kw):
        """
            zombie attacks player;
        """
        # zombie attacks player
        self.state = "attack_{}".format(self.direction)
        # notify game frame
        self.notify_event("Attacking")
    # end def


    def state_die (self, *args, **kw):
        """
            zombie dies now;
        """
        # zombie dies
        self.state = "die_{}".format(self.direction)
        # notify game frame
        self.notify_event("Dying")
    # end def


    def state_idle (self, *args, **kw):
        """
            zombie waits for events;
        """
        # zombie is idle
        if self.direction == "right":
            # idle right
            self.state = "default"
        else:
            # idle left
            self.state = "idle_left"
        # end if
    # end def


    def state_walk (self, direction=None, *args, **kw):
        """
            zombie walks toward player;
        """
        # param inits
        if direction:
            self.direction = str(direction).lower()
        # end if
        # zombie walks
        self.state = "walk_{}".format(self.direction)
        # reset to idle in a while
        self.animations.run_after(1000, self.state_idle)
    # end def

# end class TkBDZombieSprite
