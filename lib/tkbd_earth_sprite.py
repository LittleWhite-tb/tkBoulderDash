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


class TkBDEarthSprite (S.TkGameMatrixSprite):
    """
        sprite représentant la terre dans la mine
    """

    def init_sprite (self, **kw):
        """
            hook method to be reimplemented in subclass;
            this avoids re-declaring __init__ signatures all the time;
        """
        # member inits
        self.is_overable = True
        self.is_movable = False
    # end def


    def destroy (self, *args, **kw):
        """
            un sprite prioritaire détruit ce sprite
        """
        # on retire le sprite du canevas
        self.canvas.delete(self.canvas_id)
        # on notifie que le joueur a creusé la terre
        self.events.raise_event("Main:Earth:Digged")
    # end def

# end class TkBDEarthSprite
