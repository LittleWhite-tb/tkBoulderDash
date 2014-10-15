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
            "insert into SCORES (SCO_NAME, SCO_SCORE) values (?, ?)",
            winner_name, best_score
        )
        # give created row id
        return self.last_row_id
    # end def


    def dump_tables (self, *args, limit=100):
        """
            dumps listed tables to stdout (CLI);
            dumps all tables if @args is omitted;
        """
        # param controls
        if not args:
            args = ("OPTIONS", "SCORES")
        # end if
        # browse table list
        for _table in args:
            # SQL statement
            self.sql_query(
                "select * from '{}' limit {}".format(_table, limit)
            )
            # dump table
            print("\nTable: '{}'".format(_table))
            # get table contents
            _rows = self.fetch(self.ALL)
            # got a recordset?
            if _rows:
                # show description
                print(
                    "Columns:",
                    tuple(c[0] for c in self.cursor.description)
                )
                # dump rows
                print("Rows:")
                for _idx, _row in enumerate(_rows):
                    print("{:03d}:".format(_idx + 1), tuple(_row))
                # end for
            else:
                print("This table is *empty*.")
            # end if
        # end for
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


    def get_hall_of_fame (self):
        """
            retrieves last best scores (hall of fame);
        """
        # get last best scores
        self.sql_query(
            "select SCO_NAME, SCO_SCORE from SCORES "
            "order by SCO_SCORE desc, SCO_CREATED desc limit 7"
        )
        return self.fetch(self.ALL)
    # end def


    def get_option (self, opt_name):
        """
            retrieves app option value along with its @opt_name;
        """
        # get option value
        self.sql_query(
            "select OPT_VALUE from OPTIONS "
            "where OPT_NAME = ? limit 1",
            opt_name
        )
        return self.fetch(default=[None])[0]
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
            -- FIXME: comment out the following lines after debugging
            drop table if exists SCORES;
            drop table if exists OPTIONS;
            /*
                HIGH SCORES and HALL OF FAME;
            */
            create table if not exists SCORES
            (
                -- do *NOT* use autoincrement!
                -- see https://www.sqlite.org/autoinc.html
                SCO_KEY         integer primary key,
                SCO_CREATED     date not null default current_date,
                SCO_NAME        not null,
                SCO_SCORE       not null
            );
            /*
                APP OPTIONS;
            */
            create table if not exists OPTIONS
            (
                OPT_KEY         integer primary key,
                OPT_CREATED     date not null default current_date,
                OPT_NAME        not null unique,
                OPT_VALUE       not null
            );
            /*
                testing and debugging
            */
            insert into SCORES (SCO_NAME, SCO_SCORE)
                values
                    ('fafi le foofoo', 329568),
                    ('chtumlu69', 23587),
                    ('zoubi123568', 12547),
                    ('nom super long de la mort', 1235698),
                    ('toto147', 655878),
                    ('barouette29', 998055),
                    ('bozo le zobo', 6332455),
                    ('miss_tigri56', 2350),
                    ('fornicator45', 500),
                    ('turluru pouet pouet', 123045)
            ;
            /*
                vacuum makes some good clean-ups before starting app;
            */
            vacuum;
        """)
    # end def


    def set_option (self, opt_name, opt_value):
        """
            creates/replaces app option value along with its @opt_name;
        """
        # set option value
        self.sql_query(
            "insert or replace into OPTIONS "
            "(OPT_NAME, OPT_VALUE) values (?, ?)",
            opt_name, opt_value
        )
        # give created row id
        return self.last_row_id
    # end def

# end class GameDatabase


# exception handling

class GameDatabaseError (Exception):
    """
        exception handler for GameDatabase class;
    """
    pass
# end class
