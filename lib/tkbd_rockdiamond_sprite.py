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
from . import tkbd_rock_sprite as R
from . import tkbd_diamond_sprite as D


class TkBDRockDiamondSprite (R.TkBDRockSprite, D.TkBDDiamondSprite):
    """
        Magic Rock changing to Diamond sprite in the mine;
    """

    # class constants
    STATUS = {
        "default": {
            "loop": True,
            "sequence": True,
            "delay": 200,
        },

        "change": {
            "loop": False,
            "sequence": True,
            "delay": 50,
        },

        "diamond": {
            "loop": True,
            "sequence": True,
            "delay": 100,
        },
    }

    def init_sprite (self, **kw):
        """
            hook method to be reimplemented in subclass;
            this avoids re-declaring __init__ signatures all the time;
        """
        # super class inits
        super().init_sprite(**kw)
        # member inits
        self.is_movable = True
        self.is_overable = False
    # end def


    def on_sequence_end (self, *args, **kw):
        """
            on image animation sequence end;
        """
        # state has changed
        self.state = "diamond"
        self.is_movable = False
        self.is_overable = True
        # notify game frame
        self.notify_event("Changed")
    # end def


    def touched_down (self):
        """
            hook method to be implemented by subclasses;
        """
        # current sprite is still a rock?
        if self.state == "default":
            # who's below?
            sprite = self.look_ahead(0, +1)["sprite"]
            # current sprite may change only when falling down
            # on a rock-like sprite!
            if "rock" in sprite.role:
                self.state = "change"
                self.notify_event("Changing")
            else:
                # rock part has touched down
                self.notify_event("TouchedDown")
            # end if
        # became a diamond
        else:
            # diamond part has touched down
            self.notify_event("TouchedDown")
        # end if
    # end def

# end class TkBDRockDiamondSprite
