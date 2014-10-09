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

# lib imports
import os.path as OP
import sqlite3 as DB


# private module member
__database = None


# app-wide unique instance getter
def get_database (**kw):
    """
        retrieves app-wide unique instance;
    """
    global __database
    if not isinstance(__database, TkGameDatabase):
        __database = TkGameDatabase(**kw)
    # end if
    return __database
# end def


class TkGameDatabase:
    """
        TkGame SQLite3 database manager;
    """

    def __init__ (self, **kw):
        """
            class constructor;
        """
        # mandatory inits
        self.db_path = kw.get("db_path") or "data/sqlite3/game.db"
        # hook_method
        self.init_members(**kw)
        # hook method
        self.open_database(**kw)
        # hook method
        self.init_database(**kw)
    # end def


    def close_database (self, *args, **kw):
        """
            event handler;
            closes current database connection, if any;
            raises TkGameDatabaseError otherwise;
        """
        # pending connection?
        if self.connection:
            # commit changes
            self.connection.commit()
            # close database
            self.connection.close()
            # reset members
            self.init_members()
        # no pending connection
        else:
            # throw exception
            raise TkGameDatabaseError(
                "could not close database: "
                "no pending connection by now (DB not open?)."
            )
        # end if
    # end def


    def commit (self, *args, **kw):
        """
            event handler;
            commits current pending transaction in database;
            raises TkGameDatabaseError otherwise;
        """
        # pending connection?
        if self.connection:
            # commit transaction
            self.connection.commit()
        # no pending connection
        else:
            # throw exception
            raise TkGameDatabaseError(
                "could not commit current transaction in database: "
                "no pending connection by now (DB not open?)."
            )
        # end if
    # end def


    @property
    def db_path (self):
        """
            database pathname (canonized);
        """
        return self.__db_path
    # end def


    @db_path.setter
    def db_path (self, value):
        self.__db_path = OP.abspath(OP.expanduser(value))
    # end def


    @db_path.deleter
    def db_path (self):
        del self.__db_path
    # end def


    def init_database (self, **kw):
        """
            hook method to be reimplemented in subclass;
        """
        pass
    # end def


    def init_members (self, **kw):
        """
            hook method to be reimplemented in subclass;
        """
        # member inits
        self.connection = None
        self.cursor = None
    # end def


    def open (self, *args, **kw):
        """
            event handler;
            opens database along with self.db_path DB pathname;
        """
        # open database
        self.connection = DB.connect(self.db_path)
        # get cursor
        self.cursor = self.connection.cursor()
    # end def


    def rollback (self, *args, **kw):
        """
            event handler;
            commits current pending transaction in database;
            raises TkGameDatabaseError otherwise;
        """
        # pending connection?
        if self.connection:
            # commit transaction
            self.connection.commit()
        # no pending connection
        else:
            # throw exception
            raise TkGameDatabaseError(
                "could not commit current transaction in database: "
                "no pending connection by now (DB not open?)."
            )
        # end if
    # end def


    def sql_query (self, sql, *args, **kw):
        """
            executes a unique SQL statement;
            use sql_script() for many SQL statements;
        """
        # enabled?
        if self.cursor:
            # execute SQL statement
            self.cursor.execute(sql, args or kw)
        else:
            # throw exception
            raise TkGameDatabaseError(
                "could not execute SQL statement: "
                "no pending cursor by now."
            )
        # end if
    # end def


    def sql_script (self, script):
        """
            executes an SQL multiple statements script;
            use sql_query() if you're looking for only one SQL
            statement with optional arguments;
        """
        # enabled?
        if self.cursor:
            # execute SQL statement
            self.cursor.executescript(script)
        else:
            # throw exception
            raise TkGameDatabaseError(
                "could not execute SQL script: "
                "no pending cursor by now."
            )
        # end if
    # end def

# end class TkGameDatabase


# exception handling

class TkGameDatabaseError (Exception):
    """
        exception handler for TkGameDatabase class;
    """
    pass
# end class
