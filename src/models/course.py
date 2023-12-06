from typing import ClassVar, Dict, Union, Optional

"""
This File contain Models for Course and Course_Collection Classes
"""


class _Course:
    """
    The Course class is a reprsentation of a course in class
    Args:
                name: The name of the course
                unit: The unit of the course
                Grade: The grade of the course(NONE by default)
    """

    Total_courses: ClassVar[int] = 0

    def __init__(
        self, code: str, title: str, unit: int, grade: Optional[str] = None
    ) -> None:
        self.code: str = code
        self.title: str = title
        self.unit: int = unit
        self.grade: Optional[str] = grade or None
        self.__class__.Total_courses += 1

    @property
    def code(self) -> str:
        """Return the course code for the course"""

        return self.__code

    @code.setter
    def code(self, value: str) -> None:
        """Set the course code for the course"""

        if type(value) is not str:
            raise TypeError("name must be an string")
        self.__code = value

    @property
    def title(self) -> str:
        """Return the title of the course"""

        return self.__name

    @title.setter
    def title(self, value: str) -> None:
        """Set the title for the course"""

        if type(value) is not str:
            raise TypeError("name must be an string")
        self.__name = value

    @property
    def unit(self) -> int:
        """Return the unit of the course"""

        return self.__unit

    @unit.setter
    def unit(self, value: int) -> None:
        """Set the unit of the course"""

        if type(value) is not int:
            raise TypeError("unit must be an integer")
        self.__unit = value

    @property
    def grade(self) -> str:
        """Return the grade of the course"""

        return self.__grade

    @grade.setter
    def grade(self, value: str) -> None:
        """Set the grade of the course"""
        from models.course_collection import _CourseCollection

        if value is not None and type(value) is not str:
            raise TypeError("grade must be an string")
        if value is not None and value not in _CourseCollection.grade:
            raise ValueError("grade must be between A - F")
        self.__grade = value
