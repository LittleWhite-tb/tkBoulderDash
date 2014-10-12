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


class TkBDTreasureSprite (S.TkBDFallingSprite):
    """
        Treasure sprite in the mine;
    """

    # class constants
    STATUS = {
        "default": {
            "loop": True,
            "sequence": True,
            "delay": 200,
        },

        "open": {
            "loop": False,
            "sequence": True,
            "delay": 100,
        },
    }


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
        # event inits
        self.events_dict.update(
            {
                "Game:GoldenKey:Destroyed": self.unlock_treasure,
                "Main:Game:Started": self.game_started,
            }
        )
    # end def


    def unlock_treasure (self, *args, **kw):
        """
            event handler;
            opens treasure when golden key is collected;
        """
        def deferred ():
            self.state = "open"
            self.is_overable = True
            self.is_movable = False
            self.notify_event("Opened")
        # end def
        # deferred changes
        self.animations.run_after(500, deferred)
    # end def

# end class TkBDTreasureSprite
