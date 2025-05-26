Casting Agency API
Introduction
The Casting Agency API models a company that is responsible for creating movies and managing and assigning actors to those movies. This API allows casting assistants, casting directors, and executive producers to manage the database of movies and actors based on their assigned permissions.
Live URL
https://casting-agency-final.herokuapp.com/
Motivation
This project is the capstone project for the Udacity Full Stack Web Developer Nanodegree Program. It demonstrates the culmination of the skills learned throughout the program, including:

Database modeling with PostgreSQL & SQLAlchemy
API Development with Flask
Authentication and Role-Based Access Control (RBAC) with Auth0
Testing with unittest
Deployment on Heroku

Project Dependencies
Python 3.7 or later

Follow instructions to install the latest version of python for your platform in the python docs

PostgreSQL

Follow instructions to install PostgreSQL for your platform:

PostgreSQL Downloads



Virtual Environment

It's recommended to work within a virtual environment. This keeps your dependencies for each project separate and organized.
Instructions for setting up a virtual environment for your platform:
bashCopy# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# For Windows:
venv\Scripts\activate
# For MacOS/Linux:
source venv/bin/activate


PIP Dependencies

Install dependencies by running:
bashCopypip install -r requirements.txt


Local Development
Database Setup
With PostgreSQL running, create a database:
bashCopycreatedb casting_agency
Environment Variables
Set up the environment variables:
bashCopysource setup.sh

Note: You'll need to update the setup.sh file with your Auth0 credentials.

Running the Server
To run the server, execute:
bashCopy# Apply database migrations
python manage.py db upgrade

# Seed the database with initial data (optional)
python manage.py seed

# Run the Flask application
flask run
By default, the server will run on http://127.0.0.1:5000/.
API Reference
Authentication
This API uses Auth0 for authentication and implements Role-Based Access Control (RBAC).
Roles and Permissions

Casting Assistant

Can view actors and movies

get:actors
get:movies




Casting Director

All permissions a Casting Assistant has and...
Add or delete an actor from the database

post:actors
delete:actors


Modify actors or movies

patch:actors
patch:movies




Executive Producer

All permissions a Casting Director has and...
Add or delete a movie from the database

post:movies
delete:movies





Getting Started with Auth0
To set up authentication with Auth0, follow these steps:

Create a free account at Auth0
Create a new API:

API Name: Casting Agency API
Identifier: casting-agency-api


Define the following permissions:

get:actors
get:movies
post:actors
post:movies
patch:actors
patch:movies
delete:actors
delete:movies


Create the following roles and assign permissions:

Casting Assistant: get:actors, get:movies
Casting Director: All Casting Assistant permissions + post:actors, delete:actors, patch:actors, patch:movies
Executive Producer: All Casting Director permissions + post:movies, delete:movies


Update setup.sh with your Auth0 domain, API identifier, and client ID.

Error Handling
Errors are returned as JSON objects in the following format:
jsonCopy{
  "success": false,
  "error": 400,
  "message": "Bad request"
}
The API will return the following error types when requests fail:

400: Bad Request
401: Unauthorized
403: Forbidden
404: Resource Not Found
405: Method Not Allowed
422: Unprocessable Entity
500: Internal Server Error

Endpoints
GET /actors

General:

Returns a list of all actors
Requires get:actors permission


Sample request:
bashCopycurl -X GET https://your-app-name.herokuapp.com/actors \
  -H "Authorization: Bearer {ACCESS_TOKEN}"

Sample response:
jsonCopy{
  "success": true,
  "actors": [
    {
      "id": 1,
      "name": "Brad Pitt",
      "age": 59,
      "gender": "Male",
      "movies": [1, 3]
    },
    {
      "id": 2,
      "name": "Meryl Streep",
      "age": 74,
      "gender": "Female",
      "movies": [2]
    }
  ]
}


POST /actors

General:

Creates a new actor
Requires post:actors permission


Request body:
jsonCopy{
  "name": "Tom Holland",
  "age": 27,
  "gender": "Male"
}

Sample request:
bashCopycurl -X POST https://your-app-name.herokuapp.com/actors \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {ACCESS_TOKEN}" \
  -d '{"name": "Tom Holland", "age": 27, "gender": "Male"}'

Sample response:
jsonCopy{
  "success": true,
  "created": 5,
  "actor": {
    "id": 5,
    "name": "Tom Holland",
    "age": 27,
    "gender": "Male",
    "movies": []
  }
}


PATCH /actors/{actor_id}

General:

Updates an existing actor
Requires patch:actors permission


