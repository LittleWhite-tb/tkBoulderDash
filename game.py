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
from lib import game_frame as GAME


class Game (TK.Tk):
    """
        game app wrapper;
    """

    def __init__ (self, **kw):
        """
            class constructor;
        """
        # super class inits
        super().__init__()
        # member inits
        self.title("Tkinter Game")
        self.resizable(width=False, height=False)
        self.game = GAME.get_game(self, **kw)
        self.game.pack(padx=5, pady=5)
    # end def


    def run (self, **kw):
        """
            running app;
        """
        # delegate to game frame
        self.game.run(**kw)
        # tkinter events main loop
        self.mainloop()
    # end def

# end class Game


# self-launch script
if __name__ == "__main__":
    # go, buddy!
    Game().run()
# end if
