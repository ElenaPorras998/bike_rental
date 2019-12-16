from flask import render_template, Blueprint
from flask_login import login_required
from .models import Bicycles
from . import db

# Define the main blueprint
main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    return render_template('index.html')


@main.route('/coordinates')
@login_required
def coordinates():
    # Retrieve all the bicycles from the database and pass them to an html page.
    coordinates = Bicycles.query.all()
    return render_template('coordinates.html', locations=coordinates)
