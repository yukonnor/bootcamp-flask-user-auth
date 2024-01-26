"""
   User Feedback App utilizing bcrypt user auth.
   Note: As we're using the create_app() workaround run app with `python3 -m app`instead of using `flask run`. 
"""

from flask import Flask, request, render_template,  redirect, flash, session
from models import db, connect_db, User
from forms import TBD

def create_app(db_name, testing=False, developing=False):

    app = Flask(__name__)
    app.testing = testing
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql:///{db_name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']  =  False
    app.config['SECRET_KEY'] = "chickenzarecool21837"

    if developing: 
        app.config['SQLALCHEMY_ECHO'] =  True
        app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    @app.route('/')
    def home():
        """User Feedback app's home page."""
        
        return render_template('home.html')
    
    return app

if __name__ == '__main__':
    app = create_app('user_feedback', developing=True)
    app.app_context().push() # comment out when done testing
    connect_db(app)
    app.run(debug=True)      