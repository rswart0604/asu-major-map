from bs4 import BeautifulSoup
import urllib.request

class MajorMap:
    AEROSPACE = "https://degrees.apps.asu.edu/major-map/ASU00/ESAEROBSE/null/ALL/2020?init=false&nopassive=true"
    ENGLISH = "https://degrees.apps.asu.edu/major-map/ASU00/LAENGBA/null/ONLINE/2013?init=false&nopassive=true"
    CS = 'https://degrees.apps.asu.edu/major-map/ASU00/ESCSEBS/null/ALL/2021?init=false&nopassive=true'

    def __init__(self, major_map_url: str):
        """Create your favorite major map

        :param major_map_url: the url of the major map
        """


        # get our soup
        foo = urllib.request.urlopen(major_map_url)
        a = foo.read()
        a.decode("utf8")
        soup = BeautifulSoup(a, features='html.parser')

        # set up return arrays, etc. and get our tables we're looking at
        self.hours_term_list = []
        self.hours_terms_dict = {}
        self.terms_list = []
        self.terms_dict = {}
        tables = soup.find_all("table", class_="termTbl")

        # print("hello!")  # sanity

        # go thru each table
        for table in tables:  # this will go through each term
            # here, get some preliminary data. the term number, the courses table, etc
            table_rows = table.find_all('tr')
            term_number = table_rows[0].td.span.get_text()  # there is one for each table
            courses_table = table_rows[1].td.table
            courses_table_rows = courses_table.find_all('tr')

            # sift through that courses list and get the specific courses and their credit hour amounts
            temp_hours_course_list = []
            temp_course_list = []
            for course_tr in courses_table_rows:
                if course_tr.div is not None:  # if the course is a thing, get its data
                    course_text = course_tr.div.get_text()  # the course name
                    try:
                        hours = str(course_tr.find_all('td')[2].get_text()).split()[0]  # the credit hours needed
                    except Exception:
                        continue
                    if len(hours) == 0:
                        continue
                    course = str(course_text).strip().replace("  ", " ").replace("\n", "").replace("\r", "")
                    temp_hours_course_list.append((course, hours))  # combine the course and hours needed
                    temp_course_list.append(course)
            self.hours_term_list.append(temp_hours_course_list)  # add this term's courses to our overall list
            self.hours_terms_dict[term_number] = temp_hours_course_list  # and dict
            self.terms_list.append(temp_course_list)
            self.terms_dict[term_number] = temp_course_list

    def get_term_list(self, hours=False, labels=False):
        """Will return a list of the courses in the map. Will be a nested list
        where each term's worth of courses are in their own list

        :param hours: if True, each course will instead be a tuple with their credit
        hours listed ie (course, # of credit hours)
        :param labels: if True, this will return a dict that has each list labeled by their term
        :return: with no args, a list of lists of each course (string), each list being a term
        """
        if hours and labeled:
            return self.hours_terms_dict
        if labeled:
            return self.terms_dict
        if hours:
            return self.hours_term_list
        return self.terms_list

    def find_similar_courses(self, map: 'MajorMap'):
        list1 = self.terms_list
        list2 = map.get_term_list()
        out = [item for item in list1 if item in list2]
        return out

    def total_classes(self, map: 'MajorMap', labels=False):
        if labels:  # use stupid term labels
            dict1 = dict(self.get_term_list(False, True))
            dict2 = dict(map.get_term_list(False, True))
            for term, courses in dict2:
                for course in courses:
                    if course not in self.get_term_list():
                        dict1[term].append(course)
            return dict1
        else:
            list1 = list(self.terms_list)
            for x in map.get_term_list():
                if x not in list1:
                    list1.append(x)
            return list1


# def total_classes(list1, list2, labels=False):
#     if (labels):   # list1 and list2 are dicts with term labels -> {'term': [(class, hour), (class, hour)]}
#         d1 = dict(list1)
#         d2 = dict(list2)
#         if (len(d1) != len(d2)):
#             raise Exception  # deal with stupid A and B terms if they exist
#         for term, courses in d2:
#             for course in courses:
#                 if course not in d1
#     else:  # list1 and list2 have no term labels. normal lists
#         l1 = list(list1)
#         l2 = list(list2)
#         l1 = flatten(remove_hours(l1))
#         l2 = flatten(remove_hours(l2))
#         new_l = list(l1)
#         for x in l2:
#             if x not in l1:
#                 new_l.append(x)
#         return new_l