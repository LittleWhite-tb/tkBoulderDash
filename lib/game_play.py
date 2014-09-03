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
from . import tkgame_animations as AP
from . import tkgame_fx_rotating_sun as FXRS


class GamePlay:
    """
        gestionnaire de partie
    """

    # class constants
    TPL_LEVEL_FILE = "data/json/level_{}.json"


    def __init__ (self, owner, canvas, level=1):
        """
            class constructor
        """
        # member inits
        self.owner = owner
        self.canvas = canvas
        self.level = level
        self.events = EM.get_event_manager()
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
            activation des événements canvas
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
            gestionnaire d'événements appli
        """
        # connecting people...
        self.events.connect_dict(
            {
                "Main:Earth:Digged": self.earth_digged,
                "Main:Diamond:Collected": self.diamond_collected,
                "Main:Player:Splashed": self.player_splashed,
                "Main:Player:Dead": self.player_dead,
            }
        )
        self.bind_canvas_events()
    # end def


    def center_xy (self, widget):
        """
            retourne le tuple (x, y) du point central d'un widget
            tkinter donné;
        """
        return (widget.winfo_reqwidth()/2, widget.winfo_reqheight()/2)
    # end def


    def clear_canvas (self, *args, **kw):
        """
            efface le canevas graphique
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


    def diamond_collected (self, *args, **kw):
        """
            gère le cas d'un diamant absorbé par le joueur
        """
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
            drawing game play level
        """
        self.clear_canvas()
        self.objects.load_data(self.get_level_fpath(self.level))
        for _sprite in self.objects.matrix.objects():
            _sprite.start()
        # end for
        # init remaining diamonds
        self.remaining_id = self.canvas.create_text(
            10, 10,
            anchor=TK.NE,
            text=str(self.objects.diamonds_count),
            font="sans 26 bold",
            fill="bisque2",
        )
        # init player score
        self.score = 0
        self.score_id = self.canvas.create_text(
            10, 10,
            anchor=TK.N,
            text=self.format_score(),
            font="sans 26 bold",
            fill="bisque1",
        )
        # reconfigure canvas
        self.canvas.configure(
            bg="sienna",
            scrollregion=self.objects.matrix.bbox_xy(),
        )
        self.scroll_to_player(ticks=25.0, autoloop=False)
        self.animations.run_after(1000, self.bind_events)
        self.animations.run_after(1000, self.scroll_to_player)
    # end def


    def earth_digged (self, *args, **kw):
        """
            gère le cas du joueur qui creuse la terre
        """
        # ça vaut 50 points
        self.score_add(50)
    # end if


    def format_score (self, value=None):
        """
            formate l'affichage du score
        """
        if value is None:
            value = self.score
        # end if
        return "{:04d}".format(value)
    # end def


    def get_level_fpath (self, level):
        """
            retourne le chemin absolu du fichier JSON de données
            d'un niveau jouable;
            le paramètre @level est un entier non nul;
        """
        return OP.abspath(
            OP.expanduser(
                self.TPL_LEVEL_FILE.format(max(1, int(level)))
            )
        )
    # end def


    def next_level (self, *args, **kw):
        """
            passage au niveau suivant ou retour au menu principal si
            pas de niveau suivant (après bouquet final quand même);
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
            le joueur demande à sortir du jeu
        """
        # go to main menu screen
        self.owner.main_menu_screen()
    # end def


    def on_key_pressed (self, event=None):
        """
            gestionnaire appuis touches du clavier
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
        self.mouse_down = True
        self.canvas.scan_mark(event.x, event.y)
        self.animations.stop(self.scroll_to_player)
    # end def


    def on_mouse_move (self, event=None):
        if self.mouse_down:
            self.canvas.scan_dragto(event.x, event.y)
        # end if
    # end def


    def on_mouse_up (self, event=None):
        self.mouse_down = False
        self.animations.run_after(1, self.scroll_to_player)
    # end def


    def pause_game (self, *args, **kw):
        """
             le joueur suspend la partie
        """
        # got to resume?
        if self.game_paused:
            self.game_paused = False
            self.canvas.unbind_all("<space>")
            self.canvas.delete("pause_group")
            self.events.raise_event("Main:Game:Resumed")
            self.scroll_to_player()
            self.bind_canvas_events()
        # pause game
        else:
            self.game_paused = True
            self.unbind_canvas_events()
            self.animations.stop(
                self.scroll_to_player, self.scroll_animation_loop
            )
            self.events.raise_event("Main:Game:Paused")
            x, y = self.viewport_center_xy()
            _opts = dict(
                anchor=TK.CENTER,
                text="PAUSE",
                font="sans 96 bold",
                tags="pause_group",
            )
            self.canvas.create_text(x + 4, y + 4, fill="#400", **_opts)
            self.canvas.create_text(x, y, fill="gold", **_opts)
            self.canvas.create_text(
                x, y + 70,
                text="Press spacebar to continue",
                font="sans 20 bold",
                fill="pale goldenrod",
                tags="pause_group",
            )
            self.canvas.bind_all("<space>", self.pause_game)
        # end if
    # end def


    def player_dead (self, *args, **kw):
        """
            le joueur vient de mourir
        """
        self.animations.run_after(3000, self.owner.main_menu_screen)
    # end def


    def player_splashed (self, *args, **kw):
        """
            le joueur vient de se faire écraser
        """
        # on désactive les événements canevas
        self.unbind_canvas_events()
    # end def


    def run (self):
        """
            game play inits
        """
        self.draw_level()
    # end def


    def score_add (self, value):
        """
            ajoute une valeur au score
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
            boucle animation incrémentation du score
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
            boucle d'animation du défilement écran
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
            self.remaining_id, self.canvas.canvasx(cw - 10), y
        )
        # update pos
        self.canvas.coords(self.score_id, self.canvas.canvasx(cx), y)
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
            ajuste la zone d'affichage du canvas de sorte que le
            joueur soit toujours visible;
        """
        # animation inits
        x, y = self.objects.player_sprite.xy
        x0, y0 = self.viewport_center_xy()
        cx, cy = self.center_xy(self.canvas)
        cw = self.canvas.winfo_reqwidth()
        mw, mh = self.objects.matrix.width_height()
        # ceci corrige des imprécisions de canevas
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
            désactivation des événements propres au canevas
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
            désactivation de tous les événements
        """
        # unbind app events
        self.events.disconnect_all()
        # unbind canvas events
        self.unbind_canvas_events()
    # end def


    def viewport_center_xy (self):
        """
            retourne le tuple (x, y) du point central du canevas
            converti en position réelle dans la scrollregion;
        """
        return self.viewport_xy(self.center_xy(self.canvas))
    # end def


    def viewport_xy (self, xy):
        """
            retourne le tuple (x, y) d'un point de position relative
            (screenx, screeny) dans le viewport du canevas en
            position absolue dans la scrollregion du canevas;
        """
        # conversion viewport --> scrollregion
        return (self.canvas.canvasx(xy[0]), self.canvas.canvasy(xy[1]))
    # end def


    def won_all (self):
        """
            le joueur a tout gagné ! super congrats !
        """
        # clean-ups
        self.clear_canvas()
        # new graphical special effects
        _fx = FXRS.TkGameFXRotatingSun(self.canvas)
        _fx.start()
        # inits
        x, y = self.viewport_center_xy()
        # texts
        self.canvas.create_text(
            x + 4, y - 46,
            text="Champion !",
            font="bdcartoonshout 48 bold",
            fill="grey20",
        )
        self.canvas.create_text(
            x, y - 50,
            text="Champion !",
            font="bdcartoonshout 48 bold",
            fill="lemon chiffon",
        )
        self.canvas.create_text(
            x, y + 20,
            text="Vous avez tout gagné !",
            font="andreakarime 24 bold",
            fill="powder blue",
        )
        # reset level
        self.level = 1
        # events binding
        self.canvas.bind_all("<Escape>", self.on_key_escape)
        # main menu screen
        self.animations.run_after(5000, self.owner.main_menu_screen)
    # end def


    def won_level (self):
        """
            le joueur a réussi le niveau ! congrats !
        """
        # clean-ups
        self.clear_canvas()
        # new graphical special effects
        _fx = FXRS.TkGameFXRotatingSun(
            self.canvas, bgcolor="saddle brown", fgcolor="sienna"
        )
        _fx.start()
        # inits
        x, y = self.viewport_center_xy()
        # texts
        self.canvas.create_text(
            x + 4, y - 46,
            text="Bravo !",
            font="bdcartoonshout 48 bold",
            fill="grey20",
        )
        self.canvas.create_text(
            x, y - 50,
            text="Bravo !",
            font="bdcartoonshout 48 bold",
            fill="yellow",
        )
        self.canvas.create_text(
            x, y + 20,
            text="Vous avez réussi !",
            font="andreakarime 24 bold",
            fill="antique white",
        )
        # niveau suivant
        self.animations.run_after(3000, self.next_level)
    # end def

# end class GamePlay
