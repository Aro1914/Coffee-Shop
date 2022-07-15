import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)
# BASE_URL = '/api/v1.0'
# CORS(app, resources={r"{BASE_URL}/*": {"origins": "*"}})


# @app.after_request
# def after_request(response):
#     response.headers.add(
#         "Access-Control-Allow-Headers", "Content-Type, Authorization, true"
#     )
#     response.headers.add(
#         "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE"
#     )
# return response


error = 0


def set_error(code):
    global error
    error = code


def get_error():
    global error
    return error


'''
@TODO uncomment the following line to initialize the database
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this function will add one
'''
#db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks')
def get_drinks():
    set_error(500)
    try:
        drinks = Drink.query.all()
        if drinks is None:
            set_error(404)
            raise

        s_drinks = [drink.short() for drink in drinks]

        return jsonify({
            'success': True,
            'drinks': s_drinks,
        })
    except:
        abort(get_error())


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail():
    set_error(500)
    try:
        drinks = Drink.query.all()
        if drinks is None:
            set_error(404)
            raise

        l_drinks = [drink.long() for drink in drinks]

        return jsonify({
            'success': True,
            'drinks': l_drinks,
        })
    except:
        abort(get_error())


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink():
    set_error(500)
    try:
        try:
            set_error(400)
            if not 'title' in request.get_json() or not 'recipe' in request.get_json():
                set_error(422)
                raise
            incoming_title = request.get_json()['title']
            incoming_recipe = request.get_json()['recipe']
            if incoming_title == '' or len(incoming_recipe) == 0:
                set_error(422)
                raise
        except:
            raise

        query_drink = Drink.query.filter(
            Drink.title.ilike(str(incoming_title))).first()

        if query_drink is None:
            try:
                drink = Drink(title=incoming_title,
                              recipe=json.dumps(incoming_recipe))
                drink.insert()
            except:
                set_error(500)
        else:
            set_error(409)
            raise

        return jsonify({
            'success': True,
            'drinks': [drink.long()],
        })
    except:
        abort(get_error())


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def edit_drink(id):
    # This sets the status code to 500 in the event of any unhandled errors
    set_error(500)
    try:
        # This attempts to retrieve the requested drink to be updated from the database
        drink = Drink.query.filter(Drink.id == id).one_or_none()
        # If the drink does not exist then a 404 error is thrown
        if drink is None:
            set_error(404)
            raise
        '''
        Variables to store the incoming title, and recipe are declared 
        regardless of if they do exist in the request body
        '''
        incoming_title = None
        incoming_recipe = None
        # Boolean variables to hold the occurrence of the title or recipe in the request body
        has_title = 'title' in request.get_json()
        has_recipe = 'recipe' in request.get_json()
        '''
        Attempt to assign the values from the request body properties 
        to the variables that will be used in the update
        '''
        try:
            '''
            This sets the status code to 400 in the event the title cannot be 
            parsed to string or the recipe cannot be converted to a list
            '''
            set_error(400)
            '''
            Check to see if either title or recipe was present in the request body
            properties, if neither were present then a 422 status code is returned 
            indicating that the request cannot be processed
            '''
            if not (has_title or has_recipe):
                set_error(422)
                raise
            '''
            If the title was present, the value is assigned to a variable that will
            be used for update
            '''
            if has_title:
                incoming_title = str(request.get_json()['title'])
            '''
            If the recipe was present, the value is assigned to a variable that will
            be used for update
            '''
            if has_recipe:
                incoming_recipe = json.dumps(
                    request.get_json()['recipe'])
        except:
            raise
        '''
        This attempts to retrieve a drink with the title in the request body this is
        to ensure that the update would not result in a conflict with a title of 
        another drink to enforce uniqueness of drink titles
        '''
        query_drink = Drink.query.filter(
            Drink.title.ilike(str(incoming_title))).first()
        '''
        This validates that no other drink has a title as the one in the request body
        else the title is the same as the one for the drink with ID provided to be
        updated that way a conflict would not arise as the title would be unchanged
        after the update 
        '''
        if query_drink is None or query_drink.title == drink.title:
            try:
                # If the title was provided then the drink's title is updated
                if has_title:
                    drink.title = incoming_title
                # If the recipe was provided then the drink's recipe is updated
                if has_recipe:
                    drink.recipe = incoming_recipe
                # The changes are effected to the database
                drink.update()
            except:
                raise
        else:
            set_error(409)
            raise
        # The result of the request is sent back to the client
        return jsonify({
            'success': True,  # Indicating the request was processed successfully
            # The full representation of the updated drink
            'drinks': [drink.long()],
        })
    except:
        '''
        The current status code is aborted depending on which part of the 
        endpoint encountered an error or did not pass a condition
        '''
        abort(get_error())


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(id):
    set_error(500)
    try:
        drink = Drink.query.filter(Drink.id == id).one_or_none()
        if drink is None:
            set_error(404)
            raise

        drink.delete()

        return jsonify({
            'success': True,
            'delete': id,
        })
    except:
        abort(get_error())

# Error Handling


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''


@app.errorhandler(400)
def bad_request(error):
    return (
        jsonify(
            {
                "success": False,
                "error": 400,
                "message": "bad request",
            }
        ),
        400,
    )


'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''


@app.errorhandler(404)
def not_found(error):
    return (
        jsonify(
            {
                "success": False,
                "error": 404,
                "message": "resource not found",
            }
        ),
        404,
    )


@app.errorhandler(405)
def method_not_allowed(error):
    return (
        jsonify(
            {
                "success": False,
                "error": 405,
                "message": "method not allowed"
            }
        ),
        405,
    )


@app.errorhandler(409)
def conflict(error):
    return (
        jsonify(
            {
                "success": False,
                "error": 409,
                "message": "conflict",
            }
        ),
        409,
    )


@app.errorhandler(422)
def unprocessable(error):
    return (
        jsonify(
            {
                "success": False,
                "error": 422,
                "message": "unprocessable",
            }
        ),
        422,
    )


@app.errorhandler(500)
def internal_server_error(error):
    return (
        jsonify(
            {
                "success": False,
                "error": 500,
                "message": "internal server error"
            }
        ),
        500,
    )


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''


@app.errorhandler(AuthError)
def auth_error(error):
    return (
        jsonify(
            {
                'success': False,
                'error': error.status_code,
                'message': error.error['description']
            }
        ),
        error.status_code,
    )
