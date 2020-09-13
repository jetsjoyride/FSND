# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql

1. In PSQL: create database trivia
2. In PSQL: create role caryn with superuser createdb login encrypted password 'caryn';
2. In Gitbash: psql -d trivia -1 -f trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle GET requests for all available categories.
4. Create an endpoint to DELETE question using a question ID.
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.
6. Create a POST endpoint to get questions based on category.
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422 and 500.

REVIEW_COMMENT

## API Definitions

### Base URL
At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend.

### Error Handling
Errors are returned as JSON objects in the following format:
> {\
"success": False,\
"error": 400,\
"message": "bad request"\
}

The API will return three error types when requests fail:
>    404: Resource Not Found\
    422: Not Processable

### GET '/categories'

General: Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
Request Arguments: Include a request argument to choose page number, starting from 1.
Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. Results are paginated in groups of 10.

Sample Command: curl -X "GET" http://127.0.0.1:5000/categories

Sample Response:
>{ "categories": [\
{"id": 1,\
"type": "Science"\
},\
{\
"id": 2,\
"type": "Art"\
  },\
],\
"success": true\
}

### GET '/categories/\<category_id\>/questions'

General: Fetches a dictionary of questions for a specific category.
Request Arguments: Valid category ID. Include a request argument to choose page number, starting from 1.\
Returns: Results are paginated in groups of 10.\

Sample Command: curl -X "GET" http://127.0.0.1:5000/categories/4/questions

Sample Response: same as GET '/questions' below

### GET '/questions'

  General: Fetches a dictionary of questions in which the keys are the ids and it contains information about the question, it's difficulty and category as well as a tuple of category id and type.\
  Request Arguments: Include a request argument to choose page number, starting from 1.\
  Returns: Results are paginated in groups of 10.\

  Sample Command: curl -X "GET" http://127.0.0.1:5000/questions

  Sample Response:
  >  { "categories": [\
      "1": "Science",\
      "2": "Art",\
      "3": "Geography",\
      "4": "History",\
      "5": "Entertainment",\
      "6": "Sports"\
    },\
    "current_category": null,\
    "questions": [\
      {\
        "answer": "Agra",\
        "category": 3,\
        "difficulty": 2,\
        "id": 15,\
        "question": "The Taj Mahal is located in which Indian city?"\
      },\
    {\
      "answer": "Blood",\
      "category": 1,\
      "difficulty": 4,\
      "id": 22,\
      "question": "Hematology is a branch of medicine involving the study of\ what?"\
    },\
    {\
      "answer": "Scarab",\
      "category": 4,\
      "difficulty": 4,\
      "id": 23,\
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"\
    }\
    ],\
    "status_code": 200,\
    "success": true,\
    "total_questions": 19\
    }

### DELETE '/questions/\<question_id\>'

General: Delete a specific question\
Request Arguments: Valid question ID.\
Returns: Confirmation response with deleted ID if successful

Sample Command: curl -X "DELETE" http://127.0.0.1:5000/questions/23

Sample Response:
>({ 'status_code': 200,\
   'success': True,\
   'deleted': 23,\
})


## Testing
To run the tests, run python test_flaskr.py

Pre-requisites:
It expects to have trivia_test database setup. This should be a copy of the trivia database (be sure to use flask db upgrade to get to the correct database version.)

Recommended setup from PSQL:
> dropdb trivia_test;\
  createdb trivia_test with template trivia;\

```
