from csv import DictReader, DictWriter, QUOTE_NONNUMERIC
from typing import List, Dict, Any, Union

class DataConverter:
    def __init__(self) -> None:
        self.data: Dict[str, Dict[str, Dict[str, Dict[str, Any]]]] = {}
        self.buffer: list = []

    def _update_data_structure(self, row) -> dict:
        """Changes a csv row representation to a desired representation which is add to the self.data attribute
        Args:
            row: Row representation of csv data"""
        formatted_data = {
            "Year {}".format(row.get("Year")): {
                "semester {}".format(row.get("Semester")): {
                    row.get("Code"): {
                        "title": row.get("Title"),
                        "unit": row.get("Unit"),
                        "grade": row.get("Grade"),
                    }
                }
            }
        }

        year: str
        semester: Dict[str, Dict[str, Dict[str, Any]]]
        year, semester = list(*formatted_data.items())
        if year in list(self.data.keys()):
            if list(semester.keys())[0] in list(self.data[year].keys()):
                semester, course = list(*semester.items())
                course_code, course_attr = list(*course.items())
                self.data[year][semester][course_code] = course_attr
            else:
                semester, course = list(*semester.items())
                self.data[year][semester] = course
        else:
            self.data[year] = semester
        return formatted_data

    def _validate_grade_input(self, msg: str) -> Union[str, None]:
        """
        Makes sure the grade give is valid.
        Args:
            msg: Prompt message
        """
        while True:
            grade = input(msg)
            if len(grade) < 1 or "A" <= grade.upper() <= "F":
                break
            else:
                print(
                    "Invalid input. Please enter a letter from A to F (case-insensitive)."
                )
        return grade.upper() if grade else None

    def convert_raw_template(self, template_file: str) -> None:
        """
        Uses the CSV template given to generate new data from your grade input to  write another CSV file and json file.
        Args:
            template_file: filename of the template

        The csv file must be in format
            Year,Semester,Code,Title,Unit
        """
        newfile = input("Please Input Name for new CSV file with grades:  ") + ".csv"
        with open(template_file, newline="") as csv_read:
            reader = DictReader(csv_read)
            print("Input Grades: ")
            for row in reader:
                grade = self._validate_grade_input("{}: ".format(row.get("Title")))
                row["Grade"] = grade
                self.buffer.append(row)
        self._write_to_file(newfile)

    def convert_complete_template(self, filename: str) -> None:
        """
        Use file which might contain grade information for some courses or all courses to generate
        required data and write to file. It used when update need to be made to a file
        Args:
            filename: csv file containing grade information
        """
        with open(filename, newline="") as csv_read:
            reader = DictReader(csv_read)
            for row in reader:
                if not row.get("Grade"):
                    row["Grade"] = self._validate_grade_input(
                        "{}: ".format(row.get("Title"))
                    )
                self.buffer.append(row)
        self._write_to_file(filename)

    def _write_to_file(self, filename: str) -> None:
        """
        Write new csv data to the file
        Args:
            filename: The name of the file to write to
        """
        with open(filename, "w+", newline="") as csv_write:
            fieldnames = ["Year", "Semester", "Code", "Title", "Unit", "Grade"]
            writer = DictWriter(csv_write, fieldnames=fieldnames)
            writer.writeheader()
            for row in self.buffer:
                writer.writerow(row)
                if not row["Grade"]:
                    row["Grade"] = None
                self._update_data_structure(row)
        self._write_to_json(filename.replace(".csv", ".json"))

    def _write_to_json(self, filename: str) -> None:
        """
        Write the new data in json format to a file
        Args:
            filename: name of json file to write to
        """
        import json

        # Write the data to the JSON file
        with open(filename, "w") as json_file:
            json.dump(self.data, json_file, indent=4)

        print(f"Data has been written to {filename}")


if __name__ == "__main__":
    converter = DataConverter()
    # converter.convert_raw_template("../test_txt.csv")
    converter.convert_complete_template("val.csv")
