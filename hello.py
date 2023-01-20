
from email.policy import default
from urllib import request
from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

# Create a Flask Instance
app = Flask(__name__)
# Add Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:FOotball30!@localhost/users'
# Secret Key
app.config['SECRET_KEY'] = "my super secret key"
# Initialize Database
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    favorite_color = db.Column(db.String(120))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

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
            user = Users(name=form.name.data, email=form.email.data, favorite_color=form.favorite_color.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
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


