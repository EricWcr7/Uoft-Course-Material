# Assignment 2 - Course Planning!
#
# CSC148 Fall 2014, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
# STUDENT INFORMATION
#
# List your group members below, one per line, in format
# <full name>, <utorid>
# Su Young Lee, leesu9
# Rui Qiu, qiurui2
#
# ---------------------------------------------
"""Course prerequisite data structure.

This module contains the class that should store all of the
data about course prerequisites and track taken courses.
Note that by tracking "taken" courses, we are restricting the use
of this class to be one instance per student (otherwise,
"taken" doesn't make sense).

Course: a course and its prerequisites.
"""


class UntakeableError(Exception):
    pass

class PrerequisiteError(Exception):
    pass

class Course:
    """A tree representing a course and its prerequisites.

    This class not only tracks the underlying prerequisite relationships,
    but also can change over time by allowing courses to be "taken".

    Attributes:
    - name (str): the name of the course
    - prereqs (list of Course): a list of the course's prerequisites
    - taken (bool): represents whether the course has been taken or not
    """

    # Core Methods - implement all of these
    def __init__(self, name, prereqs=None):
        """ (Course, str, list of Courses) -> NoneType

        Create a new course with given name and prerequisites.
        By default, the course has no prerequisites (represent this
        with an empty list, NOT None).
        The newly created course is not taken.
        """
        self.name = name
        if prereqs == None:
            self.prereqs = []
        else:
            self.prereqs = prereqs
        self.taken = False

    def is_takeable(self):
        """ (Course) -> bool

        Return True if the user can take this course.
        A course is takeable if and only if all of its prerequisites are taken.
        """
        if self.prereqs == []:
            return True
        else:
            for prereq in self.prereqs:
                return prereq.taken == True

    def take(self):
        """ (Course) -> NoneType

        If this course is takeable, change self.taken to True.
        Do nothing if self.taken is already True.
        Raise UntakeableError if this course is not takeable.
        """
        if self.is_takeable():
            self.taken = True
        else:
            raise UntakeableError

    def add_prereq(self, prereq):
        """ (Course, Course) -> NoneType

        Add a prereq as a new prerequisite for this course.

        Raise PrerequisiteError if either:
        - prereq has this course in its prerequisite tree, or
        - this course already has prereq in its prerequisite tree
        """
        if self.name == prereq.name:
            raise PrerequisiteError
        # above is not stated in handout, but i think it's necessary
        else:
            if prereq.in_prereq_tree(self):
                raise PrerequisiteError
            elif self.in_prereq_tree(prereq):
                raise PrerequisiteError
            else:
                self.prereqs.append(prereq)
            
    # helper function
    def in_prereq_tree(self, item):
        """ (Course, Course) -> Bool
        
        Return True if item is in the prerequisite tree of self.
        """
        if item in self.prereqs:
            return True
        elif self.prereqs == []:
            return False
        else:
            for course in self.prereqs:
                return course.in_prereq_tree(item)

    def missing_prereqs(self):
        """ (Course) -> list of str

        Return a list of all of the names of the prerequisites of this course
        that are not taken.

        The returned list should be in alphabetical order, and should be empty
        if this course is not missing any prerequisites.
        
        This method missing_prereqs should be recursive, i.e., if self has a missing prerequisite course CSC148, and CSC148 has a missing prerequisite CSC108, then both "CSC108" and "CSC148" should appear in the returned list.
        """
        # the recursion part is in helper function:
        
        missing = []        
        if self.all_prereqs() == []:
            return []
        else:
            for course in self.all_prereqs():
                if not course.taken:
                    missing.append(course.name)
            missing.sort()
            return missing
    
    # another helper function
                    
    def all_prereqs(self):
        """ (Course) -> list of Course
        
        Return a list of all prerequisites of a given course, and all prereqs of prereqs etc.
        
        Return empty list if the given course has no prerequisite.
        """
        
        lst = []
        if self.prereqs == []:
            return []
        else:
            for course in self.prereqs:
                lst.extend(course.all_prereqs())
            return lst + self.prereqs
