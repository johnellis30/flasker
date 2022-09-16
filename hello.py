from flask import Flask, render_template

#Create a Flask Instance
app = Flask(__name__)


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


# Invalid URL Error
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 404


