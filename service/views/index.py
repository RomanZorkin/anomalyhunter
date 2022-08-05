from flask import Blueprint, render_template

view = Blueprint('index', __name__)


@view.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
