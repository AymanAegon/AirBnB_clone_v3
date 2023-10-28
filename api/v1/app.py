from flask import Flask
from api.v1.views import app_views
from models import storage
from os import getenv
app = Flask(__name__)

# Register Blueprint
app.register_blueprint(app_views)

# Teardown app context to close the database connection
@app.teardown_appcontext
def teardown_db(exception):
    storage.close()

if __name__ == "__main__":
    # Get host and port from environment variables or use defaults
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(getenv('HBNB_API_PORT', 5000))
    
    # Run the Flask server
    app.run(host=host, port=port, threaded=True)

