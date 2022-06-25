# asu-major-map

A basic scraper and analyzer of major maps at ASU. Each major has a website with a mapping of its course per each term or semester. 
This repo takes that data and organizes it into lists using MajorMap objects.

A MajorMap can:
- Find similar courses with another MajorMap
- Delete courses or move them to different terms
- Find the number of credit hours per course or per term or overall
- Find the prerequisites for a course in the major
- Find the total number of unique courses with another MajorMap
- Be added to other MajorMaps
- Work with abbreviations

In addition, Chart objects can display info from a major's terms and courses.
They can be made either lists of courses or, more conveniently, MajorMap objects themselves.
A Chart object can create an svg containing a table with the courses from the list put in order of terms.
Giving it a MajorMap object (whether this is composite or singular or edited or anything) will display
the courses in it per term and also draw arrows from each course's prerequisites (if it has any) to that course.
Editing a MajorMap object passed into a Chart and then calling that Chart object's getGraph() again will reflect
the changes made to the MajorMap object.