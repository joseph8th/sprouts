from models import Position



class SproutsGame(object):
    """
    Class to encapsulate the data and methods needed to play a Sprouts game.
    Accepts a Position instance as initial parameter.

    """

    def __init__(self, init_position):
        self.init_position = init_position


    def move(self, pos, face_ix, bnd_incl_t, start_d, end_d): 
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
        new_vtx = max( pos.get_seed_list() ) + 1

############33
        print "New Vtx: ", new_vtx, "Start Bnd: ", start_bnd, "End bnd: ", end_bnd, \
            "Start vtx: ", start_vtx, "End vtx: ", end_vtx

        # for joins in the same boundary => creating a new face
        if start_bnd == end_bnd:
 
            # 1st put together the replacement boundaries
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
#####33
                print start_degs[start_vtx], start_degs[end_vtx]
                print "Boundary: ", start_bnd

                if start_degs[start_vtx] < 3 and start_degs[end_vtx] < 3:
                    new_bnd1.extend( start_bnd[:start_d['vtx']] )
                    new_bnd1.extend( [start_vtx, new_vtx, end_vtx] )

                    start_degs[start_vtx] += 1
                    start_degs[end_vtx] += 1
                    start_degs[new_vtx] = 2

                    new_bnd2.extend(
                        [v for v in start_bnd[start_d['vtx']:end_d['vtx']]] )
                    new_bnd2.append(new_vtx)

            if not new_bnd1 or not new_bnd2:
                return []

            # 2nd put together the new faces with the right boundaries incl
            orig_face = [new_bnd1,]
            new_face = [new_bnd2,]

            orig_face.extend([ work_face[bnd_ix] 
                               for bnd_ix in range(len(work_face))
                               if bnd_ix != start_d['bnd']
                               and bnd_ix not in bnd_incl_t ])
            
            new_face.extend([ work_face[bnd_ix]
                              for bnd_ix in bnd_incl_t
                              if bnd_ix != start_d['bnd'] ])

            # 3rd put together a new faces list with orig & new
            new_faces_l = [orig_face, new_face,]

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
                    [ v for v in start_bnd[start_d['vtx']:] ] )

            repl_face = [new_bnd,]

            repl_face.extend([ work_face[bnd_ix]
                               for bnd_ix in range(len(work_face)) 
                               if bnd_ix not in [start_d['bnd'], end_d['bnd']] ])

        # create a new complete faces list incl new_faces_l + other orig faces
        new_faces_l.extend([ pos.faces[ix] for ix in range(len(pos.faces)) if ix != face_ix ])

#########3
        print "New faces list: ", new_faces_l

        new_position = Position(new_faces_l, string_input=False)
        return new_position


    def play(self, args):
        pass
