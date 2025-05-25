import json
import unittest
from tests.test_base import CastingAgencyTestCase
from app.models import Movie, Actor


class RBACTestCase(CastingAgencyTestCase):
    """Test case for Role-Based Access Control"""

    # Tests for Casting Assistant role
    def test_assistant_can_view_actors(self):
        """Test Casting Assistant can view actors"""
        res = self.client().get('/actors', headers={
            'Authorization': f'Bearer {self.assistant_token}'
        })
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']) > 0)

    def test_assistant_can_view_movies(self):
        """Test Casting Assistant can view movies"""
        res = self.client().get('/movies', headers={
            'Authorization': f'Bearer {self.assistant_token}'
        })
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']) > 0)

    def test_assistant_cannot_add_actor(self):
        """Test Casting Assistant cannot add actor"""
        res = self.client().post('/actors', 
            headers={'Authorization': f'Bearer {self.assistant_token}'},
            json=self.new_actor
        )
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_assistant_cannot_delete_movie(self):
        """Test Casting Assistant cannot delete movie"""
        with self.app.app_context():
            movie = Movie.query.first()
            
            res = self.client().delete(f'/movies/{movie.id}',
                headers={'Authorization': f'Bearer {self.assistant_token}'}
            )
            data = json.loads(res.data)
            
            self.assertEqual(res.status_code, 403)
            self.assertEqual(data['success'], False)

    # Tests for Casting Director role
    def test_director_can_add_actor(self):
        """Test Casting Director can add actor"""
        res = self.client().post('/actors', 
            headers={'Authorization': f'Bearer {self.director_token}'},
            json=self.new_actor
        )
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_director_can_delete_actor(self):
        """Test Casting Director can delete actor"""
        # Create an actor to delete
        with self.app.app_context():
            actor = Actor(name='Actor to Delete', age=45, gender='Male')
            actor.insert()
            
            res = self.client().delete(f'/actors/{actor.id}',
                headers={'Authorization': f'Bearer {self.director_token}'}
            )
            data = json.loads(res.data)
            
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertEqual(data['deleted'], actor.id)

    def test_director_can_update_movie(self):
        """Test Casting Director can update movie"""
        with self.app.app_context():
            movie = Movie.query.first()
            update_data = {
                'title': 'Updated By Director',
                'release_date': '2024-02-01'
            }
            
            res = self.client().patch(f'/movies/{movie.id}',
                headers={'Authorization': f'Bearer {self.director_token}'},
                json=update_data
            )
            data = json.loads(res.data)
            
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertEqual(data['updated'], movie.id)

    def test_director_cannot_add_movie(self):
        """Test Casting Director cannot add movie"""
        res = self.client().post('/movies', 
            headers={'Authorization': f'Bearer {self.director_token}'},
            json=self.new_movie
        )
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    # Tests for Executive Producer role
    def test_producer_can_add_movie(self):
        """Test Executive Producer can add movie"""
        res = self.client().post('/movies', 
            headers={'Authorization': f'Bearer {self.producer_token}'},
            json=self.new_movie
        )
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_producer_can_delete_movie(self):
        """Test Executive Producer can delete movie"""
        # Create a movie to delete
        with self.app.app_context():
            movie = Movie(title='Movie to Delete', release_date='2023-03-15')
            movie.insert()
            
            res = self.client().delete(f'/movies/{movie.id}',
                headers={'Authorization': f'Bearer {self.producer_token}'}
            )
            data = json.loads(res.data)
            
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertEqual(data['deleted'], movie.id)