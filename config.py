import os
import pickle

# Fetch environment variables for database connection
DB_CONFIG = {
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'root@123'),
    'host': os.getenv('DB_HOST', '127.0.0.1'),
    'database': os.getenv('DB_NAME', 'mental_health_db')
}

# Path to the trained machine learning model
MODEL_PATH = os.getenv('MODEL_PATH', 'models/mood_predictor.pkl')  # Default path if not set via env

# Load the model using the path defined above
with open(MODEL_PATH, 'rb') as model_file:
    model = pickle.load(model_file)
