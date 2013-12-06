

class Report(object):
    """
    Class to report a summary of information about given game tree.
    """

    def __init__(self, tree):
        self.report(tree)


    def report(self, tree):
        ret_str = "\nGame Summary:\n=============\n\n"
        ret_str += "Initial Position: %s\n" % (tree.root.get_faces_string())
        ret_str += "Game Tree Depth: %s\tGame Tree Size: %s\n" % (tree.depth, tree.size)

        print ret_str
