
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

@manager.command
def db_upgrade():
    """Apply database migrations"""
    upgrade()

@manager.command
def seed():
    """Seeds the database with initial data"""
    # Create actors
    actor1 = Actor(name='Brad Pitt', age=59, gender='Male')
    actor2 = Actor(name='Meryl Streep', age=74, gender='Female')
    actor3 = Actor(name='Tom Hanks', age=67, gender='Male')
    actor4 = Actor(name='Viola Davis', age=58, gender='Female')
    
    # Create movies
    movie1 = Movie(title='The Color Purple', release_date='1985-12-20')
    movie2 = Movie(title='Forrest Gump', release_date='1994-07-06')
    movie3 = Movie(title='The Devil Wears Prada', release_date='2006-06-30')
    
    # Add to database
    db.session.add_all([actor1, actor2, actor3, actor4, movie1, movie2, movie3])
    db.session.commit()
    
    # Create relationships
    movie1.actors.extend([actor2, actor4])
    movie2.actors.append(actor3)
    movie3.actors.append(actor2)
    db.session.commit()
    
    print('Database seeded successfully!')

@manager.command
def drop_and_create_all():
    """Drops and creates fresh database tables"""
    from app.models import db_drop_and_create_all
    db_drop_and_create_all()
    print('Database reset complete!')

if __name__ == '__main__':
    manager.run()