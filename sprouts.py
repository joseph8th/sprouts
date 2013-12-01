#!/usr/bin/env python2


def parse_args(argv):
    """
    Function to parse command line string argument and initialize faces list.
    """

    FACE_TOKEN = '/'
    BND_TOKEN = ';'
    VTX_TOKEN = ','

    # parse the command line
    if not len(argv) > 1:
        exit("Sprouts position expected.")
        
    input_str = str(argv[1])  
    faces_l = []                                     # init list of faces
        
    for face in input_str.split(FACE_TOKEN):
        bound_l = []
        faces_l.append(bound_l)
        for bnd in face.split(BND_TOKEN):
            vtx_l = []
            bound_l.append(vtx_l)
            for vtx in bnd.split(VTX_TOKEN):
                vtx_l.append(vtx)

    return faces_l



def main():
    """
    'Main' function to run sprouts game analysis.
    """

    faces_l = parse_args(sys.argv)

    print "\n-----------------------\nSprouts position input:\n-----------------------"
    for ix in range(len(faces_l)):
        print "Face [%d] has %d boundaries: " % (ix, len(faces_l[ix]))
        print "  --> ", faces_l[ix]



# top runs as script
import sys

if __name__=="__main__":
    main()
    
