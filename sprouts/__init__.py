import sys
from models import Position


def main():
    """
    'Main' function to run sprouts game analysis.
    """

    # parse the command line
    if not len(sys.argv) > 1:
        exit("Sprouts position expected.")

    input_str = str(argv[1])  

    # instantiate the initial position model
    init_pos = Position(input_str)

    # instantiate a sprouts game object
    game = SproutsGame(Position)

    # output the initial game state
    print "Sprouts position input:\n-----------------------"
    print game.get_state_str(init=True)

    gametree = game.gen_gametree()
