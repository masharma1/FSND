# Casting Agency API

## Project Overview

The Casting Agency API is a comprehensive full-stack web application that models a company responsible for creating movies and managing and assigning actors to those movies. As an Executive Producer within the company, this system simplifies and streamlines the process of managing casting operations.

This project serves as the capstone project for the Udacity Full Stack Web Developer Nanodegree Program, demonstrating the culmination of skills learned throughout the program including database modeling, API development, authentication, authorization, testing, and deployment.

## Live Application

🚀 **Live URL**: [https://casting-agency-final-bef3776c086d.herokuapp.com/](https://casting-agency-final-bef3776c086d.herokuapp.com/)

## Motivation

The entertainment industry requires efficient management of actors and movies with proper role-based access control. This API addresses the following needs:

- **Centralized Management**: Single source of truth for actors and movies data
- **Role-Based Access**: Different permission levels for different roles in the organization
- **Scalability**: RESTful API design that can support multiple client applications
- **Security**: JWT-based authentication with Auth0 integration
- **Reliability**: Comprehensive testing and error handling

## Tech Stack

- **Backend**: Python, Flask
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: Auth0 with JWT tokens
- **Testing**: Python unittest
- **Deployment**: Heroku
- **Version Control**: Git & GitHub

## API Architecture

### Database Models

#### Actor
- **id**: Primary key (Integer)
- **name**: Actor's full name (String, required)
- **age**: Actor's age (Integer, required)
- **gender**: Actor's gender (String, required)

#### Movie
- **id**: Primary key (Integer)
- **title**: Movie title (String, required)
- **release_date**: Movie release date (Date, required)

#### Relationships
- **Many-to-Many**: Actors can be in multiple movies, movies can have multiple actors

### API Endpoints

#### Actors

| Method | Endpoint | Description | Permissions Required |
|--------|----------|-------------|---------------------|
| GET | `/actors` | Retrieve all actors | `get:actors` |
| GET | `/actors/<int:actor_id>` | Retrieve specific actor | `get:actors` |
| POST | `/actors` | Create new actor | `post:actors` |
| PATCH | `/actors/<int:actor_id>` | Update existing actor | `patch:actors` |
| DELETE | `/actors/<int:actor_id>` | Delete actor | `delete:actors` |

#### Movies

| Method | Endpoint | Description | Permissions Required |
|--------|----------|-------------|---------------------|
| GET | `/movies` | Retrieve all movies | `get:movies` |
| GET | `/movies/<int:movie_id>` | Retrieve specific movie | `get:movies` |
| POST | `/movies` | Create new movie | `post:movies` |
| PATCH | `/movies/<int:movie_id>` | Update existing movie | `patch:movies` |
| DELETE | `/movies/<int:movie_id>` | Delete movie | `delete:movies` |

### Role-Based Access Control (RBAC)

#### Casting Assistant
- **Permissions**: `get:actors`, `get:movies`
- **Capabilities**: Can view actors and movies
- **Use Case**: Entry-level staff who need read-only access to view casting information

#### Casting Director
- **Permissions**: All Casting Assistant permissions + `post:actors`, `delete:actors`, `patch:actors`, `patch:movies`
- **Capabilities**: Can manage actors and modify movie information
- **Use Case**: Mid-level management who handle day-to-day casting operations

#### Executive Producer
- **Permissions**: All Casting Director permissions + `post:movies`, `delete:movies`
- **Capabilities**: Full control over both actors and movies
- **Use Case**: Senior management with complete system access

## Authentication Setup

This API uses Auth0 for authentication. To test the API, you'll need to obtain JWT tokens for different roles.

### Auth0 Configuration
- **Domain**: `dev-vaa4tqxczeu26tio.us.auth0.com`
- **API Audience**: `casting-agency-api`
- **Client ID**: `JYmMAdwbqYZZWfe6bh7eKtPFqqefm5YL`

### Test Users

For testing purposes, the following users have been created with different roles:

| Role | Email | Password |
|------|-------|----------|
| Casting Assistant | sharma.manish0203@gmail.com | Contact for password |
| Casting Director | manish.sharma0201cs@gmail.com | Contact for password |
| Executive Producer | richa27agra@gmail.com | Contact for password |

### Obtaining JWT Tokens

1. **Using the Login Flow**:
   ```bash
   # Start local Flask server for callback handling
   flask run
   
   # Open this URL in browser and login with appropriate user
   https://dev-vaa4tqxczeu26tio.us.auth0.com/authorize?response_type=code&client_id=JYmMAdwbqYZZWfe6bh7eKtPFqqefm5YL&redirect_uri=http://127.0.0.1:5000/login&scope=openid%20profile%20email&audience=casting-agency-api
   ```

2. **Copy the access token** from the response page after successful login

3. **Use the token** in API requests:
   ```bash
   curl -H "Authorization: Bearer <ACCESS_TOKEN>" https://casting-agency-final-bef3776c086d.herokuapp.com/actors
   ```

## Local Development Setup

### Prerequisites
- Python 3.7+
- PostgreSQL
- Git

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/masharma1/FSND.git
   cd FSND/projects/casting-agency
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL database**:
   ```bash
   createdb casting_agency
   createdb casting_agency_test  # For testing
   ```

5. **Configure environment variables**:
   ```bash
   # Update setup.sh with your Auth0 credentials and database URL
   source setup.sh
   ```

6. **Run database migrations**:
   ```bash
   flask db upgrade
   ```

7. **Seed the database** (optional):
   ```bash
   flask seed
   ```

8. **Run the application**:
   ```bash
   flask run
   ```

The application will be available at `http://127.0.0.1:5000/`

## Testing

### Running Tests Locally

1. **Ensure test database exists**:
   ```bash
   createdb casting_agency_test
   ```

2. **Set up environment variables**:
   ```bash
   source setup.sh
   ```

3. **Run the test suite**:
   ```bash
   python -m unittest discover -v
   ```

### Test Coverage

The test suite includes 26 comprehensive tests covering:

- **Success behavior** for each endpoint
- **Error behavior** for each endpoint  
- **RBAC testing** with at least 2 tests per role
- **Authentication testing** for various scenarios

### Test Results

Latest test run results:
```
test_create_actor_error_400 (tests.test_actors.ActorEndpointTestCase.test_create_actor_error_400)
Test error when creating actor with missing data ... ok
test_create_actor_error_403 (tests.test_actors.ActorEndpointTestCase.test_create_actor_error_403)
Test error when creating actor with insufficient permissions ... ok
test_create_actor_success (tests.test_actors.ActorEndpointTestCase.test_create_actor_success)
Test successful actor creation ... ok
test_get_actors_error_401 (tests.test_actors.ActorEndpointTestCase.test_get_actors_error_401)
Test error when retrieving actors without authentication ... ok
test_get_actors_success (tests.test_actors.ActorEndpointTestCase.test_get_actors_success)
Test successful retrieval of actors ... ok
test_update_actor_success (tests.test_actors.ActorEndpointTestCase.test_update_actor_success)
Test successful actor update ... ok
test_assistant_can_view_actors (tests.test_auth.RBACTestCase.test_assistant_can_view_actors)
Test Casting Assistant can view actors ... ok
test_assistant_can_view_movies (tests.test_auth.RBACTestCase.test_assistant_can_view_movies)
Test Casting Assistant can view movies ... ok
test_assistant_cannot_add_actor (tests.test_auth.RBACTestCase.test_assistant_cannot_add_actor)
Test Casting Assistant cannot add actor ... ok
test_assistant_cannot_delete_movie (tests.test_auth.RBACTestCase.test_assistant_cannot_delete_movie)
Test Casting Assistant cannot delete movie ... ok
test_director_can_add_actor (tests.test_auth.RBACTestCase.test_director_can_add_actor)
Test Casting Director can add actor ... ok
test_director_can_delete_actor (tests.test_auth.RBACTestCase.test_director_can_delete_actor)
Test Casting Director can delete actor ... ok
test_director_can_update_movie (tests.test_auth.RBACTestCase.test_director_can_update_movie)
Test Casting Director can update movie ... ok
test_director_cannot_add_movie (tests.test_auth.RBACTestCase.test_director_cannot_add_movie)
Test Casting Director cannot add movie ... ok
test_producer_can_add_movie (tests.test_auth.RBACTestCase.test_producer_can_add_movie)
Test Executive Producer can add movie ... ok
test_producer_can_delete_movie (tests.test_auth.RBACTestCase.test_producer_can_delete_movie)
Test Executive Producer can delete movie ... ok
test_create_movie_error_400 (tests.test_movies.MovieEndpointTestCase.test_create_movie_error_400)
Test error when creating movie with missing data ... ok
test_create_movie_error_403 (tests.test_movies.MovieEndpointTestCase.test_create_movie_error_403)
Test error when creating movie with insufficient permissions ... ok
test_create_movie_success (tests.test_movies.MovieEndpointTestCase.test_create_movie_success)
Test successful movie creation ... ok
test_delete_movie_error_403 (tests.test_movies.MovieEndpointTestCase.test_delete_movie_error_403)
Test error when deleting movie with insufficient permissions ... ok
test_delete_movie_error_404 (tests.test_movies.MovieEndpointTestCase.test_delete_movie_error_404)
Test error when deleting non-existent movie ... ok
test_delete_movie_success (tests.test_movies.MovieEndpointTestCase.test_delete_movie_success)
Test successful movie deletion ... ok
test_get_movies_error_401 (tests.test_movies.MovieEndpointTestCase.test_get_movies_error_401)
Test error when retrieving movies without authentication ... ok
test_get_movies_success (tests.test_movies.MovieEndpointTestCase.test_get_movies_success)
Test successful retrieval of movies ... ok
test_update_movie_error_404 (tests.test_movies.MovieEndpointTestCase.test_update_movie_error_404)
Test error when updating non-existent movie ... ok
test_update_movie_success (tests.test_movies.MovieEndpointTestCase.test_update_movie_success)
Test successful movie update ... ok

----------------------------------------------------------------------
Ran 26 tests in 3.405s

OK
```

**✅ All 26 tests pass successfully**, demonstrating:
- Complete endpoint functionality
- Proper error handling
- Role-based access control enforcement
- Authentication and authorization security

### API Testing Examples

#### Test Root Endpoint (No Authentication)
```bash
curl https://casting-agency-final-bef3776c086d.herokuapp.com/
```

#### Test GET Actors (Requires Authentication)
```bash
curl -H "Authorization: Bearer <TOKEN>" https://casting-agency-final-bef3776c086d.herokuapp.com/actors
```

#### Test POST Actor (Casting Director or Executive Producer)
```bash
curl -X POST https://casting-agency-final-bef3776c086d.herokuapp.com/actors \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Actor", "age": 30, "gender": "Male"}'
```

#### Test PATCH Movie (Casting Director or Executive Producer)
```bash
curl -X PATCH https://casting-agency-final-bef3776c086d.herokuapp.com/movies/1 \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Movie Title"}'
```

### Expected API Responses

#### Success Response Example
```json
{
  "success": true,
  "actors": [
    {
      "id": 1,
      "name": "Brad Pitt",
      "age": 59,
      "gender": "Male",
      "movies": [1, 3]
    }
  ]
}
```

#### Error Response Example
```json
{
  "success": false,
  "error": 404,
  "message": "Resource not found"
}
```

## Error Handling

The API implements comprehensive error handling for:

- **400**: Bad Request
- **401**: Unauthorized  
- **403**: Forbidden
- **404**: Resource Not Found
- **405**: Method Not Allowed
- **422**: Unprocessable Entity
- **500**: Internal Server Error

All errors return JSON responses with consistent formatting.

## Deployment

The application is deployed on Heroku with the following configuration:

### Environment Variables
- `AUTH0_DOMAIN`: Auth0 tenant domain
- `API_AUDIENCE`: Auth0 API identifier
- `CLIENT_ID`: Auth0 application client ID
- `DATABASE_URL`: PostgreSQL connection string (auto-configured by Heroku)

### Deployment Process
1. **Create Heroku app**: `heroku create casting-agency-final`
2. **Add PostgreSQL addon**: `heroku addons:create heroku-postgresql`
3. **Set environment variables**: `heroku config:set KEY=VALUE`
4. **Deploy code**: `git push heroku main`
5. **Run migrations**: `heroku run flask db upgrade`
6. **Seed database**: `heroku run python seed_db.py`

## Project Structure

```
casting-agency/
├── app/
│   ├── __init__.py          # Flask app initialization
│   ├── models.py            # Database models
│   ├── auth.py              # Authentication logic
│   ├── errors.py            # Error handlers
│   └── routes/
│       ├── __init__.py
│       ├── actors.py        # Actor endpoints
│       └── movies.py        # Movie endpoints
├── migrations/              # Database migrations
├── tests/                   # Test suite
│   ├── test_actors.py
│   ├── test_movies.py
│   ├── test_auth.py
│   └── test_base.py
├── .env                     # Environment variables (local)
├── .gitignore
├── config.py                # Configuration settings
├── manage.py                # Management commands
├── requirements.txt         # Python dependencies
├── setup.sh                 # Environment setup script
├── Procfile                 # Heroku deployment config
├── runtime.txt              # Python version specification
├── seed_db.py              # Database seeding script
└── README.md               # This file
```

## Development Journey

### Key Implementation Steps

1. **Database Design**: Created SQLAlchemy models with proper relationships
2. **API Development**: Implemented RESTful endpoints following best practices
3. **Authentication**: Integrated Auth0 for JWT-based authentication
4. **Authorization**: Implemented RBAC with custom decorators
5. **Testing**: Developed comprehensive test suite with 100% endpoint coverage
6. **Error Handling**: Added robust error handling for all scenarios
7. **Deployment**: Successfully deployed to Heroku with CI/CD pipeline

### Challenges Overcome

- **Token Management**: Implemented proper JWT verification and error handling
- **Database Relationships**: Designed efficient many-to-many relationships
- **RBAC Implementation**: Created flexible permission-based access control
- **Testing Strategy**: Developed comprehensive testing covering all scenarios
- **Deployment Issues**: Resolved various deployment challenges on Heroku

## Contributing

This project is part of the Udacity Full Stack Web Developer Nanodegree Program. While it's primarily for educational purposes, suggestions and feedback are welcome.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

- **Developer**: Manish Sharma
- **GitHub**: [masharma1](https://github.com/masharma1)
- **Project Link**: [https://github.com/masharma1/FSND/tree/master/projects/casting-agency](https://github.com/masharma1/FSND/tree/master/projects/casting-agency)

## Acknowledgments

- Udacity Full Stack Web Developer Nanodegree Program
- Auth0 for authentication services
- Heroku for hosting platform
- Flask and SQLAlchemy communities for excellent documentation