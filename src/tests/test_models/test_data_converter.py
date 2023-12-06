import io
import unittest
import os

from pathlib import PosixPath
from models.result_checker import CGPAChecker
from models.data_converter import DataConverter

from unittest.mock import patch, mock_open, call


class TestDataConverter(unittest.TestCase):
    def setUp(self) -> None:
        self.converter = DataConverter()

    def test_update_data_structure(self):
        # Case 1: Update data for a new year, semester, and course code
        row = {"Year": "2", "Semester": "2", "Code": "C002", "Title": "Physics", "Unit": "4", "Grade": "B"}
        self.converter._update_data_structure(row)
        expected_data = {"Year 2": {"semester 2": {"C002": {"title": "Physics", "unit": "4", "grade": "B"}}}}
        self.assertEqual(self.converter.data, expected_data)

        # Case 2: Update data for an existing year, semester, and a new course code
        row = {"Year": "2", "Semester": "2", "Code": "C003", "Title": "Chemistry", "Unit": "4", "Grade": "C"}
        self.converter._update_data_structure(row)
        expected_data["Year 2"]["semester 2"]["C003"] = {"title": "Chemistry", "unit": "4", "grade": "C"}
        self.assertEqual(self.converter.data, expected_data)

        # Case 3: Update data for an existing year, semester, and course code
        row = {"Year": "2", "Semester": "2", "Code": "C002", "Title": "Physics II", "Unit": "3", "Grade": "A"}
        self.converter._update_data_structure(row)
        expected_data["Year 2"]["semester 2"]["C002"] = {"title": "Physics II", "unit": "3", "grade": "A"}
        self.assertEqual(self.converter.data, expected_data)

    def test_validate_grade_input(self):
        #Case 1: Valid Uppercase letters
        with patch('builtins.input', return_value="A"):
            grade = self.converter._validate_grade_input("Enter grade: ")
        self.assertEqual(grade, "A")

        #Case 2: Valid Lowercase letters
        with patch('builtins.input', return_value="b"):
            grade = self.converter._validate_grade_input("Enter grade: ")
        self.assertEqual(grade, "B")
        self.assertNotEqual(grade, "b")

        #Case 3: Invalid Input Followed by valid Input
        with patch("builtins.input", side_effect=["V", "c"]), patch("sys.stdout", new_callable=io.StringIO) as mock_obj:
            grade = self.converter._validate_grade_input("Enter grade: ")
        self.assertEqual(grade, "C")
        self.assertEqual(mock_obj.getvalue(), "Invalid input. Please enter a letter from A to F (case-insensitive).\n")

    def test_convert_raw_template(self):
        template_content = 'Year,Semester,Code,Title,Unit\n1,1,EGR 101,Math,2\n'
        mock_file = mock_open(read_data=template_content)
        with patch("builtins.input", side_effect=["student_result", "A"]), patch("sys.stdout", new_callable=io.StringIO) as mock_obj:
            with patch("builtins.open", mock_file):
                self.converter.convert_raw_template("template_file.csv")
        self.assertEqual(self.converter.buffer, [{"Year": "1", "Semester": "1", "Code": "EGR 101", "Title": "Math", "Unit": "2", "Grade": "A"}])
        self.assertEqual(self.converter.data, {"Year 1": {"semester 1": {"EGR 101": {"title": "Math", "unit": "2", "grade": "A"}}}})

        mock_file.assert_has_calls([call('student_result.csv', 'w+', newline='')])

    def test_convert_complete_template(self):
        #Case 1: content has grade
        template_content = 'Year,Semester,Code,Title,Unit,Grade\n1,1,EGR 101,Math,2,A\n'
        mock_file = mock_open(read_data=template_content)
        with patch("builtins.open", mock_file), patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            self.converter.convert_complete_template("template_file")
        self.assertEqual(self.converter.buffer, [{"Year": "1", "Semester": "1", "Code": "EGR 101", "Title": "Math", "Unit": "2", "Grade": "A"}])
        self.assertEqual(self.converter.data, {"Year 1": {"semester 1": {"EGR 101": {"title": "Math", "unit": "2", "grade": "A"}}}})
        self.assertEqual(mock_stdout.getvalue(), "Data has been written to template_file\n")

        #Case 2: content doesn't have grades
        self.converter.buffer = []
        self.converter.data = {}
        template_content = 'Year,Semester,Code,Title,Unit\n1,1,EGR 101,Math,2\n'
        mock_file = mock_open(read_data=template_content)
        with patch("builtins.input", return_value="A"):
            with patch("builtins.open", mock_file), patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
                self.converter.convert_complete_template("template_file")
        self.assertEqual(self.converter.buffer, [{"Year": "1", "Semester": "1", "Code": "EGR 101", "Title": "Math", "Unit": "2", "Grade": "A"}])
        self.assertEqual(self.converter.data, {"Year 1": {"semester 1": {"EGR 101": {"title": "Math", "unit": "2", "grade": "A"}}}})
        self.assertEqual(mock_stdout.getvalue(), "Data has been written to template_file\n")

    def test_write_to_file(self):
        self.converter.buffer = [{'Year': '1', 'Semester': '1', 'Code': 'EGR 101', 'Title': 'Math', 'Unit': '2', 'Grade': 'A'}]
        template_content = 'Year,Semester,Code,Title,Unit,Grade\n1,1,EGR 101,Math,2,A\n'
        mock_file = mock_open(read_data=template_content)
        mock_file.replace = mock_open(read_data=template_content)
        with patch("builtins.open", mock_file), patch("sys.stdout", new_callable=io.StringIO) as mock_obj:
            self.converter._write_to_file(mock_file)
        self.assertEqual(self.converter.buffer, [{"Year": "1", "Semester": "1", "Code": "EGR 101", "Title": "Math", "Unit": "2", "Grade": "A"}])
        self.assertEqual(self.converter.data, {"Year 1": {"semester 1": {"EGR 101": {"title": "Math", "unit": "2", "grade": "A"}}}})

    def test_write_to_file_exists(self):
        self.converter.buffer = [{"Year": "1", "Semester": "1", "Code": "C001", "Title": "Math", "Unit": "3", "Grade": "A"}]
        with patch("sys.stdout", new_callable=io.StringIO), patch("builtins.open", create=True) as mock_open:
            self.converter._write_to_file("output.csv")
            mock_open.assert_any_call("output.csv", "w+", newline="")

    def test_write_to_json(self):
        self.converter.data = {"Year 1": {"semester 1": {"C001": {"title": "Math", "unit": "3", "grade": "A"}}}}
        with patch("sys.stdout", new_callable=io.StringIO), patch("builtins.open", create=True) as mock_open:
            self.converter._write_to_json("output.json")
        mock_open.assert_called_once_with("output.json", "w")

    def tearDown(self) -> None:
        if os.path.exists("output.json"):
            os.remove("output.json")

        if os.path.exists("output.csv"):
            os.remove("output.csv")


