import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

from .game import Game
from .tagged import Tagged
from .constants import Constants
from .methods import Methods, ErrorMessages
from .config import Config
