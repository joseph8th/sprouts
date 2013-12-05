
FACE_TOKEN = '/'
BND_TOKEN = ';'
VTX_TOKEN = ','



class Seed(object):
    """
    A class to encapsulate 'seed' vertex data.
    """

    value = None
    edges = 0

    def __init__(self, value, edges=0):
        self.value = value
        self.edges = edges

    def __repr__(self):
        return str(self.value)



class Position(object):
    """
    A class to encapsulate gameboard position data.
    """

    faces = None
    edges = None

    def __init__(self, input_str):
        self._set_faces_list(input_str)


    def __str__(self):
        # Override the '__str__' method of 'object'.

        if not self.faces:
            return ''
        return self.get_faces_string()


    def _set_faces_list(self, input_str):
        # 'Private' method to parse string argument into list of lists of lists.
        
        faces_l = []
        edges_l = []

        # use .strip().split() to strip whitespace then tokenize 
        for face in input_str.strip().split(FACE_TOKEN):
            bound_l = []
            faces_l.append(bound_l)

            edges_bound_l = []
            edges_l.append(edges_bound_l)

            for bnd in face.strip().split(BND_TOKEN):
                seed_l = []
                bound_l.append(seed_l)

                vtx_l = bnd.strip().split(VTX_TOKEN)
                next_seed = vtx_l[0]

                edges_seed_d = dict([v,0] for v in vtx_l)

                for vtx_ix in range(len(vtx_l)):
                    seed = vtx_l[vtx_ix].strip()

                    # increment the directed edges counter dict ...
                    if vtx_ix < len(vtx_l)-1:
                        next_seed = vtx_l[vtx_ix+1].strip()
                    else:
                        next_seed = vtx_l[0].strip()

                    # ... but not if the seed is alone in its boundary
                    if len(vtx_l) > 1:
                        edges_seed_d[seed] += 1
                        edges_seed_d[next_seed] += 1

                    # add the seed to the seed list (in faces list)
                    seed_l.append(seed)

#############3                    print "Edges at end of vtx loop:", edges_seed_d

                # stash the edges dict for this boundary in edges_l list
                edges_bound_l.append(edges_seed_d)

        # set the self.faces and self.edges lists
        self.faces = faces_l
        self.edges = edges_l

##############3        
        print "Edges final:", self.edges, "\nFaces final:", self.faces


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
                    faces_s += str(bnd[vtx_ix])
                    faces_s += VTX_TOKEN if vtx_ix < len(bnd)-1 else ''
                faces_s += BND_TOKEN if bnd_ix < len(face)-1 else ''
            faces_s += FACE_TOKEN if face_ix < len(self.faces)-1 else ''

        return faces_s



class GameTree(object):
    """
    Class to encapsulate the game's directed acyclic graph (DAG) 'tree'.
    Expects a SproutsGame instance as initial parameter.
    """

    def __init__(self, game):
        self.game = game
        self.root = self.game.init_position
        self.tree = self.gen_tree(self.root)


    def get_current_position(self):
        return self.tree[-1][-1]
                    

    def gen_tree(self, parent_pos):
        tree = {'pos': parent_pos, 'wins': 0, 'kids': None}

        for face_ix in range(len(parent_pos.faces)):
            face = parent_pos.faces[face_ix]

            for start_bnd_ix in range(len(face)):
                start_bnd = face[start_bnd_ix]
                for end_bnd_ix in range(len(face)):
                    end_bnd = face[end_bnd_ix]

                    for start_vtx_ix in range(len( start_bnd )):
                        for end_vtx_ix in range(len( end_bnd )):
                            new_position = self.game.move(
                                parent_pos, face_ix, 
                                {'start': (start_bnd_ix, start_vtx_ix), 
                                 'end': (end_bnd_ix, end_vtx_ix)}       
                            )

                            # recurse into child trees
                            if new_position:
                                new_tree = self.gen_tree(new_position)
                                tree['kids'] = new_tree

        return tree



class SproutsGame(object):
    """
    Class to encapsulate the data and methods needed to play a Sprouts game.
    Accepts a Position instance as initial parameter.
    """

    def __init__(self, init_position):
        self.init_position = init_position


    def move(self, position, face_ix, join):        
        face = position.faces[face_ix]
        start_bnd = face[ join['start'][0] ]
        start_vtx = start_bnd[ join['start'][1] ]
        end_bnd = face[ join['end'][0] ]
        end_vtx = end_bnd[ join['end'][1] ]

        new_position = None

        return new_position


    def play(self, args):
        pass
