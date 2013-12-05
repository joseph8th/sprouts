
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

                seed_l = []
                bound_l.append(seed_l)

                vtx_l = bnd.strip().split(VTX_TOKEN)
                vtx_l = [v.strip() for v in vtx_l]
                next_seed = vtx_l[0]

                degrees_seed_d = dict([int(v),0] for v in vtx_l)

                for vtx_ix in range(len(vtx_l)):
                    seed = int( vtx_l[vtx_ix] )

                    # increment the directed edges counter dict ...
                    if vtx_ix < len(vtx_l)-1:
                        next_seed = int( vtx_l[vtx_ix+1] )
                    else:
                        next_seed = int( vtx_l[0] )

                    # ... but not if the seed is isolated
                    if len(vtx_l) > 1:
                        degrees_seed_d[seed] += 1
                        degrees_seed_d[next_seed] += 1

                    # add the seed to the seed list for its boundary in faces list
                    seed_l.append(seed)

#############3                    print "Degrees at end of vtx loop:", degrees_seed_d

                # stash the degrees dict for this boundary in degrees_l list
                degrees_bound_l.append(degrees_seed_d)

        # set the self.faces and self.degrees lists
        self.faces = faces_l
        self.degrees = degrees_l

##############3        print "Degrees final:", self.degrees, "\nFaces final:", self.faces


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

    def __init__(self, game):
        self.game = game
        self.root = self.game.init_position
        self.tree = self.gen_tree(self.root)


    def gen_tree(self, parent_pos):
        """
        Method to recursively generate the game tree.
        """
##########3
        print parent_pos.faces

        tree = {'pos': parent_pos, 'wins': 0, 'kids': None}

        # loop all faces of this parent position ...
        for face_ix in range(len(parent_pos.faces)):
            face = parent_pos.faces[face_ix]

            # loop all possible start and end boundaries in this face
            for start_bnd_ix in range(len(face)):
                start_bnd = face[start_bnd_ix]
                for end_bnd_ix in range(len(face)):
                    end_bnd = face[end_bnd_ix]

                    # loop all poss start/end verts in this start/end bnds
                    for start_vtx_ix in range(len( start_bnd )):
                        for end_vtx_ix in range(len( end_bnd )):
                            new_position = self.game.move(
                                parent_pos, face_ix, 
                                {'bnd': start_bnd_ix, 'vtx': start_vtx_ix}, 
                                {'bnd': end_bnd_ix, 'vtx': end_vtx_ix}       
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


    def move(self, pos, face_ix, bnd_incl_l, start_d, end_d): 
        """
        Method to perform only legal move (join) with 2 given vertices.
        """

        # breakout vals of indexed args for convenience (pos=position)
        work_face = pos.faces[face_ix]
        start_bnd = work_face[ start_d['bnd'] ]
        start_vtx = start_bnd[ start_d['vtx'] ]
        end_bnd = work_face[ end_d['bnd'] ]
        end_vtx = end_bnd[ end_d['vtx'] ]
        start_degs = pos.degrees[face_ix][ start_d['bnd'] ]
        end_degs = pos.degrees[face_ix][ end_d['bnd'] ]

        # new stuff
        new_pos_l = []
        new_vtx = max( pos.get_seed_list() ) + 1

        # for joins in the same boundary => creating a new face
        if start_bnd == end_bnd:
            new_bnd1 = []
            new_bnd2 = []

            # for joining a vertex to itself
            if start_vtx == end_vtx:
                if start_degs[start_vtx] < 2:
                    new_bnd1.extend( [start_vtx, new_vtx] )

                    new_bnd2.extend(
                        [ v for v in start_bnd[:start_d['vtx']] ] )
                    new_bnd2.append(new_vtx)
                    new_bnd2.extend(
                        [ v for v in start_bnd[start_d['vtx']:] ] )
                    
            # for joining diff verts in same boundary
            else:
                if start_degs[start_vtx] < 3 and start_degs[end_vtx] < 3:
                    new_bnd1.extend( 
                        [ v for v in start_bnd[:start_d['vtx']] ] )
                    new_bnd1.extend( [new_vtx, end_vtx] )

                    new_bnd2.extend(
                        [v for v in start_bnd[start_d['vtx']:end_d['vtx']]] )
                    new_bnd2.append(new_vtx)

            # which boundaries included in which face?
            orig_face = []
            new_face = []
            orig_face.append(new_bnd1)
            orig_face.extend([ work_face[bnd_ix] 
                               for bnd_ix in range(len(work_face))
                               if bnd_ix != start_d['bnd']
                               and bnd_ix not in bnd_incl_l ])
            
            new_face.append(new_bnd2)
            new_face.extend([ work_face[bnd_ix]
                              for bnd_ix in bnd_incl_l
                              if bnd_ix != start_d['bnd'] ])

            new_faces_l = []
            # 1st grab all the other faces in the pos.faces list
            if len(pos.faces) > 1:
                new_faces_l.extend([ pos.faces[ix] 
                                     for ix in range(len(faces)) 
                                     if ix != face_ix ])
            # then tack on the modified orig and new faces
            new_faces_l.extend([orig_face, new_face])


        # otherwise joins in diff boundaries => joining boundaries
        else:
            new_bnd = []
            if start_degs[start_vtx] < 3 and end_degs[end_vtx] < 3:
                new_bnd.extend(
                    [ v for v in start_bnd[:start_d['vtx']] ] )
                new_bnd.append(new_vtx)
                new_bnd.extend(
                    [ v for v in end_bnd[end_d['vtx']:] ] )
                new_bnd.extend(
                    [ v for v in end_bnd[:end_d['vtx']] ] )
                new_bnd.append(new_vtx)
                new_bnd.extend(
                    [ v for v ind start_bnd[start_d['vtx']:] ] )


        return new_position


    def play(self, args):
        pass
