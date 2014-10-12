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
from . import tkbd_falling_sprite as S


class TkBDDiamondSprite (S.TkBDFallingSprite):
    """
        Diamond sprite in the mine;
    """

    # class constants
    STATUS = {
        "default": {
            "loop": True,
            "sequence": True,
            "delay": 100,
        },
    }


    def destroy (self, *args, **kw):
        """
            player caught the diamond;
        """
        # enabled?
        if not self.locked:
            # super class inits
            super().destroy(*args, **kw)
            # notify gameplay
            self.events.raise_event(
                self.get_event_name("Collected"), sprite=self
            )
        # end if
    # end def


    def has_moved (self, c_dict):
        """
            hook method to be reimplemented in subclass;
            determines if sprite can be pushed in the given
            direction, provided it is an horizontal one;
        """
        # no vertical pushes admitted here
        if c_dict["sy"]:
            return False
        # end if
        # horizontal moves
        _moved = self.move_sprite(
            c_dict["sx"], 0, lambda c: not c["sprite"]
        )
        if _moved:
            self.events.raise_event(
                "Game:{}:Pushed".format(self.get_event_name()),
                sprite=self
            )
        # end if
        return _moved
    # end def


    def init_sprite (self, **kw):
        """
            hook method to be reimplemented in subclass;
            this avoids re-declaring __init__ signatures all the time;
        """
        # super class inits
        super().init_sprite(**kw)
        # member inits
        self.is_overable = True
        self.is_movable = False
    # end def


    def on_start (self, *args, **kw):
        """
            hook method to be reimplemented in subclass;
            this happens just after self.start() has been called;
        """
        # enter the loop (delayed)
        self.animations.run_after(
            100 + 100 * random.randint(1, 10),
            self.update_image_animation_loop
        )
        # event bindings
        self.bind_events()
    # end def


    def touched_down (self):
        """
            hook method to be implemented by subclass;
        """
        self.events.raise_event(
            "Game:{}:TouchedDown".format(self.get_event_name()),
            sprite=self
        )
    # end def

# end class TkBDDiamondSprite
