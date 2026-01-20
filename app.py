from flask import Flask, render_template, request, jsonify
from data_processor import DataProcessor
from user_analyzer import UserAnalyzer
from recommendation_engine import RecommendationEngine
import json
from datetime import datetime

app = Flask(__name__)

# Initialize components
data_processor = DataProcessor()
user_analyzer = UserAnalyzer()
recommendation_engine = RecommendationEngine()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    # Get summary statistics
    stats = data_processor.get_summary_stats()
    return render_template('dashboard.html', stats=stats)

@app.route('/user_analysis')
def user_analysis():
    heavy_users = user_analyzer.get_heavy_users()
    return render_template('user_analysis.html', heavy_users=heavy_users)

@app.route('/recommendations')
def recommendations():
    user_id = request.args.get('user_id', 'user_101')
    recommendations = recommendation_engine.get_recommendations(user_id)
    return render_template('recommendations.html', 
                          user_id=user_id, 
                          recommendations=recommendations)

@app.route('/api/user_behavior/<user_id>')
def api_user_behavior(user_id):
    behavior = user_analyzer.get_user_behavior(user_id)
    return jsonify(behavior)

@app.route('/api/traffic_data')
def api_traffic_data():
    # Generate simulated traffic data
    traffic_data = data_processor.generate_traffic_data()
    return jsonify(traffic_data)

@app.route('/api/purchase_patterns')
def api_purchase_patterns():
    patterns = data_processor.get_purchase_patterns()
    return jsonify(patterns)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)