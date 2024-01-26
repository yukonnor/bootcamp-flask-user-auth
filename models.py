from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    with app.app_context():
        db.app = app
        db.init_app(app)
        db.create_all()

class User(db.Model):
    __tablename__ = 'users'

    username = db.Column(db.String(20),
                   primary_key=True,
                   nullable=False)

    password = db.Column(db.Text,  
                     nullable=False)
    
    email = db.Column(db.String(50),
                       nullable=False)

    first_name = db.Column(db.String(30),
                       nullable=False)

    last_name = db.Column(db.String(30),
                       nullable=False)

    def __repr__(self):
        u = self
        return f"<User username={u.username} first_name={u.first_name} last_name={u.last_name}>"
    
    @classmethod
    def register(cls, first_name, last_name, email, username, password):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(password)

        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        # return instance of user w/ hashed pwd
        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)


    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            # return user instance
            return user
        else:
            return False



                     



                     


