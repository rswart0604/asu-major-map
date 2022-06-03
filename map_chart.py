from major_map import MajorMap
import schemdraw
from schemdraw import flow
import math


def format_words(course: str):
    words = course.split()
    word_list = []
    tmp = ""
    for word in words:
        tmp += (word + " ")
        if len(tmp) > 12:
            word_list.append((tmp + '\n'))

            tmp = str('')
    if tmp != '':
        word_list.append(tmp)
    result = ''.join(word_list)
    if result == '':  # if we only have one word for our course (ie 'Elective'), this catches that
        result = course
    result = result.replace('&', 'and')
    return result


class Chart:

    def __init__(self, *args):
        """We want this class to be able to handle not just MajorMap objects, but possibly lists
        made by combining major map term lists, etc
        :param args: a MajorMap object, a dict from a MajorMap, or a nested list of courses in a map
        """
        if type(args[0]) is MajorMap:
            self.map = args[0].get_terms_list(False, True)
            self.maj_map = args[0]
        else:
            self.map = args[0]
            self.maj_map = None
        self.BOX_WIDTH = 5
        self.BOX_HEIGHT = 3.5
        self.dx = 2
        self.dy = 2

    def get_graph(self):
        file_name = str(self.maj_map).lower().replace(' ', '_') + '.svg' if self.maj_map is not None else 'major_map.svg'
        with schemdraw.Drawing(file=file_name, fontsize=12) as d:

            if self.maj_map is not None:
                print('MAJ MAP!!!')
                course_to_box = {}
                x_pos = 0
                for term, courses in self.map.items():
                    d += flow.Box(w=self.BOX_WIDTH, h=self.BOX_HEIGHT).label(term).at((x_pos, 0))  # our term label
                    y_pos = 0
                    for course in courses:  # go through each term's courses pls
                        y_pos -= (self.BOX_HEIGHT + self.dy)

                        # stupid stupid string formatting stuff. no more than 20 chars per line
                        result = format_words(course)

                        course_to_box[course] = flow.Box(w=self.BOX_WIDTH, h=self.BOX_HEIGHT).label(result).at((x_pos, y_pos))
                        d += course_to_box[course]
                        prereqs = self.maj_map.find_prereqs(course)
                        if len(prereqs) > 0 and x_pos > 0:
                            print(course + ": " + str(prereqs))
                            for prereq in prereqs:
                                if prereq != course:
                                    d += flow.ArcN(arrow='->').at(course_to_box[prereq].E).to(course_to_box[course].W)

                    x_pos += (self.BOX_WIDTH + self.dx)
            elif type(self.map) is dict:  # term labels! yay! for once!
                x_pos = 0
                for term, courses in self.map.items():
                    d += flow.Box(w=self.BOX_WIDTH, h=self.BOX_HEIGHT).label(term).at((x_pos, 0))  # our term label
                    y_pos = 0
                    for course in courses:  # go through each term's courses pls
                        y_pos -= (self.BOX_HEIGHT + self.dy)

                        # stupid stupid string formatting stuff. no more than 20 chars per line
                        result = format_words(course)

                        d += flow.Box(w=self.BOX_WIDTH, h=self.BOX_HEIGHT).label(result.strip()).at((x_pos, y_pos))
                    x_pos += (self.BOX_WIDTH + self.dx)
            else:  # we got a nested list on our hands
                x_pos = 0
                for courses in self.map:
                    y_pos = self.BOX_HEIGHT + self.dy
                    for course in courses:
                        y_pos -= (self.BOX_HEIGHT + self.dy)

                        # stupid stupid string formatting stuff. no more than 20 chars per line
                        result = format_words(course)

                        d += flow.Box(w=self.BOX_WIDTH, h=self.BOX_HEIGHT).label(result).at((x_pos, y_pos))
                    x_pos += (self.BOX_WIDTH + self.dx)
