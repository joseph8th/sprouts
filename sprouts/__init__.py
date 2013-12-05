import sys
from models import Position, SproutsGame, GameTree


def main():
    """
    'Main' function to run sprouts game analysis.
    """

    # parse the command line
    if not len(sys.argv) > 1:
        exit("Sprouts position expected.")

    input_str = str(sys.argv[1])  

    # instantiate the initial position model
    init_pos = Position(input_str)
    print "Initial position: ", init_pos

    # instantiate a sprouts game object
    game = SproutsGame(Position)

    # output the initial game state

#    print game.get_state_str(init=True)

    gametree = GameTree(game)
