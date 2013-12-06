from itertools import combinations


FACE_TOKEN = '/'
BND_TOKEN = ';'
VTX_TOKEN = ','



class Position(object):
    """
    A class to encapsulate gameboard position data.
    """

    faces = None
    degrees = None

    def __init__(self, faces_in, string_input=True):
        self._set_faces_list(faces_in, string_input)


    def __str__(self):
        if not self.faces:
            return ''
        return self.get_faces_string()


    # 'Private' method to parse string argument into list of lists of lists.
    def _set_faces_list(self, faces_in, string_input):
        faces_l = []
        degrees_l = []

        # if string_input => .strip().split() to strip whitespace & tokenize 
        faces_in_l = faces_in.strip().split(FACE_TOKEN) \
                     if string_input else faces_in[:]

        # loop the list of faces (looped by index for string_input option)
        for face_ix in range(len(faces_in_l)):
            face = faces_in_l[face_ix]              # handle, for convenience

            # append sync'd, empty sublists for vertices & their degrees
            bound_l = []
            faces_l.append(bound_l)
            degrees_bound_l = []
            degrees_l.append(degrees_bound_l)

            # loop the boundaries in this face (again, by index)
            bound_in_l = face.strip().split(BND_TOKEN) \
                         if string_input else faces_in[face_ix][:]

            for bnd_ix in range(len(bound_in_l)):
                bnd = bound_in_l[bnd_ix]

                # loop the verts (called seeds now)
                seed_l = []
                bound_l.append(seed_l)

                if string_input:
                    vtx_l = bnd.strip().split(VTX_TOKEN)
                    vtx_l = [v.strip() for v in vtx_l]
                else:
                    vtx_l = faces_in[face_ix][bnd_ix]

                # setting degrees for verts on the fly I hope
                degrees_seed_d = dict([int(v),0] for v in vtx_l)

                for vtx_ix in range(len(vtx_l)):
                    seed = int( vtx_l[vtx_ix] )

                    # increment the degrees dict ...
                    if vtx_ix < len(vtx_l)-1:
                        next_seed = int( vtx_l[vtx_ix+1] )
                    else:
                        next_seed = int( vtx_l[0] )

                    # ... but not if the seed is isolated ...
                    if len(vtx_l) > 1:
                        degrees_seed_d[seed] += 1
                        degrees_seed_d[next_seed] += 1

                    # ... incr once more for any vert in another face
                    for other_face in [faces_l[f_ix] for f_ix in range(len(faces_l)) if f_ix != face_ix]:
                        for tmp_bnd in other_face:
                            for tmp_seed in tmp_bnd:
                                if tmp_seed == seed:
                                    degrees_seed_d[seed] += 1

                    # add the seed to the seed list for its boundary in faces list
                    seed_l.append(seed)

                # stash the degrees dict for this boundary in degrees_l list
                degrees_bound_l.append(degrees_seed_d)

        # set the self.faces and self.degrees lists
        self.faces = faces_l
        self.degrees = degrees_l
#####33
        print "Degrees dict: ", self.degrees


    def get_faces_string(self):
        """
        Method to get position as formatted string, 
        assuming self.faces is set on __init__.
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


    def get_seed_list(self):
        """
        Method returns a list of all unique seed labels.
        """

        seed_l = []
        for face in self.degrees:
            for bnd in face:
                for seed in bnd.keys():
                    if not seed in seed_l:
                        seed_l.append(seed)

        return seed_l



class GameTree(object):
    """
    Class to encapsulate the game's directed acyclic graph (DAG) 'tree'.
    Expects a SproutsGame instance as initial parameter.

    """

    game = None
    root = None
    tree = None
    size = 0
    depth = 0

    def __init__(self, game):
        self.game = game
        self.root = self.game.init_position
        self.tree = self.gen_tree(self.root)
        self.size = 1
        self.depth = 1


    def gen_tree(self, parent_pos):
        """
        Method to recursively generate the game tree.
        """

        tree = {'pos': parent_pos, 'wins': 0, 'kids': None}

        # loop all faces of this parent position ...
        for face_ix in range(len(parent_pos.faces)):
            face = parent_pos.faces[face_ix]

            # loop all possible start and end boundaries in this face
            for start_bnd_ix in range(len(face)):
                start_bnd = face[start_bnd_ix]
                for end_bnd_ix in range(len(face)):
                    end_bnd = face[end_bnd_ix]

                    # setup combinatorial list of tuples of other bnds to incl
                    bnd_incl_combo_l = []
                    other_bnd_ix_l = [ ix for ix in range(len(face))
                                       if ix not in [start_bnd_ix, end_bnd_ix] ]

##############3                    print "Other bounds: ", other_bnd_ix_l

                    # r=[radius of the combination]
                    for r in range(len(other_bnd_ix_l)):
                        r_l = [ c for c in combinations(other_bnd_ix_l, r) ]
                        bnd_incl_combo_l.extend(r_l)

                    # loop all poss start/end verts in this start/end bnds
                    for start_vtx_ix in range(len( start_bnd )):
                        start_vtx = start_bnd[start_vtx_ix]
                        for end_vtx_ix in range(len( end_bnd )):
                            end_vtx = end_bnd[end_vtx_ix]

################33                            print "Other bound combos: ", bnd_incl_combo_l

                            # loop all the poss other-bound inclusion combos
                            for bnd_incl_t in bnd_incl_combo_l:

                                # get a new position from SproutsGame.move()
                                new_position = self.game.move(
                                    parent_pos, face_ix, bnd_incl_t, 
                                    {'bnd': start_bnd_ix, 'vtx': start_vtx_ix}, 
                                    {'bnd': end_bnd_ix, 'vtx': end_vtx_ix}       
                                    )

                                # increment size (# of nodes)
                                if new_position:
                                    self.size += 1

                                    new_tree = self.gen_tree(new_position)
                                    tree['kids'] = new_tree

                                    # increment depth (# of levels)
                                    if new_tree:
                                        self.depth += 1

        return tree
