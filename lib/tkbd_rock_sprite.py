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
from . import tkgame_sprite as S


class TkBDRockSprite (S.TkGameSprite):
    """
        sprite représentant un rocher dans la mine
    """

    def __init__ (self, owner, canvas, **kw):
        """
            class constructor
        """
        # super class inits
        super().__init__(owner, canvas, **kw)
        # member inits
        self.is_overable = False
        self.is_movable = False
        self.is_falling = False
        self.need_looping = False
    # end def


    def fall_down (self):
        """
            le rocher chute tant qu'il y a du vide sous lui ou
            écrase le joueur s'il le croise durant sa chute;
        """
        self.animations.run_after(100, self.falling_loop)
    # end def


    def falling_loop (self):
        """
            boucle de gestion de la chute du rocher
        """
        self.move_sprite(0, +1, callback=self.filter_collisions)
        if self.need_looping:
            self.animations.run_after(200, self.falling_loop)
        else:
            self.animations.stop(self.falling_loop)
            self.is_falling = False
        # end if
    # end def


    def filter_collisions (self, c_dict):
        """
            traite les collisions pour accorder ou refuser un
            déplacement du sprite;
        """
        # init veille chute
        self.need_looping = True
        # param inits
        sprite = c_dict["sprite"]
        if sprite:
            if sprite is self.owner.player_sprite:
                if self.is_falling:
                    # on écrase le joueur
                    sprite.splashed()
                    self.is_falling = False
                # end if
            else:
                # la chute s'arrête ici
                self.need_looping = False
            # end if
            # mouvement refusé
            return False
        # end if
        # cette fois-ci on tombe
        self.is_falling = True
        # mouvement accordé
        return True
    # end def

# end class TkBDRockSprite
