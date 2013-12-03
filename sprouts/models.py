
FACE_TOKEN = '/'
BND_TOKEN = ';'
VTX_TOKEN = ','



class Position(object):
    """
    A class to encapsulate gameboard position data.
    """

    faces = None

    def __init__(self, args):
        self.faces = self._init_faces(faces)               # a 'public' attribute


    def __str__(self):
        # Override the '__str__' method of 'object'.

        if not self.faces:
            return ''
        return self.get_faces_string()


    def _init_faces(self, input_str):
        # 'Private' method to parse string argument into list of lists of lists.
        
        faces_l = []
        # use .strip().split(TOKEN) to strip whitespace before tokenizing into lists
        for face in input_str.strip().split(FACE_TOKEN):
            bound_l = []
            faces_l.append(bound_l)
            for bnd in face.strip().split(BND_TOKEN):
                vtx_l = []
                bound_l.append(vtx_l)
                for vtx in bnd.strip().split(VTX_TOKEN):
                    vtx_l.append(vtx.strip())

        return faces_l


    def get_faces_string(self):
        """
        Method to get position as formatted string, assuming self.faces is set on __init__.
        """

        faces_s = ''
        for face_ix in range(len(self.faces)):
            face = self.faces[face_ix]
            for bnd_ix in range(len(face)):
                bnd = face[bnd_ix]
                for vtx_ix in range(len(bnd)):
                    faces_s += bnd[vtx_ix]
                    faces_s += VTX_TOKEN if vtx_ix < len(bnd)-1 else ''
                faces_s += BND_TOKEN if bnd_ix < len(face)-1 else ''
            faces_s += FACE_TOKEN if face_ix < len(self.faces)-1 else ''

        return faces_s



class GameTree(object):
    """
    Class to encapsulate the game's directed acyclic graph (DAG) 'tree'.
    """

    def __init__(self, init_position):
        self.root = init_position
        self.tree = self.gen_gametree()


    def get_current_position(self):
        return self.game_tree[-1:][-1:]
                    

    def gen_gametree(self):
        pass



class SproutsGame(object):
    """
    Class to encapsulate the data and methods needed to play a Sprouts game.
    Accepts a Position instance as initial parameter.
    """

    def __init__(self, init_position):
        self.game_tree = GameTree(init_position)


    def play(self, args):
        pass
