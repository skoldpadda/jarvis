#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import wx
import wx.richtext as rt
import datetime
import sys, os, shlex

import socket # For user computer name

from wx.lib.embeddedimage import PyEmbeddedImage
from wx.lib.newevent import NewEvent


# Rebinding stdout so that any print() messages go into Jarvis window as well...
wxStdOut, EVT_STDDOUT = NewEvent()


# A dictionary of plugins that Jarvis knows about
plugins = {}


# A dictionary of themes that Jarvis knows about
themes = {}


DEBUG = True


# Get a hook to the system shell
if sys.platform == 'win32':
	SHELL = 'cmd.exe'
else:
	if 'SHELL' in os.environ:
		SHELL = os.environ['SHELL']
	else:
		SHELL = '/bin/sh'



#TODO: Should this go here?
JarvisIcon = PyEmbeddedImage("iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAQAAADZc7J/AAAACXBIWXMAAAsTAAALEwEAmpwYAAADGGlDQ1BQaG90b3Nob3AgSUNDIHByb2ZpbGUAAHjaY2BgnuDo4uTKJMDAUFBUUuQe5BgZERmlwH6egY2BmYGBgYGBITG5uMAxIMCHgYGBIS8/L5UBFTAyMHy7xsDIwMDAcFnX0cXJlYE0wJpcUFTCwMBwgIGBwSgltTiZgYHhCwMDQ3p5SUEJAwNjDAMDg0hSdkEJAwNjAQMDg0h2SJAzAwNjCwMDE09JakUJAwMDg3N+QWVRZnpGiYKhpaWlgmNKflKqQnBlcUlqbrGCZ15yflFBflFiSWoKAwMD1A4GBgYGXpf8EgX3xMw8BSMDVQYqg4jIKAUICxE+CDEESC4tKoMHJQODAIMCgwGDA0MAQyJDPcMChqMMbxjFGV0YSxlXMN5jEmMKYprAdIFZmDmSeSHzGxZLlg6WW6x6rK2s99gs2aaxfWMPZ9/NocTRxfGFM5HzApcj1xZuTe4FPFI8U3mFeCfxCfNN45fhXyygI7BD0FXwilCq0A/hXhEVkb2i4aJfxCaJG4lfkaiQlJM8JpUvLS19QqZMVl32llyfvIv8H4WtioVKekpvldeqFKiaqP5UO6jepRGqqaT5QeuA9iSdVF0rPUG9V/pHDBYY1hrFGNuayJsym740u2C+02KJ5QSrOutcmzjbQDtXe2sHY0cdJzVnJRcFV3k3BXdlD3VPXS8Tbxsfd99gvwT//ID6wIlBS4N3hVwMfRnOFCEXaRUVEV0RMzN2T9yDBLZE3aSw5IaUNak30zkyLDIzs+ZmX8xlz7PPryjYVPiuWLskq3RV2ZsK/cqSql01jLVedVPrHzbqNdU0n22VaytsP9op3VXUfbpXta+x/+5Em0mzJ/+dGj/t8AyNmf2zvs9JmHt6vvmCpYtEFrcu+bYsc/m9lSGrTq9xWbtvveWGbZtMNm/ZarJt+w6rnft3u+45uy9s/4ODOYd+Hmk/Jn58xUnrU+fOJJ/9dX7SRe1LR68kXv13fc5Nm1t379TfU75/4mHeY7En+59lvhB5efB1/lv5dxc+NH0y/fzq64Lv4T8Ffp360/rP8f9/AA0ADzT6lvFdAAAAIGNIUk0AAHolAACAgwAA+f8AAIDpAAB1MAAA6mAAADqYAAAXb5JfxUYAAAFhSURBVHjapJXdcYMwEIS/8eQ9KkElUILcQdIBJTgd4ApcAiWQDpQO7A5EBzgVKA9g0M9JNpPTC6DTanfvJPAw4dfhsGigxdKjAVB0WDoABix2XTEAnmD5PAxg8XgmGhRu+Q55Lm/UQjEwLjzmiN9AHYRl9+BZY6K5McltJIAbO+LAvrjtBThzjN5/XwUYgTtnOn74ZKwIE8pYiy4t+TMJhvZ/Jvb0qFqC1EhNoPcLHfXF+ysA4Y7fGbggYcx0l0NLVRgSZ6eAw0dkohEOnoc2+9ytSxw+gLNJnpsZbAd2G3plcArYpFntDCBNWUF/us314cF800jotR70i9n+UbqpYiXobP6yVaGkcAgAcvtUCiDJOBXBTdgHWwe6TEZTpZ8ASI0yYbgW6WcAkte+Ql8AINvPV+iLALniMn0RQPJ8G410GvO4FJZ38qUqheSELd3K8l/RPVVfBYAmgnCCegD+BgB2zHwJiCScOQAAAABJRU5ErkJggg==")

