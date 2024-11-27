import os
import pickle

# Fetch environment variables for database connection
DB_CONFIG = {
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'root@123'),
    'host': os.getenv('DB_HOST', 'mental-health-db.render.com'),
    'database': os.getenv('DB_NAME', 'mental_health_db')
}

# Path to the trained machine learning model
MODEL_PATH = os.getenv('MODEL_PATH', '/opt/render/project/src/models/mood_predictor.pkl')

# Load the model using the path defined above
try:
    with open(MODEL_PATH, 'rb') as model_file:
        model = pickle.load(model_file)
except FileNotFoundError:
    print(f"Error: Model file not found at {MODEL_PATH}")
    raise  # Re-raise the error for logging
