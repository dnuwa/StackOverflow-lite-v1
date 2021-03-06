# StackOverflow-lite-v1         [![Build Status](https://travis-ci.org/dnuwa/StackOverflow-lite-v1.svg?branch=develop)](https://travis-ci.org/dnuwa/StackOverflow-lite-v1)           [![Coverage Status](https://coveralls.io/repos/github/dnuwa/StackOverflow-lite-v1/badge.svg?branch=develop)](https://coveralls.io/github/dnuwa/StackOverflow-lite-v1?branch=develop)          [![Maintainability](https://api.codeclimate.com/v1/badges/435ecbae727fc0572738/maintainability)](https://codeclimate.com/github/dnuwa/StackOverflow-lite-v1/maintainability)       
StackOverflow-lite is a platform where people can ask questions and provide answers. 

### Installation and Set Up

Clone the repo from GitHub:

```
https://github.com/dnuwa/StackOverflow-lite-v1.git
```
Create a virtual environment and activate it.
```
virtualenv venv
venv\Scripts\activate
```

Install necessary requirements
```
pip install -r requirements.txt
```

Run unit tests
```
pytest test_api.py
```

### Running the application on a local machine

Test to see how the end points work

### API Endpoints

| Resource URL | Methods | Description | Requires Token |
| -------- | ------------- | --------- |--------------- |
| `/api/v1/auth/signup` | `POST, GET`  | Post new user and get all users | `FALSE` |
| `/api/v1/auth/login` | `POST`  | User Login | `FALSE` |
| `/api/v1/questions` | `GET, POST` | Add & Fetch questions | `TRUE` |
| `/api/v1/questions/<questionId>` | `GET, DELETE` | Manipulate a single question | `TRUE` |
| `/api/v1/questions/<questionId>/answers` | `POST` | Add an answer | `TRUE` |
| `/api/v1/questions/<questionId>/answers/<answerId>/edit` | `PUT` | Edit an answer | `TRUE` |
| `/api/v1/questions/<questionId>/answers/<ananswerId>/preffered` | `PUT` | Mark an Answer as Preferred | `TRUE` |

### inputs
```
sign up -> {"display_name": "","email": "","password": ""}
login -> {"display_name": "","password": ""}
post a question -> {"question": "" }
post an answer -> {"answer": ""}
edit an answer -> {"answer": ""}
```

### Running api tests
***
install postgre sql
create database test_db
set testing environment by using the command --> set APP_SETTINGS=testing
run nosetests

****

Everything set! :+1: - you are good togo! :shipit:
