from flask import Blueprint

# Create the Blueprint instance
api = Blueprint('api', __name__)

# Import the routes to register them with the Blueprint
from .api import *

# If you have more route files, you can import them similarly
# from .another_module import *

# This makes sure the Blueprint is created and routes are registered when the package is imported
