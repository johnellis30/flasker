
from email.policy import default
from urllib import request
from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.widgets import TextArea

# Create a Flask Instance
app = Flask(__name__)
# Add Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:FOotball30!@localhost/users'
# Secret Key
app.config['SECRET_KEY'] = "my super secret key"
# Initialize Database
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Create Blog Post Model
class Blogs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    author = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    slug = db.Column(db.String(255))

# Create a Blog form
class BlogForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = StringField("Content", validators=[DataRequired()], widget=TextArea()) 
    author = StringField("Author", validators=[DataRequired()])  
    slug = StringField("Slug", validators=[DataRequired()]) 
    submit = SubmitField("Submit") 

#Add list of blog posts
@app.route('/blogs')
def blogs():
    #grab all of the blog posts
    blogs = Blogs.query.order_by(Blogs.date_posted)
    return render_template("blogs.html", blogs=blogs)

#Add list of blog posts
@app.route('/blogs/<int:id>')
def blog(id):
    #grab all of the blog posts
    blog = Blogs.query.get_or_404(id)
    return render_template("blog.html", blog=blog)

#Add Blog Post Page
@app.route('/add-blog', methods=['GET', 'POST'])
def add_blog():
    form = BlogForm()
    
    if form.validate_on_submit():
        blog = Blogs(title=form.title.data,
            content=form.content.data,
            author=form.author.data,
            slug=form.slug.data)

        #clear the form    
        form.title.data = ''
        form.content.data = ''
        form.author.data = ''
        form.slug.data = ''

        #add form data to db
        db.session.add(blog)
        db.session.commit()

        flash("Congrats, you've submitted a Blog Post!")

    # Redirect to the webpage
    return render_template("add_blog.html", form=form)
        

# JSON Example
@app.route('/date')
def get_current_date():
    return {"Date": date.today()}

# Create Users Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    favorite_color = db.Column(db.String(120))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    #Password stuff
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Create A String
    def __repr__(self):
        return '<Name %r>' % self.name

# Update database record
@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    name = None
    form = UserForm()

    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User Deleted Successfully!")

        our_users = Users.query .order_by(Users.date_added)
        return render_template("add_user.html",
            form=form,
            name=name,
            our_users=our_users)

    except:
        flash("Whoops! There was a problem deleting the user.")
        return render_template("add_user.html",
            form=form,
            name=name,
            our_users=our_users)

# Create User Form Class
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo("password_hash2", message="Passwords must match")])
    password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])
    favorite_color = StringField("Favorite Color")
    submit = SubmitField("Submit")


# Update database record
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favorite_color = request.form['favorite_color']
        try:
            db.session.commit()
            flash("User Updated Succesfully!")
            return render_template("update.html",
                form=form,
                name_to_update=name_to_update)
        except:
            flash("Error! Try Again")
            return render_template("update.html",
                form=form,
                name_to_update=name_to_update)
    else:
        return render_template("update.html",
                form=form,
                name_to_update=name_to_update,
                id = id)



# Create a Form Class
class NamerForm(FlaskForm):
    name = StringField("What's Your Name", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Create a Password Form Class
class PasswordForm(FlaskForm):
    email = StringField("What's Your Email", validators=[DataRequired()])
    password_hash = PasswordField("What's Your Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

# Create index route decorator
@app.route('/')

def index():
    first_name = "John"
    stuff = "This is bold text!"

    favorite_pizza = ["Pepperoni", "Cheese", "Mushrooms", 41]
    return render_template("index.html", 
        first_name=first_name, 
        stuff=stuff,
        favorite_pizza=favorite_pizza)

# User profile page
@app.route('/user/<name>')

def user(name):
    return render_template("user.html", name=name)

# Name form page
@app.route('/name', methods=['GET', 'POST'])

def name():
    name = None
    form = NamerForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form Submitted Successfully")
    return render_template("name.html",
        name=name,
        form=form)



# Name form page
@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            # Hash Password
            hashed_pw=generate_password_hash(form.password_hash.data, "sha256")
            user = Users(name=form.name.data, 
            email=form.email.data, 
            favorite_color=form.favorite_color.data,
            password_hash=hashed_pw)
            
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.password_hash.data = ''
        form.favorite_color.data = ''
        flash("User Successfully Added")
    our_users = Users.query .order_by(Users.date_added)
    return render_template("add_user.html",
        form=form,
        name=name,
        our_users=our_users)

# def add_user():
#     name = None
#     form = UserForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form Submitted Successfully")
#     return render_template("name.html",
#         name=name,
#         form=form)



# Invalid URL Error
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 404



# Test PW form page
@app.route('/test_pw', methods=['GET', 'POST'])

def test_pw():
    email = None
    password = None
    pw_to_check = None
    user_to_check = None
    passed = None
    form = PasswordForm()

    #validate the form
    if form.validate_on_submit():
        email = form.email.data
        password = form.password_hash.data

        form.email.data = ''
        form.password_hash.data = ''

        #Looked up user by email address
        pw_to_check = Users.query.filter_by(email=email).first()

        #Check the hashed password
        passed = check_password_hash(pw_to_check.password_hash, password)

        #flash("Submitted Successfully")
    return render_template("test_pw.html",
        email=email,
        password=password,
        pw_to_check=pw_to_check,
        passed = passed,
        form=form)
