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


    def run (self):
        """
            game play inits
        """
        self.draw_level()
    # end def


    def draw_level (self):
        """
            drawing game play level
        """
        self.unbind_events()
        self.clear_canvas()
        self.objects.load_data(self.get_level_fpath(self.level))
        for _sprite in self.objects.collection:
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
        self.scroll_to_player(25.0)
        self.bind_events()
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


    def clear_canvas (self, *args, **kw):
        """
            efface le canevas graphique
        """
        self.canvas.delete(TK.ALL)
        self.canvas.configure(bg="black", scrollregion=(0,0,10,10))
    # end def


    def format_score (self, value=None):
        """
            formate l'affichage du score
        """
        if value is None:
            value = self.score
        # end if
        return "{:04d}".format(value)
    # end def


    def score_add (self, value):
        """
            ajoute une valeur au score
        """
        # param inits
        value = abs(int(value))
        # score display animation
        self.animations.run_after(
            100,
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
        self.canvas.itemconfigure(
            self.score_id, text=self.format_score(start)
        )
        start = min(stop, start + step)
        if start <= stop:
            self.animations.run_after(
                50, self.score_display_loop, start, stop, step
            )
        # end if
    # end def


    def scroll_to_player (self, ticks=3.0):
        """
            ajuste la zone d'affichage du canvas de sorte que le
            joueur soit toujours visible;
        """
        # animation inits
        x, y = self.objects.player_sprite.xy
        oldx, oldy = self.objects.player_sprite.old_xy
        cx, cy = self.center_xy(self.canvas)
        cw = self.canvas.winfo_reqwidth()
        mw, mh = self.objects.matrix.width_height()
        # update old coordinates
        self.objects.player_sprite.old_xy = self.objects.player_sprite.xy
        # run animation loop
        self.animations.run_after(
            50,
            self.scroll_animation_loop,
            oldx, oldy, x, y, (x - oldx)/ticks, (y - oldy)/ticks,
            cx, cy, cw, mw, mh
        )
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
        y = self.canvas.canvasy(10)
        self.canvas.coords(
            self.remaining_id, self.canvas.canvasx(cw - 10), y
        )
        self.canvas.coords(self.score_id, self.canvas.canvasx(cx), y)
        # no more movement to handle?
        if not (stepx or stepy):
            # trap out!
            return
        # end if
        # update coords
        startx += stepx
        starty += stepy
        loopx = bool(
            (stepx > 0 and startx < stopx) or
            (stepx < 0 and startx > stopx)
        )
        loopy = bool(
            (stepy > 0 and starty < stopy) or
            (stepy < 0 and starty > stopy)
        )
        # should keep on looping?
        if loopx or loopy:
            self.animations.run_after(
                40,
                self.scroll_animation_loop,
                startx, starty, stopx, stopy, stepx, stepy, cx, cy,
                cw, mw, mh
            )
        # last loop
        else:
            self.animations.run_after(
                40,
                self.scroll_animation_loop,
                stopx, stopy, 0, 0, 0, 0, cx, cy, cw, mw, mh
            )
        # end if
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
        self.canvas.bind_all("<Escape>", self.owner.main_menu_screen)
        self.canvas.bind_all("<space>", self.pause_game)
        self.canvas.bind_all("<Key>", self.on_key_pressed)
        self.canvas.bind("<Button-1>", self.on_mouse_down)
        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
    # end def


    def unbind_events (self, *args, **kw):
        """
            désactivation de tous les événements
        """
        # unbind events
        self.events.disconnect_all(
            "Main:Earth:Digged",
            "Main:Diamond:Collected",
            "Main:Player:Splashed",
            "Main:Player:Dead",
        )
        self.unbind_canvas_events()
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
            self.scroll_to_player()
        # end if
    # end def


    def on_mouse_down (self, event=None):
        self.mouse_down = True
        self.canvas.scan_mark(event.x, event.y)
    # end def


    def on_mouse_move (self, event=None):
        if self.mouse_down:
            self.canvas.scan_dragto(event.x, event.y)
        # end if
    # end def


    def on_mouse_up (self, event=None):
        self.mouse_down = False
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
            self.bind_events()
            self.scroll_to_player()
        # pause game
        else:
            self.game_paused = True
            self.unbind_events()
            self.events.raise_event("Main:Game:Paused")
            self.animations.stop_all()
            x, y = self.center_xy(self.canvas)
            x = self.canvas.canvasx(x)
            y = self.canvas.canvasy(y)
            _opts = dict(
                anchor=TK.CENTER,
                text="PAUSE",
                font="sans 96 bold",
                tags="pause_group",
            )
            self.canvas.create_text(x+4, y+4, fill="#400", **_opts)
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


    def earth_digged (self, *args, **kw):
        """
            gère le cas du joueur qui creuse la terre
        """
        # ça vaut 50 points
        self.score_add(50)
    # end if


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
            self.bravo()
        # end if
    # end def


    def player_splashed (self, *args, **kw):
        """
            le joueur vient de se faire écraser
        """
        # on désactive les événements canevas
        self.unbind_canvas_events()
    # end def


    def player_dead (self, *args, **kw):
        """
            le joueur vient de mourir
        """
        self.unbind_events()
        self.animations.run_after(3000, self.owner.main_menu_screen)
    # end def


    def bravo (self):
        """
            le joueur a réussi ! congrats !
        """
        self.unbind_events()
        self.clear_canvas()
        x, y = self.center_xy(self.canvas)
        self.canvas.create_text(
            x, y - 60,
            text="Bravo !",
            font="sans 32 bold",
            fill="yellow",
        )
        self.canvas.create_text(
            x, y - 10,
            text="Vous avez réussi !",
            font="sans 16 bold",
            fill="antique white",
        )
        # niveau suivant
        self.animations.run_after(3000, self.next_level)
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
            self.bouquet_final()
        # end if
    # end def


    def bouquet_final (self):
        """
            le joueur a tout gagné ! super congrats !
        """
        self.unbind_events()
        self.clear_canvas()
        x, y = self.center_xy(self.canvas)
        self.canvas.create_text(
            x, y - 60,
            text="Champion !",
            font="sans 32 bold",
            fill="sky blue",
        )
        self.canvas.create_text(
            x, y - 10,
            text="Vous avez tout gagné !",
            font="sans 16 bold",
            fill="bisque3",
        )
        # niveau suivant
        self.animations.run_after(3000, self.owner.main_menu_screen)
    # end def


    def center_xy (self, widget):
        """
            retourne le tuple (x, y) du point central d'un widget
            tkinter donné;
        """
        return (widget.winfo_reqwidth()/2, widget.winfo_reqheight()/2)
    # end def

# end class GamePlay
