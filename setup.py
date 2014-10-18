#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name="tkBoulderDash",
    version="0.36b",
    requires=["Tkinter"],
    description="tkBoulderDash - a Python3/Tkinter port of the famous game",
    author="Raphaël SEBAN",
    author_email="motus@laposte.net",
    maintainer="Raphaël SEBAN",
    maintainer_email="motus@laposte.net",
    url="https://github.com/tarball69/tkBoulderDash",
    download_url="https://github.com/tarball69/tkBoulderDash/releases",
    keywords=["tkinter", "game", "boulderdash"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Environment :: Win32 (MS Windows)",
        "Environment :: X11 Applications",
        "Environment :: X11 Applications :: Gnome",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: OS Independent",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Games/Entertainment",
        "Topic :: Games/Entertainment :: Arcade",
        "Topic :: Games/Entertainment :: Puzzle Games",
    ],
    license="""
Licensed under GNU General Public License v3.
    """,
    long_description="""

**tkBoulderDash** is a simple Python3/Tkinter port of **First Star
Software** famous **Boulder Dash&trade;** 1980s retro game.

This game is a **freefullware** (see [below](#freefullware)).

Please, feel free to visit [project's website] (http://tarball69.github.io/tkBoulderDash/).

Copyright
---------

Copyright (c) 2014 Raphaël Seban <motus@laposte.net>

License
-------

This software is licensed under **GNU GPL General Public License v3**.

Quick start
-----------

Notice
------

This software runs only with **Python3** and **Tkinter** installed
on your machine.

**No dependencies**, no third-part lib to install on more.

If you have Python3 correctly installed, Tkinter library should also
be installed **by default** as a Python standard lib.

Any **ImportError** will mean either you are trying to launch the
game with Python2 or you don't have **Tkinter** library correctly
installed on your system.

Installing a Python3 version of the language **does not alter** an
already installed Python2 version in any way.

You may consider installing Python3 from:

https://www.python.org/downloads/ (Ctrl+click: open in new tab)

MS-Windows users
----------------

Simply double-click on **game.py** file and play.

UNIX/Linux users
----------------

Click on **game.py** file if it has the executable sticky bit on or
open a shell console and launch file:

::

    $ python3 game.py

What is a freefullware?
-----------------------

A **freefullware** is a new kind of software:

* Free as in Freedom;
* Free of charge (gratis);
* Ad-free (no advertisement at all);
* Donate-free (no 'Donate' button at all);
* 100% virus-free;
* no counterpart at all;
* really absolutely free;

Just get it and enjoy.

That's all, folks!

Bug report
----------

In order to **track bugs** and fix them correctly, we'd like to hear
from you.

**If you encountered any problem** during the use of this game,
please leave us a comment and tell us:

* environment:
    * which platform? (Windows, macOS, Linux)
    * which Python version? (2.7+, 3.2+)
    * which game release version?
    * tkinter installed correctly? (yes/no)

* traceback (optional):
    * could you copy/paste the console error text, please?
    * could you tell us few words about what happened?

**Whatever happened**, we'd like to know about it.

You will find a bug tracker service where you can post your issues at:

https://github.com/tarball69/tkBoulderDash/issues

**Thank you for contributing** to make this project a cool game for
everyone.

"""
)
