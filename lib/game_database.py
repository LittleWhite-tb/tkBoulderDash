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

    def _get_record (self, table_name, row_id):
        """
            retrieves an entire record for table @table_name along
            with @row_id row identifier;
        """
        self.sql_query(
            "select * from {} where ROWID = ?".format(table_name),
            row_id
        )
        return self.fetch()
    # end def


    def add_best_score (self, winner_name, best_score):
        """
            adds a new record for winner + best score;
        """
        # insert new record
        self.sql_query(
            "insert into SCORES(SCO_NAME, SCO_SCORE) values (?, ?)",
            winner_name, best_score
        )
        # give created row id
        return self.last_row_id
    # end def


    def get_best_score (self):
        """
            retrieves current best score;
        """
        # get best score
        self.sql_query(
            "select SCO_SCORE from SCORES "
            "order by SCO_SCORE desc limit 1"
        )
        return self.fetch(default=[0])[0]
    # end def


    def get_score_record (self, row_id):
        """
            retrieves score record along with @row_id;
        """
        # get record
        return self._get_record("SCORES", row_id)
    # end def


    def init_database (self, **kw):
        """
            hook method to be reimplemented in subclass;
        """
        # create tables
        self.sql_script("""\
            -- FIXME comment the following once debugging is done:
            drop table if exists SCORES;
            /*
                HIGH SCORES and HALL OF FAME;
            */
            create table if not exists SCORES
            (
                SCO_KEY         integer primary key, -- do NOT use autoincrement!
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
