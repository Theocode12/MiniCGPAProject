import unittest
from models.result_checker import CGPAChecker
from tests.test_data.mock_data import data
from unittest.mock import Mock


class TestCGPAChecker(unittest.TestCase):
    def setUp(self) -> None:
        self.data_obj = Mock()
        self.data_obj.data = data

    def test_init_validation(self):
        self.assertIsInstance(CGPAChecker(self.data_obj), CGPAChecker)

    def test_check_session_with_both_semesters_provided(self):
        checker = CGPAChecker(self.data_obj)
        checker._check_session("Year 1", ["semester 1", "semester 2"])
        self.assertEqual(checker.cal_CGPA(), 5)

    def test_check_session_with_one_semester_provided(self):
        checker = CGPAChecker(self.data_obj)
        checker._check_session("Year 1", ["semester 2"])
        self.assertEqual(checker.cal_CGPA(), 5)

    def test_check_session_with_empty_semesters(self):
        checker = CGPAChecker(self.data_obj)
        checker._check_session("Year 1", [])
        self.assertEqual(checker.cal_CGPA(), 5)

    def test_check_session_with_None_semesters(self):
        checker = CGPAChecker(self.data_obj)
        checker._check_session("Year 1")
        self.assertEqual(checker.cal_CGPA(), 5)

    def test_retrieve_CGPA_without_specifics(self):
        checker = CGPAChecker(self.data_obj)
        gpa = checker.retrieve_CGPA()
        self.assertEqual(gpa, 5)

    def test_retrieve_CGPA_with_specifics(self):
        checker = CGPAChecker(self.data_obj)
        gpa = checker.retrieve_CGPA(
            {"Year 1": ["semester 1", "semester 2"], "Year 2": ["semester 1"]}
        )
        self.assertEqual(gpa, 5)

    def test_missing_year(self):
        checker = CGPAChecker(self.data_obj)
        with self.assertRaises(ValueError):
            checker._check_session("Year 5")

    def test_missing_semester(self):
        checker = CGPAChecker(self.data_obj)
        with self.assertRaises(ValueError):
            checker._check_session("Year 1", ["semester 3"])

    def test_invalid_specifics(self):
        checker = CGPAChecker(self.data_obj)
        with self.assertRaises(TypeError):
            checker.retrieve_CGPA({2: ["semester 1"]})
            checker.retrieve_CGPA({"Year 2": "invalid_data"})

    def test_empty_data(self):
        self.data_obj.data = {}
        with self.assertRaises(ValueError):
            CGPAChecker(self.data_obj)

    def test_wrong_type_for_data(self):
        self.data_obj.data = []
        with self.assertRaises(TypeError):
            CGPAChecker(self.data_obj)
