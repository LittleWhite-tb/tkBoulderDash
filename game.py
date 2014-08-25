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
import tkinter as TK
from lib import tk_boulder_dash as GAME


class Game (TK.Tk):
    """
        wrapper du jeu
    """

    def __init__ (self, **kw):
        """
            class constructor
        """
        # super class inits
        super().__init__()
        # inits fenêtre principale
        self.title(
            "TkBoulderDash: a Python3-Tkinter port of the "
            "famous Boulder Dash\u2122 game"
        )
        self.resizable(width=False, height=False)
        # inits game frame
        self.game = GAME.TkBoulderDash(**kw)
        self.game.pack(padx=5, pady=5)
    # end def


    def run (self, **kw):
        """
            lancement du jeu à proprement parler
        """
        # notification au game frame
        self.game.run(**kw)
        # boucle événementielle principale
        self.mainloop()
    # end def

# end class Game


# si script autonome
if __name__ == "__main__":
    # on lance le jeu
    Game().run()
# end if
