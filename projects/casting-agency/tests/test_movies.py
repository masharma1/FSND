import json
import unittest
from app.models import Movie
from tests.test_base import CastingAgencyTestCase


class MovieEndpointTestCase(CastingAgencyTestCase):
    """Test case for the movie endpoints"""

    def test_get_movies_success(self):
        """Test successful retrieval of movies"""
        res = self.client().get('/movies', headers={
            'Authorization': f'Bearer {self.assistant_token}'
        })
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']) > 0)

    def test_get_movies_error_401(self):
        """Test error when retrieving movies without authentication"""
        res = self.client().get('/movies')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_create_movie_success(self):
        """Test successful movie creation"""
        res = self.client().post('/movies', 
            headers={'Authorization': f'Bearer {self.producer_token}'},
            json=self.new_movie
        )
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        
        # Verify the movie was created in the database
        with self.app.app_context():
            created_movie = Movie.query.get(data['created'])
            self.assertIsNotNone(created_movie)

    def test_create_movie_error_400(self):
        """Test error when creating movie with missing data"""
        res = self.client().post('/movies',
            headers={'Authorization': f'Bearer {self.producer_token}'},
            json={'title': 'Missing Data Movie'}  # Missing release_date
        )
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_create_movie_error_403(self):
        """Test error when creating movie with insufficient permissions"""
        res = self.client().post('/movies',
            headers={'Authorization': f'Bearer {self.director_token}'},
            json=self.new_movie
        )
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_update_movie_success(self):
        """Test successful movie update"""
        # Get an existing movie
        with self.app.app_context():
            movie = Movie.query.first()
            update_data = {
                'title': 'Updated Movie Title',
                'release_date': '2024-01-01'
            }
            
            res = self.client().patch(f'/movies/{movie.id}',
                headers={'Authorization': f'Bearer {self.director_token}'},
                json=update_data
            )
            data = json.loads(res.data)
            
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertEqual(data['updated'], movie.id)
            
            # Verify movie was updated
            updated_movie = Movie.query.get(movie.id)
            self.assertEqual(updated_movie.title, 'Updated Movie Title')

    def test_update_movie_error_404(self):
        """Test error when updating non-existent movie"""
        res = self.client().patch('/movies/9999',
            headers={'Authorization': f'Bearer {self.director_token}'},
            json={'title': 'Non-existent Movie'}
        )
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_movie_success(self):
        """Test successful movie deletion"""
        # Create a movie to delete
        with self.app.app_context():
            movie = Movie(title='Movie to Delete', release_date='2023-01-01')
            movie.insert()
        
            res = self.client().delete(f'/movies/{movie.id}',
                headers={'Authorization': f'Bearer {self.producer_token}'}
            )
            data = json.loads(res.data)
            
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertEqual(data['deleted'], movie.id)
            
            # Verify movie was deleted
            with self.app.app_context():
                deleted_movie = Movie.query.get(movie.id)
                self.assertIsNone(deleted_movie)

    def test_delete_movie_error_403(self):
        """Test error when deleting movie with insufficient permissions"""
        with self.app.app_context():
            movie = Movie.query.first()
            
            res = self.client().delete(f'/movies/{movie.id}',
                headers={'Authorization': f'Bearer {self.director_token}'}
            )
            data = json.loads(res.data)
            
            self.assertEqual(res.status_code, 403)
            self.assertEqual(data['success'], False)

    def test_delete_movie_error_404(self):
        """Test error when deleting non-existent movie"""
        res = self.client().delete('/movies/9999',
            headers={'Authorization': f'Bearer {self.producer_token}'}
        )
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)