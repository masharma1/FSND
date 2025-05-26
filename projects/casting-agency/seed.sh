heroku run python -c "
from app import app
with app.app_context():
    from app.models import db, Actor, Movie
    from datetime import date
    
    # Create actors
    actor1 = Actor(name='Brad Pitt', age=59, gender='Male')
    actor2 = Actor(name='Meryl Streep', age=74, gender='Female')
    
    # Create movies  
    movie1 = Movie(title='The Color Purple', release_date=date(1985, 12, 20))
    
    # Add to database
    db.session.add_all([actor1, actor2, movie1])
    db.session.commit()
    print('Seeding completed successfully!')
" --app casting-agency-final