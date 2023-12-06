import unittest
from src.models.course_collection import _CourseCollection



class CourseCollectionTest(unittest.TestCase):
    def setUp(self) -> None:
        self.courses = [
            ["Test101", "Course1", 2, "A"],
            ["Test102", "Course2", 3, "A"],
            ["Test103", "Course3", 1, "E"],
            ["Test104", "Course4", 2, None],
        ]
        self.coll = _CourseCollection()
        for course in self.courses:
            self.course_obj = self.coll.add_course(*course)
        self.courses_dict = [
            {"Test101": {"title": "Course1", "unit": 2, "grade": "A"}},
            {"Test102": {"title": "Course2", "unit": 3, "grade": "A"}},
            {"Test103": {"title": "Course3", "unit": 1, "grade": "E"}},
            {"Test104": {"title": "Course4", "unit": 2, "grade": None}},
        ]

    def test_if_grading_system_is_correct(self):
        grade = {"A": 5, "B": 4, "C": 3, "D": 2, "E": 1, "F": 0}
        self.assertDictEqual(self.coll.grade, grade)

    def test_add_course(self):
        self.assertGreater(len(self.coll.courses), 0)
        self.assertIs(self.course_obj, self.coll.courses[-1])

    def test_total_unit(self):
        total_unit = 0
        for course in self.courses_dict:
            unit = list(course.values())[0].get("unit")
            total_unit += unit
        self.assertEqual(self.coll.total_unit, total_unit)

    def test_total_available_graded_unit(self):
        total_graded_unit = 0
        for course in self.courses_dict:
            values = list(course.values())[0]
            if values.get("grade"):
                total_graded_unit += values.get("unit")

        self.assertEqual(self.coll.available_graded_unit, total_graded_unit)

    def test_cal_CGPA(self):
        cum_grade_unit = 0  # cumulative grade unit
        graded_unit = 0
        for course in self.courses_dict:
            values = list(course.values())[0]
            if values.get("grade"):
                graded_unit += values.get("unit")
                cum_grade_unit += _CourseCollection.grade.get(
                    values.get("grade")
                ) * values.get("unit")
        True_cgpa = round(cum_grade_unit / graded_unit, 2)
        self.assertAlmostEqual(self.coll.cal_CGPA(), True_cgpa)

    def tearDown(self) -> None:
        pass
