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
        Game special effects:
        canvas flying text along a curve function y = f(x);
        admits vertical vector v = (0, dy);
    """

    def __init__ (self, canvas, **kw):
        """
            class constructor
        """
        # member inits
        self.canvas = canvas
        self.animations = AP.get_animation_pool()
        self.shadow = None
        self.cid_text = 0
        self.cid_shadow = 0
        self.x0, self.y0 = (0, 0)
        self.init_kw(**kw)
    # end def


    def animation_loop (self, startx, starty, stopx, stopy, stepx, stepy, frame=0):
        """
            special effects animation loop;
        """
        print("args:", startx, starty, stopx, stopy, stepx, stepy, frame)
        # can move along a curve?
        if stepx:
            # curve function
            try:
                # y = f(x)
                starty = self.curve(startx)
                print("(startx, starty):", (startx, starty))
            except:
                # do *NOT* change previous value of starty
                pass
            # end try
        else:
            # vertical move
            starty += stepy
        # end if
        # update positions
        startx += stepx
        # rebind values
        if abs(startx) >= abs(stopx):
            startx = stopx
        # end if
        if abs(starty) >= abs(stopy):
            starty = stopy
        # end if
        # update display
        x, y = (self.x0 + startx, self.y0 - starty)
        if self.shadow:
            rx, ry, color = self.shadow
            self.canvas.coords(self.cid_shadow, x + rx, y + ry)
        # end if
        self.canvas.coords(self.cid_text, x, y)
        # should keep on animating?
        if frame < self.frames:
            # update frame
            frame += 1
            # loop again
            self.animations.run_after(
                self.delay, self.animation_loop,
                startx, starty, stopx, stopy, stepx, stepy, frame
            )
        # animation ended
        else:
            # stop all!
            self.stop()
        # end if
    # end def


    def create_text (self, x, y, **options):
        """
            same as canvas.create_text(x, y, **options);
            admits optional shadow=(rx, ry, color);
        """
        # inits
        self.x0, self.y0 = (x, y)
        self.shadow = options.pop("shadow", None)
        self.cid_shadow = 0
        # shadow feature asked?
        if self.shadow:
            # inits
            rx, ry, color = self.shadow
            s_opts = options.copy()
            s_opts.update(fill=color)
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


    def fx_hyperbolic (self, numerator=1):
        """
            curve function y = f(x);
            closure for hyperbolic curve y = a / x;
        """
        return lambda x: numerator / x
    # end def


    def fx_linear (self, coeff=1):
        """
            curve function y = f(x);
            closure for linear curve y = a * x;
        """
        return lambda x: coeff * x
    # end def


    def fx_log (self, amplitude=1):
        """
            curve function y = f(x);
            closure for base-10 logarithmic curve y = a * log10(x);
        """
        return lambda x: amplitude * math.log10(x)
    # end def


    def fx_ln (self, amplitude=1):
        """
            curve function y = f(x);
            closure for natural logarithmic curve y = a * ln(x);
        """
        return lambda x: amplitude * math.log(x)
    # end def


    def fx_quadratic (self, amplitude=1):
        """
            curve function y = f(x);
            closure for quadratic curve y = a * x**2;
        """
        return lambda x: amplitude * x**2
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


    def on_animation_end (self, *args, **kw):
        """
            hook method to be reimplemented in subclass;
            manages the end of a given animation loop;
        """
        # drop text from canvas
        self.canvas.delete(self.cid_shadow)
        self.canvas.delete(self.cid_text)
    # end def


    def start (self, **kw):
        """
            starts animation loop on demand;
        """
        # param inits
        self.init_kw(**kw)
        # param controls
        if not callable(self.curve):
            self.curve = self.fx_linear()
        # end if
        # got something to animate?
        if self.cid_text:
            # inits
            vx, vy = self.vector
            dx = vx / self.frames
            dy = -vy / self.frames
            # run animation loop
            self.animations.run_after(
                self.delay, self.animation_loop, 0, 0, vx, vy, dx, dy
            )
        # no text by there!
        else:
            # error
            raise FXFlyingTextError(
                "no text to animate. "
                "Please, use {0}.create_text() method "
                "to set up some animated text "
                "before calling {0}.start() method."
                .format(__class__.__name__)
            )
        # end if
    # end def


    def stop (self, *args, **kw):
        """
            stops animation loop on demand;
        """
        # stop eventual loop
        self.animations.stop(self.animation_loop)
        # call hook method
        self.on_animation_end()
    # end def

# end class TkGameFXFlyingText



class FXFlyingTextError (Exception):
    """
        exception handler for class TkGameFXFlyingText;
    """
    pass

# end class FXFlyingTextError
