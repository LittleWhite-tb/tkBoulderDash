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
from . import tkgame_database as DB


# private module member
__database = None


# app-wide unique instance getter
def get_database (**kw):
    """
        retrieves app-wide unique instance;
    """
    global __database
    if not isinstance(__database, GameDatabase):
        __database = GameDatabase(**kw)
    # end if
    return __database
# end def


class GameDatabase (DB.TkGameDatabase):
    """
        Game database wrapper;
    """

    def get_best_score (self):
        """
            retrieves current best score;
        """
        # get best score
        self.sql_query(
            "select SCO_SCORE from SCORES "
            "order by SCO_SCORE desc limit 1"
        )
        row = self.fetch()
        return row[0] if row else 0
    # end def


    def init_database (self, **kw):
        """
            hook method to be reimplemented in subclass;
        """
        # create tables
        self.sql_script("""\
            /*
                HIGH SCORES and HALL OF FAME;
            */
            create table if not exists SCORES
            (
                SCO_KEY         integer primary key autoincrement,
                SCO_CREATED     date not null default current_date,
                SCO_NAME        not null,
                SCO_SCORE       not null
            );
            /*
                vacuum makes some good clean-ups before starting app;
            */
            vacuum;
        """)
    # end def

# end class GameDatabase


# exception handling

class GameDatabaseError (Exception):
    """
        exception handler for GameDatabase class;
    """
    pass
# end class
