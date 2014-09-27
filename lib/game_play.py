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
import os.path as OP
import tkinter.constants as TK
from . import object_mapper as OM
from . import tkgame_animations as AP
from . import tkgame_audio as AU
from . import tkgame_canvas_fixedlayer as FL
from . import tkgame_events as EM
from . import tkgame_fx_rotating_sun as FXRS


class GamePlay:
    """
        Here is the gameplay structure;
    """

    # class constants
    TPL_LEVEL_FILE = "data/json/level_{}.json"

    SNDTRACK_PLAYER = 1
    SNDTRACK_DIAMOND = 2
    SNDTRACK_ROCK = 3
    SNDTRACK_BACKGROUND = 4


    def __init__ (self, owner, canvas, level=1):
        """
            class constructor;
        """
        # member inits
        self.owner = owner
        self.canvas = canvas
        self.level = level
        self.events = EM.get_event_manager()
        self.soundtracks = tuple(AU.new_audio_player() for i in range(4))
        self.animations = AP.get_animation_pool()
        self.objects = OM.ObjectMapper(
            canvas=self.canvas, images_dir="images/sprites",
        )
        self.fixed_layer = FL.get_fixed_layer(canvas)
        self.mouse_down = False
        self.game_paused = False
        self.score = 0

        #~ self.level = 9 # debugging

    # end def


    def bind_canvas_events (self, *args, **kw):
        """
            canvas event bindings;
        """
        self.canvas.bind_all("<Escape>", self.on_key_escape)
        self.canvas.bind_all("<space>", self.pause_game)
        self.canvas.bind_all("<Key>", self.on_key_pressed)
        self.canvas.bind("<Button-1>", self.on_mouse_down)
        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
    # end def


    def bind_events (self, *args, **kw):
        """
            app-wide event bindings;
        """
        # connecting people...
        self.events.connect_dict(
            {
                "Main:Earth:Digged": self.earth_digged,
                "Main:Diamond:Collected": self.diamond_collected,
                "Main:Player:Moved": self.player_moved,
                "Main:Player:Splashed": self.player_splashed,
                "Main:Player:Dead": self.player_dead,
                "Main:Rock:TouchedDown": self.rock_touched_down,
                "Main:Rock:Pushed": self.rock_pushed_aside,
                "Main:RockDiamond:Changing": self.rockdiamond_changing,
                "Main:RockDiamond:Changed": self.rockdiamond_changed,
            }
        )
        self.bind_canvas_events()
    # end def


    def blink_countdown (self, flag=0):
        """
            blinks timer display;
        """
        self.canvas.itemconfigure(
            self.cid_countdown,
            text="" if not flag else self.format_time()
        )
        flag = not flag
        self.animations.run_after(250, self.blink_countdown, flag)
    # end def


    def center_xy (self, widget):
        """
            returns (x, y) tuple of a tkinter widget central point;
        """
        return (widget.winfo_reqwidth()/2, widget.winfo_reqheight()/2)
    # end def


    def clear_canvas (self, *args, **kw):
        """
            clears canvas and stops unexpected events;
        """
        # stop any scheduled thread
        self.animations.stop_all()
        # unbind all events
        self.unbind_events()
        # clear canvas
        self.canvas.delete(TK.ALL)
        # reset canvas
        self.canvas.configure(bg="black", scrollregion=(0, 0, 0, 0))
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)
    # end def


    def diamond_collected (self, sprite, *args, **kw):
        """
            event handler for diamond catch;
        """
        # play sound
        self.play_sound("player caught diamond", self.SNDTRACK_DIAMOND)
        # drop diamond from managed list
        self.objects.falling_sprites.remove(sprite)
        # free some memory
        del sprite
        # update score
        self.score_add(200)
        # update remaining diamonds
        self.objects.diamonds_count -= 1
        # update display
        self.update_diamonds_count()
        # no more diamonds?
        if self.objects.diamonds_count < 1:
            # yeah! winner!
            self.won_level()
        # end if
    # end def


    def draw_level (self):
        """
            drawing game play level;
        """
        # inits
        self.clear_canvas()
        self.objects.load_data(self.get_level_fpath(self.level))
        for _sprite in self.objects.matrix.objects():
            _sprite.start()
        # end for
        # reset canvas text items viewport fixed layer
        self.fixed_layer.clear()
        # init options
        _opts = dict(font="{} 26".format(FONT1), fill="bisque1")
        _cx, _cy = self.center_xy(self.canvas)
        _cw = self.canvas.winfo_reqwidth()
        # init remaining diamonds
        self.cid_diamonds_count = self.canvas.create_text(
            10, 10, anchor=TK.NW, **_opts
        )
        # init player score
        #~ self.score = 0       # keep score between each level /!\
        self.cid_score = self.canvas.create_text(
            _cx, 10, anchor=TK.N, **_opts
        )
        # init countdown
        self.cid_countdown = self.canvas.create_text(
            _cw - 10, 10, anchor=TK.NE, **_opts
        )
        # reset options
        _opts = dict(
            anchor=TK.CENTER,
            text=self.objects.level_name,
            font="{} 48".format(FONT1),
            tags="headings",
        )
        # show level name and number
        self.cid_level_name2 = self.canvas.create_text(
            _cx + 4, _cy + 4, fill="darkred", **_opts
        )
        self.cid_level_name1 = self.canvas.create_text(
            _cx, _cy, fill="yellow", **_opts
        )
        self.cid_level_number = self.canvas.create_text(
            _cx, _cy - 80,
            text="level {}".format(self.level),
            font="{} 36".format(FONT2),
            fill="bisque1",
            tags="headings",
        )
        # add to viewport fixed layer
        self.fixed_layer.add(
            self.cid_diamonds_count,
            self.cid_score,
            self.cid_countdown,
            self.cid_level_name1,
            self.cid_level_name2,
            self.cid_level_number,
        )
        # reconfigure canvas
        self.canvas.configure(
            bg="sienna",
            scrollregion=self.objects.matrix.bbox_xy(),
        )
        self.scroll_to_player(ticks=25.0, autoloop=False)
        self.animations.run_after(1800, self.remove_headings)
        self.animations.run_after(1000, self.bind_events)
        self.animations.run_after(1000, self.scroll_to_player)
        self.animations.run_after(800, self.update_game_data)
    # end def


    def earth_digged (self, *args, **kw):
        """
            event handler for player digging earth;
        """
        # play sound
        self.play_sound("player digged earth", self.SNDTRACK_PLAYER)
        # update score with +50 pts
        self.score_add(50)
    # end if


    def format_score (self, value=None):
        """
            score display formatting;
        """
        # param controls
        if value is None:
            value = self.score
        # end if
        return "{:04d}".format(value)
    # end def


    def format_time (self, value=None):
        """
            time display formatting;
        """
        # param controls
        if value is None:
            value = self.objects.countdown
        # end if
        return (
            "{:02d}:{:02d}:{:02d}"
            .format(value//3600, (value//60) % 60, value % 60)
        )
    # end def


    def get_level_fpath (self, level):
        """
            returns absolute path for a JSON level data file;
            param @level must be non-null integer;
        """
        return OP.abspath(
            OP.expanduser(
                self.TPL_LEVEL_FILE.format(max(1, int(level)))
            )
        )
    # end def


    def next_level (self, *args, **kw):
        """
            looks for a next level JSON data file, if any;
            shows won_all() splash screen otherwise;
        """
        # file does exist?
        if OP.isfile(self.get_level_fpath(self.level + 1)):
            # next level
            self.level += 1
            # draw new level
            self.draw_level()
        # no more levels
        else:
            # player won everything!
            self.won_all()
        # end if
    # end def


    def on_key_escape (self, event=None):
        """
            player asked for exiting;
        """
        # go to main menu screen
        self.owner.main_menu_screen()
    # end def


    def on_key_pressed (self, event=None):
        """
            generic keypress events demultiplexer;
        """
        # inits
        _method = {
            "Up": self.objects.player_sprite.move_up,
            "Down": self.objects.player_sprite.move_down,
            "Left": self.objects.player_sprite.move_left,
            "Right": self.objects.player_sprite.move_right,
        }.get(event.keysym)
        # supported keystroke?
        if callable(_method):
            # go!
            _method()
        # end if
    # end def


    def on_mouse_down (self, event=None):
        """
            mouse click button down event handler;
        """
        self.mouse_down = True
        self.canvas.scan_mark(event.x, event.y)
        self.animations.stop(self.scroll_to_player)
    # end def


    def on_mouse_move (self, event=None):
        """
            mouse move event handler;
        """
        if self.mouse_down:
            self.canvas.scan_dragto(event.x, event.y)
        # end if
    # end def


    def on_mouse_up (self, event=None):
        """
            mouse click button release event handler;
        """
        self.mouse_down = False
        self.animations.run_after(1, self.scroll_to_player)
    # end def


    def pause_game (self, *args, **kw):
        """
            user asked for a game pause/resume;
        """
        # got to resume?
        if self.game_paused:
            self.game_paused = False
            self.canvas.unbind_all("<space>")
            self.canvas.delete("pause_group")
            self.events.raise_event("Main:Game:Resumed")
            self.scroll_to_player()
            self.bind_canvas_events()
            self.update_game_data()
        # pause game
        else:
            self.game_paused = True
            self.unbind_canvas_events()
            self.animations.stop(
                self.scroll_to_player,
                self.scroll_animation_loop,
                self.update_countdown,
            )
            self.events.raise_event("Main:Game:Paused")
            # show some text
            x, y = self.viewport_center_xy()
            _opts = dict(
                anchor=TK.CENTER,
                text=_("PAUSE"),
                font="{} 96".format(FONT1),
                tags="pause_group",
            )
            self.canvas.create_text(x + 4, y + 4, fill="#400", **_opts)
            self.canvas.create_text(x, y, fill="gold", **_opts)
            self.canvas.create_text(
                x, y + 70,
                text=_("Press spacebar to continue"),
                font="{} 20".format(FONT2),
                fill="pale goldenrod",
                tags="pause_group",
            )
            self.canvas.bind_all("<space>", self.pause_game)
        # end if
    # end def


    def play_sound (self, sound_name, track=1, volume=0.5):
        """
            plays asynchronous sound;
        """
        track = max(1, min(track, len(self.soundtracks))) - 1
        sound_name = str(sound_name).replace(" ", "-")
        self.soundtracks[track].play(
            "audio/{}.wav".format(sound_name), volume
        )
    # end def


    def player_dead (self, *args, **kw):
        """
            player is now really dead;
        """
        self.animations.run_after(3000, self.owner.main_menu_screen)
    # end def


    def player_moved (self, *args, **kw):
        """
            player has moved, rocks and diamonds may fall down;
        """
        # update general falldown procedure
        self.update_falldown()
    # end def


    def remove_headings (self, *args, **kw):
        """
            removes level name and number display offs;
        """
        # delete from canvas display off
        self.canvas.delete("headings")
        # remove from viewport fixed layer
        self.fixed_layer.remove(
            self.cid_level_name1,
            self.cid_level_name2,
            self.cid_level_number,
        )
        # free some memory
        del self.cid_level_name1
        del self.cid_level_name2
        del self.cid_level_number
    # end def


    def player_splashed (self, *args, **kw):
        """
            player has been splashed;
        """
        # canvas event unbindings
        self.unbind_canvas_events()
        # play sound
        self.play_sound("player dead", self.SNDTRACK_PLAYER)
    # end def


    def rock_touched_down (self, *args, **kw):
        """
            event handler for rock touchdown;
        """
        # play sound
        self.play_sound("rock touched down", self.SNDTRACK_ROCK)
        # update general falldown procedure
        self.update_falldown()
    # end def


    def rockdiamond_changed (self, sprite, *args, **kw):
        """
            event handler for rockdiamond end of transformation;
        """
        # add some score
        self.score_add(100)
    # end def


    def rockdiamond_changing (self, sprite, *args, **kw):
        """
            event handler for rockdiamond transformation;
        """
        # play sound
        self.play_sound("rockdiamond changing", self.SNDTRACK_DIAMOND)
    # end def


    def rock_pushed_aside (self, *args, **kw):
        """
            event handler for rock pushes;
        """
        # play sound
        self.play_sound("rock pushed aside", self.SNDTRACK_PLAYER)
    # end def


    def run (self):
        """
            game play inits;
        """
        # try to draw current level
        try:
            self.draw_level()
        # got in trouble
        except Exception as e:
            # stop all!
            exit(
                "An exception has occurred:\n{}\n"
                "Fatal error while trying to draw current level!"
                .format(e)
            )
        # end try
    # end def


    def score_add (self, value):
        """
            adds a new value to score and sets up animation for this;
        """
        # param inits
        value = abs(int(value))
        # score display animation
        self.animations.run_after(
            50,
            self.score_display_loop,
            self.score,
            self.score + value,
            value//15 or 1,
        )
        # update score
        self.score += value
    # end def


    def score_display_loop (self, start, stop, step):
        """
            animation loop for score updates;
        """
        # update display
        self.update_score(start)
        # not finished?
        if start < stop:
            # update pos
            start = min(stop, start + step)
            # loop again
            self.animations.run_after(
                50, self.score_display_loop, start, stop, step
            )
        # end if
    # end def


    def scroll_animation_loop (self, *args):
        """
            camera tracking animation loop;
        """
        # inits
        startx, starty, stopx, stopy, stepx, stepy, \
        cx, cy, cw, mw, mh = args
        self.canvas.xview_moveto((startx - cx)/mw)
        self.canvas.yview_moveto((starty - cy)/mh)
        # update text items viewport fixed positions
        self.fixed_layer.update_positions()
        # no more moves?
        if startx == stopx and starty == stopy:
            # trap out!
            return
        # end if
        # update coords
        if stepx > 0:
            startx = min(stopx, startx + stepx)
        else:
            startx = max(stopx, startx + stepx)
        # end if
        # update coords
        if stepy > 0:
            starty = min(stopy, starty + stepy)
        else:
            starty = max(stopy, starty + stepy)
        # end if
        # loop again
        self.animations.run_after(
            25,
            self.scroll_animation_loop,
            startx, starty, stopx, stopy, stepx, stepy, cx, cy,
            cw, mw, mh
        )
    # end def


    def scroll_to_player (self, ticks=3.0, autoloop=True):
        """
            asks camera to track to player;
        """
        # animation inits
        x, y = self.objects.player_sprite.xy
        x0, y0 = self.viewport_center_xy()
        cx, cy = self.center_xy(self.canvas)
        cw = self.canvas.winfo_reqwidth()
        mw, mh = self.objects.matrix.width_height()
        # fixing canvas fuzzy values
        if abs(x - x0) < 2 or x > mw - cx:
            x0 = x
        # end if
        if abs(y - y0) < 2 or y > mh - cy:
            y0 = y
        # end if
        # run animation loop
        self.animations.run_after(
            1,
            self.scroll_animation_loop,
            x0, y0, x, y,
            (x - x0)/ticks, (y - y0)/ticks,
            cx, cy, cw, mw, mh
        )
        # need to loop again?
        if autoloop:
            self.animations.run_after(
                25 * (ticks + 2), self.scroll_to_player, ticks, True
            )
        # end if
    # end def


    def unbind_canvas_events (self, *args, **kw):
        """
            canvas event unbindings;
        """
        # canvas events unbind
        self.canvas.unbind_all("<Escape>")
        self.canvas.unbind_all("<space>")
        self.canvas.unbind_all("<Key>")
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
    # end def


    def unbind_events (self, *args, **kw):
        """
            app-wide event unbindings;
        """
        # unbind app events
        self.events.disconnect_all()
        # unbind canvas events
        self.unbind_canvas_events()
    # end def


    def update_countdown (self, *args, **kw):
        """
            updates timer countdown display;
        """
        self.objects.countdown = max(
            0, min(600, self.objects.countdown - 1)
        )
        self.canvas.itemconfigure(
            self.cid_countdown,
            text=self.format_time()
        )
        # hurry up!
        if self.objects.countdown <= 10:
            self.canvas.itemconfigure(
                self.cid_countdown, fill="tomato"
            )
            self.play_sound("countdown beep", self.SNDTRACK_BACKGROUND)
            self.animations.run_after(250, self.blink_countdown)
        # end if
        # time is out!
        if not self.objects.countdown:
            self.animations.stop(self.blink_countdown)
            self.objects.player_sprite.splashed()
        # keep on counting down
        else:
            self.animations.run_after(1000, self.update_countdown)
        # end if
    # end def


    def update_diamonds_count (self, *args, **kw):
        """
            updates diamond count display;
        """
        # update display
        self.canvas.itemconfigure(
            self.cid_diamonds_count,
            text=str(self.objects.diamonds_count)
        )
    # end def


    def update_falldown (self, *args, **kw):
        """
            updates falling down procedure;
        """
        for sprite in self.objects.falling_sprites:
            sprite.fall_down()
        # end for
    # end def


    def update_game_data (self, *args, **kw):
        """
            updates all game data display offs;
        """
        self.update_diamonds_count()
        self.update_score()
        self.update_countdown()
    # end def


    def update_score (self, value=None, *args, **kw):
        """
            updates diamond count display;
        """
        # update display
        self.canvas.itemconfigure(
            self.cid_score, text=self.format_score(value)
        )
    # end def


    def viewport_center_xy (self):
        """
            returns (x, y) tuple for canvas' viewport central point;
        """
        return self.viewport_xy(self.center_xy(self.canvas))
    # end def


    def viewport_xy (self, xy):
        """
            returns (x, y) tuple for a canvas viewport point location;
        """
        # viewport --> scrollregion conversion
        return (self.canvas.canvasx(xy[0]), self.canvas.canvasy(xy[1]))
    # end def


    def won_all (self):
        """
            player won everything! congrats!
        """
        # clean-ups
        self.clear_canvas()
        # new graphical special effects
        FXRS.TkGameFXRotatingSun(self.canvas).start()
        # texts
        self.won_text(
            "Champion!",
            "You won all!",
            title_color="lemon chiffon",
            subtitle_color="powder blue"
        )
        # play sound
        self.play_sound("player won all", self.SNDTRACK_BACKGROUND)
        # reset level
        self.level = 1
        # events binding
        self.canvas.bind_all("<Escape>", self.on_key_escape)
        # main menu screen
        self.animations.run_after(3300, self.owner.main_menu_screen)
    # end def


    def won_level (self):
        """
            player won the current level;
        """
        # clean-ups
        self.clear_canvas()
        # new graphical special effects
        FXRS.TkGameFXRotatingSun(
            self.canvas, bgcolor="saddle brown", fgcolor="sienna"
        ).start()
        # texts
        self.won_text(
            "Great!",
            "You got it!",
            title_color="yellow",
            subtitle_color="antique white"
        )
        # play sound
        self.owner.music.stop()
        self.play_sound("player won level", self.SNDTRACK_BACKGROUND)
        # go to next level
        self.animations.run_after(4000, self.next_level)
    # end def


    def won_text (self, title, subtitle, **kw):
        """
            texts for winning screens;
        """
        # inits
        x, y = self.viewport_center_xy()
        _opts = dict(text=_(title), font="{} 48".format(FONT1))
        # texts
        self.canvas.create_text(
            x + 4, y - 46,
            fill=kw.get("title_shadow_color") or "grey20",
            **_opts
        )
        self.canvas.create_text(
            x, y - 50,
            fill=kw.get("title_color") or "white",
            **_opts
        )
        self.canvas.create_text(
            x, y + 20,
            text=_(subtitle),
            font="{} 24".format(FONT2),
            fill=kw.get("subtitle_color") or "white",
        )
        self.canvas.create_text(
            x, y + 70,
            text=_("Score: {}").format(self.score),
            font="{} 24".format(FONT2),
            fill=kw.get("title_color") or "white",
        )
    # end def

# end class GamePlay
