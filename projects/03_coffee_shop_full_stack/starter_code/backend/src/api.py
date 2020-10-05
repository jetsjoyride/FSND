import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
import sys

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()
# ROUTES
'''
DONE!! - @TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json
    {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['GET'])
@requires_auth('get:drinks')
def get_drinks(payload):
    try:
        drinks = Drink.query.all()
    except:
        abort(422)
    return jsonify({
        'status_code': 200,
        'success': True,
        'drinks': [drink.short() for drink in drinks]
    })


'''
DONE!! - @TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json
    {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    try:
        drinks = Drink.query.all()
    except:
        abort(422)
    return jsonify({
        'status_code': 200,
        'success': True,
        'drinks': [drink.long() for drink in drinks]
        })

'''
DONE!! - @TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json
    {"success": True, "drinks": drink} where drink an array containing
     only the newly created drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drinks(payload):
    # get body
    body = request.get_json()

    try:
        new_title = body.get('title', None)
        # Needs to be string with names in double quotes
        new_recipe = json.dumps(body['recipe'])

        # Verify all the input is provided
        if new_title is None:
            abort(422)
        if new_recipe is None:
            abort(422)

        drink = Drink(title=new_title, recipe=new_recipe)
        drink.insert()

        return jsonify({
            'status_code': 200,
            'success': True,
            'drinks': [drink.long()]
            })

    except:
        abort(422)

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json
    {"success": True, "drinks": drink} where
    drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def patch_drinks(payload, drink_id):
    body = request.get_json()

    try:
        # if invalid number abort 404
        try:
            drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
        except:
            abort(404)

        # Patch whichever keys are provided
        if "title" in body:
            drink.title = body.get('title', None)

        if "recipe" in body:
            drink.recipe = json.dumps(body['recipe'])

        drink.insert()

        return jsonify({
            'status_code': 200,
            'success': True,
            'drinks': [drink.long()]
            })

    except:
        abort(422)
        return 'Failed'


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json
    {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(payload, drink_id):
        try:
            status = 200

            try:
                drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
            except:
                abort(404)

            drink.delete()

        except:
            abort(422)

        return jsonify({
            'status_code': 200,
            'success': True,
            'delete': drink_id,
            })

# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False,
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''


@app.errorhandler(404)
def not_found(error):
    return jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404


'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
                    "success": False,
                    "error": 401,
                    "message": "unauthorized"
                    }), 401


@app.errorhandler(403)
def forbidden(error):
    return jsonify({
                    "success": False,
                    "error": 403,
                    "message": "forbidden"
                    }), 403

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''


@app.errorhandler(AuthError)
def process_AuthError(error):
    response = jsonify(error.error)
    response.status_code = error.status_code

    return response
