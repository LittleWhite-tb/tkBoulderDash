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
            # lock sprite for unexpected events
            self.locked = True
            # ancestor first
            super().destroy(*args, **kw)
            # events handling
            self.events.raise_event(
                "Game:{}:Collected".format(self.get_event_name()),
                sprite=self
            )
        # end if
    # end def


    def get_event_name (self):
        """
            hook method to be reimplemented in subclass;
            returns current 'event name' for this sprite class;
        """
        return "Diamond"
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


    def update_image_animation_loop (self):
        """
            updates sprite's image animation loop;
        """
        # allowed to proceed?
        if self.started:
            self.animations.run_after(
                100 + 100 * random.randint(1, 10),
                self.image_animation_loop
            )
        # end if
    # end def

# end class TkBDDiamondSprite
