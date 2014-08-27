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
        collectionneur d'objets appartenant à un même niveau de jeu
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
        self.diamonds_count = 0
    # end def


    def load_data (self, file_path):
        """
            charge les données du niveau de jeu et crée la collection
        """
        # inits
        _fpath = OP.abspath(OP.expanduser(file_path))
        # présence du fichier data obligatoire /!\
        with open(_fpath) as file_in:
            _data = json.load(file_in)
        # end with
        # inits
        _defs = _data["defs"]
        # reset members
        self.dict_ids = dict()
        self.diamonds_count = 0
        # default values
        _diamond = "D"
        _player = "P"
        # on reconstruit les données
        for key, defs in _defs.items():
            # lib imports
            exec("from . import {module}".format(**defs))
            # update images folder
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
                    "{module}.{class}(self.matrix, self.canvas)"
                    .format(**_attrs)
                )
                _sprite.images_dir = _attrs["images_dir"]
                _sprite.row_column = (_row, _column)
                # put sprite into game matrix
                self.matrix.set_at((_row, _column), _sprite)
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
            répertoire d'images des objets gérés
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
