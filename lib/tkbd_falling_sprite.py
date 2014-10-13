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
from . import tkbd_base_sprite as S


class TkBDFallingSprite (S.TkBDBaseSprite):
    """
        Generic falling sprite in the mine;
    """

    def can_move_over (self, sprite):
        """
            hook method to be reimplemented in subclass;
            determines if current sprite may move over @sprite;
        """
        return (not sprite) or ("background" in sprite.role)
    # end def


    def destroy (self, *args, **kw):
        """
            event handler for sprite destruction;
            should be reimplemented in subclass;
        """
        # enabled?
        if not self.locked:
            # stop animations
            self.animations.lock(self.falling_loop)
            # super class inits
            super().destroy(*args, **kw)
        # end if
    # end def


    def fall_down (self):
        """
            sprite has been asked to fall down;
        """
        # enabled?
        if not (self.locked or self.need_looping):
            # lock sprite for further operations
            self.need_looping = True
            # ok, let's go!
            self.animations.run_after(100, self.falling_loop)
        # end if
    # end def


    def falling_collisions (self, c_dict):
        """
            allows or denies movement along with collision tests;
        """
        # security
        if self.locked:
            return False
        # end if
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


    def falling_loop (self, has_fallen=False):
        """
            sprite falling down animation loop;
        """
        # security
        if self.locked:
            return False
        # end if
        # evaluate falldown
        _fallen = self.move_sprite(0, +1, callback=self.falling_collisions)
        if self.need_looping:
            self.animations.run_after(100, self.falling_loop, _fallen)
        else:
            self.animations.stop(self.falling_loop)
            self.is_falling = False
            if has_fallen:
                self.touched_down()
            # end if
        # end if
    # end def


    def has_moved (self, c_dict):
        """
            hook method to be reimplemented in subclass;
            determines if sprite can be pushed in the given
            direction, provided it is an horizontal one;
        """
        # no vertical pushes admitted here
        if c_dict["sy"] or not self.is_movable:
            return False
        # end if
        # horizontal moves
        _moved = self.move_sprite(
            c_dict["sx"], 0, lambda c: self.can_move_over(c["sprite"])
        )
        if _moved:
            self.notify_event("Pushed")
        # end if
        return _moved
    # end def


    def init_sprite (self, **kw):
        """
            hook method to be reimplemented in subclass;
            this avoids re-declaring __init__ signatures all the time;
        """
        # super class inits
        super().init_sprite(**kw)
        # member inits
        self.is_falling = False
        self.need_looping = False
    # end def


    def may_roll_over (self):
        """
            determines if sprite may roll aside over one another;
        """
        # security
        if self.locked:
            return False
        # end if
        # loop on directions (left/right)
        for sx in (-1, +1):
            _s1 = self.look_ahead(sx, 0)["sprite"]
            _s2 = self.look_ahead(sx, +1)["sprite"]
            _roll = bool(
                self.can_move_over(_s1) and self.can_move_over(_s2)
            )
            # may roll over?
            if _roll:
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
        # notify gameplay
        self.notify_event("TouchedDown")
    # end def

# end class TkBDFallingSprite