def Log(msg):
	if DEBUG:
		print(msg)

def loadPlugin(name):
	try:
		plugin = __import__('plugins.{}'.format(name), fromlist=['plugins'])
	except ImportError:
		return None
	plugins[name] = plugin
	return plugin

def populatePlugins():
	os.chdir(os.path.dirname(os.path.abspath(__file__)))
	for f in os.listdir('plugins'):
		if f.endswith('.py') and not '__init__' in f and not f.startswith('_'):
			loadPlugin(f[:-3])

def help(args):
	print('help')

def history(args):
	print('history')


def loadTheme(name):
	try:
		theme = __import__('themes.{}'.format(name), fromlist=['themes'])
	except ImportError:
		return None
	themes[name] = theme
	return theme

def populateThemes():
	os.chdir(os.path.dirname(os.path.abspath(__file__)))
	for f in os.listdir('themes'):
		if f.endswith('.py') and not '__init__' in f and not f.startswith('_'):
			loadTheme(f[:-3])



# A dictionary of commands in this file
builtins = {
	'help': help,
	'history': history,
}


def runCommand(command, args):

	#TODO: Handle aliases? (preprocessing of input)

	# First, determine if the command is built-in
	if command in builtins:
		builtins[command](args)
		return

	# If it's not recognized, we attempt to load it, then fail if THAT doesn't work
	if command not in plugins:
		if not loadPlugin(command):
			print('Unrecognized command "{}"'.format(command))
			return

	# Finally run it!
	plugins[command].run(args)

	#TODO:
	# 1. If command not in plugins, attempt to load it. If that succeeds, run and return.
	# 2. Attempt to pass the command off to the underlying shell. If that succeeds, return.
	# 3. Interpret command semantically. This could include conversationally, etc.


	




class JarvisTaskBarIcon(wx.TaskBarIcon):

	def __init__(self, frame):
		wx.TaskBarIcon.__init__(self)
		self.frame = frame

		# Set the image
		icon = self.MakeIcon(JarvisIcon.GetImage())
		self.SetIcon(icon, "wxPython Demo")
		self.imgidx = 1
		
		# bind some events
		self.Bind(wx.EVT_MENU, self.OnTaskBarClose)

	def MakeIcon(self, img):
		if "wxMSW" in wx.PlatformInfo:
			img = img.Scale(16, 16)
		elif "wxGTK" in wx.PlatformInfo:
			img = img.Scale(22, 22)
		# wxMac can be any size upto 128x128, so leave the source img alone....
		icon = wx.IconFromBitmap(img.ConvertToBitmap() )
		return icon

	def OnTaskBarClose(self, evt):
		wx.CallAfter(self.frame.Close)


	
