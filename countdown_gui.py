#!BPY
# -*- coding: utf-8 -*-
#""" 
#Name: 'Countdown GUI'
#Blender: 247
#Group: 'Wizards'
#Tip: 'Countdown control script.'
#"""
__author__ = "Owen Shelton"
__version__ = "1.0"

__bpydoc__ = """\

This script provides a control interface for editing things like the frame offsets and time format used by the countdown script as well as the text object to use.
This script also automatically adds countdown.py as a FrameChanged scriptlink, as long as it is in the root directory of the user scripts folder. 
If this script is not run the countdown script will assume 0 frame offsets, will try to use the text object named Font, and will not show the time's hundreths of a second component. 
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

import Blender
from Blender import Scene, Registry, Draw, BGL, Text

EVT_UPDATE_BUTTON = 1000
EVT_OBJECT_NAME_CHANGED = 1001
EVT_START_OFFSET_CHANGED = 1002
EVT_END_OFFSET_CHANGED = 1003
EVT_SECOND_TOGGLE = 1004

objectName = "countdown"
startOffset = 0
endOffset = 0
showMilliseconds = 0

data = Registry.GetKey("CountdownInfo", True)

script = Text.Load(Blender.Get('uscriptsdir') + "countdown.py")
	
scriptLinks = Blender.Scene.getCurrent().getScriptLinks('FrameChanged')
addLink = True

linkIter = iter(scriptLinks)
while True:
		try:
			scriptLink = linkIter.next()		
			if scriptLink.getFilename() == "countdown.py":
				addLink = False
				break
		except StopIteration:
			break
	
if addLink == True:
	Blender.Scene.getCurrent().addScriptLink('countdown.py', 'FrameChanged')	

if data:
	objectName = data['objectName']
	startOffset = data['startOffset']
	endOffset = data['endOffset']
	showMilliseconds = data['showMilliseconds']
else:
	print 'Countdown Registry information not found or corrupt, resetting to default.'
	data = {}
	data['objectName'] = "countdown"
	data['startOffset'] = 0
	data['endOffset'] = 0
	data['showMilliseconds'] = 0
	objectName = data['objectName']
	startOffset = data['startOffset']
	endOffset = data['endOffset']
	showMilliseconds = data['showMilliseconds']
	Registry.SetKey('CountdownInfo', data, True)

stringBox = Draw.Create(objectName)
numBox1 = Draw.Create(startOffset)
numBox2 = Draw.Create(endOffset)
toggleBox = Draw.Create(showMilliseconds)
	
def string_event(evt, val):
	if evt == EVT_OBJECT_NAME_CHANGED:
		if val != "":
			stringBox.val = val
	elif evt == EVT_START_OFFSET_CHANGED:
		numBox1.val = val
	elif evt == EVT_END_OFFSET_CHANGED:
		numBox2.val = val

def button_event(evt):
	if evt == EVT_UPDATE_BUTTON: 
		data = {}
		data['objectName'] = stringBox.val
		data['startOffset'] = numBox1.val
		data['endOffset'] = numBox2.val
		data['showMilliseconds'] = toggleBox.val
		Registry.SetKey("CountdownInfo", data, True)
	elif evt == EVT_SECOND_TOGGLE:
		if toggleBox.val == 0: toggleBox.val = 1
		elif toggleBox.val == 1: toggleBox.val = 0

def gui():
	context = Scene.GetCurrent().getRenderingContext()
	
	Draw.Label("Countdown Setup GUI.", 10, 185, 300, 10)
	Draw.String("Text Object: ", EVT_OBJECT_NAME_CHANGED, 10, 150, 200, 20, stringBox.val, 40, "Obj name of the text object to be used.", string_event)
	Draw.Number("Starting Offset: ", EVT_START_OFFSET_CHANGED, 10, 120, 160, 20, numBox1.val, 0, context.eFrame - context.sFrame - numBox2.val,"Number of frames after the starting frame to skip.", string_event) 
	Draw.Number("Ending Offset: ", EVT_END_OFFSET_CHANGED, 10, 95, 160, 20, numBox2.val, 0, context.eFrame - context.sFrame - numBox1.val,"Number of frames before the last frame to skip.", string_event)
	Draw.Toggle("Show milliseconds?", EVT_SECOND_TOGGLE, 10, 60, 190, 20, toggleBox.val, "sets whether or not the hundreths of a second are shown, pushed in is yes, out is no.") 
	Draw.PushButton("Update", EVT_UPDATE_BUTTON, 10, 10, 100, 20, "Push the current settings to the registry, changes will not be reflected until the current frame is changed.")

Draw.Register(gui, None, button_event)