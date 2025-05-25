import json
import unittest
from app.models import Actor
from tests.test_base import CastingAgencyTestCase


class ActorEndpointTestCase(CastingAgencyTestCase):
    """Test case for the actor endpoints"""

    def test_get_actors_success(self):
        """Test successful retrieval of actors"""
        res = self.client().get('/actors', headers={
            'Authorization': f'Bearer {self.assistant_token}'
        })
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']) > 0)

    def test_get_actors_error_401(self):
        """Test error when retrieving actors without authentication"""
        res = self.client().get('/actors')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_create_actor_success(self):
        """Test successful actor creation"""
        res = self.client().post('/actors', 
            headers={'Authorization': f'Bearer {self.director_token}'},
            json=self.new_actor
        )
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        
        # Verify the actor was created in the database
        with self.app.app_context():
            created_actor = Actor.query.get(data['created'])
            self.assertIsNotNone(created_actor)

    def test_create_actor_error_400(self):
        """Test error when creating actor with missing data"""
        res = self.client().post('/actors',
            headers={'Authorization': f'Bearer {self.director_token}'},
            json={'name': 'Missing Data Actor'}  # Missing age and gender
        )
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_create_actor_error_403(self):
        """Test error when creating actor with insufficient permissions"""
        res = self.client().post('/actors',
            headers={'Authorization': f'Bearer {self.assistant_token}'},
            json=self.new_actor
        )
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_update_actor_success(self):
        """Test successful actor update"""
        # Get an existing actor
        with self.app.app_context():
            actor = Actor.query.first()
            update_data = {
                'name': 'Updated Actor Name',
                'age': 40
            }
            
            res = self.client().patch(f'/actors/{actor.id}',
                headers={'Authorization': f'Bearer {self.director_token}'},
                json=update_data
            )
            data = json.loads(res.data)
            
            self.assertEqual(res.status_code, 200)