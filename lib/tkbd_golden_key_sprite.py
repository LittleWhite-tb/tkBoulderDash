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


class TkBDGoldenKeySprite (S.TkBDDiamondSprite):
    """
        Treasure/Golden Key sprite in the mine;
    """

    def get_event_name (self):
        """
            hook method to be reimplemented in subclass;
            returns current 'event name' for this sprite class;
        """
        # concerned event names:
        # "Game:{}:Collected"
        # "Game:{}:TouchedDown"
        return "GoldenKey"
    # end def

# end class TkBDGoldenKeySprite