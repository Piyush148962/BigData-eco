import pandas as pd
import numpy as np
from data_processor import DataProcessor

class UserAnalyzer:
    def __init__(self):
        self.data_processor = DataProcessor()
    
    def get_heavy_users(self, threshold=0.9):
        transactions = self.data_processor.transactions
        users = self.data_processor.users
        
        user_stats = transactions.groupby('user_id').agg({
            'price': ['sum', 'count'],
            'quantity': 'sum'
        }).reset_index()
        
        user_stats.columns = ['user_id', 'total_spent', 'transaction_count', 'total_items']
        
        # Identify heavy users (top 10% by spending)
        spend_threshold = user_stats['total_spent'].quantile(threshold)
        heavy_users = user_stats[user_stats['total_spent'] >= spend_threshold]
        
        # Merge with user data
        heavy_users = heavy_users.merge(users, on='user_id')
        
        return heavy_users.to_dict('records')
    
    def get_user_behavior(self, user_id):
        transactions = self.data_processor.transactions
        users = self.data_processor.users
        
        user_transactions = transactions[transactions['user_id'] == user_id]
        user_data = users[users['user_id'] == user_id].iloc[0]
        
        if len(user_transactions) == 0:
            return {
                'user_id': user_id,
                'exists': False,
                'message': 'No transactions found for this user'
            }
        
        # Calculate behavior metrics
        total_spent = user_transactions['price'].sum()
        avg_order_value = total_spent / len(user_transactions)
        favorite_category = self.get_favorite_category(user_transactions)
        
        # Time-based analysis
        user_transactions['hour'] = user_transactions['timestamp'].dt.hour
        peak_hour = user_transactions['hour'].mode()[0] if len(user_transactions['hour'].mode()) > 0 else None
        
        return {
            'user_id': user_id,
            'exists': True,
            'name': user_data['name'],
            'tier': user_data['tier'],
            'location': user_data['location'],
            'total_transactions': len(user_transactions),
            'total_spent': round(total_spent, 2),
            'avg_order_value': round(avg_order_value, 2),
            'favorite_category': favorite_category,
            'peak_hour': peak_hour,
            'last_transaction': user_transactions['timestamp'].max().strftime('%Y-%m-%d %H:%M')
        }
    
    def get_favorite_category(self, user_transactions):
        products = self.data_processor.products
        user_products = user_transactions.merge(products, on='product_id')
        
        if len(user_products) == 0:
            return "None"
        
        category_counts = user_products['category'].value_counts()
        return category_counts.index[0] if len(category_counts) > 0 else "None"