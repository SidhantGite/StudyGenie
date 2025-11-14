# MCQ Generator with Gemini LangChain
A Streamlit-based application that generates Multiple Choice Questions (MCQs) from a given PDF or text file using the Gemini LangChain.

## Table of Contents
1. `Introduction`
2. `Features`
3. `Requirements`
4. `Usage`
5. `Code Structure`
6. `Contributing`
7. `License`

## Introduction
This project aims to simplify the process of generating MCQs from a given text or PDF file. Using the Gemini LangChain, we can create a chain of tasks that can analyze the input text and generate relevant MCQs. The application is built using Streamlit, making it easy to use and deploy.

## Features
- Upload a PDF or text file to generate MCQs
- Specify the number of MCQs to generate
- Choose the subject and complexity level of the questions
- Review the generated MCQs and their answers

## Requirements
- Python 3.8+
- Streamlit
- Gemini LangChain
- dotenv for environment variable management
- pandas for data manipulation

## Usage
1. Clone the repository: git clone https://github.com/sudeepjoelbayyee/MCQ-Generator-Using-Gemini
2. Install the required dependencies: 
3. Run the application: streamlit run app.py
4. Upload a PDF or text file, specify the number of MCQs, subject, and complexity level
5. Click "Create MCQs" to generate the questions

## Code Structure
- app.py: The main application file
- utils.py: Utility functions for reading files and generating table data
- mcq_generator.py: The Gemini LangChain implementation for generating MCQs
- response.json: A sample response file for testing purposes

## Contributing
Contributions are welcome! If you'd like to contribute to this project, please fork the repository and submit a pull request with your changes.

License
This project is licensed under the MIT License. See the LICENSE file for details.
