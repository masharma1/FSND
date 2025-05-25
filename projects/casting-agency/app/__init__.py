import os
from flask import Flask, jsonify
import requests
from flask_migrate import Migrate
from app.models import db
from flask_cors import CORS
from app.models import setup_db
from app.errors import register_error_handlers
from app.routes.actors import actors_blueprint
from app.routes.movies import movies_blueprint
from flask import request

def create_app(test_config=None):
    # Create and configure the Flask application
    app = Flask(__name__)
    
    # Setup database
    setup_db(app)
    
    # Enable CORS
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,PATCH,OPTIONS')
        return response
    
    # Initialize Flask-Migrate
    migrate = Migrate(app, db)

    # Register blueprints
    app.register_blueprint(actors_blueprint)
    app.register_blueprint(movies_blueprint)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Base route for API status
    @app.route('/')
    def get_status():
        return jsonify({
            'success': True,
            'message': 'Casting Agency API is running!'
        })

    @app.route('/login')
    def login_callback():
        code = request.args.get('code')
        if not code:
            return "No code provided", 400
        
        # Exchange code for token
        token_url = f'https://dev-vaa4tqxczeu26tio.us.auth0.com/oauth/token'
        payload = {
            'grant_type': 'authorization_code',
            'client_id': 'JYmMAdwbqYZZWfe6bh7eKtPFqqefm5YL',
            'client_secret': 'FgRcQez24xZIhNj5Ncg5Zua0DFbG5MwX8XEzYZvWfCugaP8GmMMoU4n_bjambAdC',
            'code': code,
            'redirect_uri': 'http://127.0.0.1:5000/login'
        }
        headers = {'Content-Type': 'application/json'}
        
        response = requests.post(token_url, json=payload, headers=headers)
        token_data = response.json()
        
        # Display the token
        return f"""
        <h1>Token Retrieved</h1>
        <p>Access Token: {token_data.get('access_token')}</p>
        <p>ID Token: {token_data.get('id_token')}</p>
        """
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)