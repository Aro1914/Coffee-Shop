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

'''
@TODO uncomment the following line to initialize the database
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this function will add one
'''
db_drop_and_create_all()

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
    drinks = Drink.query.all()
    s_drinks = [drink.short() for drink in drinks]

    return jsonify({
        'success': True, 
        'drinks': s_drinks,
    })

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
    drinks = Drink.query.all()
    l_drinks = [drink.long() for drink in drinks]

    return jsonify({
        'success': True,
        'drinks': l_drinks,
    })

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks')
@requires_auth('post:drinks')
def create_drink():
    body = json.loads(request)
    # Pending




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
@app.route('/drinks/<id>')
@requires_auth('patch:drinks')
def edit_drink(id):
    drink = Drink.query.filter(Drink.id == id).one_or_none()
    drink.title = request.get_json['title']
    drink.recipe = request.get_json['recipe']
    drink.update()

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
@app.route('/drinks/<id>')
@requires_auth('delete:drinks')
def delete_drink(id):
    drink = Drink.query.filter(Drink.id == id).one_or_none()
    drink.delete()

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
