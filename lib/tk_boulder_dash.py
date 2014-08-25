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
import tkinter as TK
import tkinter.messagebox as MB
from . import game_play as GP
from . import tkgame_animations as AP


class TkBoulderDash (TK.Frame):
    """
        c'est le game frame principal du jeu Boulder Dash(tm)
    """

    def __init__ (self, **kw):
        """
            class constructor
        """
        # super class inits
        super().__init__()
        self.configure(**self._only_tk(kw))
        self.root = TK._default_root
        self.root.protocol("WM_DELETE_WINDOW", self.quit_game)
        # member inits
        self.animations = AP.get_animation_pool()
        # init widgets
        self.canvas = TK.Canvas(
            self,
            bg="black",
            highlightthickness=0,
            # aspect ratio 16:9 (800x450)
            width=800,
            height=450,
        )
        self.canvas.pack()
        # gameplay inits
        self.game_play = GP.GamePlay(self, self.canvas, level=1)
        # bind events
        self.bind_events()
    # end def


    def _only_tk (self, kw):
        r"""
            protected method def;
            filters external keywords to suit tkinter init options;
            returns filtered dict() of keywords;
        """
        # inits
        _dict = dict()
        # TK widget *MUST* be init'ed before calling _only_tk() /!\
        # self.configure() needs self.tk to work well
        if hasattr(self, "tk") and hasattr(self, "configure"):
            _attrs = set(self.configure().keys()) & set(kw.keys())
            for _key in _attrs:
                _dict[_key] = kw.get(_key)
            # end for
        # end if
        return _dict
    # end def


    def bind_events (self):
        """
            activer les événements
        """
        self.bind_all("<Escape>", self.quit_game)
    # end def


    def unbind_events (self):
        """
            désactiver les événements
        """
        self.unbind_all("<Escape>")
    # end def


    def run (self, **kw):
        """
            lancement du jeu
        """
        # premier écran de jeu
        self.splash_screen()
    # end def


    def quit_game (self, event=None):
        """
            dialogue demande quitter le jeu ?
        """
        self.unbind_events()
        if MB.askyesno(
                "Question",
                "Voulez-vous vraiment quitter le jeu ?",
                parent=self):
            # on quitte le jeu
            self.root.destroy()
        else:
            self.bind_events()
        # end if
    # end def


    def clear_all (self, *args, **kw):
        """
            tout effacer
        """
        self.canvas.delete(TK.ALL)
        self.canvas.configure(bg="black", scrollregion=(0, 0, 10, 10))
    # end def


    def show_splash (self, fname):
        """
            affiche un écran de bienvenue (splash screen)
        """
        self.animations.stop_all()
        self.clear_all()
        self.photo = TK.PhotoImage(file="images/{}.gif".format(fname))
        self.canvas.create_image(0, 0, anchor=TK.NW, image=self.photo)
    # end def


    def splash_screen (self, *args):
        """
            premier écran de jeu (splash screen)
        """
        self.show_splash("splash")
        self.canvas.bind("<Button-1>", self.game_rules_screen)
        self.animations.run_after(5000, self.game_rules_screen)
    # end def


    def game_rules_screen (self, *args):
        """
            second écran de jeu (règles du jeu)
        """
        self.show_splash("rules")
        self.canvas.bind("<Button-1>", self.main_menu_screen)
    # end def


    def main_menu_screen (self, *args):
        """
            menu principal
        """
        # events shut down
        self.canvas.unbind("<Button-1>")
        # show main menu splash screen
        self.show_splash("main_menu")
        # inits
        x, y = self.center_xy(self.canvas)
        _opts = dict(
            anchor=TK.CENTER, font="serif 24 bold", fill="bisque2"
        )
        # CAUTION:
        # canvas.tag_bind() is buggy /!\
        # do *NOT* use it
        self.menu_id = dict()
        # menu item inits
        _id = self.canvas.create_text(x, y-60, text="Jouer", **_opts)
        self.menu_id[_id] = self.run_game
        # menu item inits
        _id = self.canvas.create_text(
            x, y + 40, text="Règles du jeu", **_opts
        )
        self.menu_id[_id] = self.game_rules_screen
        # menu item inits
        _id = self.canvas.create_text(
            x, y + 100, text="Quitter", **_opts
        )
        self.menu_id[_id] = self.quit_game
        # rebind events
        self.canvas.bind("<Button-1>", self.menu_clicked)
    # end def


    def menu_clicked (self, event):
        """
            canvas.tag_bind() étant bogué, il nous faut gérer le
            menu par nous-même;
        """
        _collisions = self.canvas.find_overlapping(
            event.x, event.y, event.x, event.y
        )
        _id = set(_collisions) & set(self.menu_id.keys())
        if _id:
            _callback = self.menu_id.get(_id.pop())
            if callable(_callback):
                #~ del self.menu_id
                _callback()
            # end if
        # end if
    # end def


    def run_game (self, *args):
        """
            lancement du jeu en lui-même
        """
        self.game_play.run()
    # end def


    def center_xy (self, widget):
        """
            retourne le tuple (x, y) du point central d'un widget
            tkinter donné;
        """
        return (widget.winfo_reqwidth()/2, widget.winfo_reqheight()/2)
    # end def

# end class TkBoulderDash
