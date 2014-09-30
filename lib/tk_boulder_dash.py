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
from . import tkgame_audio as AU
from . import tkgame_animations as AP
from . import tkgame_i18n as i18n


# internationalization support (i18n)
i18n.install()

# app-wide typefont families
# please, see tkBoulderDash/fonts/README.md
# for more detail.
__builtins__["FONT1"] = "{bd cartoon shout}"
__builtins__["FONT2"] = "{andrea karime}"


class TkBoulderDash (TK.Frame):
    """
        game mainframe class;
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


    def __init__ (self, **kw):
        """
            class constructor;
        """
        # super class inits
        super().__init__()
        self.configure(**self._only_tk(kw))
        self.root = TK._default_root
        self.root.protocol("WM_DELETE_WINDOW", self.quit_game)
        self.root.title(
            _(
                "TkBoulderDash: a Python3-Tkinter port of the "
                "famous Boulder Dash\u2122 game"
            )
        )
        # member inits
        self.music = AU.new_audio_player()
        self.animations = AP.get_animation_pool()
        # init widgets
        self.canvas = TK.Canvas(
            self,
            highlightthickness=0,
            # aspect ratio 16:9 (800x450)
            width=800,
            height=450,
        )
        self.canvas.pack()
        # other inits
        self.cw = self.canvas.winfo_reqwidth()
        self.ch = self.canvas.winfo_reqheight()
        # gameplay inits
        self.game_play = GP.GamePlay(self, self.canvas, level=1)
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
            event bindings;
        """
        self.bind_all("<Escape>", self.quit_game)
        self.bind_all("<Return>", self.run_game)
    # end def


    def game_rules_screen (self, *args):
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
        # events binding
        self.canvas.bind("<Button-1>", self.main_menu_screen)
    # end def


    def keymap_screen (self, *args):
        """
            keyboard mappings menu screen;
        """
        # background image
        self.show_splash("keymap")
        # heading
        self.set_heading("KEYBOARD MAPPINGS")
        # body
        self.set_body("""\
* Use arrow keys to move into four directions.
* Use spacebar key to pause game.
* Press escape key to trap out from a game level.
* Press escape key once more to quit game.""")
        # footer
        self.set_footer()
        # events binding
        self.canvas.bind("<Button-1>", self.main_menu_screen)
    # end def


    def main_menu_screen (self, *args):
        """
            main menu menu screen;
        """
        # background image
        self.show_splash("main_menu")
        # heading
        self.set_heading("MAIN MENU")
        # inits
        x, y = self.game_play.viewport_center_xy()
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
        self.menu_id[_id] = self.keymap_screen
        # menu item inits
        _id = self.canvas.create_text(
            x, y + 10, text=_("Game rules"), **_opts
        )
        self.menu_id[_id] = self.game_rules_screen
        # menu item inits
        _id = self.canvas.create_text(
            x, y + 60, text=_("Splash screen"), **_opts
        )
        self.menu_id[_id] = self.splash_screen
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
        # rebind events
        self.canvas.bind("<Button-1>", self.menu_clicked)
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


    def quit_game (self, event=None):
        """
            quit game dialog confirmation;
        """
        # event unbindings
        self.unbind_events()
        # dialog confirmation
        if MB.askyesno(_("Question"), _("Really quit game?")):
            # quit game app
            self.root.destroy()
        # cancelled
        else:
            # rebind events
            self.bind_events()
        # end if
    # end def


    def run (self, **kw):
        """
            running game frame;
        """
        # first menu screen
        self.splash_screen()
    # end def


    def run_game (self, *args):
        """
            running current game level;
        """
        # inits
        self.music.set_volume(self.GAME_MUSIC_VOLUME/2.0)
        self.unbind_events()
        # reset score from here
        self.game_play.score = 0
        self.game_play.run()
    # end def


    def set_body (self, body):
        """
            shows a menu screen body text;
        """
        self.canvas.create_text(
            self.cw//2, self.ch//2 + 10,
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
            self.cw//2, self.ch - 20,
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
        x = self.cw//2
        _title = dict(
            anchor=TK.N, text=_(heading), font=self.HEAD_FONT,
        )
        self.canvas.create_text(
            x + 4, 34,
            fill=self.HEAD_SHADOW_COLOR,
            **_title
        )
        self.canvas.create_text(
            x, 30,
            fill=self.HEAD_COLOR,
            **_title
        )
    # end def


    def show_splash (self, fname):
        """
            shows a menu screen background image (splash picture);
        """
        # events shut down
        self.canvas.unbind("<Button-1>")
        self.game_play.clear_canvas()
        self.unbind_events()
        # set background image
        self.photo = TK.PhotoImage(file="images/{}.gif".format(fname))
        self.canvas.create_image(0, 0, anchor=TK.NW, image=self.photo)
        # set music volume level
        self.music.set_volume(self.GAME_MUSIC_VOLUME)
        # rebind events
        self.bind_events()
    # end def


    def splash_screen (self, *args):
        """
            first menu screen;
        """
        self.show_splash("splash")
        self.music.play("audio/{}".format(self.GAME_MUSIC))
        self.canvas.bind_all("<Key>", self.main_menu_screen)
        self.canvas.bind("<Button-1>", self.main_menu_screen)
        self.animations.run_after(7000, self.game_rules_screen)
    # end def


    def unbind_events (self):
        """
            event unbindings;
        """
        self.unbind_all("<Escape>")
        self.unbind_all("<Return>")
    # end def

# end class TkBoulderDash
