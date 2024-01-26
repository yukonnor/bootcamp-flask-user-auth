"""
   User Feedback App utilizing bcrypt user auth.
   Note: As we're using the create_app() workaround run app with `python3 -m app`instead of using `flask run`. 
"""

from flask import Flask, request, render_template,  redirect, flash, session
from models import db, connect_db, User, Feedback
from forms import RegisterUserForm, LoginUserForm, FeedbackForm

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
    
    @app.route('/users/<username>')
    def user_details(username):
        """A user details page that only logged in users should be able to access."""

        # Authorize whether requester can view page:
        if "username" not in session:
            flash("Please login first!", "danger")
            return redirect('/login')
        
        # Get user
        user = User.get_user(username)
        user_feedback = user.feedback_for_user
        
        return render_template('user-details.html', user=user, feedback=user_feedback)
    
    @app.route('/users/<username>/feedback/add', methods=["GET", "POST"])
    def add_feedback(username):
        """Display a 'leave feedback for user' form and process form submitssion."""

        # Authorize whether requester can view page:
        if "username" not in session:
            flash("Please login first!", "danger")
            return redirect('/login')
        
        # instatiate an WTForm object
        form = FeedbackForm()

        if form.validate_on_submit():
            
            title = form.title.data
            text = form.text.data

            by_username = session.get('username')

            feedback = Feedback(title=title, text=text, for_username=username, by_username=by_username)
            db.session.add(feedback)
            
            try:
                db.session.commit()
                flash(f"Feedback added for {username}!", "success")
            except:
                flash(f"Somethign went wrong :/  Please check logs.", "danger")
                return render_template('add-feedback.html', for_username=username, form=form)
            
            return redirect(f'/users/{username}')

        else:
            return render_template('add-feedback.html', for_username=username, form=form)
    
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
            
            session['username'] = new_user.username
            
            flash('Welcome! Successfully Created Your Account!', "success")
            return redirect(f'/users/{username}')
        else:
            return render_template('register.html', form=form)
        
    @app.route('/login', methods=["GET", "POST"])
    def login():
        """Display user log in form and process form submission."""

        # instatiate an WTForm object
        form = LoginUserForm()

        if form.validate_on_submit():
            
            username = form.username.data
            password = form.password.data

            user = User.authenticate(username, password)
            
            if user:
                flash(f"Welcome Back, {user.username}!", "success")
                session['username'] = user.username
                return redirect(f'/users/{username}')
            else:
                form.username.errors = ['Invalid username/password.']
        else:
            return render_template('login.html', form=form)
        
    @app.route('/logout', methods=["POST"])
    def logout():
        """Log out the user. Redirects to /."""

        session.pop('username')

        flash("See you next time!", "info")
        return redirect('/')
    
    return app

if __name__ == '__main__':
    app = create_app('user_feedback', developing=True)
    app.app_context().push() # comment out when done testing
    connect_db(app)
    app.run(debug=True)      