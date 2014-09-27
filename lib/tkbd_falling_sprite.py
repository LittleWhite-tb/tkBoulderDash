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

    def can_move_over (self, sprite):
        """
            determines if current sprite may move over @sprite;
        """
        return (not sprite) or ("background" in sprite.role)
    # end def


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
        self.locked = False
    # end def


    def fall_down (self):
        """
            sprite has been asked to fall down;
        """
        # no locked sprite nor pending falldown loop?
        if not (self.locked or self.need_looping):
            # ok, let's go!
            self.animations.run_after(150, self.falling_loop)
        # end if
    # end def


    def falling_loop (self, has_fallen=False):
        """
            sprite falling down animation loop;
        """
        # evaluate falldown
        _fallen = self.move_sprite(0, +1, callback=self.falling_collisions)
        if self.need_looping and not self.locked:
            self.animations.run_after(100, self.falling_loop, _fallen)
        else:
            self.animations.stop(self.falling_loop)
            self.is_falling = False
            if has_fallen:
                self.touched_down()
            # end if
        # end if
    # end def


    def falling_collisions (self, c_dict):
        """
            allows or denies movement along with collision tests;
        """
        # inits
        self.need_looping = True
        # param inits
        sprite = c_dict["sprite"]
        if sprite:
            if "player" in sprite.role:
                if self.is_falling:
                    # splash the player!
                    sprite.splashed()
                    self.is_falling = False
                # end if
            # background sprite?
            elif "background" in sprite.role:
                # remove background sprite
                sprite.destroy()
                # now falling down
                self.is_falling = True
                # allowed movement
                return True
            # need to roll aside?
            elif isinstance(sprite, __class__):
                # depends on whatever is around
                self.need_looping = self.may_roll_over()
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


    def may_roll_over (self):
        """
            determines if sprite may roll aside over one another;
        """
        # loop on directions (left/right)
        for sx in (-1, +1):
            _s1 = self.look_ahead(sx, 0)["sprite"]
            _s2 = self.look_ahead(sx, +1)["sprite"]
            _roll = bool(
                self.can_move_over(_s1) and self.can_move_over(_s2)
            )
            # may roll over?
            if not self.locked and _roll:
                # free some space
                if _s1: _s1.destroy()
                if _s2: _s2.destroy()
                # move sprite
                self.move_sprite(sx, 0, lambda c: not c["sprite" ])
                # keep on falling
                return True
            # end if
        # end for
        # stop falling
        return False
    # end def


    def touched_down (self):
        """
            hook method to be implemented by subclass;
        """
        pass
    # end def

# end class TkBDFallingSprite
