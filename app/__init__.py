from flask import Flask

app = Flask(__name__)

from app import views

app.register_blueprint(views.view_BP)
app.config['SECRET_KEY'] = 'secret'

# Import all local view files
