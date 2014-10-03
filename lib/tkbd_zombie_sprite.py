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
from . import tkgame_matrix_sprite as S


class TkBDZombieSprite (S.TkGameMatrixSprite):
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
            "delay": 100,
        },

        "die_right": {
            "loop": False,
            "sequence": True,
            "delay": 100,
        },
    }


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
            else:
                # denied movement
                return False
            # end if
        # end if
        # allowed movement
        return True
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
    # end def


    def move_animation (self, c_dict):
        """
            sprite moving animation;
        """
        # super class move_animation
        super().move_animation(c_dict)
        # zombie sprite moved
        self.events.raise_event("Main:Zombie:Moved")
    # end def


    def move_down (self, *args, **kw):
        """
            moves down;
        """
        self.move_sprite(0, +1, callback=self.filter_collisions)
    # end def


    def move_left (self, *args, **kw):
        """
            moves left;
        """
        self.direction = "left"
        self.state = "walk_left"
        self.move_sprite(-1, 0, callback=self.filter_collisions)
        self.animations.run_after(500, self.state_idle)
    # end def


    def move_right (self, *args, **kw):
        """
            moves right;
        """
        self.direction = "right"
        self.state = "walk_right"
        self.move_sprite(+1, 0, callback=self.filter_collisions)
        self.animations.run_after(500, self.state_idle)
    # end def


    def move_up (self, *args, **kw):
        """
            moves up;
        """
        self.move_sprite(0, -1, callback=self.filter_collisions)
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

# end class TkBDZombieSprite
