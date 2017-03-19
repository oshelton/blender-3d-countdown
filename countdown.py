#!BPY
# -*- coding:Shift_JIS -*-

__author__ = "Jack Owen Shelton"
__version__ = "1.0"

__bpydoc__ = """\

This script updates the text of an already existing text object to that of a countdown.
The format is HH:MM:SS, and hundreths of a second are displayed if the option was enabled in the configuration script.
Configuration settings for this script are stored in the Blender registry and can be edited by running the countdown_gui.py script.
This script should not be run on its own!
"""

# --------------------------------------------------------------------------
# ***** BEGIN GPL LICENSE BLOCK *****
#
# Copyright (C) 2009 Owen Shelton
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
# ***** END GPL LICENCE BLOCK *****
# --------------------------------------------------------------------------

import decimal
import Blender
from Blender import Scene, Registry, Draw, BGL

data = Registry.GetKey("CountdownInfo", True)

objectName = "Font"
startOffset = 0
endOffset = 0
showMilliseconds = 0

if data:
	objectName = data['objectName']
	startOffset = data['startOffset']
	endOffset = data['endOffset']
	showMilliseconds = data['showMilliseconds']
else:
	print 'Countdown Registry information not found or corrupt, resetting to default.'
	data = {}
	data['objectName'] = "Font"
	data['startOffset'] = 0
	data['endOffset'] = 0
	data['hundrethSeconds'] = 0
	objectName = data['objectName']
	startOffset = data['startOffset']
	endOffset = data['endOffset']
	showMilliseconds = data['showMilliseconds']
	Registry.SetKey('CountdownInfo', data, True)
object = Blender.Object.Get(objectName)
text = object.getData()

renderContext = Scene.GetCurrent().getRenderingContext()
totalTime = (float((renderContext.eFrame - endOffset) - (renderContext.sFrame + startOffset))) / renderContext.fps


timeRemaining = 0
if renderContext.cFrame <= (renderContext.sFrame + startOffset):
	timeRemaining = totalTime
elif renderContext.cFrame >= (renderContext.eFrame - endOffset):
	timeRemaining = 0
else:
	timeRemaining = totalTime - (float(renderContext.cFrame - startOffset - renderContext.sFrame)) / renderContext.fps

minutes = int(timeRemaining / 60)
seconds = int(timeRemaining % 60)

secondString = ""
if seconds < 10:
	secondString = "0" + str(seconds)
else:
	secondString = str(seconds)

newText = str(minutes) + ":" + secondString
	
if showMilliseconds == 1:
	milliseconds = int(timeRemaining * 1000 % 1000 / 10)
	if milliseconds < 10:
		newText += ":0" + str(milliseconds)
	else:
		newText += ":" + str(milliseconds)

text.setText(newText)
object.makeDisplayList()
Blender.Window.RedrawAll()