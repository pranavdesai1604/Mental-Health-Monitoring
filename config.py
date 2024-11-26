import os
import pickle

# Fetch environment variables for database connection
DB_CONFIG = {
    'user': os.getenv('DB_USER', 'root'),  # Default to 'root' if not set
    'password': os.getenv('DB_PASSWORD', 'root@123'),  # Default password for local testing
    'host': os.getenv('DB_HOST', '127.0.0.1'),  # Default to localhost for local testing
    'database': os.getenv('DB_NAME', 'mental_health_db')  # Default database name
}

# Function to load the model when needed
def load_model():
    model_path = os.getenv('MODEL_PATH', '/opt/render/project/src/models/mood_predictor.pkl')  # Use environment variable if set, else default path
    with open(model_path, 'rb') as model_file:
        return pickle.load(model_file)
