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
    HEAD_COLOR2 = "gold"
    HEAD_SHADOW_COLOR = "grey20"
    BODY_FONT = "{} 24".format(FONT2)
    BODY_COLOR = "bisque2"
    BODY_COLOR2 = "white"
    BODY_COLOR3 = "lawn green"
    BODY_COLOR4 = "lemon chiffon"
    MENU_ITEM_FONT = "{} 32".format(FONT2)
    MENU_ITEM_COLOR = "bisque2"
    FOOTER_FONT ="{} 20".format(FONT2)
    FOOTER_COLOR = "indian red"
    FOOTER_COLOR2 = "gold"

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
        # widget inits
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
        # database inits (may take a while)
        self.database = DB.get_database()
        # music inits
        self.music = AU.new_audio_player()
        # menu callback
        self.menu_callback = self.screen_main_menu
        # tk event inits
        self.TKEVENTS = {
            "<Escape>": self.quit_game,
            "<Return>": self.run_game,
            "<r>": self.run_game,
            "<Key>": self.switch_to_main_menu,
        }
        # app-wide events (should never be unbound in any case)
        self.events.connect_dict(
            {
                "Main:Menu:ShowSplash": self.screen_splash,
                "Main:Menu:ShowMainMenu": self.verify_high_score,
                "Main:Menu:ShowGameRules": self.screen_game_rules,
                "Main:Menu:ShowKeymap": self.screen_keymap,
                "Main:Music:Start": self.start_music,
                "Main:Music:Stop": self.stop_music,
                "Stats:Level:Started": self.stats_level_started,
                "Stats:Level:Won": self.stats_level_won,
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


    def on_quit_game (self, *args, **kw):
        """
            hook method to be reimplemented in subclass;
            happens unconditionnaly just before app is destroyed;
            put here what needs to be stopped before ending;
        """
        # close database
        self.database.close_database()
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
            # hook method
            self.on_quit_game(*args, **kw)
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
        # background image
        self.show_splash("best_score")
        # disable local events
        self.unbind_tkevents()
        # heading
        self.set_heading("NEW BEST SCORE", color=self.HEAD_COLOR2)
        # body
        _opts = dict(font=self.BODY_FONT, width=self.cw * 0.9,)
        self.canvas.create_text(
            self.cx, self.cy - 80,
            text=_("You scored:"),
            fill=self.BODY_COLOR2,
            **_opts
        )
        self.canvas.create_text(
            self.cx, self.cy - 30,
            text="{:06d}".format(new_score),
            fill=self.BODY_COLOR3,
            **_opts
        )
        self.canvas.create_text(
            self.cx, self.cy + 20,
            text=_("Please, enter your name:"),
            fill=self.BODY_COLOR2,
            **_opts
        )
        # user input entry inits
        _entry = TK.Entry(
            self,
            bd=0,
            bg="#3753A6",
            fg=self.BODY_COLOR3,
            font=self.BODY_FONT,
            highlightthickness=0,
            insertbackground=self.BODY_COLOR2,
            justify=TK.CENTER,
            relief=TK.FLAT,
            selectbackground=self.BODY_COLOR3,
            selectforeground=self.BODY_COLOR2,
            width=16,
        )
        self.canvas.create_window(
            self.cx, self.cy + 70, window=_entry
        )
        _entry.insert(
            0, self.database.get_option("Winner:Name") or _("Winner")
        )
        _entry.select_range(0, TK.END)
        _entry.focus_set()
        # footer
        self.set_footer(
            "Press <Return> to validate", color=self.FOOTER_COLOR2
        )
        # entry validation
        def validate_entry (*args):
            if MB.askyesno(_("Question"), _("Do you confirm?")):
                _entry.unbind("<Return>")
                _name = _entry.get() or _("Winner")
                self.database.add_best_score(_name, new_score)
                self.database.set_option("Winner:Name", _name)
                #~ self.database.dump_tables()
                self.screen_main_menu()
            # end if
        # end def
        # event bindings
        _entry.bind("<Return>", validate_entry)
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


    def screen_game_options (self, *args):
        """
            game options menu screen;
        """
        # background image
        self.show_splash("game_options")
        # heading
        self.set_heading("GAME OPTIONS", color=self.HEAD_COLOR2)
        # body
        self.set_body("""TODO""", color=self.BODY_COLOR2)
        # footer
        self.set_footer(color=self.FOOTER_COLOR2)
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
    # end def


    def screen_game_scores (self, *args):
        """
            game high-scores menu screen;
        """
        # background image
        self.show_splash("game_scores")
        # heading
        self.set_heading("HALL OF FAME", color=self.HEAD_COLOR2)
        # get recordset
        _rows = self.database.get_hall_of_fame()
        # empty set?
        if not _rows:
            # body
            self.set_body("No heroes by there.", color=self.BODY_COLOR2)
        # filled set
        else:
            # inits
            x, y = (self.cw//10, self.cy - 100)
            # browse recordset
            for _row in _rows:
                # inits
                _name, _score = tuple(_row)
                # show text
                self.canvas.create_text(
                    x, y,
                    text=str(_name),
                    anchor=TK.W,
                    fill=self.BODY_COLOR4,
                    font=self.BODY_FONT,
                )
                self.canvas.create_text(
                    self.cw - x, y,
                    text="{:n}".format(_score),
                    anchor=TK.E,
                    fill=self.BODY_COLOR2,
                    font=self.BODY_FONT,
                )
                # update pos
                y += 40
            # end for
        # end if
        # footer
        self.set_footer(color=self.FOOTER_COLOR2)
    # end def


    def screen_game_stats (self, *args):
        """
            game stats menu screen;
        """
        # background image
        self.show_splash("game_stats")
        # heading
        self.set_heading("GAME STATISTICS", color=self.HEAD_COLOR2)
        # body
        self.set_body("""TODO""", self.BODY_COLOR2)
        # footer
        self.set_footer(color=self.FOOTER_COLOR2)
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
    # end def


    def screen_main_menu (self, *args):
        """
            main menu menu screen;
        """
        # inits
        self.menu_callback = self.screen_main_menu
        # background image
        self.show_splash("main_menu")
        # heading
        self.set_heading("MAIN MENU")
        # show menu items
        self.show_menu(
            (
                ("Play", self.run_game),
                ("Game rules", self.screen_game_rules),
                ("Keyboard mappings", self.screen_keymap),
                ("More options", self.screen_main_menu_2),
                ("Quit game", self.quit_game),
            )
        )
        # footer
        self.set_footer(
            "a Python3-Tkinter port of the "
            "famous Boulder Dash\u2122 game"
        )
    # end def


    def screen_main_menu_2 (self, *args):
        """
            main menu 2 menu screen;
        """
        # inits
        self.menu_callback = self.screen_main_menu_2
        # background image
        self.show_splash("main_menu")
        # heading
        self.set_heading("MORE OPTIONS")
        # show menu items
        self.show_menu(
            (
                ("Hall of fame", self.screen_game_scores),
                ("Game stats", self.screen_game_stats),
                ("Game options", self.screen_game_options),
                ("Main menu", self.screen_main_menu),
                ("Quit game", self.quit_game),
            )
        )
        # footer
        self.set_footer(
            "a Python3-Tkinter port of the "
            "famous Boulder Dash\u2122 game"
        )
    # end def


    def screen_splash (self, *args):
        """
            first menu screen;
        """
        # background image
        self.show_splash("splash")
        # game music play off
        self.start_music()
        # show game rules after a while
        self.animations.run_after(7000, self.screen_game_rules)
    # end def


    def set_body (self, body, color=None):
        """
            shows a menu screen body text;
        """
        self.canvas.create_text(
            self.cx, self.cy + 10,
            anchor=TK.CENTER,
            text=_(body),
            font=self.BODY_FONT,
            fill=color or self.BODY_COLOR,
            width=self.cw * 0.9,
        )
    # end def


    def set_footer (self, footer=None, color=None):
        """
            shows a menu screen footer text;
        """
        footer = footer or "Click to continue"
        self.canvas.create_text(
            self.cx, self.ch - 20,
            anchor=TK.S,
            text=_(footer),
            font=self.FOOTER_FONT,
            fill=color or self.FOOTER_COLOR,
        )
    # end def


    def set_heading (self, heading=None, color=None):
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
            fill=color or self.HEAD_COLOR,
            **_title
        )
    # end def


    def show_menu (self, menu_list):
        """
            shows off menu items;
        """
        # inits
        x, y = (self.cx, self.cy - 95)
        _opts = dict(
            anchor=TK.CENTER,
            font=self.MENU_ITEM_FONT,
            fill=self.MENU_ITEM_COLOR,
        )
        # CAUTION:
        # canvas.tag_bind() is buggy /!\
        # do *NOT* use it
        self.menu_id = dict()
        # browse menu items
        for (menu_text, menu_cb) in menu_list:
            # menu item inits
            _id = self.canvas.create_text(
                x, y, text=_(menu_text), **_opts
            )
            self.menu_id[_id] = menu_cb
            # update pos
            y += 55
        # end for
        # canvas only mouse events
        self.canvas.bind("<Button-1>", self.menu_clicked)
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
        # rebind tk events
        self.bind_tkevents()
        # canvas only mouse events
        self.canvas.bind("<Button-1>", self.switch_to_main_menu)
    # end def


    def start_music (self, *args, **kw):
        """
            event handler;
            starts game music background;
        """
        if not self.database.get_option("Music:Switch:Off"):
            self.music.set_volume(self.GAME_MUSIC_VOLUME)
            self.music.play("audio/{}".format(self.GAME_MUSIC))
        # end if
    # end def


    def stats_level_started (self, level, *args, **kw):
        """
            event handler;
            updates some stats data;
        """
        print("Stats:Level started:", level)
    # end def


    def stats_level_won (self, level, *args, **kw):
        """
            event handler;
            updates some stats data;
        """
        print("Stats:Level won:", level)
    # end def


    def stop_music (self, *args, **kw):
        """
            event handler;
            stops game music background;
        """
        self.music.stop()
    # end def


    def switch_to_main_menu (self, *args, **kw):
        """
            event handler;
            switches to last selected main menu page;
        """
        if callable(self.menu_callback):
            self.menu_callback(*args, **kw)
        # end if
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