class ControlPanel(wx.Dialog):

	def __init__(self, parent, ID, title, size=wx.DefaultSize, pos=wx.DefaultPosition, style=wx.DEFAULT_DIALOG_STYLE):

		super(ControlPanel, self).__init__(parent, ID, title=title, size=size, pos=pos, style=style)

		icon = JarvisIcon.GetIcon()
		self.SetIcon(icon)

		# Now continue with the normal construction of the dialog
		# contents
		sizer = wx.BoxSizer(wx.VERTICAL)

		label = wx.StaticText(self, -1, "Work In Progress")
		sizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

		box = wx.BoxSizer(wx.HORIZONTAL)

		label = wx.StaticText(self, -1, "Field #1:")
		box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

		text = wx.TextCtrl(self, -1, "", size=(80,-1))
		box.Add(text, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

		sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

		box = wx.BoxSizer(wx.HORIZONTAL)

		label = wx.StaticText(self, -1, "Field #2:")
		box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

		text = wx.TextCtrl(self, -1, "", size=(80,-1))
		box.Add(text, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

		sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

		line = wx.StaticLine(self, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
		sizer.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 5)

		btnsizer = wx.StdDialogButtonSizer()
		
		if wx.Platform != "__WXMSW__":
			btn = wx.ContextHelpButton(self)
			btnsizer.AddButton(btn)
		
		btn = wx.Button(self, wx.ID_OK)
		btn.SetDefault()
		btnsizer.AddButton(btn)

		btn = wx.Button(self, wx.ID_CANCEL)
		btnsizer.AddButton(btn)
		btnsizer.Realize()

		sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

		self.SetSizer(sizer)
		sizer.Fit(self)



class Shell(wx.Frame):

	def __init__(self, parent, title):
		#print(wx.version())
		super(Shell, self).__init__(parent, title=title, size=(720, 420))
		self.SetMinSize((360, 210))
		#self.SetupHotKey()

		# Set the taskbar icon
		icon = JarvisIcon.GetIcon()
		self.SetIcon(icon)
		try:
			self.tbicon = JarvisTaskBarIcon(self)
		except:
			self.tbicon = None

		# Event bindings
		self.Bind(wx.EVT_CLOSE, self.OnClose)


		self.InitUI()
		self.RefreshTheme()
		self.intc.SetFocus()
		self.JarvisMessage('Starting up on {}'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

	def SetupHotKey(self):
		self.hkid = hkid = wx.NewId()
		self.Bind(wx.EVT_HOTKEY, self.OnHotKey, id=hkid)
		result = self.RegisterHotKey(hkid, wx.MOD_CONTROL|wx.MOD_SHIFT, wx.WXK_F12)
		if not result:
			print('Could not register hot key!', file=sys.stderr)

	def OnHotKey(self, event):
		print("Received hot key")

	def RefreshTheme(self):
		self.SetBackgroundColour(current_theme.app)
		self.outtc.SetBackgroundColour(current_theme.out_bg)
		self.intc.SetBackgroundColour(current_theme.in_bg)
		self.intc.SetForegroundColour(current_theme.in_fg)
		self.Refresh()


	def InitOutPanel(self, parent, box):
		outbox = wx.BoxSizer(wx.HORIZONTAL)
		self.outtc = rt.RichTextCtrl(parent, style=wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER)
		self.outtc.SetEditable(False)
		self.outtc.SetFont(wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas'))
		self.outtc.Bind(EVT_STDDOUT, self.StdOutEnter)
		outbox.Add(self.outtc, proportion=1, flag=wx.EXPAND)
		box.Add(outbox, proportion=1, flag=wx.LEFT|wx.RIGHT|wx.TOP|wx.EXPAND, border=10)

	def InitInPanel(self, parent, box):
		inbox = wx.BoxSizer(wx.HORIZONTAL)

		but_default = JarvisIcon.GetImage().ConvertToBitmap()
		self.jarvis_button = wx.BitmapButton(parent, bitmap=but_default)
		self.jarvis_button.SetToolTip(wx.ToolTip("Control Panel"))
		self.jarvis_button.Bind(wx.EVT_BUTTON, self.JarvisButtonClicked)
		inbox.Add(self.jarvis_button, flag=wx.EXPAND)

		inbox.AddSpacer(10)

		self.intc = wx.TextCtrl(parent, style=wx.TE_PROCESS_TAB|wx.TE_PROCESS_ENTER)
		self.intc.SetFont(wx.Font(24, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas'))

		self.intc.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
		self.intc.Bind(wx.EVT_CHAR, self.OnChar)
		self.intc.Bind(wx.EVT_KEY_UP, self.OnKeyUp)

		#self.intc.Bind(wx.EVT_TEXT_ENTER, self.UserEnter)
		inbox.Add(self.intc, proportion=1)

		box.Add(inbox, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM, border=10)

	def JarvisButtonClicked(self, event):
		dlg = ControlPanel(self, -1, 'Control Panel', size=(350, 200))
		dlg.CenterOnScreen()

		# This does not return until the dialog is closed
		val = dlg.ShowModal()

		dlg.Destroy()

	def InitUI(self):
		panel = wx.Panel(self)
		vbox = wx.BoxSizer(wx.VERTICAL)
		self.InitOutPanel(panel, vbox)
		self.InitInPanel(panel, vbox)
		panel.SetSizer(vbox)
		

	# IMPORTANT: Remember that WriteText() will print a newline if given an empty string!!! (yeah this is stupid)
	def WriteMessage(self, out, tag, tag_color, message):
		#print(repr(message), file=sys.stderr)

		out.SetInsertionPointEnd()

		if tag:
			out.BeginBold()
			out.BeginTextColour(tag_color)
			out.WriteText(tag)
			out.EndTextColour()
			out.EndBold()

		# Technically there could be a case where an empty string SHOULD be printed...not sure when though
		if message:
			out.BeginTextColour(current_theme.out_fg)
			out.WriteText(message)
			out.EndTextColour()

		#out.Newline() <-- We don't do this here. Let the message have full control over line breaks
		out.ShowPosition(out.GetLastPosition())

	def JarvisMessage(self, message):
		self.WriteMessage(self.outtc, 'Jarvis > ', current_theme.jarvis_msg, message + '\n')

	def UserMessage(self, message):
		self.WriteMessage(self.outtc, '{} > '.format(socket.gethostname()), current_theme.user_msg, message + '\n')




	def OnKeyDown(self, event):
		key = event.GetKeyCode()

		if key == wx.WXK_RETURN:
			self.UserEnter(event)

		#TODO: Tab Completion
		elif key == wx.WXK_TAB:
			pass

		#TODO: Cycle through previous command history
		elif key in [wx.WXK_UP, wx.WXK_NUMPAD_UP]:
			pass

		#TODO: Cycle towards most recent commands in history
		elif key in [wx.WXK_DOWN, wx.WXK_NUMPAD_DOWN]:
			pass

		else:
			event.Skip()

	def OnChar(self, event):
		event.Skip()

	def OnKeyUp(self, event):
		event.Skip()


	def UserEnter(self, event):
		#global theme
		#theme = default
		#self.RefreshTheme()

		#self.SetTitle('Jarvis - {}'.format(self.intc.GetValue()))

		uin = self.intc.GetValue()
		self.intc.SetValue('')

		self.UserMessage(uin)
		if uin:
			raw_cmd = shlex.split(uin)
			if raw_cmd[0] in ['exit', 'quit', 'bye']:
				self.Close()
			else:
				runCommand(raw_cmd[0], raw_cmd[1:])

	def StdOutEnter(self, event):
		self.WriteMessage(self.outtc, '', current_theme.out_fg, event.text)


	def OnClose(self, event):
		print('Exiting...')
		if self.tbicon is not None:
			self.tbicon.Destroy()
		self.Destroy()

		# in your close handler you need to make sure you end threads, destroy taskbar icons, close open files, etc so nothing hangs.


class SysOutListener:
	def write(self, string):
		sys.__stdout__.write(string)
		evt = wxStdOut(text=string)
		wx.PostEvent(wx.GetApp().frame.outtc, evt)


class JarvisApp(wx.App):
	def OnInit(self):
		self.frame = Shell(None, title='Jarvis')
		self.frame.Show(True)
		self.frame.Center()
		return True


if __name__ == '__main__':

	# Find all plugins we know about
	populatePlugins()

	# Find all themes we know about
	populateThemes()

	#TODO: Theme manager (separate)
	current_theme = themes['default']

	app = JarvisApp(redirect=False) # We do not want to redirect our stdout/stderr to the console
	
	# Redirect stdout to our window
	sys.stdout = SysOutListener()

	app.MainLoop()