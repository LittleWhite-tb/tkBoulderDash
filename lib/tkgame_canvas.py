#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    tkGAME - all-in-one Game library for Tkinter

    Copyright (c) 2014+ Raphaël Seban <motus@laposte.net>

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
import tkinter as TK
from . import tkgame_basewidget as BW


# private module member
__game_canvas = None


# app-wide unique instance getter
def get_canvas (master=None, **options):
    """
        retrieves app-wide unique instance;
    """
    global __game_canvas
    if not isinstance(__game_canvas, TkGameCanvas):
        __game_canvas = TkGameCanvas(master, **options)
    # end if
    return __game_canvas
# end def


class TkGameCanvas (BW.TkGameBaseWidget, TK.Canvas):
    """
        Game specific tkinter Canvas widget;
    """

    # predefined options
    CONFIG = dict(
        bg="black",
        highlightthickness=0,
        width=800,
        height=600,
        scrollregion=(0, 0, 0, 0),
    )


    def __init__ (self, master=None, **options):
        """
            class constructor;
        """
        # super class inits
        self._safe_init(TK.Canvas, master, **options)
    # end def

# end class TkGameCanvas
