
FACE_TOKEN = '/'
BND_TOKEN = ';'
VTX_TOKEN = ','



class Position(object):
    """
    A class to encapsulate gameboard position data.
    """

    faces = None

    def __init__(self, args):
        self.faces = self.get_faces_list(args)


    def __str__(self):
        if not self.faces:
            return ''
        return self.get_faces_string()


    def get_faces_list(self, input_str):
        """
        Method to parse string argument into list of lists of lists
        """
        
        faces_l = []
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
        Method to get position as formated string.
        """

        faces_s = ""
        for face_ix in range(len(self.faces)):
            face = self.faces[face_ix]
            for bnd_ix in range(len(face)):
                bnd = face[bnd_ix]
                for vtx_ix in range(len(bnd)):
                    faces_s += bnd[vtx_ix]
                    faces_s += VTX_TOKEN if vtx_ix < len(bnd)-1 else ""
                faces_s += BND_TOKEN if bnd_ix < len(face)-1 else ""
            faces_s += FACE_TOKEN if face_ix < len(self.faces)-1 else ""

        return faces_s
                    


class SproutsGame(object):

    def __init__(self, init_position):
        self.init_position = init_position
