import copy

from bs4 import BeautifulSoup
import urllib.request


def flatten(nested_list: list) -> list:
    temp = []
    for x in nested_list:
        if type(x) is list:
            for y in x:
                temp.append(y)
        else:
            temp.append(x)
    return temp


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
        self.terms_dict_urls = {}
        self.course_to_url = {}
        self.abbreviation_to_course_name = {}
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
            temp_urls_course_list = []
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
                    url = course_tr.div.a['href']
                    temp_urls_course_list.append((course, url))
                    self.course_to_url[course] = url
                    temp_hours_course_list.append((course, hours))  # combine the course and hours needed
                    temp_course_list.append(course)

            self.hours_term_list.append(temp_hours_course_list)  # add this term's courses to our overall list
            self.hours_terms_dict[term_number] = temp_hours_course_list  # and dict
            self.terms_list.append(temp_course_list)
            self.terms_dict[term_number] = temp_course_list
            self.terms_dict_urls[term_number] = temp_urls_course_list

    def get_terms_list(self, hours=False, labels=False, urls=False):
        """Will return a list of the courses in the map. Will be a nested list
        where each term's worth of courses are in their own list

        :param hours: if True, each course will instead be a tuple with their credit
        hours listed ie (course, # of credit hours)
        :param labels: if True, this will return a dict that has each list labeled by their term
        :return: with no args, a list of lists of each course (string), each list being a term
        """
        if hours and labels:
            return copy.deepcopy(self.hours_terms_dict)
        if labels:
            return copy.deepcopy(self.terms_dict)
        if hours:
            return copy.deepcopy(self.hours_term_list)
        if urls:
            return copy.deepcopy(self.terms_dict_urls)
        return copy.deepcopy(self.terms_list)

    def get_sim_courses(self, maj_map: 'MajorMap'):
        list1 = self.terms_list
        list2 = maj_map.get_terms_list()
        out = [item for item in list1 if item in list2]
        return out

    def get_diff_courses(self, maj_map: 'MajorMap'):
        """Finds mutually exclusive courses
        :param maj_map: a major map that you want to find the exclusive courses of
        :return: a list of all courses in maj_map that are not in self
        """
        list1 = flatten(self.get_terms_list())
        list2 = flatten(maj_map.get_terms_list())
        out = [x for x in list2 if x not in list1]
        return out

    def get_total_courses(self, maj_map: 'MajorMap', labels=False):
        if labels:  # use stupid term labels
            dict1 = self.get_terms_list(False, True)
            dict2 = maj_map.get_terms_list(False, True)
            flat_list = flatten(self.get_terms_list())
            for term, courses in dict2.items():
                for course in courses:
                    if course not in flat_list:
                        dict1[term].append(course)
            return dict1
        else:
            list1 = flatten(self.get_terms_list())
            list2 = flatten(maj_map.get_terms_list())
            for x in list2:
                if x not in list1:
                    list1.append(x)
            return list1

    def get_total_hours(self):
        total = 0
        for courses in self.get_terms_list(True):
            for course, hour in courses:
                total += hour
        return total

    def get_hours_per_term(self):
        terms_and_hours = {}
        for term, courses in self.get_terms_list(True, True).items():
            tmp_hours = 0
            for course, hours in courses:
                try:
                    tmp_hours += int(hours)
                except ValueError:
                    tmp_hours += int(hours[0])  # if there's a range (ie 1-2 hours), just take the first one
            terms_and_hours[term] = tmp_hours
        return terms_and_hours

    def get_course_abbreviations(self):
        """this will return only the class abbreviation (ie ENG 101). Still keep as a dict
        *** if the course does not have a label, it will be omitted!!
        :return: a dict of classes and term labels without hours and only abbreviations. see below
        """
        foo = self.get_terms_list(False, True)
        out = {}
        for term, courses in foo.items():
            tmp_courses = []
            for course in courses:
                if course[0:3].isupper() and course[3] == ' ' and course[4:7].isdigit():
                    tmp_courses.append(course[0:7])
                    self.abbreviation_to_course_name[course[0:7]] = course
            out[term] = tmp_courses
        return out  # return is of form {term label: [course abbreviation, ...]}

    def find_prereqs(self, course_name: str):
        # take all of the abbreviations that we have
        # scrape and find the official prereqs text
        # add each item in abbreviations list that is in prereqs text and add to a list
        # turn that list into where it actually has the official naming
        # output that official naming list
        url = self.course_to_url[course_name]

        # get some more soup!
        new_url = url.replace('courselist', 'mycourselistresults')
        print(new_url)
        foo = urllib.request.urlopen(new_url)
        a = foo.read()
        a.decode("utf8")
        soup = BeautifulSoup(a, features='html.parser')
        text = soup.find('td', class_='courseTitleLongColumnValue').text

        out = []
        abbreviations = flatten(self.get_course_abbreviations().values())
        for abb in abbreviations:
            if abb in text:
                out.append(self.abbreviation_to_course_name[abb])
            elif abb[0:3] in text and abb[4:7] in text:  # going a lil complicated but cmon just work already
                out.append(self.abbreviation_to_course_name[abb])
        return out
