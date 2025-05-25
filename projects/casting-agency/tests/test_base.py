import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from datetime import date

from app import create_app
from app.models import db, setup_db, Actor, Movie  # Make sure db is imported here


class CastingAgencyTestCase(unittest.TestCase):
    """Base test case for Casting Agency API tests"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        
        # Use a test database
        self.database_name = "casting_agency_test"
        self.database_path = f"postgresql://postgres:password@localhost:5432/{self.database_name}"
        
        # Update the database path without reinitializing
        with self.app.app_context():
            self.app.config["SQLALCHEMY_DATABASE_URI"] = self.database_path  # Changed from app to self.app
            db.create_all()
            # Add sample data
            self.create_sample_data()

        # Sample data for test cases
        self.new_actor = {
            'name': 'Test Actor',
            'age': 30,
            'gender': 'Male'
        }
        
        self.new_movie = {
            'title': 'Test Movie',
            'release_date': '2023-12-31'
        }
        
        # Auth tokens
        self.assistant_token = os.environ.get('CASTING_ASSISTANT_TOKEN', '')
        self.director_token = os.environ.get('CASTING_DIRECTOR_TOKEN', '')
        self.producer_token = os.environ.get('EXECUTIVE_PRODUCER_TOKEN', '')

    def tearDown(self):
        """Executed after each test"""
        pass

    def create_sample_data(self):
        """Create some sample data for testing"""
        try:
            # Create sample actors
            actor1 = Actor(name='John Doe', age=35, gender='Male')
            actor2 = Actor(name='Jane Smith', age=28, gender='Female')
            actor1.insert()
            actor2.insert()
            
            # Create sample movies
            movie1 = Movie(title='Sample Movie 1', release_date=date(2023, 1, 15))
            movie2 = Movie(title='Sample Movie 2', release_date=date(2023, 6, 30))
            movie1.insert()
            movie2.insert()
            
            # Add relationships
            movie1.actors.append(actor1)
            movie1.actors.append(actor2)
            movie2.actors.append(actor1)
            movie1.update()
            movie2.update()
            
        except Exception as e:
            print(f"Error creating sample data: {e}")