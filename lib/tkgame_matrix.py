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


class TkGameMatrix:
    """
        Game Matrix for Tkinter GUI environment
    """

    # class constants
    TOP_LEFT = "top left"
    TOP_RIGHT = "top right"
    BOTTOM_LEFT = "bottom left"
    BOTTOM_RIGHT = "bottom right"


    def __init__ (self, **kw):
        """
            class constructor
        """
        self.__data = dict()
        self.rows = kw.get("rows") or 0
        self.columns = kw.get("columns") or 0
        self.cellsize = kw.get("cellsize") or 0
        # matrix data support
        self.matrix_data = kw.get("matrix_data")
        if self.matrix_data:
            self.resize(self.matrix_data)
        # end if
    # end def


    def at (self, row_column):
        """
            retrieves object at row_column = (row, column), if exists;
        """
        return self.data[row_column]
    # end def


    def at_xy (self, xy):
        """
            retrieves object at (x, y) converted to matrix (row,
            column) or None if object is not found;
        """
        return self.data[self.row_column(xy)]
    # end def


    def bbox (self):
        """
            returns estimated graphical bounding box of the matrix
        """
        return (0, 0, self.columns * self.cellsize, self.rows * self.cellsize)
    # end def


    @property
    def cellsize (self):
        """
            size of a square matrix cell
        """
        return self.__cellsize
    # end def

    @cellsize.setter
    def cellsize (self, value):
        self.__cellsize = abs(int(value))
    # end def

    @cellsize.deleter
    def cellsize (self):
        del self.__cellsize
    # end def


    def center_xy (self, row_column):
        """
            returns center (x, y) coordinates of a matrix cell
            located at (row, column);
        """
        row, column = row_column
        return (
            (column + 0.5) * self.cellsize, (row + 0.5) * self.cellsize
        )
    # end def


    def corner_xy (self, row_column, corner=None):
        """
            returns top/bottom left/right (x, y) corner coordinates
            of a matrix cell located at (row, column); parameter
            @corner should be one of self.TOP_LEFT, self.TOP_RIGHT,
            self.BOTTOM_LEFT or self.BOTTOM_RIGHT; will default to
            self.TOP_LEFT if omitted or incorrect param value;
        """
        row, column = row_column
        dx, dy = {
            self.TOP_LEFT: (0, 0),
            self.TOP_RIGHT: (1, 0),
            self.BOTTOM_LEFT: (0, 1),
            self.BOTTOM_RIGHT: (1, 1),
        }.get(corner) or (0, 0)
        return (
            (column + dx) * self.cellsize, (row + dy) * self.cellsize
        )
    # end def


    @property
    def data (self):
        """
            matrix internal data (read-only property);
        """
        return self.__data
    # end def

    @data.setter
    def data (self, value):
        """
            forbidden - read-only internal data
        """
        raise MatrixError("data attribute is READ-ONLY.")
    # end def

    @data.deleter
    def data (self):
        del self.__data
    # end def


    def duplicate (self, from_rowcol, to_rowcol, raise_error=False):
        """
            duplicates object located at from_rowcol in to_rowcol
            location;
            if @raise_error is True:
            - raises MatrixCellError if destination is not None,
            - raises MatrixCellError if source is None;
        """
        self.move(from_rowcol, to_rowcol, raise_error, duplicate=True)
    # end def


    def move (self, from_rowcol, to_rowcol,
                                    raise_error=False, duplicate=False):
        """
            absolute move from (row0, column0) to (row1, column1);
            if @raise_error is True:
            - raises MatrixCellError if destination is not None,
            - raises MatrixCellError if source is None;
        """
        # inits
        _object = self.at(to_rowcol)
        # error handling
        if _object and raise_error:
            raise MatrixCellError(
                "while trying to move/duplicate: "
                "destination cell is busy."
            )
        # it's OK, let's try to move
        else:
            # look for source object
            _object = self.at(from_rowcol)
            # got something to move?
            if _object:
                # move it!
                self.set_at(to_rowcol, _object)
                # no duplicata (simple move)?
                if not duplicate:
                    # remove from source location
                    self.data.pop(from_rowcol, None)
                # end if
            # error handling
            elif raise_error:
                raise MatrixCellError(
                    "while trying to move/duplicate: "
                    "no object found in source cell."
                )
            # end if
        # end if
    # end def


    def move_xy (self, from_xy, to_xy,
                                    raise_error=False, duplicate=False):
        """
            absolute move from (row0, column0) to (row1, column1);
            if @raise_error is True:
            - raises MatrixCellError if destination is not None,
            - raises MatrixCellError if source is None;
        """


    def rel_duplicate (self, from_rowcol, rel_rowcol, raise_error=False):
        """
            duplicates object located at from_rowcol to relative
            rel_rowcol location;
            if @raise_error is True:
            - raises MatrixCellError if destination is not None,
            - raises MatrixCellError if source is None;
        """
        self.rel_move(
            from_rowcol, rel_rowcol, raise_error, duplicate=True
        )
    # end def


    def rel_move (self, from_rowcol, rel_rowcol,
                                    raise_error=False, duplicate=False):
        """
            relative move from (row, column) to (row + rel_row,
            column + rel_column);
            if @raise_error is True:
            - raises MatrixCellError if destination is not None,
            - raises MatrixCellError if source is None;
        """
        row, column = from_rowcol
        rr, rc = rel_rowcol
        self.move(
            from_rowcol,
            (row + rr, column + rc),
            raise_error,
            duplicate
        )
    # end def


    def resize (self, matrix_data):
        """
            resizes inner matrix (rows, columns) along with
            @matrix_data; this parameter must be at least a list of
            iterables;
        """
        # inits
        _data = list(matrix_data)
        self.rows = len(_data)
        self.columns = max(0, 0, *map(len, _data))
        # return results
        return (self.rows, self.columns)
    # end def


    def row_column (self, xy):
        """
            converts an xy = (x, y) position to (row, column) position
        """
        x, y = xy
        return (x//self.cellsize, y//self.cellsize)
    # end def


    def set_at (self, row_column, object_):
        """
            sets object at row_column = (row, column);
        """
        self.data[row_column] = object_
    # end def


    def set_at_xy (self, xy, object_):
        """
            sets object at xy = (x, y) converted to matrix (row,
            column);
        """
        self.data[self.row_column(xy)] = object_
    # end def


    def width_height (self):
        """
            returns estimated graphical (width, height) of the matrix
        """
        return (self.columns * self.cellsize, self.rows * self.cellsize)
    # end def

# end class TkGameMatrix


# exception handling

class MatrixError (Exception):
    """
        handles matrix specific errors;
    """
    pass
# end class MatrixError


# exception handling

class MatrixCellError (Exception):
    """
        handles matrix' cell specific errors;
    """
    pass
# end class MatrixCellError
