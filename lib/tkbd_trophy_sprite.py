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
from . import tkbd_falling_sprite as S


class TkBDTrophySprite (S.TkBDFallingSprite):
    """
        Prize sprite in the mine;
    """

    # class constants
    STATUS = {
        "default": {
            "loop": True,
            "sequence": True,
            "delay": 200,
        },

        "open": {
            "loop": True,
            "sequence": True,
            "delay": 100,
        },
    }


    def decrement_diamonds_count (self, *args, **kw):
        """
            event handler;
            decrements Prize-Unlocker Diamond count;
            unlocks prize when count = 0;
        """
        # inits
        self.diamonds_count -= 1
        # should unlock prize?
        if self.diamonds_count <= 0:
            # yes, do it
            self.unlock_prize()
        # end if
    # end def


    def game_started (self, *args, **kw):
        """
            event handler;
            hook method to be reimplemented in subclass;
            game has started;
        """
        def deferred ():
            # raise sprite to foreground
            self.canvas.tag_raise(self.canvas_id, "all")
        # end def
        # deferred action
        self.animations.run_after(2000, deferred)
    # end def


    def increment_diamonds_count (self, *args, **kw):
        """
            event handler;
            increments Prize-Unlocker Diamond count;
        """
        # inits
        self.diamonds_count += 1
        print("pu-diamonds:", self.diamonds_count)
    # end def


    def init_sprite (self, **kw):
        """
            hook method to be reimplemented in subclass;
            this avoids re-declaring __init__ signatures all the time;
        """
        # super class inits
        super().init_sprite(**kw)
        # member inits
        self.is_overable = False
        self.is_movable = True
        self.diamonds_count = 0
        # event inits
        self.events_dict.update(
            {
                "Game:PUDiamond:Started": self.increment_diamonds_count,
                "Game:PUDiamond:Destroyed": self.decrement_diamonds_count,
            }
        )
        # must bind events *RIGHT NOW*
        # if you want to count PUDiamonds /!\
        self.bind_events()
    # end def


    def unlock_prize (self, *args, **kw):
        """
            event handler;
            unlocks prize when all is OK;
        """
        def deferred ():
            self.state = "open"
            self.is_movable = False
            self.is_overable = True
            self.notify_event("Opened")
        # end def
        # deferred action
        self.animations.run_after(500, deferred)
    # end def

# end class TkBDTrophySprite
