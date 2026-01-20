# Big Data E-Commerce Analytics

A comprehensive system for analyzing and managing heavy purchase users during major e-commerce sale events like Amazon Prime Day and Flipkart Big Billion Days.

## Features

- Real-time traffic monitoring during sale events
- Identification and analysis of heavy purchase users
- Personalized product recommendations
- Server load balancing simulation
- Interactive dashboard with visual analytics

## Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python app.py`
4. Open your browser and navigate to `http://localhost:5000`

## Project Structure

- `app.py` - Main Flask application
- `data_processor.py` - Handles data generation and processing
- `user_analyzer.py` - Analyzes user behavior and identifies heavy users
- `recommendation_engine.py` - Provides personalized product recommendations
- `load_balancer.py` - Simulates server load balancing during peak traffic
- `templates/` - HTML templates for the web interface
- `static/` - CSS and JavaScript files for styling and interactivity

## Usage

1. **Dashboard**: View overall statistics and traffic patterns
2. **User Analysis**: Search for specific users and view their behavior patterns
3. **Recommendations**: Get personalized product recommendations for users
4. **Heavy Users**: View a list of top spending users during sale events

## Technologies Used

- Python
- Flask
- Pandas
- Scikit-learn
- Chart.js
- Bootstrap