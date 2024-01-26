"""Seed file to make sample data for Pet db."""

from models import db, connect_db, User, Feedback
from app import create_app

app = create_app('user_feedback', developing=True)
connect_db(app)

# Create all tables
with app.app_context():
    db.drop_all()
    db.create_all()

    # If table isn't empty, empty it
    User.query.delete()
    Feedback.query.delete()

    # Add users
    randy = User.register(username='RandyPops', first_name='Rand', last_name="Smith", email="test@example.com", password="password")
    cooper = User.register(username='Cooper', first_name='Coop', last_name="Smith", email="test@example.com", password="password")
    pasta = User.register(username='Pasta', first_name='Pasta', last_name="Smith", email="test@example.com", password="password")

    db.session.add_all([randy, cooper, pasta])
    db.session.commit()

    # Add feedback
    f1 = Feedback(title="Post 1", text="Test test test test", for_username="RandyPops", by_username="RandyPops")
    f2 = Feedback(title="Post 2", text="Test test test test", for_username="RandyPops", by_username="Pasta")
    f3 = Feedback(title="Post 3", text="Test test test test", for_username="Pasta", by_username="Pasta")
    f4 = Feedback(title="Post 4", text="Test test test test", for_username="Pasta", by_username="RandyPops")

    db.session.add_all([f1, f2, f3, f4])
    db.session.commit()

