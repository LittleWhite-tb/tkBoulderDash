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

    # class constant defs
    # current DB tables and views
    TABLES = ("OPTIONS", "SCORES", "STATS", "GAME_STATS")


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
        # super class inits
        super().dump_tables(*(args or self.TABLES), limit=limit)
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
        return self.get_record("SCORES", row_id)
    # end def


    def get_stats (self):
        """
            retrieves game stats for all levels;
        """
        # get game stats
        return self.get_all("GAME_STATS")
    # end def


    def init_database (self, **kw):
        """
            hook method to be reimplemented in subclass;
        """
        # create tables
        self.sql_script("""\
            -- FIXME: comment out the following lines after debugging
            -- drop table if exists SCORES;
            -- drop table if exists OPTIONS;
            -- drop table if exists STATS;
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
                GAME STATS;
            */
            create table if not exists STATS
            (
                STA_KEY         integer primary key,
                STA_CREATED     date not null default current_date,
                STA_LEVEL       not null unique,
                STA_PLAYED      not null default 0,
                STA_WON         not null default 0,
                STA_BEST_SCORE  not null default 0
            );
            create temporary view GAME_STATS as
                select
                    STA_LEVEL as 'Level',
                    STA_PLAYED as 'Played',
                    STA_WON as 'Won',
                    round(100*STA_WON/STA_PLAYED) as 'Success (%)',
                    STA_BEST_SCORE as 'Best score'
                from STATS
                order by STA_LEVEL asc
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


    def stats_update_played (self, level):
        """
            updates stats data for started/played game level;
        """
        # CAUTION: since UPDATE OR REPLACE does *NOT* work as expected,
        # we must set up default row by ourselves;
        # set default row, if needed
        self.sql_query(
            "insert or ignore into STATS (STA_LEVEL) values (?)",
            level
        )
        # update data
        self.sql_query(
            "update STATS "
            "set STA_PLAYED = STA_PLAYED + 1 "
            "where STA_LEVEL = ?",
            level
        )
    # end def


    def stats_update_won (self, level, score):
        """
            updates stats data for won game level;
        """
        # update data
        self.sql_query(
            "update STATS "
            "set STA_WON = STA_WON + 1, "
            "STA_BEST_SCORE = max(STA_BEST_SCORE, ?) "
            "where STA_LEVEL = ?",
            score, level
        )
    # end def

# end class GameDatabase


# exception handling

class GameDatabaseError (Exception):
    """
        exception handler for GameDatabase class;
    """
    pass
# end class
