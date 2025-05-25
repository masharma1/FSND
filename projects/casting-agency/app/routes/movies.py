from flask import Blueprint, jsonify, request, abort
from app.models import Movie
from app.auth import requires_auth
from datetime import datetime

movies_blueprint = Blueprint('movies', __name__)

@movies_blueprint.route('/movies', methods=['GET'])
@requires_auth('get:movies')
def get_movies(payload):
    """
    Get all movies
    Permission: 'get:movies'
    """
    try:
        movies = Movie.query.all()
        formatted_movies = [movie.format() for movie in movies]
        
        return jsonify({
            'success': True,
            'movies': formatted_movies
        }), 200
    except Exception as e:
        abort(500)


@movies_blueprint.route('/movies/<int:movie_id>', methods=['GET'])
@requires_auth('get:movies')
def get_movie(payload, movie_id):
    """
    Get a specific movie by ID
    Permission: 'get:movies'
    """
    movie = Movie.query.get(movie_id)
    
    if not movie:
        abort(404)
    
    return jsonify({
        'success': True,
        'movie': movie.format()
    }), 200


@movies_blueprint.route('/movies', methods=['POST'])
@requires_auth('post:movies')
def create_movie(payload):
    """
    Create a new movie
    Permission: 'post:movies'
    """
    body = request.get_json()
    
    if not body:
        abort(400)
    
    title = body.get('title')
    release_date_str = body.get('release_date')
    
    if not title or not release_date_str:
        abort(400)
    
    try:
        # Parse the date string to a date object
        release_date = datetime.strptime(release_date_str, '%Y-%m-%d').date()
        
        movie = Movie(title=title, release_date=release_date)
        
        # Add actors if provided
        if 'actors' in body and isinstance(body['actors'], list):
            from app.models import Actor
            actors = Actor.query.filter(Actor.id.in_(body['actors'])).all()
            movie.actors = actors
        
        movie.insert()
        
        return jsonify({
            'success': True,
            'created': movie.id,
            'movie': movie.format()
        }), 201
    except ValueError:
        # Date format error
        abort(400)
    except Exception as e:
        abort(422)


@movies_blueprint.route('/movies/<int:movie_id>', methods=['PATCH'])
@requires_auth('patch:movies')
def update_movie(payload, movie_id):
    """
    Update an existing movie
    Permission: 'patch:movies'
    """
    movie = Movie.query.get(movie_id)
    
    if not movie:
        abort(404)
    
    body = request.get_json()
    
    if not body:
        abort(400)
    
    if 'title' in body:
        movie.title = body['title']
    
    if 'release_date' in body:
        try:
            release_date = datetime.strptime(body['release_date'], '%Y-%m-%d').date()
            movie.release_date = release_date
        except ValueError:
            abort(400)
    
    # Update actors if provided
    if 'actors' in body and isinstance(body['actors'], list):
        from app.models import Actor
        actors = Actor.query.filter(Actor.id.in_(body['actors'])).all()
        movie.actors = actors
    
    try:
        movie.update()
        
        return jsonify({
            'success': True,
            'updated': movie.id,
            'movie': movie.format()
        }), 200
    except Exception as e:
        abort(422)


@movies_blueprint.route('/movies/<int:movie_id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movie(payload, movie_id):
    """
    Delete a movie
    Permission: 'delete:movies'
    """
    movie = Movie.query.get(movie_id)
    
    if not movie:
        abort(404)
    
    try:
        movie_id = movie.id
        movie.delete()
        
        return jsonify({
            'success': True,
            'deleted': movie_id
        }), 200
    except Exception as e:
        abort(422)