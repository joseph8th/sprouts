import sys
from models import Position, GameTree
from game import SproutsGame
from views import Report


def main():
    """
    'Main' function.
    """

    # parse the command line
    if not len(sys.argv) > 1:
        sys.exit("Sprouts position expected.")
    input_str = str(sys.argv[1])  

    # instantiate the initial position model
    init_pos = Position(input_str)

    # instantiate a sprouts game object
    game = SproutsGame(Position)

    # instantiate a GameTree object
    gametree = GameTree(game)

    # output a Report object
    Report(gametree)
