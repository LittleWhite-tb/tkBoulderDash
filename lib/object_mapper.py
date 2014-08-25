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
        self.collection = list()
        self.dict_ids = dict()
        self.matrix = None
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
        # reset collection
        self.collection = list()
        self.dict_ids = dict()
        self.diamonds_count = 0
        # default value
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
        self.matrix = MX.TkGameMatrix(
            _data["matrix"], _defs, cellsize=self.CELLSIZE
        )
        for _row, _rdata in enumerate(self.matrix.data):
            for _column, _cdata in enumerate(_rdata):
                _attrs = _defs[_cdata]
                _sprite = eval(
                    "{module}.{class}(self, self.canvas)"
                    .format(**_attrs)
                )
                _sprite.images_dir = _attrs["images_dir"]
                _sprite.xy = self.matrix.center_xy(_row, _column)
                _sprite.dict_ids = self.dict_ids
                _sprite.cellsize = self.CELLSIZE
                self.collection.append(_sprite)
                if _cdata == _diamond:
                    self.diamonds_count += 1
                elif _cdata == _player:
                    self.player_sprite = _sprite
                # end if
            # end for
        # end for
        # register events
        self.events.connect_dict(
            {
                "Canvas:Sprite:Created": self.register_sprite,
            }
        )
    # end def


    def register_sprite (self, canvas_id, sprite):
        """
            enregistre un sprite dans la table d'équivalence
        """
        # register sprite
        self.dict_ids[canvas_id] = sprite
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
