#!/bin/python3
if __name__ == "__main__":
    # Implement how you would like to check your CGPA
    import os
    import sys

    curr_cwd = os.getcwd()
    sys.path.append(curr_cwd)

    from src.models.result_checker import CGPAChecker
    from src.models.data_converter import DataConverter


    cgpa_data = DataConverter()
    cgpa_data.convert_complete_template(curr_cwd + "/CGPA_Checker/vals_grade.csv")

    cgpa_checker = CGPAChecker(cgpa_data)
    print("\n\nYour CGPA is {}".format(cgpa_checker.retrieve_CGPA()))
