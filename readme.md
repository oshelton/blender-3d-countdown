Jack "Owen" Shelton
Blender3D Countdown Script

# Archived

This is for an ancient version of Blender that nobody should really be using anymore.

# Intro

This script allows for the creation of animated countdowns using Blender's Text object.  The script uses Blender3D's animation length and framerate setting to generate a countdown.

This script only works with pre 2.5 versions of blender.  Odds are there are alternatives for newer versions of Blender.

![](countdown.jpg)

# Features

User-defined object name, the countdown can be applied to any Text object.
Start and end offsets, allowing for delays before the coundown starts and after it ends.
Option to show or hide milliseconds remaining.


# Installation

Move the countdown_gui.py file and countdown.py file to your Blender3D scripts directory.  The countdown_gui.py file will register countdown.py as a FrameChanged script link, but it only searches in the script directory so it is extremely importantthat both script files are in the scripts directory and not a subfolder of it.


# Running

Execute the Countdown Gui script from the wizards script menu and have fun!  Remember that in order for any changes made in the gui to be reflected on the text object the update button must be clicked.


# Licensing

Both script files, much like pretty much every Blender script, are licensed under the terms of the GPL.
