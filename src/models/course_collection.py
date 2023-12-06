from typing import ClassVar, Dict, Sequence, Union, List

"""
This File contain Models for Course and Course_Collection Classes
"""
from ..models.course import _Course


class _CourseCollection:
    """
    This handles all the courses object and calculation related methods
    Args: None
    """

    grade: ClassVar[Dict[str, int]] = {"A": 5, "B": 4, "C": 3, "D": 2, "E": 1, "F": 0}

    def __init__(self) -> None:
        self.courses: List[_Course] = []
        self.total_unit: int = 0
        self.available_graded_unit: int = 0

    def add_course(
        self, course_code, course_name: str, unit: int, grade: Union[str, None] = None
    ) -> _Course:
        """Add a new course"""
        self.courses.append(_Course(course_code, course_name, unit, grade))
        self.cal_total_unit(unit)
        if grade is not None:
            self.cal_total_available_graded_unit(unit)
        return self.courses[-1]

    def cal_total_unit(self, unit: int) -> int:
        """Calculates the total units of all the courses"""
        self.total_unit += unit
        return self.total_unit

    def cal_total_available_graded_unit(self, unit: int) -> int:
        """Calulates the total unit for course which has grades"""
        self.available_graded_unit += unit
        return self.available_graded_unit

    def cal_CGPA(self) -> float:
        """Calculates the CGPA for the courses which have grades. Returns float with two decimal places"""
        cum_grade_unit = 0  # cumulative grade unit
        self.available_graded_unit = 0
        for course in self.courses:
            if course.grade:
                self.cal_total_available_graded_unit(course.unit)
                cum_grade_unit += (
                    _CourseCollection.grade.get(course.grade, 0) * course.unit
                )

        return round(cum_grade_unit / self.available_graded_unit, 2)
