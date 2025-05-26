import os
import click
from flask import Flask
from flask.cli import with_appcontext
from flask_migrate import Migrate, upgrade
from datetime import date

from app import app
from app.models import db, Actor, Movie

migrate = Migrate(app, db)

@app.cli.command()
@with_appcontext
def seed():
    """Seeds the database with initial data"""
    # Create actors
    actor1 = Actor(name='Brad Pitt', age=59, gender='Male')
    actor2 = Actor(name='Meryl Streep', age=74, gender='Female')
    actor3 = Actor(name='Tom Hanks', age=67, gender='Male')
    actor4 = Actor(name='Viola Davis', age=58, gender='Female')
    
    # Create movies
    movie1 = Movie(title='The Color Purple', release_date=date(1985, 12, 20))
    movie2 = Movie(title='Forrest Gump', release_date=date(1994, 7, 6))
    movie3 = Movie(title='The Devil Wears Prada', release_date=date(2006, 6, 30))
    
    # Add to database
    db.session.add_all([actor1, actor2, actor3, actor4, movie1, movie2, movie3])
    db.session.commit()
    
    # Create relationships
    movie1.actors.extend([actor2, actor4])
    movie2.actors.append(actor3)
    movie3.actors.append(actor2)
    db.session.commit()
    
    print('Database seeded successfully!')

@app.cli.command()
@with_appcontext
def drop_and_create_all():
    """Drops and creates fresh database tables"""
    from app.models import db_drop_and_create_all
    db_drop_and_create_all()
    print('Database reset complete!')

if __name__ == '__main__':
    app.run()