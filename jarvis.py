#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function

import datetime
import sys
import os
import shlex
import subprocess
import socket  # For user computer name
import json

from os.path import dirname, join

from PySide.QtCore import QObject, Slot, Signal, QCoreApplication
from PySide.QtGui import QApplication, QDesktopWidget, QIcon
from PySide.QtWebKit import QWebView, QWebSettings
from PySide.QtNetwork import QNetworkRequest


from thememanager import ThemeManager

# @TODO: Theme management. Should now be handled css-side? (what's to become of python theme files?)


# A dictionary of plugins that Jarvis knows about
plugins = {}

# @TODO: Things like this should be in a global config .py file, not here.
DEBUG = True

# @TODO: Save current directory?
current_directory = os.path.expanduser('~')



class directory:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = newPath

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)





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

# @TODO: Error-checking! Does directory exist? spaces in directory name? if user just types "cd", go back to home!
def cd(args):
    global current_directory
    with directory(current_directory):
        os.chdir(args[0])
        current_directory = os.getcwd()
    JARVIS.shell.setWindowTitle('Jarvis - {}'.format(current_directory))

def help(args):
    print('help')

def history(args):
    print('history')


# A dictionary of commands in this file
builtins = {
    'cd': cd,
    'help': help,
    'history': history,
}


def runCommand(command, args):

    # @TODO: Handle aliases? (preprocessing of input)

    # First, determine if the command is built-in
    if command in builtins:
        builtins[command](args)
        return

    # If it's a plugin, run it
    if command in plugins:
        plugins[command].run(args)
        return

    # Maybe it by chance hasn't been loaded?
    if loadPlugin(command):
        plugins[command].run(args)
        return

    # Attempt to pass the command off to the underlying OS
    # @TODO: Error checking! (does command exist?)
    try:
        with directory(current_directory):
            subprocess.call([command] + args)
        return
    except OSError:
        pass

    # Okay...we really don't know what to do
    print('Unrecognized command "{}"'.format(command))



    # @TODO:
    # 2. Attempt to pass the command off to the underlying shell. If that succeeds, return.
    # 3. Interpret command semantically. This could include conversationally, etc.




class PyJSBridge(QObject):

    to_client = Signal(unicode)
    to_kernel = Signal(unicode)

    def __init__(self):
        super(PyJSBridge, self).__init__()

    @Slot(unicode)
    def from_client(self, message):
        self.to_kernel.emit(message)

    


class Shell(QWebView):
    def __init__(self):
        super(Shell, self).__init__()
        self.JarvisIcon = QIcon('media/jarvis-icon.png')
        self.initUI()
        self.loadFinished.connect(self.on_load)
        self.load(join(dirname(__file__), "web/index.html").replace('\\', '/'))
        self.show()

        

    def initUI(self):
        self.resize(720, 420)
        self.setMinimumSize(360, 210)
        self.center()
        self.setWindowTitle('Jarvis - {}'.format(current_directory))
        self.setWindowIcon(self.JarvisIcon)

    def center(self):
        fg = self.frameGeometry()
        fg.moveCenter(QDesktopWidget().availableGeometry().center())
        self.move(fg.topLeft())

    def on_load(self):
        if not getattr(self, 'bridge', False):
            self.bridge = PyJSBridge()

        # Sets a bridge between Python and JavaScript
        self.bridge.to_kernel.connect(self.receive_from_client)
        self.frame = self.page().mainFrame()
        self.frame.addToJavaScriptWindowObject('bridge', self.bridge)
        self.frame.evaluateJavaScript("linkBridge()")

        self.jarvis_message('Starting up on {}'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))



    def write_message(self, author, tag, message):
        data = {'author': author, 'tag': tag, 'message': message.replace('\n', '<br>').replace(' ', '&nbsp;')}
        self.bridge.to_client.emit(json.dumps(data))
        #self.jarvis_out.moveCursor(QtGui.QTextCursor.End)
        #self.jarvis_out.insertHtml(u'<span style="color:{}"><b>{}</b></span>{}'.format(tag_color, tag, message.replace('\n', '<br>').replace(' ', '&nbsp;')))
        #self.jarvis_out.moveCursor(QtGui.QTextCursor.End)

    def jarvis_message(self, message):
        self.write_message('jarvis', 'Jarvis > ', message + '\n')

    def user_message(self, message):
        self.write_message('user', '{} > '.format(socket.gethostname()), message + '\n')

    @Slot(unicode)
    def receive_from_client(self, message):
        self.user_enter(message)

    # @TODO: Tab completion? up/down arrows cycle through history? (logically now this should happen in JS)
    def user_enter(self, uin):
        self.user_message(uin)
        if uin:
            # @TODO: This should not happen here. If for example the user types "i'm doing fine" (note the quote)
            # shlex will throw a ValueError
            raw_cmd = shlex.split(uin)
            if raw_cmd[0] in ['exit', 'quit', 'bye']:
                QCoreApplication.instance().quit()
            else:
                runCommand(raw_cmd[0], raw_cmd[1:])

    @Slot()
    def on_control_panel(self):
        pass


    @Slot(unicode)
    def on_stdout(self, string):
        self.write_message('', '', string)
    

class StdOutListener(QObject):
    """Handles redirecting stdout to our application GUI"""

    message = Signal(unicode)

    def write(self, string):
        self.message.emit(unicode(string))


class Jarvis(object):
    def __init__(self):
        populatePlugins()  # Find all plugins we know about
        self.theme_manager = ThemeManager()

    def run_app(self):
        self.app = QApplication(sys.argv)
        self.app.setApplicationName('Jarvis')
        
        self.shell = Shell()

        stdoutlistener = StdOutListener()
        stdoutlistener.message.connect(self.shell.on_stdout)
        sys.stdout = stdoutlistener

        sys.exit(self.app.exec_())


if __name__ == '__main__':
    JARVIS = Jarvis()
    JARVIS.run_app()