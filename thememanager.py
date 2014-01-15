import os

# A dictionary of themes that Jarvis knows about
themes = {}

def load_theme(name):
    try:
        theme = __import__('themes.{}'.format(name), fromlist=['themes'])
    except ImportError:
        return None
    themes[name] = theme
    return theme

def populate_themes():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    for f in os.listdir('themes'):
        if f.endswith('.py') and not '__init__' in f and not f.startswith('_'):
            load_theme(f[:-3])


class ThemeManager:
    def __init__(self):
        populate_themes()
        self.current_theme = themes['default']  # @TODO: Set current theme based on preferences (save file)