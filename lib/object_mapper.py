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
import os.path as OP
import json
from . import tkgame_events as EM
from . import tkgame_matrix as MX


class ObjectMapper:
    """
        Game level objects mapper;
    """

    # class constants
    CELLSIZE = 64       # in pixels


    def __init__ (self, canvas, images_dir=None):
        """
            class constructor
        """
        self.canvas = canvas
        self.images_dir = images_dir
        self.events = EM.get_event_manager()
        self.matrix = MX.TkGameMatrix(cellsize=self.CELLSIZE)
        self.player_sprite = None
        self.falling_sprites = None
        self.countdown = 0
        self.diamonds_count = 0
    # end def


    def load_data (self, file_path):
        """
            loads data from game level JSON file;
        """
        # inits
        _fpath = OP.abspath(OP.expanduser(file_path))
        # data file *MUST* exist /!\
        with open(_fpath) as file_in:
            _data = json.load(file_in)
        # end with
        # reset members
        self.countdown = int(_data.get("countdown") or 600)
        self.diamonds_count = 0
        self.falling_sprites = list()
        # default values
        _diamond = "D"
        _player = "P"
        # def inits
        _defs = _data["defs"]
        # rebuild data
        for key, defs in _defs.items():
            # lib imports
            exec("from . import {module}".format(**defs))
            # update images dir
            defs["images_dir"] = OP.abspath(
                OP.join(self.images_dir, defs["images_dir"])
            )
            defs["role"] = str(defs["role"]).lower()
            if "diamond" in defs["role"]:
                # here is the diamond char
                _diamond = key
            elif "player" in defs["role"]:
                # here is the player char
                _player = key
            # end if
        # end for
        # init game matrix
        self.matrix.resize(_data["matrix"])
        self.matrix.defs = _defs
        for _row, _rdata in enumerate(_data["matrix"]):
            for _column, _cdata in enumerate(_rdata):
                # _cdata *MUST* be defined in defs /!\
                _attrs = _defs[_cdata]
                # create sprite
                _sprite = eval(
                    "{module}.{class}(self, self.matrix, self.canvas)"
                    .format(**_attrs)
                )
                _sprite.images_dir = _attrs["images_dir"]
                _sprite.row_column = (_row, _column)
                # put sprite into game matrix
                self.matrix.set_at((_row, _column), _sprite)
                # feed falling sprites list
                if hasattr(_sprite, "fall_down"):
                    self.falling_sprites.append(_sprite)
                # end if
                # special cases
                if _cdata == _diamond:
                    self.diamonds_count += 1
                elif _cdata == _player:
                    self.player_sprite = _sprite
                # end if
            # end for
        # end for
    # end def


    @property
    def images_dir (self):
        """
            root images directory for objects in collection;
        """
        return self.__images_dir
    # end def

    @images_dir.setter
    def images_dir (self, value):
        self.__images_dir = OP.abspath(OP.expanduser(value))
    # end def

    @images_dir.deleter
    def images_dir(self):
        del self.__images_dir
    # end def

# end class ObjectMapper
