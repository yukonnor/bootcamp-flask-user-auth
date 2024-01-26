"""
   User Feedback App utilizing bcrypt user auth.
   Note: As we're using the create_app() workaround run app with `python3 -m app`instead of using `flask run`. 
"""

from flask import Flask, request, render_template,  redirect, flash, session
from models import db, connect_db, User
from forms import RegisterUserForm, LoginUserForm

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
    def root():
        """User Feedback app's root URL. Redirects to /register."""
        
        return redirect('/register')
    
    @app.route('/register', methods=["GET", "POST"])
    def register():
        """Display user registration form and process form submission."""

        # instatiate an WTForm object
        form = RegisterUserForm()

        if form.validate_on_submit():
            
            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data
            username = form.username.data
            password = form.password.data

            new_user = User.register(first_name, last_name, email, username, password)
            db.session.add(new_user)
            
            try:
                db.session.commit()
            except IntegrityError:
                form.username.errors.append('Username taken.  Please pick another')
                return render_template('register.html', form=form)
            
            session['user_id'] = new_user.id
            
            flash('Welcome! Successfully Created Your Account!', "success")
            return redirect('/secret')
        else:
            return render_template('register.html', form=form)
    
    return app

if __name__ == '__main__':
    app = create_app('user_feedback', developing=True)
    app.app_context().push() # comment out when done testing
    connect_db(app)
    app.run(debug=True)      