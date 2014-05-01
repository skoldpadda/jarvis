import os
import glob


__all__ = [os.path.basename(f)[:-3] for f in glob.glob('{}/*.py'.format(os.path.dirname(__file__)))]