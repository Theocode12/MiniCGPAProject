# Academic Performance Tracker

This project serves as a user-friendly tool for effortless CGPA calculation and performance tracking throughout your academic journey in university or college. Designed with simplicity in mind, it allows you to update grades with a single click, view your CGPA instantly, and even make predictions about your final CGPA based on your current academic performance.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Tests](#Tests)
- [Contributions](#contributing)
- [License](#license)

## Installation

To install or get the code sample simply clone the repository using the following command
```bash
git clone https://github.com/Theocode12/MiniCGPAProject.git
```
## Usage
1 Input Grade Updates:
  - Utilize the provided DataConverter class to effortlessly convert raw CSV data containing course information and grades into a structured format.
  ```python
  Dc = DataConverter()
  Dc.convert_raw_template("template_course.csv")
  ```
CSV must be in the format :

```
Year,Semester,Code,Title,Unit
```
To run the main.py script make sure that the current directory is the project root folder and run
```bash
python3 CGPA_Checker/main.py
```

2 Track Your CGPA:
  - Leverage the CGPAChecker class to abstract CGPA calculations based on the converted data.
Retrieve CGPA for specific years and semesters, gaining insights into your academic performance.

3 Plan for the Future:
  - Easily predict your future CGPA based on your current grades, helping you plan and set academic goals.

## Features
+ Effortless Grade Updates: The project provides a seamless way to update grades, making the process quick and straightforward.

+ Real-time CGPA Monitoring: With just one click, you can instantly view your current CGPA, allowing you to stay informed about your academic standing.

+ Progress Predictions: The tool enables you to make predictions about your future CGPA as you progress through your academic journey, providing valuable insights into your potential academic outcomes.

## Test
To run test you must run command from project root directory :
```bash
	python3 -m unittest discover -s src
```
or
```bash
	python3 -m unittest discover
```

## Contributions
We welcome contributions to improve Academic Performance Tracker. Whether you want to fix a bug, implement a new feature, or suggest an enhancement, we appreciate your efforts.

Please follow these guidelines when contributing:

### How to Contribute
1. Fork the Repository: Fork the repository to your GitHub account.

1. Clone the Repository: Clone the forked repository to your local machine:
	```bash
	git clone https://github.com/Theocode12/MiniCGPAProject.git
	```

1. Create a Branch: Create a new branch for your contribution:
	```bash
	git checkout -b feature/your-feature
	```

1. Make Changes: Implement your changes or add new features.

1. Test Your Changes: Ensure that your changes do not break existing functionality.

1. Commit Your Changes: Commit your changes with a clear and concise commit message:
	```bash
	git commit -m "Your commit message here"
	```

1. Push Changes: Push your changes to your forked repository:
	```bash
	git push origin feature/your-feature
	```

1. Create a Pull Request: Open a pull request from your forked repository to the original repository.

### Code Style and Guidelines

- Follow the existing code style and guidelines used in the project.
- Maintain clear and concise code.
- Provide documentation for new features or changes when necessary.
- Reporting Issues
- If you encounter any issues or have suggestions for improvements, please create an issue in the repository.

### NOTE

Tests must be done for contributions to be accepted
