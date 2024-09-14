from flask import Flask # Import the Flask class from the flask module, which is the main class of the Flask framework

# import blueprints
from process_navigator import home
# create a create_app function that initializes the Flask application, we can add other logic depending on set up

def create_app():
    app = Flask(__name__) # Create an instance of the Flask class and assign it to the variable app
    app.config['SECRET_KEY'] = 'dev' # Set the secret key of the app to 'dev'

    # register blueprints
    app.register_blueprint(home.bp)
    
    return app