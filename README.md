# coronavirus-tracker
A live tracker for the spread of COVID-19

![Quick example](https://github.com/rtedwards/coronavirus-tracker/blob/master/images/coronavirus-tracker.gif)

# Setup
### 1. Clone the repo

> git clone https://github.com/rtedwards/coronavirus-tracker  

### 2. Create Environment

> conda env create -f environment.yml

### 3. Create Database and Pull Data

> python -m coronavirus.db_utils.db_utils

### 4. Start Streamlit App

> streamlit run app.y

# Testing

To run all tests:  
> python -m unittest discover

To run tests separatly:  
> python -m unittest tests/db_tests/db_utils_tests.py