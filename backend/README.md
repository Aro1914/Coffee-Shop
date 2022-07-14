# Coffee Shop Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=api.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## API EndPoints

### Get Drinks

`GET '/drinks'`

Fetches a lists of drinks - Available to the public and users with Barista or Manager roles.

- Request Arguments: None
- Returns: An object with the following properties:
  - `success`: A boolean representing the status of the result of the request.
  - `drinks`: An array of objects with the following properties:
    - `id`: The ID of the drink.
    - `title`: The title of the drink.
    - `recipe`: An array of objects with the following properties:
      - `color`: A color in string format.
      - `parts`: An integer representing the distribution.

Example Response:

```json
{
  "success": true,
  "drinks": [
   {
      "id": 1,
      "title": "Water",
      "recipe": [
         {
            "color": "blue",
            "parts": 1
         },
      ]
   },
  ]
}
```

### Get Drink Detail

`GET '/drink-details'`

Fetches a list of drinks with the names of their ingredients - Available only to users with Barista or Manager roles.

- Returns: An object with the following properties:
  - `success`: A boolean representing the status of the result of the request.
  - `drinks`: An array of object(s) with the following properties:
    - `id`: The ID of the drink.
    - `title`: The title of the drink.
    - `recipe`: An array of objects with the following properties:
      - `name`: The name of the ingredient.
      - `color`: A color in string format.
      - `parts`: An integer representing the distribution.

Example Response:

```json
{
  "success": true,
  "drinks": [
   {
      "id": 1,
      "title": "Water",
      "recipe": [
         {
            "name": "water",
            "color": "blue",
            "parts": 1
         },
      ]
   },
  ]
}
```

### Delete Drink

`DELETE '/drinks/<int:id>'`

Deletes a drink - Available only to users with Manager roles.

- Request Arguments: None
- Returns: An object with the following properties:
  - `success`: A boolean representing the status of the result of the request.
  - `delete`: A integer representing the ID of the deleted drink.

Example Response:

```json
{
  "success": true,
  "delete": 0,
}
```

### Update Drink

`PATCH '/drinks/<int:id>'`

Update a drink - Available only to users with Manager roles.

- Request Arguments: None
- Request Body Properties:
  - `title`: The question
  - `recipe`: An array of object(s) with the following properties:
    - `name`: The name of the ingredient.
    - `color`: A color in string format.
    - `parts`: An integer representing the distribution.
- Returns: An object with the following properties:
  - `recipe`: HTTP status code
  - `success`: A boolean representing the status of the result of the request.
  - `drink`: An array with a single object representing the updated drink with the following properties:
    - `id`: The ID of the drink.
    - `title`: The title of the drink.
    - `recipe`: An array of objects with the following properties:
      - `name`: The name of the ingredient.
      - `color`: A color in string format.
      - `parts`: An integer representing the distribution.

Example Response:

```json
{
  "success": true,
  "drink": [
   {
      "id": 1,
      "title": "Water",
      "recipe": [
         {
            "name": "water",
            "color": "blue",
            "parts": 1
         },
      ]
   }
  ]
}
```

### Create a new Drink

`POST '/drinks'`

Creates a new drink - Available only to users with Manager roles.

- Request Arguments: None
- Request Body Properties:
  - `title`: The question
  - `recipe`: An array of object(s) with the following properties:
    - `name`: The name of the ingredient.
    - `color`: A color in string format.
    - `parts`: An integer representing the distribution.
- Returns: An object with the following properties:
  - `recipe`: HTTP status code
  - `success`: A boolean representing the status of the result of the request.
  - `drink`: An array with a single object representing the newly created drink with the following properties:
    - `id`: The ID of the drink.
    - `title`: The title of the drink.
    - `recipe`: An array of objects with the following properties:
      - `name`: The name of the ingredient.
      - `color`: A color in string format.
      - `parts`: An integer representing the distribution.
  
Example Response:

```json
{
  "status_code": 201,
  "success": true,
  "message": "created"
}
```

## Errors

The following are the mostly likely errors that can occur when making requests:

### Bad Request

This could be as a result of passing:

- Empty or incomplete body parameters
- Invalid type of data

```json
{
  "success": false,
  "error": 400,
  "message": "bad request",
}
```

### Resource not Found

This means that no result could be found for the requested resource.

```json
{
  "success": false,
  "error": 404,
  "message": "resource not found",
}
```

### Method not Allowed

This is because no endpoint is specified for the specified method of request

```json
{
  "success": false,
  "error": 405,
  "message": "method not allowed"
}
```

### Conflict

This indicates that data requested to be created, already exists and as such would cause a conflict if created.

```json
{
  "success": false,
  "error": 409,
  "message": "conflict",
}
```

### Unprocessable Entity

This indicates that a request passed an empty value.

Example Request Body:

```json
{
  "title": ""
}
```

Example Response:

```json
{
  "success": false,
  "error": 422,
  "message": "unprocessable",
}
```

### Internal Server error

This indicates that the server encountered an error on attempt to process the request.
> _Notice_: If this is encountered, please create an issue on this repo and give a detailed description of events leading up to the error.

Example Response:

```json
{
  "success": false,
  "error": 500,
  "message": "internal server error"
}
```

### Authentication and Authorization Errors

These are the most likely errors you may come across relating to Authentication and Authorization.

#### 401 Errors

Header related Errors:

```json
{
  "success": false,
  "error": 401,
  "message": "Authorization header is expected.",
}
```

```json
{
  "success": false,
  "error": 401,
  "message": "Authorization header must start with 'Bearer'.",
}
```

```json
{
  "success": false,
  "error": 401,
  "message": "Token not found.",
}
```

```json
{
  "success": false,
  "error": 401,
  "message": "Authorization header must be bearer token.",
}
```

```json
{
  "success": false,
  "error": 401,
  "message": "Authorization malformed.",
}
```

Permission related errors:

```json
{
  "success": false,
  "error": 400,
  "message": "Permissions not included in JWT.",
}
```

```json
{
  "success": false,
  "error": 403,
  "message": "Permission not found.",
}
```

Token related errors:

```json
{
  "success": false,
  "error": 401,
  "message": "Authorization malformed.",
}
```

```json
{
  "success": false,
  "error": 401,
  "message": "Incorrect claims. Please, check the audience and issuer.",
}
```

```json
{
  "success": false,
  "error": 400,
  "message": "Unable to find the appropriate key.",
}
```
