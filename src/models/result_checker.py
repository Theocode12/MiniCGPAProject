from typing import Dict, Union, List
from models.course_collection import _CourseCollection


class CGPAChecker(_CourseCollection):
    """
    This class provide a level of abstraction for checking CGPA, so that
    there is no interaction with the CourseCollection class itself.
    Args:
        data: the data attribute must be an instance which has attribute data which must be in the format below:
            {
                "Year 1":{
                    "semester 1":{
                        "#code_1":{
                            "title": "#title",
                            "unit": "#unit",
                            "grade": "#grade", -> optional
                        },
                        "#code_2":{
                            "title": "#title,
                            "unit": "#unit"
                            "grade": "#grade" -> optional
                        },
                        ...
                    },
                    "semester 2":{
                        "#code_1":{
                            "title": "#title",
                            "unit": "#unit",
                            "grade": "#grade", -> optional
                        },
                        "#code_2":{
                            "title": "#title,
                            "unit": "#unit"
                            "grade": "#grade" -> optional
                        },
                        ...
                    }
                }
                "Year 2":{
                    "semester 1":{
                        "#code_1":{
                            "title": "#title",
                            "unit": "#unit",
                            "grade": "#grade", -> optional
                        },
                        "#code_2":{
                            "title": "#title,
                            "unit": "#unit"
                            "grade": "#grade" -> optional
                        },
                        ...
                    },
                    "semester 2":{
                        "#code_1":{
                            "title": "#title",
                            "unit": "#unit",
                            "grade": "#grade", -> optional
                        },
                        "#code_2":{
                            "title": "#title,
                            "unit": "#unit"
                            "grade": "#grade" -> optional
                        },
                        ...
                    }
                }
            }
    """

    def __init__(self, data_obj) -> None:
        self.data = data_obj.data
        super().__init__()

    # make setter and getters to validate data
    @property
    def data(self) -> dict:

        return self.__data

    @data.setter
    def data(self, data):
        if not isinstance(data, dict):
            raise TypeError("data must be a dict")

        if len(data) == 0:
            raise ValueError("data must not be empty")

        for year, year_data in data.items():
            if not isinstance(year, str):
                raise TypeError("{} must be a string".format(year))

            if not year.startswith("Year"):
                raise ValueError("{} must start with 'Year'".format(year))

            if not isinstance(year_data, dict):
                return TypeError("{} is not a dict".format(year_data))

            for semester, semester_data in year_data.items():
                if not isinstance(semester, str):
                    raise TypeError("{} must be a string".format(semester))

                if not semester.startswith("semester"):
                    raise ValueError("{} must start with 'semester'".format(semester))

                if not isinstance(semester_data, dict):
                    return TypeError("{} is not a dict".format(semester_data))

                for course_code, course_info in semester_data.items():
                    if not isinstance(course_code, str):
                        raise TypeError("{} must be a string".format(course_code))

                    if not isinstance(course_info, dict):
                        raise TypeError("{} must be a dict".format(course_info))

                    required_keys = {"title", "unit"}
                    optional_keys = {"grade"}

                    if not all(key in course_info for key in required_keys):
                        raise Exception("title and unit must be specified")

        self.__data = data

    def retrieve_CGPA(self, specifics: Union[Dict[str, List[str]], None] = None):
        """
        Retrives CGPA from data using the specified specifics
        Args:
                specifics: A dictionary which contains the what part of the data is used to determine the CGPA

                Below is an example of specifics
                {"Year 1": ["semester 1","semester 2"], "Year 2": ["semester 1"]}

                if no specifics is specified, the whole data will be used to determine the CGPA
        """
        if specifics is None:
            specifics = {}
            for year in list(self.data.keys()):
                specifics[year] = []
        else:
            if not isinstance(specifics, dict):
                raise TypeError("specifics must be a dict")
            for key in list(specifics.keys()):
                if not isinstance(key, str):
                    raise TypeError("key must be a string")
            for value in list(specifics.values()):
                if not isinstance(value, list) and not value is None:
                    raise TypeError("value must be list or None")

        for year, semesters in specifics.items():
            self._check_session(year, semesters)

        return self.cal_CGPA()

    def _check_session(self, year: str, semesters: Union[list, None] = None) -> None:
        if semesters is None or len(semesters) == 0:
            semesters = ["semester 1", "semester 2"]
        for semester in semesters:
            if semester_data := self.data.get(year):
                if courses := semester_data.get(semester):
                    self._init_courses(courses)
                else:
                    raise ValueError("Invalid semester")
            else:
                raise ValueError("{} Not part of Data".format(year))

    def _init_courses(self, courses: Dict) -> None:
        for code, attr in courses.items():
            self.add_course(
                code, attr.get("title"), int(attr.get("unit")), attr.get("grade")
            )
