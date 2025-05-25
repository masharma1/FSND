from flask import Blueprint, jsonify, request, abort
from app.models import Actor
from app.auth import requires_auth

actors_blueprint = Blueprint('actors', __name__)

@actors_blueprint.route('/actors', methods=['GET'])
@requires_auth('get:actors')
def get_actors(payload):
    """
    Get all actors
    Permission: 'get:actors'
    """
    try:
        actors = Actor.query.all()
        formatted_actors = [actor.format() for actor in actors]
        
        return jsonify({
            'success': True,
            'actors': formatted_actors
        }), 200
    except Exception as e:
        abort(500)


@actors_blueprint.route('/actors/<int:actor_id>', methods=['GET'])
@requires_auth('get:actors')
def get_actor(payload, actor_id):
    """
    Get a specific actor by ID
    Permission: 'get:actors'
    """
    actor = Actor.query.get(actor_id)
    
    if not actor:
        abort(404)
    
    return jsonify({
        'success': True,
        'actor': actor.format()
    }), 200


@actors_blueprint.route('/actors', methods=['POST'])
@requires_auth('post:actors')
def create_actor(payload):
    """
    Create a new actor
    Permission: 'post:actors'
    """
    body = request.get_json()
    
    if not body:
        abort(400)
    
    name = body.get('name')
    age = body.get('age')
    gender = body.get('gender')
    
    if not name or not age or not gender:
        abort(400)
    
    try:
        actor = Actor(name=name, age=age, gender=gender)
        actor.insert()
        
        return jsonify({
            'success': True,
            'created': actor.id,
            'actor': actor.format()
        }), 201
    except Exception as e:
        abort(422)


@actors_blueprint.route('/actors/<int:actor_id>', methods=['PATCH'])
@requires_auth('patch:actors')
def update_actor(payload, actor_id):
    """
    Update an existing actor
    Permission: 'patch:actors'
    """
    actor = Actor.query.get(actor_id)
    
    if not actor:
        abort(404)
    
    body = request.get_json()
    
    if not body:
        abort(400)
    
    if 'name' in body:
        actor.name = body['name']
    
    if 'age' in body:
        actor.age = body['age']
    
    if 'gender' in body:
        actor.gender = body['gender']
    
    try:
        actor.update()
        
        return jsonify({
            'success': True,
            'updated': actor.id,
            'actor': actor.format()
        }), 200
    except Exception as e:
        abort(422)


@actors_blueprint.route('/actors/<int:actor_id>', methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actor(payload, actor_id):
    """
    Delete an actor
    Permission: 'delete:actors'
    """
    actor = Actor.query.get(actor_id)
    
    if not actor:
        abort(404)
    
    try:
        actor_id = actor.id
        actor.delete()
        
        return jsonify({
            'success': True,
            'deleted': actor_id
        }), 200
    except Exception as e:
        abort(422)