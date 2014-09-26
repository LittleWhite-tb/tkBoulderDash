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


class TkBDBarrierSprite (S.TkGameMatrixSprite):
    """
        Barrier sprite in the mine;
    """

    def init_sprite (self, **kw):
        """
            hook method to be reimplemented in subclass;
            this avoids re-declaring __init__ signatures all the time;
        """
        # member inits
        self.is_overable = False
        self.is_movable = False
        self.locked = False
        # bind events
        self.events.connect("Main:Barrier:Removed", self.destroy)
    # end def


    def destroy (self, *args, **kw):
        """
            falling sprites may remove this sprite;
        """
        # enabled?
        if not self.locked:
            # disable unexpected events
            self.locked = True
            # delete from canvas
            self.canvas.delete(self.canvas_id)
            # delete from matrix
            self.matrix.drop_xy(self.xy)
            # events handling
            self.events.raise_event("Main:Barrier:Removed")
        # end if
    # end def

# end class TkBDBarrierSprite
