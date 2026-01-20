import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

class DataProcessor:
    def __init__(self):
        self.users = self.generate_users(1000)
        self.products = self.generate_products(500)
        self.transactions = self.generate_transactions(10000)
        
    def generate_users(self, n):
        users = []
        for i in range(n):
            users.append({
                'user_id': f'user_{i}',
                'name': f'User {i}',
                'tier': random.choice(['basic', 'prime', 'vip']),
                'join_date': datetime.now() - timedelta(days=random.randint(1, 1000)),
                'location': random.choice(['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata'])
            })
        return pd.DataFrame(users)
    
    def generate_products(self, n):
        products = []
        categories = ['Electronics', 'Fashion', 'Home', 'Books', 'Sports']
        for i in range(n):
            products.append({
                'product_id': f'prod_{i}',
                'name': f'Product {i}',
                'category': random.choice(categories),
                'price': round(random.uniform(100, 10000), 2),
                'stock': random.randint(0, 1000)
            })
        return pd.DataFrame(products)
    
    def generate_transactions(self, n):
        transactions = []
        start_date = datetime.now() - timedelta(days=30)
        for i in range(n):
            user = random.choice(self.users['user_id'].values)
            product = random.choice(self.products['product_id'].values)
            product_price = self.products[self.products['product_id'] == product]['price'].values[0]
            
            transactions.append({
                'transaction_id': f'trans_{i}',
                'user_id': user,
                'product_id': product,
                'quantity': random.randint(1, 5),
                'timestamp': start_date + timedelta(seconds=random.randint(0, 30*24*3600)),
                'price': product_price,
                'status': random.choice(['completed', 'pending', 'cancelled'])
            })
        return pd.DataFrame(transactions)
    
    def get_summary_stats(self):
        total_users = len(self.users)
        total_products = len(self.products)
        total_transactions = len(self.transactions)
        revenue = (self.transactions['price'] * self.transactions['quantity']).sum()
        
        heavy_users = self.transactions.groupby('user_id').agg({
            'price': 'sum',
            'transaction_id': 'count'
        }).reset_index()
        heavy_users = heavy_users[heavy_users['price'] > heavy_users['price'].quantile(0.9)]
        
        return {
            'total_users': total_users,
            'total_products': total_products,
            'total_transactions': total_transactions,
            'revenue': round(revenue, 2),
            'heavy_users_count': len(heavy_users)
        }
    
    def generate_traffic_data(self):
        # Simulate website traffic data
        hours = 24
        traffic = []
        base_traffic = 1000
        for hour in range(hours):
            # Peak hours have more traffic
            multiplier = 1.5 if 10 <= hour <= 16 else 1.0
            # Big sale day has even more traffic
            sale_multiplier = 3.0 if 8 <= hour <= 22 else 1.5
            traffic.append({
                'hour': hour,
                'users': int(base_traffic * multiplier * sale_multiplier * random.uniform(0.9, 1.1)),
                'page_views': int(base_traffic * multiplier * sale_multiplier * random.uniform(2, 5)),
                'orders': int(base_traffic * multiplier * sale_multiplier * random.uniform(0.05, 0.1))
            })
        return traffic
    
    def get_purchase_patterns(self):
        patterns = []
        categories = self.products['category'].unique()
        
        for category in categories:
            category_products = self.products[self.products['category'] == category]
            category_transactions = self.transactions[
                self.transactions['product_id'].isin(category_products['product_id'])
            ]
            
            total_sales = (category_transactions['price'] * category_transactions['quantity']).sum()
            patterns.append({
                'category': category,
                'sales': round(total_sales, 2),
                'transactions': len(category_transactions),
                'avg_order_value': round(total_sales / len(category_transactions), 2) if len(category_transactions) > 0 else 0
            })
        
        return patterns