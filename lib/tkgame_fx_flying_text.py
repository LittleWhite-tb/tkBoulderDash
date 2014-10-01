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

import math
import tkinter.constants as TK
from . import tkgame_animations as AP


class TkGameFXFlyingText:
    """
        Game special effects: canvas flying text;
    """

    def __init__ (self, canvas, **kw):
        """
            class constructor
        """
        # member inits
        self.canvas = canvas
        self.animations = AP.get_animation_pool()
        self.cid_text = 0
        self.cid_shadow = 0
        self.x0, self.y0 = (0, 0)
        self.init_kw(**kw)
    # end def


    def animation_loop (self, startx, starty, stopx, stopy, stepx, stepy):
        """
            special effects animation loop;
        """
        # inits
        # loop again
        self.animations.run_after(
            self.delay, self.animation_loop,
            startx, starty, stopx, stopy, stepx, stepy
        )
    # end def


    def create_text (self, x, y, **options):
        """
            same as canvas.create_text(x, y, **options);
            admits optional shadow=(rx, ry, color);
        """
        # inits
        self.x0, self.y0 = (x, y)
        shadow = options.pop("shadow", None)
        self.cid_shadow = 0
        # shadow feature asked?
        if shadow:
            # inits
            rx, ry, color = shadow
            s_opts = options.copy().update(fill=color)
            # create shadow text
            self.cid_shadow = self.canvas.create_text(
                x + rx, y + ry, **s_opts
            )
        # end if
        # create text
        self.cid_text = self.canvas.create_text(x, y, **options)
        # set text above all
        self.canvas.tag_raise(self.cid_shadow, TK.ALL)
        self.canvas.tag_raise(self.cid_text, TK.ALL)
    # end def


    def fx_hyperbolic (self, x):
        """
            curve function y = f(x);
            hyperbolic curve y = 1/x;
        """
        return 1.0/x
    # end def


    def fx_linear (self, x):
        """
            curve function y = f(x);
            linear curve y = x;
        """
        return x
    # end def


    def fx_log (self, x):
        """
            curve function y = f(x);
            base-10 logarithmic curve y = log10(x);
        """
        return math.log10(x)
    # end def


    def fx_ln (self, x):
        """
            curve function y = f(x);
            natural logarithmic curve y = ln(x);
        """
        return math.log(x)
    # end def


    def fx_quadratic (self, x):
        """
            curve function y = f(x);
            quadratic curve y = x**2;
        """
        return x**2
    # end def


    def init_kw (self, **kw):
        """
            member keyword inits;
        """
        # keyword inits
        self.delay = kw.get("delay") or 100
        self.vector = kw.get("vector") or (0, -100)
        self.frames = kw.get("frames") or 10
        self.curve = kw.get("curve")
    # end def


    def start (self, **kw):
        """
            starts animation loop on demand;
        """
        # param inits
        self.init_kw(**kw)
        # param controls
        if not callable(self.curve):
            self.curve = self.fx_linear
        # end if
        # inits
        vx, vy = self.vector
        dx = vx / self.frames
        dy = vy / self.frames
        # run animation loop
        self.animations.run_after(
            self.delay, self.animation_loop, 0, 0, vx, vy, dx, dy
        )
    # end def

# end class TkGameFXFlyingText
