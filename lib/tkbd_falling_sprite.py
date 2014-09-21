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


class TkBDFallingSprite (S.TkGameMatrixSprite):
    """
        Generic falling sprite in the mine;
    """

    def init_sprite (self, **kw):
        """
            hook method to be reimplemented in subclass;
            this avoids re-declaring __init__ signatures all the time;
        """
        # member inits
        self.is_overable = False
        self.is_movable = False
        self.is_falling = False
        self.need_looping = False
    # end def


    def fall_down (self):
        """
            sprite has been asked to fall down;
        """
        self.animations.run_after(150, self.falling_loop)
    # end def


    def falling_loop (self):
        """
            sprite falling down animation loop;
        """
        # got something above?
        c_dict = self.look_ahead(0, -1)
        sprite = c_dict["sprite"]
        if sprite and hasattr(sprite, "fall_down"):
            # make it fall
            sprite.fall_down()
        # end if
        self.move_sprite(0, +1, callback=self.filter_collisions)
        if self.need_looping:
            self.animations.run_after(100, self.falling_loop)
        else:
            self.animations.stop(self.falling_loop)
            self.is_falling = False
            self.touched_down()
        # end if
    # end def


    def filter_collisions (self, c_dict):
        """
            allows or denies movement along with collision tests;
        """
        # inits
        self.need_looping = True
        # param inits
        sprite = c_dict["sprite"]
        if sprite:
            if sprite is self.owner.player_sprite:
                if self.is_falling:
                    # splash the player!
                    sprite.splashed()
                    self.is_falling = False
                # end if
            else:
                # no more falling down
                self.need_looping = False
            # end if
            # denied movement
            return False
        # end if
        # now falling down
        self.is_falling = True
        # allowed movement
        return True
    # end def


    def touched_down (self):
        """
            hook method to be implemented by subclasses;
        """
        pass
    # end def

# end class TkBDFallingSprite