class DataConverterResultCheckerIntegrationTest(unittest.TestCase):
    def setUp(self):
        self.filename = 'test_txt.csv'
        self.converter = DataConverter()

    def test_convert_from_raw_template(self):
        with patch("sys.stdout", new_callable=io.StringIO), patch("builtins.input", return_value="A"):
            self.converter.convert_raw_template(self.filename)
        expected_buffer = [{'Year': '1', 'Semester': '1', 'Code': 'EGR 101', 'Title': 'Introduction to Engineering', 'Unit': '2', 'Grade': 'A'}, {'Year': '1', 'Semester': '1', 'Code': 'CHM 101', 'Title': 'Basic Principles of Chemistry', 'Unit': '2', 'Grade': 'A'}, {'Year': '1', 'Semester': '1', 'Code': 'CHM 171', 'Title': 'Basic Practical Chemistry', 'Unit': '2', 'Grade': 'A'}, {'Year': '1', 'Semester': '2', 'Code': 'EGR 102', 'Title': 'Applied Mechanics', 'Unit': '3', 'Grade': 'A'}, {'Year': '1', 'Semester': '2', 'Code': 'MTH 122', 'Title': 'Elementary Mathematics III', 'Unit': '3', 'Grade': 'A'}]
        expected_data = {'Year 1': {'semester 1': {'EGR 101': {'title': 'Introduction to Engineering', 'unit': '2', 'grade': 'A'}, 'CHM 101': {'title': 'Basic Principles of Chemistry', 'unit': '2', 'grade': 'A'}, 'CHM 171': {'title': 'Basic Practical Chemistry', 'unit': '2', 'grade': 'A'}}, 'semester 2': {'EGR 102': {'title': 'Applied Mechanics', 'unit': '3', 'grade': 'A'}, 'MTH 122': {'title': 'Elementary Mathematics III', 'unit': '3', 'grade': 'A'}}}}
        self.assertListEqual(self.converter.buffer, expected_buffer)
        self.assertDictEqual(self.converter.data, expected_data)
        self.assertTrue(os.path.exists("A.json"))
        self.assertTrue(os.path.exists("A.csv"))

        cgpa_data = CGPAChecker(self.converter)
        self.assertEqual(cgpa_data.retrieve_CGPA(), 5)

    def tearDown(self) -> None:
        if os.path.exists("A.csv"):
            os.remove("A.csv")
        if os.path.exists("A.json"):
            os.remove("A.json")
