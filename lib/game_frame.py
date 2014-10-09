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
from . import game_database as DB
from . import tkgame_audio as AU
from . import tkgame_canvas as GC
from . import tkgame_frame as GF
from . import tkgame_i18n as i18n


# internationalization support (i18n)
i18n.install()

# app-wide typefont families
# please, see tkBoulderDash/fonts/README.md
# for more detail.
__builtins__["FONT1"] = "{bd cartoon shout}"
__builtins__["FONT2"] = "{andrea karime}"


# module private member
__game_frame = None


# app-wide unique instance getter
def get_game (master=None, **kw):
    """
        retrieves app-wide unique instance;
    """
    global __game_frame
    if not isinstance(__game_frame, TkBoulderDash):
        __game_frame = TkBoulderDash(master, **kw)
    # end if
    return __game_frame
# end def


class TkBoulderDash (GF.TkGameFrame):
    """
        TkBoulderDash main game frame;
    """

    # class constants
    HEAD_FONT = "{} 36".format(FONT1)
    HEAD_COLOR = "indian red"
    HEAD_SHADOW_COLOR = "grey20"
    BODY_FONT = "{} 24".format(FONT2)
    BODY_COLOR = "bisque2"
    MENU_ITEM_FONT = "{} 32".format(FONT2)
    MENU_ITEM_COLOR = "bisque2"
    FOOTER_FONT ="{} 20".format(FONT2)
    FOOTER_COLOR = "indian red"

    GAME_MUSIC = "david-filskov-boulder-dash-trash-mix.wav"
    GAME_MUSIC_VOLUME = 0.5


    def bind_tkevents (self):
        """
            tkevent bindings;
        """
        # app-wide tkinter event bindings
        for _seq, _cb in self.TKEVENTS.items():
            self.bind_all(_seq, _cb)
        # end for
    # end def


    def init_widget (self, **kw):
        """
            hook method to be reimplemented in subclass;
        """
        # main window inits
        self.root = TK._default_root
        self.root.protocol("WM_DELETE_WINDOW", self.quit_game)
        self.root.title(
            _(
                "TkBoulderDash: a Python3-Tkinter port of the "
                "famous Boulder Dash\u2122 game"
            )
        )
        # member inits
        self.database = DB.get_database()
        self.music = AU.new_audio_player()
        self.TKEVENTS = {
            "<Escape>": self.quit_game,
            "<Return>": self.run_game,
            "<r>": self.run_game,
            "<Key>": self.screen_main_menu,
        }
        # init widgets
        self.canvas = GC.TkGameCanvas(
            self,
            # aspect ratio 16:9 (800x450)
            width=800,
            height=450,
        )
        self.canvas.pack()
        # other inits
        self.cx, self.cy = self.canvas.center_xy()
        self.cw, self.ch = self.canvas.size()
        # gameplay inits
        self.game_play = GP.GamePlay(self.canvas, level=1)
        # app-wide events (not to be unbound in any case)
        self.events.connect_dict(
            {
                "Main:Menu:ShowSplash": self.screen_splash,
                "Main:Menu:ShowMainMenu": self.verify_high_score,
                "Main:Menu:ShowGameRules": self.screen_game_rules,
                "Main:Menu:ShowKeymap": self.screen_keymap,
                "Main:Music:Start": self.start_music,
                "Main:Music:Stop": self.stop_music,
            }
        )
    # end def


    def menu_clicked (self, event):
        """
            as canvas.tag_bind() has been found buggy, we must
            manage events by ourselves;
        """
        _collisions = self.canvas.find_overlapping(
            event.x, event.y, event.x, event.y
        )
        _id = set(_collisions) & set(self.menu_id.keys())
        if _id:
            _callback = self.menu_id.get(_id.pop())
            if callable(_callback):
                _callback()
            # end if
        # end if
    # end def


    def quit_game (self, *args, **kw):
        """
            event handler;
            quit game dialog confirmation;
        """
        # event unbindings
        self.unbind_tkevents()
        # dialog confirmation
        if MB.askyesno(_("Question"), _("Really quit game?")):
            # quit game app
            self.root.destroy()
        # cancelled
        else:
            # rebind events
            self.bind_tkevents()
        # end if
    # end def


    def register_new_best_score (self, new_score):
        """
            registers winner's name and new best score in database;
        """
        pass                                                                # FIXME
    # end def


    def run (self, *args, **kw):
        """
            event handler;
            running game frame;
        """
        # first menu screen
        self.screen_splash()
    # end def


    def run_game (self, *args, **kw):
        """
            event handler;
            running current game level;
        """
        # inits
        self.unbind_all_events()
        self.music.set_volume(self.GAME_MUSIC_VOLUME/2.0)
        self.game_play.run()
    # end def


    def screen_game_rules (self, *args):
        """
            game rules menu screen;
        """
        # background image
        self.show_splash("rules")
        # heading
        self.set_heading("GAME RULES")
        # body
        self.set_body("""\
Go and catch all diamonds in the mine to get to the next level.
Take care of countdown, enemies and other surprises...
But never forget: it's only a game.
Have fun!""")
        # footer
        self.set_footer()
        # canvas only mouse events
        self.canvas.bind("<Button-1>", self.screen_main_menu)
    # end def


    def screen_keymap (self, *args):
        """
            keyboard mappings menu screen;
        """
        # background image
        self.show_splash("keymap")
        # heading
        self.set_heading("KEYBOARD MAPPINGS")
        # body
        self.set_body("""\
* <arrow> keys to move.
* <spacebar> key to pause game.
* <R> or <Return> key to (re)play.
* <escape> key to trap/quit game.""")
        # footer
        self.set_footer()
        # canvas only mouse events
        self.canvas.bind("<Button-1>", self.screen_main_menu)
    # end def


    def screen_main_menu (self, *args):
        """
            main menu menu screen;
        """
        # background image
        self.show_splash("main_menu")
        # heading
        self.set_heading("MAIN MENU")
        # inits
        x, y = (self.cx, self.cy)
        _opts = dict(
            anchor=TK.CENTER,
            font=self.MENU_ITEM_FONT,
            fill=self.MENU_ITEM_COLOR,
        )
        # CAUTION:
        # canvas.tag_bind() is buggy /!\
        # do *NOT* use it
        self.menu_id = dict()
        # menu item inits
        _id = self.canvas.create_text(
            x, y - 100, text=_("Play"), **_opts
        )
        self.menu_id[_id] = self.run_game
        # menu item inits
        _id = self.canvas.create_text(
            x, y - 40, text=_("Keyboard mappings"), **_opts
        )
        self.menu_id[_id] = self.screen_keymap
        # menu item inits
        _id = self.canvas.create_text(
            x, y + 10, text=_("Game rules"), **_opts
        )
        self.menu_id[_id] = self.screen_game_rules
        # menu item inits
        _id = self.canvas.create_text(
            x, y + 60, text=_("Splash screen"), **_opts
        )
        self.menu_id[_id] = self.screen_splash
        # menu item inits
        _id = self.canvas.create_text(
            x, y + 110, text=_("Quit game"), **_opts
        )
        self.menu_id[_id] = self.quit_game
        # footer
        self.set_footer(
            "a Python3-Tkinter port of the "
            "famous Boulder Dash\u2122 game"
        )
        # canvas only mouse events
        self.canvas.bind("<Button-1>", self.menu_clicked)
    # end def


    def screen_splash (self, *args):
        """
            first menu screen;
        """
        self.show_splash("splash")
        self.start_music()
        self.animations.run_after(7000, self.screen_game_rules)
        # canvas only mouse events
        self.canvas.bind("<Button-1>", self.screen_main_menu)
    # end def


    def set_body (self, body):
        """
            shows a menu screen body text;
        """
        self.canvas.create_text(
            self.cx, self.cy + 10,
            anchor=TK.CENTER,
            text=_(body),
            font=self.BODY_FONT,
            fill=self.BODY_COLOR,
            width=self.cw * 0.9,
        )
    # end def


    def set_footer (self, footer=None):
        """
            shows a menu screen footer text;
        """
        footer = footer or "Click to continue"
        self.canvas.create_text(
            self.cx, self.ch - 20,
            anchor=TK.S,
            text=_(footer),
            font=self.FOOTER_FONT,
            fill=self.FOOTER_COLOR,
        )
    # end def


    def set_heading (self, heading=None):
        """
            shows a menu screen heading text;
        """
        heading = heading or "MENU SCREEN"
        _title = dict(
            anchor=TK.N, text=_(heading), font=self.HEAD_FONT,
        )
        self.canvas.create_text(
            self.cx + 4, 34,
            fill=self.HEAD_SHADOW_COLOR,
            **_title
        )
        self.canvas.create_text(
            self.cx, 30,
            fill=self.HEAD_COLOR,
            **_title
        )
    # end def


    def show_splash (self, fname):
        """
            shows a menu screen background image (splash picture);
        """
        # events shut down
        self.unbind_all_events()
        self.game_play.clear_canvas()
        # set background image
        self.photo = TK.PhotoImage(file="images/{}.gif".format(fname))
        self.canvas.create_image(0, 0, anchor=TK.NW, image=self.photo)
        # set music volume level
        self.music.set_volume(self.GAME_MUSIC_VOLUME)
        # rebind tkevents only
        self.bind_tkevents()
    # end def


    def start_music (self, *args, **kw):
        """
            event handler;
            starts game music background;
        """
        self.music.set_volume(self.GAME_MUSIC_VOLUME)
        self.music.play("audio/{}".format(self.GAME_MUSIC))
    # end def


    def stop_music (self, *args, **kw):
        """
            event handler;
            stops game music background;
        """
        self.music.stop()
    # end def


    def unbind_all_events (self):
        """
             unbinds all local events;
        """
        # unbind keyboard events
        self.unbind_tkevents()
        # unbind mouse events
        self.canvas.unbind("<Button-1>")
    # end def


    def unbind_tkevents (self):
        """
            event unbindings;
        """
        # app-wide tkinter event unbindings
        for _seq in self.TKEVENTS:
            self.unbind_all(_seq)
        # end for
    # end def


    def verify_high_score (self, *args, **kw):
        """
            event handler;
            verifies if current high-score is the new best score;
            goes to main menu otherwise;
        """
        # get current best score
        best_score = self.database.get_best_score()
        high_score = self.game_play.high_score
        # new best score?
        if high_score > best_score:
            # register winner
            self.register_new_best_score(high_score)
        # no best score
        else:
            # go to main menu
            self.screen_main_menu()
        # end if
    # end def

# end class TkBoulderDash
