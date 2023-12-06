import unittest
from models.course import _Course

class CourseTest(unittest.TestCase):
    def setUp(self) -> None:
        self.course_1 = _Course("TST101", "TestCourse1", 3)
        self.course_2 = _Course("TST102", "TestCourse2", 2, "B")

    def test_course_code(self):
        self.assertEqual("TST101", self.course_1.code)
        self.assertNotEqual("TST103", self.course_1.code)

    def test_course_title(self):
        self.assertEqual("TestCourse1", self.course_1.title)
        self.assertNotEqual("WrongCourse", self.course_1.title)

    def test_course_unit(self):
        self.assertEqual(3, self.course_1.unit)
        self.assertNotEqual(4, self.course_1.unit)

    def test_course_grade_if_missing(self):
        self.assertIsNone(self.course_1.grade)

    def test_course_grade_if_available_after_class_creation(self):
        self.course_1.grade = "A"
        self.assertEqual("A", self.course_1.grade)
        self.assertNotEqual("B", self.course_1.grade)

    def test_course_grade_if_available_before_class_creation(self):
        self.assertEqual("B", self.course_2.grade)
        self.assertNotEqual("A", self.course_2.grade)

    def test_wrong_grade(self):
        with self.assertRaises(ValueError):
            self.course_2.grade = "G"

    def test_course_title_with_wrong_type(self):
        with self.assertRaises(TypeError):
            _Course("Test101", None, 4)

    def test_course_unit_with_wrong_type(self):
        with self.assertRaises(TypeError):
            _Course("Test101", "Course", "4")

    def test_course_grade_with_wrong_type(self):
        with self.assertRaises(TypeError):
            _Course("Test101", "Course", 4, 5)

    def test_course_grade_with_wrong_value(self):
        with self.assertRaises(ValueError):
            _Course("Test101", "Course", 4, "AA")

    def test_total_number_of_course_objects(self):
        self.assertEqual(2, _Course.Total_courses)
        another_course = _Course("Test103", "TestCourse1", 2, "B")
        self.assertEqual(3, _Course.Total_courses)

    def tearDown(self) -> None:
        _Course.Total_courses = 0
