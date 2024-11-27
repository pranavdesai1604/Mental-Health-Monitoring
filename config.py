import os
import pickle

# Fetch environment variables for database connection from Clever Cloud
DB_CONFIG = {
    'user': os.getenv('MYSQL_ADDON_USER', 'uquaijjll5pkweqk'),  # Default to the Clever Cloud user
    'password': os.getenv('MYSQL_ADDON_PASSWORD', '4Boi0J3HVPqukEKl6xxZ'),  # Default password for the database
    'host': os.getenv('MYSQL_ADDON_HOST', 'b6wf7qtmlju0b7jgmngz-mysql.services.clever-cloud.com'),  # Host from Clever Cloud
    'database': os.getenv('MYSQL_ADDON_DB', 'b6wf7qtmlju0b7jgmngz'),  # Database name from Clever Cloud
    'port': os.getenv('MYSQL_ADDON_PORT', '3306')  # Port number (default MySQL port)
}
# Path to the trained machine learning model
MODEL_PATH = os.getenv('MODEL_PATH', 'models/mood_predictor.pkl')

# Load the model using the path defined above
try:
    with open(MODEL_PATH, 'rb') as model_file:
        model = pickle.load(model_file)
except FileNotFoundError:
    print(f"Error: Model file not found at {MODEL_PATH}")
    raise  # Re-raise the error for logging
