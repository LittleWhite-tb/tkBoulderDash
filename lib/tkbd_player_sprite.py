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


class TkBDPlayerSprite (S.TkGameMatrixSprite):
    """
        sprite représentant le joueur
    """

    # class constants
    STATUS = {
        "default": {
            "loop": True,
            "sequence": True,
            "delay": 200,
        },

        "walk_left": {
            "loop": True,
            "sequence": True,
            "delay": 100,
        },

        "walk_right": {
            "loop": True,
            "sequence": True,
            "delay": 100,
        },

        "splashed": {
            "loop": False,
            "sequence": True,
            "delay": 40,
        },
    }

    def init_sprite (self, **kw):
        """
            hook method to be reimplemented in subclass;
            this avoids re-declaring __init__ signatures all the time;
        """
        # member inits
        pass
    # end def


    def move_up (self, *args, **kw):
        """
            déplace le joueur vers le haut
        """
        self.move_sprite(0, -1, callback=self.filter_collisions)
    # end def


    def move_down (self, *args, **kw):
        """
            déplace le joueur vers le bas
        """
        self.move_sprite(0, +1, callback=self.filter_collisions)
    # end def


    def move_left (self, *args, **kw):
        """
            déplace le joueur vers la gauche
        """
        self.state = "walk_left"
        self.move_sprite(-1, 0, callback=self.filter_collisions)
        self.animations.run_after(500, self.player_idle)
    # end def


    def move_right (self, *args, **kw):
        """
            déplace le joueur vers la droite
        """
        self.state = "walk_right"
        self.move_sprite(+1, 0, callback=self.filter_collisions)
        self.animations.run_after(500, self.player_idle)
    # end def


    def filter_collisions (self, c_dict):
        """
            traite les collisions pour accorder ou refuser un
            déplacement du sprite;
        """
        # init sprite détecté en collision
        sprite = c_dict["sprite"]
        # on a un sprite ?
        if sprite:
            # sprite écrasable?
            if sprite.is_overable:
                # on a priorité sur le sprite détecté
                # on peut le dégager
                sprite.destroy()
            else:
                # mouvement refusé
                return False
            # end if
        # end if
        # mouvement accordé
        return True
    # end def


    def move_animation (self, c_dict):
        """
            gestionnaire boucle animation mouvement du sprite
        """
        # super class move_animation
        super().move_animation(c_dict)
        # y a-t-il un rocher au-dessus ?
        c_dict = self.look_ahead(0, -1)
        sprite = c_dict["sprite"]
        if sprite and hasattr(sprite, "fall_down"):
            # fait tomber ce qui le peut
            sprite.fall_down()
        # end if
    # end def


    def player_idle (self, *args, **kw):
        """
            le joueur revient en position d'attente
        """
        # player is idle
        self.state = "default"
    # end def


    def splashed (self, *args, **kw):
        """
            un rocher vient de nous écraser...
        """
        self.events.raise_event("Main:Player:Splashed")
        self.animations.stop(self.player_idle)
        self.state = "splashed"
    # end def


    def on_sequence_end (self, *args, **kw):
        """
            méthode virtuelle à réimplémenter dans les classes dérivées
        """
        # player is dead
        self.canvas.delete(self.canvas_id)
        self.matrix.drop_xy(self.xy)
        self.canvas.create_text(
            self.x+3, self.y+3,
            text="Bobo!",
            font="bdcartoonshout 32 bold",
            fill="black",
        )
        self.canvas.create_text(
            self.x, self.y,
            text="Bobo!",
            font="bdcartoonshout 32 bold",
            fill="khaki1",
        )
        self.events.raise_event("Main:Player:Dead")
    # end def

# end class TkBDPlayerSprite
