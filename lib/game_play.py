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
from . import tkgame_fx_flying_text as FXFT
from . import tkgame_fx_rotating_sun as FXRS


class GamePlay:
    """
        Here is the gameplay structure;
    """

    # class constants
    TPL_LEVEL_FILE = "data/json/level_{}.json"

    SNDTRACK = {
        "alarm": 1,
        "player": 2,
        "diamond": 3,
        "rock": 4,
        "rockdiamond": 5,
        "background": 6,
        "enemy": 7,
    }


    def __init__ (self, canvas, level=1):
        """
            class constructor;
        """
        # member inits
        self.canvas = canvas
        self.level = level
        self.animations = AP.get_animation_pool()
        self.events = EM.get_event_manager()
        self.soundtracks = tuple(
            AU.new_audio_player() for i in range(len(self.SNDTRACK))
        )
        self.objects = OM.ObjectMapper(
            canvas, images_dir="images/sprites"
        )
        self.fixed_layer = FL.get_fixed_layer(canvas)
        self.mouse_down = False
        self.game_paused = False
        self.score = 0
        self.high_score = 0
        # instance constant defs
        self.KEYMAP = {
            "<Escape>": self.on_key_escape,
            "<space>": self.pause_game,
            "<Return>": self.reset_game,
            "<r>": self.reset_game,
            "<Key>": self.on_key_pressed,
        }
        self.events_dict = {
            "Game:Diamond:Destroyed": self.diamond_collected,
            "Game:Diamond:TouchedDown": self.diamond_touched_down,
            "Game:Earth:Destroyed": self.earth_digged,
            "Game:GoldenKey:Destroyed": self.golden_key_collected,
            "Game:GoldenKey:TouchedDown": self.golden_key_touched_down,
            "Game:Player:Destroyed": self.player_dead,
            "Game:Player:Frozen": self.player_frozen,
            "Game:Player:Splashed": self.player_splashed,
            "Game:PUDiamond:Destroyed": self.pudiamond_collected,
            "Game:PUDiamond:TouchedDown": self.diamond_touched_down,
            "Game:RockDiamond:Changed": self.rockdiamond_changed,
            "Game:RockDiamond:Changing": self.rockdiamond_changing,
            "Game:RockDiamond:Destroyed": self.diamond_collected,
            "Game:RockDiamond:Pushed": self.rock_pushed_aside,
            "Game:RockDiamond:TouchedDown": self.rockdiamond_touched_down,
            "Game:Rock:Pushed": self.rock_pushed_aside,
            "Game:Rock:TouchedDown": self.rock_touched_down,
            "Game:Treasure:Destroyed": self.treasure_collected,
            "Game:Treasure:Opened": self.treasure_opened,
            "Game:Treasure:Pushed": self.treasure_pushed_aside,
            "Game:Treasure:TouchedDown": self.treasure_touched_down,
            "Game:Trophy:Destroyed": self.trophy_collected,
            "Game:Trophy:Opened": self.trophy_opened,
            "Game:Trophy:Pushed": self.trophy_pushed_aside,
            "Game:Trophy:TouchedDown": self.trophy_touched_down,
            "Game:ZDiamond:Destroyed": self.zdiamond_collected,
            "Game:ZDiamond:TouchedDown": self.diamond_touched_down,
            "Game:Zombie:Attacking": self.zombie_attacking,
            "Game:Zombie:Dying": self.zombie_dying,
        }

        #~ self.level = 7 # debugging

    # end def


    def bind_canvas_events (self, *args, **kw):
        """
            event handler;
            canvas event bindings;
        """
        # canvas keyboard event bindings
        for _seq, _cb in self.KEYMAP.items():
            self.canvas.bind_all(_seq, _cb)
        # end for
        # canvas mouse event bindings
        self.canvas.bind("<Button-1>", self.on_mouse_down)
        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
    # end def


    def bind_events (self, *args, **kw):
        """
            event handler;
            app-wide event bindings;
        """
        # connecting people...
        self.events.connect_dict(self.events_dict)
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


    def clear_canvas (self, *args, **kw):
        """
            event handler;
            clears canvas and stops unexpected events;
        """
        # unbind all events
        self.unbind_events()
        # stop any scheduled thread
        self.animations.clear_all()
        # clear canvas
        self.canvas.clear()
    # end def


    def decrease_diamonds_count (self, *args, **kw):
        """
            event handler;
            updates diamond collection counter;
        """
        # update remaining diamonds
        self.objects.diamonds_count -= 1
        # update display
        self.update_diamonds_count()
        # no more diamonds?
        if self.objects.diamonds_count < 1:
            # yeah! winner!
            self.won_level()
            # confirm it is finished
            return True
        # end if
        # not finished
        return False
    # end def


    def diamond_collected (self, sprite, *args, **kw):
        """
            event handler for diamond catch;
        """
        # counted falling sprite has been collected
        self.sprite_collected(sprite, "diamond", 200)
    # end def


    def diamond_touched_down (self, *args, **kw):
        """
            event handler for diamond touchdown;
        """
        # play sound
        self.play_sound("diamond touched down", trackname="diamond")
    # end def


    def draw_level (self):
        """
            drawing game play level;
        """
        # inits
        self.clear_canvas()
        # try to set up current level
        try:
            # load level data
            self.objects.load_data(self.get_level_fpath(self.level))
        # got in trouble
        except Exception as e:
            #~ raise e from None
            # stop all!
            exit(
                "An exception has occurred:\n{}\n"
                "Fatal error while trying to draw level {}"
                .format(e, self.level)
            )
        # end try
        for _sprite in self.objects.matrix.objects():
            _sprite.start()
        # end for
        # set player to foreground
        self.canvas.tag_raise(
            self.objects.player_sprite.canvas_id, TK.ALL
        )
        # reset canvas text items viewport fixed layer
        self.fixed_layer.clear()
        # init options
        _opts = dict(font="{} 26".format(FONT1), fill="bisque1")
        _cx, _cy = self.canvas.center_xy()
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
            text=_(self.objects.level_name),
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
            text=_("level {}").format(self.level),
            font="{} 36".format(FONT2),
            fill="white",
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
        # scheduled tasks
        self.scroll_to_player(ticks=25.0, autoloop=False)
        self.animations.run_after(1800, self.remove_headings)
        self.animations.run_after(1200, self.update_falldown)
        self.animations.run_after(1000, self.bind_events)
        self.animations.run_after(1000, self.scroll_to_player)
        self.animations.run_after(800, self.update_game_data)
        # notify stats unit
        self.events.raise_event(
            "Stats:Level:Started", level=self.level
        )
        # notify game has started
        self.events.raise_event(
            "Main:Game:Started",
            player_sprite=self.objects.player_sprite,
            objects=self.objects,
        )
    # end def


    def earth_digged (self, *args, **kw):
        """
            event handler for digged earth;
        """
        # play sound
        self.play_sound("earth digged", trackname="background")
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


    def golden_key_collected (self, sprite, *args, **kw):
        """
            event handler for golden key catch;
        """
        # counted falling sprite has been collected
        self.sprite_collected(sprite, "golden key", 500)
    # end def


    def golden_key_touched_down (self, *args, **kw):
        """
            event handler for golden key touchdown;
        """
        # play sound
        self.play_sound("golden key touched down", trackname="diamond")
    # end def


    def goto_main_menu (self, *args, **kw):
        """
            event handler;
            ask to return to game's main menu;
        """
        self.events.raise_event("Main:Menu:ShowMainMenu")
    # end def


    def next_level (self, *args, **kw):
        """
            event handler;
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
        # disable gameplay events
        self.unbind_events()
        # go to main menu screen
        self.goto_main_menu()
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
            event handler;
            user asked for a game pause/resume;
        """
        # got to resume?
        if self.game_paused:
            self.game_paused = False
            self.canvas.unbind_all("<space>")
            self.canvas.delete("pause_group")
            self.events.raise_event("Main:Game:Resumed")
            self.scroll_to_player()
            self.update_falldown()
            self.bind_canvas_events()
            self.update_game_data()
        # pause game
        else:
            self.game_paused = True
            self.unbind_canvas_events()
            self.animations.stop(
                self.scroll_to_player,
                self.scroll_animation_loop,
                self.update_falldown,
                self.update_countdown,
            )
            self.events.raise_event("Main:Game:Paused")
            # show some text
            x, y = self.canvas.viewport_center_xy()
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


    def play_sound (self, sound_name, trackname=None, volume=0.5):
        """
            plays asynchronous sound;
        """
        # game options
        if not self.switch_off_sound:
            # inits
            track = self.SNDTRACK.get(str(trackname).lower()) or 1
            track = max(1, min(track, len(self.soundtracks))) - 1
            sound_name = str(sound_name).replace(" ", "-")
            # play sound
            self.soundtracks[track].play(
                "audio/{}.wav".format(sound_name), volume
            )
        # end if
    # end def


    def player_dead (self, *args, **kw):
        """
            event handler;
            player is now really dead;
        """
        # animated text
        x, y = self.canvas.viewport_center_xy()
        _fx = FXFT.TkGameFXFlyingText(self.canvas)
        _fx.create_text(
            x, y + 50,
            text=_("GAME OVER"),
            font="{} 48".format(FONT1),
            fill="yellow",
            shadow=(+4, +4, "darkred"),
        )
        _fx.start(
            curve_y=_fx.fx_ln(amplitude=20, offset=1),
            keep_alive=True,
        )
        # notify game has ended
        self.events.raise_event("Main:Game:Over")
        # return to main menu screen
        self.animations.run_after(3000, self.goto_main_menu)
    # end def


    def player_frozen (self, *args, **kw):
        """
            event handler;
            player has been frozen by an enemy;
        """
        # canvas event unbindings
        self.unbind_canvas_events()
        # play sound
        self.play_sound("player frozen", trackname="player")
    # end def


    def player_splashed (self, *args, **kw):
        """
            event handler;
            player has been splashed;
        """
        # canvas event unbindings
        self.unbind_canvas_events()
        # play sound
        self.play_sound("player dead", trackname="player")
    # end def


    def pudiamond_collected (self, sprite, *args, **kw):
        """
            event handler for prize-unlocker diamond catch;
        """
        # counted falling sprite has been collected
        self.sprite_collected(sprite, "diamond", 500)
    # end def


    def remove_falling (self, sprite, *args, **kw):
        """
            event handler;
            removes sprite from falling_sprites list;
        """
        # drop sprite from managed list
        if sprite in self.objects.falling_sprites:
            self.objects.falling_sprites.remove(sprite)
        # end if
    # end def


    def remove_headings (self, *args, **kw):
        """
            event handler;
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


    def rock_pushed_aside (self, *args, **kw):
        """
            event handler for rock pushes;
        """
        # play sound
        self.play_sound("rock pushed aside", trackname="player")
    # end def


    def rock_touched_down (self, *args, **kw):
        """
            event handler for rock touchdown;
        """
        # play sound
        self.play_sound("rock touched down", trackname="rock")
    # end def


    def rockdiamond_changed (self, *args, **kw):
        """
            event handler for rockdiamond end of transformation;
        """
        # add some score
        self.score_add(100)
    # end def


    def rockdiamond_changing (self, *args, **kw):
        """
            event handler for rockdiamond transformation;
        """
        # play sound
        self.play_sound(
            "rockdiamond changing", trackname="rockdiamond"
        )
    # end def


    def rockdiamond_touched_down (self, sprite, *args, **kw):
        """
            event handler for rockdiamond touchdown;
        """
        # rock state?
        if sprite.state == "default":
            # rock touched down
            self.rock_touched_down()
        else:
            # diamond touched down
            self.diamond_touched_down()
        # end if
    # end def


    def run (self, *args, **kw):
        """
            event handler;
            game play inits;
        """
        # reset score from here
        self.score = 0
        # draw current level
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
        cx, cy = self.canvas.center_xy()
        cw = self.canvas.winfo_reqwidth()
        x, y = self.objects.player_sprite.xy
        x0, y0 = self.canvas.viewport_xy((cx, cy))
        dx, dy = (x - x0), (y - y0)
        mw, mh = self.objects.matrix.width_height()
        # fixing canvas fuzzy values
        if abs(dx) < 2 or x > mw - cx:
            x0 = x
        # end if
        if abs(dy) < 2 or y > mh - cy:
            y0 = y
        # end if
        # run animation loop
        self.animations.run_after(
            25,
            self.scroll_animation_loop,
            x0, y0, x, y,
            dx/ticks, dy/ticks,
            cx, cy, cw, mw, mh
        )
        # need to loop again?
        if autoloop:
            self.animations.run_after(
                25 * (ticks + 2), self.scroll_to_player, ticks, True
            )
        # end if
    # end def


    def show_cool_info (self, tuple_xy, **options):
        """
            shows a short flying text at position (x, y);
        """
        # inits
        _frms = options.pop("frames", 5)
        _delay = options.pop("delay", 50)
        _opts = dict(
            text="cool info",
            font="{} 28".format(FONT2),
            fill="yellow",
        )
        _opts.update(options)
        x, y = tuple_xy
        _fx = FXFT.TkGameFXFlyingText(self.canvas)
        _fx.create_text(x, y, **_opts)
        # show cool info
        _fx.start(frames=_frms, delay=_delay)
    # end def


    def sprite_collected (self, sprite, sname, score, trackname="diamond"):
        """
            counted falling sprite has been collected;
        """
        # play sound
        self.play_sound("{} collected".format(sname), trackname)
        # drop sprite from managed list
        self.remove_falling(sprite)
        # show cool info on canvas
        self.show_cool_info(sprite.xy, text="+{}".format(score))
        # free some memory
        del sprite
        # update score
        self.score_add(score)
        # decrement diamonds count
        return self.decrease_diamonds_count()
    # end def


    def treasure_collected (self, sprite, *args, **kw):
        """
            event handler for open treasure catch;
        """
        # counted falling sprite has been collected
        self.sprite_collected(sprite, "treasure", 1000)
    # end def


    def treasure_opened (self, *args, **kw):
        """
            event handler for treasure opening;
        """
        # play sound
        self.play_sound("treasure opened", trackname="player")
    # end def


    def treasure_pushed_aside (self, *args, **kw):
        """
            event handler for treasure pushes;
        """
        # play sound
        self.play_sound("treasure pushed aside", trackname="player")
    # end def


    def treasure_touched_down (self, *args, **kw):
        """
            event handler for treasure touchdown;
        """
        # play sound
        self.play_sound("treasure touched down", trackname="diamond")
    # end def


    def trophy_collected (self, sprite, *args, **kw):
        """
            event handler for trophy catch;
        """
        # counted falling sprite has been collected
        self.sprite_collected(sprite, "trophy", 5000)
    # end def


    def trophy_opened (self, sprite, *args, **kw):
        """
            event handler for trophy opening/enabling;
        """
        # play sound
        self.play_sound("trophy opened", trackname="player")
        # show cool info on canvas
        self.show_cool_info(sprite.xy, text="+1000", delay=100, frames=10)
        # add some good points
        self.score_add(1000)
    # end def


    def trophy_pushed_aside (self, *args, **kw):
        """
            event handler for trophy pushes;
        """
        # play sound
        self.play_sound("trophy pushed aside", trackname="player")
    # end def


    def trophy_touched_down (self, *args, **kw):
        """
            event handler for trophy touchdown;
        """
        # play sound
        self.play_sound("trophy touched down", trackname="diamond")
    # end def


    def unbind_canvas_events (self, *args, **kw):
        """
            event handler;
            canvas event unbindings;
        """
        # canvas keyboard event unbindings
        for _seq in self.KEYMAP:
            self.canvas.unbind_all(_seq)
        # end for
        # canvas mouse event unbindings
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
    # end def


    def unbind_events (self, *args, **kw):
        """
            event handler;
            gameplay event unbindings;
        """
        # unbind gameplay events
        # CAUTION: do *NOT* use
        # self.events.disconnect_dict(self.events_dict)
        # here as we must also disconnect sprites' refs
        # to get entirely clear
        self.events.disconnect_group("Game:")
        self.events.disconnect_group("Main:Game:")
        # unbind canvas events
        self.unbind_canvas_events()
    # end def


    def update_countdown (self, *args, **kw):
        """
            event handler;
            updates timer countdown display;
        """
        _c = self.objects.countdown = max(
            0, min(600, self.objects.countdown - 1)
        )
        self.canvas.itemconfigure(
            self.cid_countdown,
            text=self.format_time()
        )
        # hurry up!
        if _c <= 10:
            self.canvas.itemconfigure(
                self.cid_countdown, fill="tomato"
            )
            if _c and not (_c % 2):
                self.play_sound(
                    "countdown alarm", trackname="alarm"
                )
            # end if
            self.animations.run_after(250, self.blink_countdown)
        # end if
        # time is out!
        if not _c:
            self.animations.stop(self.blink_countdown)
            self.objects.player_sprite.splashed()
        # keep on counting down
        else:
            self.animations.run_after(1000, self.update_countdown)
        # end if
    # end def


    def update_db_options (self, db):
        """
            updates game options along with @db database, if any;
        """
        # param controls
        if db:
            # inits
            self.switch_off_sound = db.get_option("Sound:Switch:Off")
        else:
            # default values
            self.switch_off_sound = False
        # end if
    # end def


    def update_diamonds_count (self, *args, **kw):
        """
            event handler;
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
            event handler;
            updates falling down procedure;
        """
        for sprite in self.objects.falling_sprites:
            sprite.fall_down()
        # end for
        self.animations.run_after(200, self.update_falldown)
    # end def


    def update_game_data (self, *args, **kw):
        """
            event handler;
            updates all game data display offs;
        """
        self.update_diamonds_count()
        self.update_score()
        self.update_countdown()
    # end def


    def update_score (self, value=None, *args, **kw):
        """
            event handler;
            updates diamond count display;
        """
        # update display
        self.canvas.itemconfigure(
            self.cid_score, text=self.format_score(value)
        )
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
            self.high_score,
            title_color="lemon chiffon",
            subtitle_color="powder blue"
        )
        # stop game music background
        self.events.raise_event("Main:Music:Stop")
        # play sound
        self.play_sound("player won all", trackname="background")
        # notify stats unit
        self.events.raise_event(
            "Stats:Level:Won:All", score=self.high_score
        )
        # reset level
        self.level = 1
        # main menu screen
        self.animations.run_after(3300, self.goto_main_menu)
        # events binding
        self.canvas.bind_all("<Escape>", self.on_key_escape)
    # end def


    def won_level (self):
        """
            player won the current level;
        """
        #~ print("remaining time:", self.objects.countdown)
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
            self.score,
            title_color="yellow",
            subtitle_color="antique white"
        )
        # stop game music background
        self.events.raise_event("Main:Music:Stop")
        # play sound
        self.play_sound("player won level", trackname="background")
        # update high score
        self.high_score = max(self.high_score, self.score)
        # notify stats unit
        self.events.raise_event(
            "Stats:Level:Won", level=self.level, score=self.score
        )
        # go to next level
        self.animations.run_after(4000, self.next_level)
        # events binding
        self.canvas.bind_all("<Escape>", self.on_key_escape)
    # end def


    def won_text (self, title, subtitle, score, **kw):
        """
            texts for winning screens;
        """
        # inits
        x, y = self.canvas.center_xy()
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
            text=_("Score: {}").format(score),
            font="{} 24".format(FONT2),
            fill=kw.get("title_color") or "white",
        )
    # end def


    def zdiamond_collected (self, sprite, *args, **kw):
        """
            event handler for zdiamond catch;
        """
        # counted falling sprite has been collected
        if not self.sprite_collected(sprite, "zdiamond", 500):
            # show cool info on canvas
            self.show_cool_info(
                sprite.xy,
                text=_("you killed a zombie!"),
                font="{} 20".format(FONT1),
                fill="white",
                delay=100,
                frames=10,
            )
            # remove only one zombie at a time
            for sprite in self.objects.matrix.objects():
                if "zombie" in sprite.role and hasattr(sprite, "killed"):
                    sprite.killed()
                    break
                # end if
            # end for
        # end if
    # end def


    def zombie_attacking (self, *args, **kw):
        """
            event handler for attacking zombie;
        """
        # play sound
        self.play_sound("zombie attacking", trackname="enemy")
    # end def


    def zombie_dying (self, sprite, *args, **kw):
        """
            event handler for dying zombie;
        """
        # play sound
        self.play_sound("zombie dying", trackname="enemy")
        # show cool info on canvas
        self.show_cool_info(sprite.xy, text="+100")
        # free some memory
        del sprite
        # update score
        self.score_add(100)
    # end def
    
    def reset_game(self, *args, **kw):
        """
            event handler to reset the game
            
            Afterwards, we can add a number of life and so, decrease it
            from here too
        """
        self.objects.player_sprite.splashed()

# end class GamePlay
