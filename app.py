from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import pickle
from config import MODEL_PATH
import re
from textblob import TextBlob  # For sentiment analysis
from werkzeug.security import generate_password_hash, check_password_hash
import plotly.express as px
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = 'c913093f2de71f85ed4d79bdf18b44aa'  # Required for session management

# Load the trained model
with open(MODEL_PATH, 'rb') as model_file:
    model = pickle.load(model_file)

# Database connection
def get_db_connection():
    connection = mysql.connector.connect(
        host=os.getenv('DB_HOST', 'mental-health-db.render.com'),  # Use environment variable for database host
        user=os.getenv('DB_USER', 'root'),  # Database user
        password=os.getenv('DB_PASSWORD', 'root@123'),  # Database password
        database=os.getenv('DB_NAME', 'mental_health_db')  # Database name
    )
    return connection

# Preprocess input text and analyze sentiment
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    sentiment = TextBlob(text).sentiment.polarity  # Sentiment analysis using TextBlob
    return text, sentiment

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, hashed_password))
        connection.commit()
        cursor.close()
        connection.close()

        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
            user = cursor.fetchone()
            cursor.close()
            connection.close()

            if user and check_password_hash(user[2], password):
                session['username'] = user[1]
                return redirect(url_for('log_data'))
            else:
                print(f"Debug: Login failed for username {username}")
                return "Login failed. Check your username and password."
        except Exception as e:
            print(f"Debug: Error in login - {e}")
            return "An error occurred during login."
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/log_data', methods=['GET', 'POST'])
def log_data():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        mood = request.form['mood']
        activity = request.form['activity']
        sleep = int(request.form['sleep'])

        # Calculate mood score (example logic)
        mood_score = len(mood)  # Replace this with your actual scoring logic

        # Preprocess input and perform sentiment analysis
        combined_input = f"{mood} {activity} {sleep}"
        processed_input, sentiment = preprocess_text(combined_input)

        # Predict mood using the trained model
        predicted_mood = model.predict([processed_input])[0]

        # Insert data into the logs table
        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                'INSERT INTO logs (mood, mood_score, activity, sleep, predicted_mood, sentiment) VALUES (%s, %s, %s, %s, %s, %s)',
                (mood, mood_score, activity, sleep, predicted_mood, sentiment)
            )
            connection.commit()

            # Fetch recommendation from the recommendations table
            cursor.execute('SELECT recommendation FROM recommendations WHERE LOWER(mood) = LOWER(%s) AND LOWER(activity) = LOWER(%s) AND sleep = %s LIMIT 1',
                           (mood.strip(), activity.strip(), sleep))
            recommendation = cursor.fetchone()

            # Debugging
            print(f"Debug: Mood - {mood}, Activity - {activity}, Sleep - {sleep}")
            print(f"Debug: Recommendation fetched - {recommendation}")

        except Exception as e:
            print(f"Error: {e}")
            recommendation = None

        finally:
            cursor.close()
            connection.close()

        # Handle case if no recommendation is found
        recommendation_text = recommendation[0] if recommendation else "No specific recommendation found, but keep a positive mindset!"

        # Pass the recommendation and other data to the template
        return render_template(
            'analysis.html',
            mood=mood,
            activity=activity,
            sleep=sleep,
            predicted_mood=predicted_mood,
            sentiment=sentiment,
            recommendation=recommendation_text
        )

    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT mood, mood_score, activity, sleep, predicted_mood, sentiment FROM logs')
    logs = cursor.fetchall()
    cursor.close()
    connection.close()

    df = pd.DataFrame(logs)
    fig = px.line(df, x=df.index, y=['mood_score', 'sleep'], title='Mood Score and Sleep Over Time')
    graph = fig.to_html(full_html=False)

    return render_template('dashboard.html', graph=graph)

@app.route('/model_evaluation')
def model_evaluation():
    if 'username' not in session:
        return redirect(url_for('login'))

    # Here you would typically load evaluation metrics from your training process
    # For example, accuracy, confusion matrix, etc.
    evaluation_metrics = {
        'accuracy': 0.85,
        'precision': 0.88,
        'recall': 0.87
    }

    return render_template('model_evaluation.html', evaluation_metrics=evaluation_metrics)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
