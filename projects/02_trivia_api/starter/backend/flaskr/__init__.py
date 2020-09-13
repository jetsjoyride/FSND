import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    # app = Flask(__name__, instance_relative_config=True)
    app = Flask(__name__)
    app.config.from_object('config')

    setup_db(app)

    '''
    DONE!  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    '''
    # Setup CORS
    # Basic way to Setup:
    # CORS(app)
    # Setup with specific configurations:
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    '''
    DONE!  @TODO: Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response


    def pagination(request, data):
        # Set default to first page if not input
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        return data[start:end]

    '''
    DONE!  @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    '''
    @app.route('/categories', methods=['GET'])
    @cross_origin()  ## Enables CORS on this specific endpoint
    def get_categories():
        try:
            status = 200
            # categories = Category.query.all()
            # formatted_categories = [category.format() for category in categories]

            categories = {}
            for category in Category.query.all():
                categories[category.id] = category.type

            if len(categories) == 0:
                status = 404
        except:
            abort(422)

        if status == 404:
            abort(404)
        else:
            return jsonify({
                'status_code': status,
                'success': True,
                'categories': categories
                })


    '''
    DONE!  @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    '''

    @app.route('/questions', methods=['GET'])
    @cross_origin()  ## Enables CORS on this specific endpoint
    def get_questions():
        try:
            status = 200
            questions = Question.query.all()
            formatted_questions = [question.format() for question in questions]
            paged_data = pagination(request, formatted_questions)

            if len(paged_data) == 0:
                status = 404

            categories = {}
            for category in Category.query.all():
                categories[category.id] = category.type

        except:
            abort(422)

        if status == 404:
            abort(404)
        else:
            return jsonify({
                'status_code': 200,
                'success': True,
                'total_questions': len(questions),
                'questions': paged_data,
                'categories': categories,
                'current_category': None # Category.query.first().type
                })

    '''
    DONE!  @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    '''

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    @cross_origin()  ## Enables CORS on this specific endpoint
    def delete_question(question_id):
        try:
            status = 200
            question = Question.query.filter(Question.id==question_id).one_or_none()

            question.delete()

            return jsonify({
                'status_code': 200,
                'success': True,
                'deleted': question_id,
                })

        except:
            abort(422)


    '''
    DONE!  @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    '''

    '''
    DONE!  @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''

    @app.route('/questions', methods=['POST'])
    @cross_origin()  ## Enables CORS on this specific endpoint
    def add_a_question():
        status = 200
        body = request.get_json()

        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_difficulty = body.get('difficulty', None)
        new_category = body.get('category', None)
        search = body.get('searchTerm', None)

        try:
            if search:
                selection = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(search)))

                formatted_questions = [question.format() for question in selection]

                # throw error is no questions based on search term - that way GUI has positive empty response
                if len(formatted_questions) == 0:
                    status = 404

                categories = {}
                for category in Category.query.all():
                    categories[category.id] = category.type

            else:
                # Verify all the input is provided
                if new_question is None:
                    abort(422)
                if new_answer is None:
                    abort(422)
                if new_difficulty is None:
                    abort(422)
                if new_category is None:
                    abort(422)

                question = Question(question=new_question, answer=new_answer, difficulty=int(new_difficulty), category_id=new_category)
                question.insert()

                return jsonify({
                    'status_code': 200,
                    'success': True,
                    'created': question.id,
                    })

        except:
            abort(422)

        if search:
            if status == 200:
                return jsonify({
                    'status_code': 200,
                    'success': True,
                    'total_questions': len(formatted_questions),
                    'questions': formatted_questions,
                    'categories': categories, # does not seem used . . . by QuestionView.js line 94
                    'current_category': None # Category.query.first().type
                    })
            else:
                # return not found
                abort(404)


    '''
    DONE!  @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    @cross_origin()  ## Enables CORS on this specific endpoint
    def get_questions_in_a_category(category_id):
        try:
            status = 200
            questions = Question.query.filter(Question.category_id==category_id).all()
            formatted_questions = [question.format() for question in questions]
            paged_data = pagination(request, formatted_questions)

            if len(paged_data) == 0:
                status = 404

            categories = {}
            for category in Category.query.all():
                categories[category.id] = category.type

        except:
            abort(422)

        if status == 404:
            abort(404)
        else:
            return jsonify({
                'status_code': 200,
                'success': True,
                'total_questions': len(questions),
                'questions': paged_data,
                'categories': categories,
                'current_category': Category.query.get(category_id).type
                })



    '''
    DONE!  @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    '''


    @app.route('/quizzes', methods=['POST'])
    @cross_origin()  ## Enables CORS on this specific endpoint
    def play_trivia():
        status = 200
        body = request.get_json()

        previous_questions = body.get('previous_questions', None)
        quiz_category = body.get('quiz_category', None)

        try:
            # get questions associated to category
            if quiz_category:
                questions = Question.query.filter(Question.category_id==quiz_category).all()
            else:
                questions = Question.query.all()

            # make an array of valid questions to randomly choose from
            possible_questions = []
            if previous_questions:
                for question in questions:
                    if question.id not in previous_questions:
                        possible_questions.append(question.id)
            # run more efficiently in no previous questions
            else:
                for question in questions:
                    possible_questions.append(question.id)

            # abort if there are no more valid questions to return (meaning that all questions have been played)
            if len(possible_questions) == 0:
                abort(422)

            # select a random possible question and format for json use
            question = Question.query.filter(Question.id==random.choice(possible_questions)).first().format()

            return jsonify({
                'status_code': 200,
                'success': True,
                'question': question,
                })

        except:
            # if category ID is blank - abort with 422 - unprocessable
            abort(422)

    '''
    DONE!   @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify ({
            "success": False,
            "error": 404,
            "message": "resource not found",
            }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify ({
            "success": False,
            "error": 422,
            "message": "unprocessable",
            }), 422

    return app
