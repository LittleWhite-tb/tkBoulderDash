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
from . import tkbd_barrier_sprite as S


class TkBDSyncBarrierSprite (S.TkBDBarrierSprite):
    """
        Role group synchronized barrier sprite in the mine;
    """

    def bind_events (self, *args, **kw):
        """
            class event bindings;
        """
        # bind events
        self.events.connect(
            self.get_event_name("removed"), self.destroy
        )
    # end def


    def get_event_name (self, action):
        """
            hook method to be reimplemented in subclass;
            returns formatted event name;
        """
        return "Group:{}:{}".format(self.role, str(action).capitalize())
    # end def


    @property
    def role (self):
        return self.__role
    # end def


    @role.setter
    def role (self, value):
        # disconnect old events
        if hasattr(self, "__role") and self.__role:
            self.unbind_events()
        # end if
        # init new value
        self.__role = str(value)
        # group sync event bindings
        self.bind_events()
    # end def


    @role.deleter
    def role (self):
        del self.__role
    # end def


    def unbind_events (self, *args, **kw):
        """
            class event unbindings;
        """
        # unbind events
        self.events.disconnect(
            self.get_event_name("removed"), self.destroy
        )
    # end def

# end class TkBDSyncBarrierSprite
