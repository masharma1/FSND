from app import app
from app.models import db, Actor, Movie
from datetime import date

with app.app_context():
    # Create actors
    actor1 = Actor(name='Brad Pitt', age=59, gender='Male')
    actor2 = Actor(name='Meryl Streep', age=74, gender='Female')
    actor3 = Actor(name='Tom Hanks', age=67, gender='Male')
    
    # Create movies  
    movie1 = Movie(title='The Color Purple', release_date=date(1985, 12, 20))
    movie2 = Movie(title='Forrest Gump', release_date=date(1994, 7, 6))
    
    # Add to database
    db.session.add_all([actor1, actor2, actor3, movie1, movie2])
    db.session.commit()
    print('Database seeded successfully!')