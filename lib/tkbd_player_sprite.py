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
from . import tkbd_base_sprite as S


class TkBDPlayerSprite (S.TkBDBaseSprite):
    """
        Player's sprite avatar;
    """

    # class constants
    STATUS = {

        "default": {
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

        "frozen": {
            "loop": False,
            "sequence": True,
            "delay": 50,
        },

        "splashed": {
            "loop": False,
            "sequence": True,
            "delay": 50,
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
            # touched an enemy?
            if "enemy" in sprite.role:
                # player is dead!
                self.freeze()
            # is overable?
            elif sprite.is_overable:
                # run over it!
                sprite.destroy()
            # is pushable?
            elif sprite.is_movable:
                # player may move only if sprite has moved
                return sprite.has_moved(c_dict)
            else:
                # denied movement
                return False
            # end if
        # end if
        # allowed movement
        return True
    # end def


    def freeze (self, *args, **kw):
        """
            player has been frozen by an enemy;
        """
        # enabled?
        if not self.locked:
            self.animations.lock(self.player_idle)
            self.state = "frozen"
            self.notify_event("Frozen")
        # end if
    # end def


    def move_down (self, *args, **kw):
        """
            moves down;
        """
        # move sprite
        self.move_sprite(0, +1, callback=self.filter_collisions)
    # end def


    def move_left (self, *args, **kw):
        """
            moves left;
        """
        # move sprite
        self.state = "walk_left"
        self.move_sprite(-1, 0, callback=self.filter_collisions)
        self.animations.run_after(500, self.player_idle)
    # end def


    def move_right (self, *args, **kw):
        """
            moves right;
        """
        # move sprite
        self.state = "walk_right"
        self.move_sprite(+1, 0, callback=self.filter_collisions)
        self.animations.run_after(500, self.player_idle)
    # end def


    def move_up (self, *args, **kw):
        """
            moves up;
        """
        # move sprite
        self.move_sprite(0, -1, callback=self.filter_collisions)
    # end def


    def on_sequence_end (self, *args, **kw):
        """
            on image animation sequence end;
        """
        # player is dead
        self.destroy(*args, **kw)
    # end def


    def player_idle (self, *args, **kw):
        """
            player waits for events;
        """
        # player is idle
        self.state = "default"
    # end def


    def splashed (self, *args, **kw):
        """
            player has been splashed;
        """
        # enabled?
        if not self.locked:
            self.animations.lock(self.player_idle)
            self.state = "splashed"
            self.notify_event("Splashed")
        # end if
    # end def

# end class TkBDPlayerSprite
