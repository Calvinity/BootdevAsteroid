from enum import Enum

class GameState(Enum):
    MENU = "menu"
    PLAYING = "playing"
    GAME_OVER = "game_over"
    PAUSED = "paused"  # For future use if you want pause functionality
    OPTIONS = "options"