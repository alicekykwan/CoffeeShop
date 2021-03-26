import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink, db
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
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks}
    where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks')
def show_drinks():
    drinks = Drink.query.all()
    if not drinks:
        abort(404)
    res = []
    for drink in drinks:
        res.append(drink.short())
    return jsonify({
        "success": True,
        "drinks": res
    })


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks}
    where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def show_drinks_detail(payload):
    drinks = Drink.query.all()
    if not drinks:
        abort(404)
    res = []
    for drink in drinks:
        res.append(drink.long())
    return jsonify({
        "success": True,
        "drinks": res
    })


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink}
     where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drink(payload):
    try:
        body = request.get_json()
        app.logger.error(body)
        newtitle = body.get('title', None)
        # app.logger.info(body.get('recipe'))
        newrecipe = json.dumps(body.get('recipe', None))
        app.logger.error(newrecipe)
        newDrink = Drink(title=newtitle, recipe=newrecipe)
        db.session.add(newDrink)
        db.session.commit()
        res_drink = [newDrink.long()]
        return jsonify({
            "success": True,
            "drinks": res_drink
        })

    except BaseException:
        abort(422)
    finally:
        db.session.close()


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink}
     where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def patch_drink(payload, id):
    drink = Drink.query.get(id)
    if not drink:
        abort(404)
    try:
        body = request.get_json()
        patched_title = body.get('title', None)
        if patched_title:
            drink.title = patched_title
        if body.get('recipe', None) is not None:
            patched_recipe = json.dumps(body.get('recipe'))
            drink.recipe = patched_recipe
        db.session.commit()
        res_drink = [drink.long()]
        return jsonify({
            "success": True,
            "drinks": res_drink
        })
    except BaseException:
        abort(422)
    finally:
        db.session.close()


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id}
     where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, id):
    drink = Drink.query.get(id)
    if not drink:
        abort(404)
    try:
        db.session.delete(drink)
        db.session.commit()
        return jsonify({
            "success": True,
            "delete": id
        })
    except BaseException:
        abort(422)
    finally:
        db.session.close()


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
# repeated TODO?

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''


@app.errorhandler(AuthError)
def auth_error(error):
    print(error)
    return jsonify({
        "success": False,
        "error": error.error['code'],
        "message": error.error['description']
    }), error.status_code
