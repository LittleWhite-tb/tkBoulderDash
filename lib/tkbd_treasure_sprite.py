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
from . import tkbd_diamond_sprite as S


class TkBDTreasureSprite (S.TkBDDiamondSprite):
    """
        Treasure/Golden Key sprite in the mine;
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


    def bind_events (self, *args, **kw):
        """
            class event bindings;
        """
        # bind events
        self.events.connect_dict(self.events_dict)
    # end def


    def game_started (self, *args, **kw):
        """
            event handler for game start;
        """
        # raise sprite to foreground
        self.canvas.tag_raise(self.canvas_id, "all")
    # end def


    def get_event_name (self):
        """
            hook method to be reimplemented in subclass;
            returns current 'event name' for this sprite class;
        """
        # concerned event names:
        # "Game:{}:Collected"
        # "Game:{}:Pushed"
        # "Game:{}:TouchedDown"
        return "Treasure"
    # end def


    def has_moved (self, c_dict):
        """
            determines if the treasure can be pushed in the given
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
        self.is_overable = False
        self.is_movable = True
        # event inits
        self.events_dict = {
            "Main:Game:Started": self.game_started,
            "Game:GoldenKey:Collected": self.unlock_treasure,
        }
    # end def


    def unbind_events (self, *args, **kw):
        """
            class event unbindings;
        """
        # unbind events
        self.events.disconnect_dict(self.events_dict)
    # end def


    def unlock_treasure (self, *args, **kw):
        """
            event handler;
            opens treasure when golden key is collected;
        """
        self.state = "open"
        self.is_movable = False
        self.is_overable = True
        self.events.raise_event("Game:Treasure:Opened", sprite=self)
    # end def

# end class TkBDTreasureSprite