Request body (all fields optional):
jsonCopy{
  "name": "Tom Holland",
  "age": 28,
  "gender": "Male"
}

Sample request:
bashCopycurl -X PATCH https://your-app-name.herokuapp.com/actors/5 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {ACCESS_TOKEN}" \
  -d '{"age": 28}'

Sample response:
jsonCopy{
  "success": true,
  "updated": 5,
  "actor": {
    "id": 5,
    "name": "Tom Holland",
    "age": 28,
    "gender": "Male",
    "movies": []
  }
}


DELETE /actors/{actor_id}

General:

Deletes an actor
Requires delete:actors permission


Sample request:
bashCopycurl -X DELETE https://your-app-name.herokuapp.com/actors/5 \
  -H "Authorization: Bearer {ACCESS_TOKEN}"

Sample response:
jsonCopy{
  "success": true,
  "deleted": 5
}


GET /movies

General:

Returns a list of all movies
Requires get:movies permission


Sample request:
bashCopycurl -X GET https://your-app-name.herokuapp.com/movies \
  -H "Authorization: Bearer {ACCESS_TOKEN}"

Sample response:
jsonCopy{
  "success": true,
  "movies": [
    {
      "id": 1,
      "title": "The Color Purple",
      "release_date": "1985-12-20",
      "actors": [2, 4]
    },
    {
      "id": 2,
      "title": "Forrest Gump",
      "release_date": "1994-07-06",
      "actors": [3]
    }
  ]
}


POST /movies

General:

Creates a new movie
Requires post:movies permission


Request body:
jsonCopy{
  "title": "Spider-Man: Far From Home",
  "release_date": "2019-07-02",
  "actors": [5, 6]
}

Sample request:
bashCopycurl -X PATCH https://your-app-name.herokuapp.com/movies/4 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {ACCESS_TOKEN}" \
  -d '{"title": "Spider-Man: Far From Home", "release_date": "2019-07-02"}'

Sample response:
jsonCopy{
  "success": true,
  "updated": 4,
  "movie": {
    "id": 4,
    "title": "Spider-Man: Far From Home",
    "release_date": "2019-07-02",
    "actors": [5]
  }
}


DELETE /movies/{movie_id}

General:

Deletes a movie
Requires delete:movies permission


Sample request:
bashCopycurl -X DELETE https://your-app-name.herokuapp.com/movies/4 \
  -H "Authorization: Bearer {ACCESS_TOKEN}"

Sample response:
jsonCopy{
  "success": true,
  "deleted": 4
}


Testing
To run the tests, execute:
bashCopy# Set up the test database
dropdb casting_agency_test
createdb casting_agency_test

# Run tests
python -m unittest discover -v
The test suite includes:

Success behavior tests for each endpoint
Error behavior tests for each endpoint
RBAC tests for each role

Deployment
Heroku Deployment
To deploy this application to Heroku, follow these steps:

Install the Heroku CLI: Heroku CLI Installation
Login to Heroku:

bashCopyheroku login

Create a new Heroku app:

bashCopyheroku create your-app-name

Add Heroku PostgreSQL addon:

bashCopyheroku addons:create heroku-postgresql:hobby-dev --app your-app-name

Set environment variables:

bashCopyheroku config:set AUTH0_DOMAIN='your-auth0-domain.auth0.com' --app your-app-name
heroku config:set API_AUDIENCE='casting-agency-api' --app your-app-name
heroku config:set CLIENT_ID='your-client-id' --app your-app-name

Push to Heroku:

bashCopygit push heroku master

Run migrations:

bashCopyheroku run python manage.py db upgrade --app your-app-name

Seed the database (optional):

bashCopyheroku run python manage.py seed --app your-app-name
Authors

Your Name

Acknowledgements

The team at Udacity for the great Full Stack Web Developer Nanodegree Program
Auth0 for providing authentication services-Man: No Way Home",
"release_date": "2021-12-17",
"actors": [5]
}
Copy

Sample request:
bashCopycurl -X POST https://your-app-name.herokuapp.com/movies \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {ACCESS_TOKEN}" \
  -d '{"title": "Spider-Man: No Way Home", "release_date": "2021-12-17", "actors": [5]}'

Sample response:
jsonCopy{
  "success": true,
  "created": 4,
  "movie": {
    "id": 4,
    "title": "Spider-Man: No Way Home",
    "release_date": "2021-12-17",
    "actors": [5]
  }
}


PATCH /movies/{movie_id}

General:

Updates an existing movie
Requires patch:movies permission


Request body (all fields optional):
jsonCopy{
  "title": "Spider

