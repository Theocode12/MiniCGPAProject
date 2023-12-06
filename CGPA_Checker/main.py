if __name__ == "__main__":
    # Implement how you would like to check your CGPA
    from models.result_checker import CGPAChecker
    from models.data_converter import DataConverter

    cgpa_data = DataConverter()
    cgpa_data.convert_complete_template("vals_grade.csv")

    cgpa_checker = CGPAChecker(cgpa_data)
    print("\n\nYour CGPA is {}".format(cgpa_checker.retrieve_CGPA()))
