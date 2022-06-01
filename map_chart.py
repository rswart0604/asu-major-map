from major_map import MajorMap
import schemdraw
from schemdraw import flow


class Chart:

    def __init__(self, *args):
        """We want this class to be able to handle not just MajorMap objects, but possibly lists
        made by combining major map term lists, etc
        :param args: a MajorMap object, a dict from a MajorMap, or a nested list of courses in a map
        """
        if type(args[0]) is MajorMap:
            self.map = args[0].get_terms_list(False, True)
        else:
            self.map = args[0]
        self.BOX_WIDTH = 6
        self.BOX_HEIGHT = 4



    def get_graph(self):
        with schemdraw.Drawing() as d:
            if type(self.map) is dict:
                x_pos = 0
                for term, courses in self.map.items():
                    d += flow.Box(w=self.BOX_WIDTH, h=self.BOX_HEIGHT).label(term).at((x_pos, 0))  # our term label
                    y_pos = 0
                    for course in courses:
                        y_pos -= (self.BOX_HEIGHT + 1)

                        # stupid stupid string formatting stuff. no more than 20 chars per line
                        words = course.split()
                        word_list = []
                        tmp = ""
                        for word in words:
                            tmp += (word + " ")
                            if len(tmp) > 12:
                                word_list.append((tmp + '\n'))
                                tmp = str('')
                        result = ''.join(word_list)
                        if result == '':  # if we only have one word for our course (ie 'Elective'), this catches that
                            result = course

                        d += flow.Box(w=self.BOX_WIDTH, h=self.BOX_HEIGHT).label(result).at((x_pos, y_pos))
                    x_pos += (self.BOX_WIDTH + 1)
            else:  # we got a nested list on our hands
                return