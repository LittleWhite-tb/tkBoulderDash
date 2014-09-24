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
from . import tkgame_events as EM
from . import tkgame_audio as AU
from . import tkgame_animations as AP
from . import tkgame_fx_rotating_sun as FXRS


class GamePlay:
    """
        Here is the gameplay structure;
    """

    # class constants
    TPL_LEVEL_FILE = "data/json/level_{}.json"


    def __init__ (self, owner, canvas, level=1):
        """
            class constructor;
        """
        # member inits
        self.owner = owner
        self.canvas = canvas
        self.level = level
        self.events = EM.get_event_manager()
        self.sounds = AU.new_audio_player()
        self.animations = AP.get_animation_pool()
        self.objects = OM.ObjectMapper(
            canvas=self.canvas, images_dir="images/sprites",
        )
        self.mouse_down = False
        self.game_paused = False
        self.score = 0
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
            }
        )
        self.bind_canvas_events()
    # end def


    def blink_countdown (self, flag=0):
        """
            blinks timer display;
        """
        self.canvas.itemconfigure(
            self.countdown_id,
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

    # end def


    def diamond_collected (self, sprite, *args, **kw):
        """
            event handler for diamond catch;
        """
        # play sound
        self.play_sound("player caught diamond")
        # drop diamond from managed list
        self.objects.falling_sprites.remove(sprite)
        # update score
        self.score_add(200)
        # update remaining diamonds
        self.objects.diamonds_count -= 1
        # update display
        self.canvas.itemconfigure(
            self.remaining_id, text=str(self.objects.diamonds_count)
        )
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
        # init options
        _opts = dict(font="{} 26".format(FONT1), fill="bisque1")
        # init remaining diamonds
        self.remaining_id = self.canvas.create_text(
            10, 10,
            anchor=TK.NW,
            text=str(self.objects.diamonds_count),
            **_opts
        )
        # init player score
        self.score = 0
        self.score_id = self.canvas.create_text(
            10, 10,
            anchor=TK.N,
            text=self.format_score(),
            **_opts
        )
        # init countdown
        self.countdown_id = self.canvas.create_text(
            10, 10,
            anchor=TK.NE,
            text=self.format_time(),
            **_opts
        )
        # reconfigure canvas
        self.canvas.configure(
            bg="sienna",
            scrollregion=self.objects.matrix.bbox_xy(),
        )
        self.scroll_to_player(ticks=25.0, autoloop=False)
        self.animations.run_after(1000, self.bind_events)
        self.animations.run_after(1000, self.scroll_to_player)
        self.animations.run_after(1000, self.update_countdown)
    # end def


    def earth_digged (self, *args, **kw):
        """
            event handler for player digging earth;
        """
        # play sound
        self.play_sound("player digged earth")
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
            self.update_countdown()
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


    def play_sound (self, sound_name, volume=0.5):
        """
            plays asynchronous sound;
        """
        sound_name = str(sound_name).replace(" ", "-")
        self.sounds.play("audio/{}.wav".format(sound_name), volume)
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
        for sprite in self.objects.falling_sprites:
            sprite.fall_down()
        # end for
    # end def


    def player_splashed (self, *args, **kw):
        """
            player has been splashed;
        """
        # canvas event unbindings
        self.unbind_canvas_events()
        # play sound
        self.play_sound("player dead")
    # end def


    def rock_touched_down (self, *args, **kw):
        """
            event handler for rock touchdown;
        """
        # play sound
        self.play_sound("rock touched down")
    # end def


    def rock_pushed_aside (self, *args, **kw):
        """
            event handler for rock pushes;
        """
        # play sound
        self.play_sound("rock pushed aside")
    # end def


    def run (self):
        """
            game play inits;
        """
        self.draw_level()
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
        self.canvas.itemconfigure(
            self.score_id, text=self.format_score(start)
        )
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
        # inits
        y = self.canvas.canvasy(10)
        # update pos
        self.canvas.coords(
            self.remaining_id, self.canvas.canvasx(10), y
        )
        self.canvas.coords(self.score_id, self.canvas.canvasx(cx), y)
        self.canvas.coords(
            self.countdown_id, self.canvas.canvasx(cw - 10), y
        )
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
            self.countdown_id,
            text=self.format_time()
        )
        # hurry up!
        if self.objects.countdown <= 10:
            self.canvas.itemconfigure(
                self.countdown_id, fill="tomato"
            )
            self.play_sound("countdown beep")
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
        self.play_sound("player won all")
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
        self.play_sound("player won level")
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
