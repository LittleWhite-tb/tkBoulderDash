#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name = "tk2048",
    version = "1.1",
    requires = ["Tkinter"],
    description = "tk2048 - Python3-Tkinter port of Gabriele Cirulli's 2048 famous Game",
    author = "Raphaël SEBAN",
    author_email = "motus@laposte.net",
    maintainer = "Raphaël SEBAN",
    maintainer_email = "motus@laposte.net",
    url = "https://github.com/tarball69/tk2048",
    download_url = "https://github.com/tarball69/tk2048",
    keywords = ["tkinter", "game", "2048"],
    classifiers = [
        "Development Status :: 5 - Production/Stable",
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
        "Topic :: Games/Entertainment :: Board Games",
        "Topic :: Games/Entertainment :: Puzzle Games",
    ],
    license = """
Licensed under GNU General Public License v3.
    """,
    long_description = """

tk2048 - Python3-Tkinter port of Gabriele Cirulli's 2048 famous Game.

This game is a **freefullware** (see below).

Copyright
---------

Copyright (c) 2014 Raphaël Seban <motus@laposte.net>

License
-------

This software is licensed under **GNU GPL General Public License v3**.

New in v1.1
-------------

* added new high-score feature;

* added new 'New Game' button;

* added new GridAnimation class;

Quick start
-----------

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

**If you encountered any problem** during the use of `tk2048`,
please leave us a comment and tell us:

* environment:
    * which platform? (Windows, macOS, Linux)
    * which Python version? (2.7+, 3.2+)
    * which tk2048 version?
    * tkinter installed correctly? (yes/no)

* traceback (optional):
    * could you copy/paste the console error text, please?
    * could you tell us few words about what happened?

**Whatever happened**, we'd like to know about it.

You will find an open issue **"It did *NOT* work for me!"** at:

https://github.com/tarball69/tk2048/issues/1

**Thank you for contributing** to make `tk2048` a cool game for
everyone.

"""
)
