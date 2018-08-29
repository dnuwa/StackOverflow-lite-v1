# StackOverflow-lite-v1         [![Build Status](https://travis-ci.org/dnuwa/StackOverflow-lite-v1.svg?branch=develop)](https://travis-ci.org/dnuwa/StackOverflow-lite-v1)           [![Coverage Status](https://coveralls.io/repos/github/dnuwa/StackOverflow-lite-v1/badge.svg?branch=master)](https://coveralls.io/github/dnuwa/StackOverflow-lite-v1?branch=develop)          [![Maintainability](https://api.codeclimate.com/v1/badges/435ecbae727fc0572738/maintainability)](https://codeclimate.com/github/dnuwa/StackOverflow-lite-v1/maintainability)       
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

| Resource URL | Methods | Description | Requires Token | Inputs |
| -------- | ------------- | --------- |--------------- |
| `/api/v1/auth/signup` | `POST, GET`  | Post new user and get all users | `FALSE` |{"display_name": "","email": "","password": ""}|
| `/api/v1/auth/login` | `POST`  | User Login | `FALSE` |{"display_name": "","password": ""}|
| `/api/v1/questions` | `GET, POST` | Add & Fetch questions | `TRUE` |{"question": "" }|
| `/api/v1/questions/<questionId>` | `GET, DELETE` | Manipulate a single question | `TRUE` |
| `/api/v1/questions/<questionId>/answers` | `POST` | Add an answer | `TRUE` |{"answer": ""}|
| `/api/v1/questions/<questionId>/answers/<answerId>` | `PUT` | Edit an answer | `TRUE` |{ "answer": "" }|
| `/api/v1/questions/<qn_Id>/answers/<ans_id>` | `PUT` | Mark an Answer as Preferred | `TRUE` |