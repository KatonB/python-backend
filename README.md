# Python Backend Project

This project contains various algorithms implemented in Python. Each homework (`hw1`, `hw2`, `hw3`, etc.) contains 
different sets of algorithms and their corresponding tests.

## Project Structure
```
├─.github/: 
│   └── workflows/: Contains GitHub Actions workflows.
│       └── ci.yml: GitHub Actions CI workflow.
├─ hw1/: Contains the first set of algorithms and their tests.
│   └── main.py: Implementation of the algorithms.
│   └── tests.py: Unit tests for the algorithms.
│   └── requirements.txt: Dependencies for the hw1.
├─ hw2/: ...
│ ...
├─ hwN/: ...
├─ .gitignore: Git ignore file.
├─ README.md: Project documentation.
```

## Setup

1. Clone the repository:
    ```sh
    git clone <git@github.com:KatonB/python-backend.git>
    cd python-backed
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
   
3. Install the required dependencies for specific homework (N = 1 or 2 or 3 etc.):
    ```sh
    pip install -r hwN/requirements.txt
    ```

## Running Scripts

### Homework 1
Run the following command to start the server:
   ```sh
   python3 hw1/main.py
   ```
Then, open your browser and navigate to `http://127.0.0.1:8000/method?n=value` where `value` is the number you want 
to calculate the `method={factorial or fibonacci}` for and use RESTClient or Postman to test the mean with JSON data
(ex. [1,2,3]).