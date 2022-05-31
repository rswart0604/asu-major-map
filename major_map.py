from bs4 import BeautifulSoup
import urllib.request
from pprint import pprint

AEROSPACE = "https://degrees.apps.asu.edu/major-map/ASU00/ESAEROBSE/null/ALL/2020?init=false&nopassive=true"
ENGLISH = "https://degrees.apps.asu.edu/major-map/ASU00/LAENGBA/null/ONLINE/2013?init=false&nopassive=true"
CS = 'https://degrees.apps.asu.edu/major-map/ASU00/ESCSEBS/null/ALL/2021?init=false&nopassive=true'


def major_map(major_map_url: str, return_dict=False, keep_hours=True):
    """Obtain a list representation of your favorite major map! With no
    extra args, it will return a list of lists with tuples. The lists demarcate the different terms
    and the tuples are the courses themselves in the form (course, # of credit hours)

    :param major_map_url: the url of the major map you want to turn into a list
    :param return_dict: if this is True, this will return a dict where the
        different terms are labeled (ie {'Term 1': [('ASU101', '1'), ...)
    :param keep_hours: if this is True, the tuples will be kept for courses
        ie (course_name, # of credit hours). Otherwise, just the course name (no tuple) will be kept
    :return: a list of term lists that contain that courses as tuples,
        or a dict of term lists that have tuple courses
    """

    # get our soup
    foo = urllib.request.urlopen(major_map_url)
    a = foo.read()
    a.decode("utf8")
    soup = BeautifulSoup(a, features='html.parser')

    # set up return arrays, etc. and get our tables we're looking at
    term_list = []
    terms_labeled = {}
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
        temp_course_list = []
        for course_tr in courses_table_rows:
            if course_tr.div is not None:  # if the course is a thing, get its data
                course_text = course_tr.div.get_text()  # the course name
                try:
                    hours = str(course_tr.find_all('td')[2].get_text()).split()[0] # the credit hours needed
                except Exception:
                    continue
                if len(hours) == 0:
                    continue
                course = str(course_text).strip().replace("  ", " ").replace("\n", "").replace("\r", "")
                # print(term_number)
                # print(course)
                # print(hours)
                # print("--------")
                if keep_hours:
                    temp_course_list.append((course, hours))  # combine the course and hours needed
                else:
                    temp_course_list.append(course)
        term_list.append(temp_course_list)  # add this term's courses to our overall list
        terms_labeled[term_number] = temp_course_list  # and dict
    if return_dict:
        return terms_labeled
    else:
        return term_list


def flatten(nested_list: list) -> list:
    temp = []
    for x in nested_list:
        if type(x) is list:
            for y in x:
                temp.append(y)
        else:
            temp.append(x)
    return temp


def remove_hours(map: list) -> list:
    temp_course_list = []
    for term in map:
        temp_terms = []
        for class_set in term:
            if type(class_set) is tuple:
                temp_terms.append(class_set[0])
            else:
                temp_terms.append(class_set)
        temp_course_list.append(temp_terms)
    return temp_course_list


def list_sim(list1, list2) -> list:
    l1 = list(list1)
    l2 = list(list2)
    l1 = flatten(remove_hours(l1))
    l2 = flatten(remove_hours(l2))
    out = [item for item in l1 if item in l2]
    return out


def total_classes(list1: list, list2: list):
    l1 = list(list1)
    l2 = list(list2)
    l1 = flatten(remove_hours(l1))
    l2 = flatten(remove_hours(l2))
    new_l = list(l1)
    for x in l2:
        if x not in l1:
            new_l.append(x)
    return new_l
