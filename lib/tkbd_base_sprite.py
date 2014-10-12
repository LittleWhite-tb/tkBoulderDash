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


class TkBDBaseSprite (S.TkGameMatrixSprite):
    """
        TkBoulderDash game base sprite (root ancestor);
    """

    def bind_events (self, *args, **kw):
        """
            event handler;
            hook method to be reimplemented in subclass;
            class event bindings;
        """
        self.events.connect_dict(self.events_dict)
    # end def


    def game_over (self, *args, **kw):
        """
            event handler;
            hook method to be reimplemented in subclass;
            game is over;
        """
        pass
    # end def


    def game_resumed (self, *args, **kw):
        """
            event handler;
            hook method to be reimplemented in subclass;
            game is resumed;
        """
        # inits
        self.game_paused = False
    # end def


    def game_started (self, *args, **kw):
        """
            event handler;
            hook method to be reimplemented in subclass;
            game has started;
        """
        pass
    # end def


    def game_suspended (self, *args, **kw):
        """
            event handler;
            hook method to be reimplemented in subclass;
            game is paused;
        """
        # inits
        self.game_paused = True
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
        self.is_movable = False
        self.game_paused = False
        self.events_dict = {
            #~ "Main:Game:Over": self.game_over,
            #~ "Main:Game:Paused": self.game_suspended,
            #~ "Main:Game:Resumed": self.game_resumed,
            "Main:Game:Started": self.game_started,
        }
    # end def


    @property
    def sprite_name (self):
        """
            READ-ONLY property;
            hook method to be reimplemented in subclass;
            returns sprite's genuine name (case-sensitive);
            you may define some logic along with your own sprite
            naming convention;
        """
        # tkBoulderDash Naming Convention:
        # TkBD{sprite_name}Sprite
        return self.class_name[4:-6]
    # end def


    def unbind_events (self, *args, **kw):
        """
            event handler;
            hook method to be reimplemented in subclass;
            class event unbindings;
        """
        self.events.disconnect_dict(self.events_dict)
    # end def

# end class TkBDBaseSprite
