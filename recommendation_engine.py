import pandas as pd
import numpy as np
from data_processor import DataProcessor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics.pairwise import cosine_similarity

class RecommendationEngine:
    def __init__(self):
        self.data_processor = DataProcessor()
        self.user_item_matrix = self.create_user_item_matrix()
        self.item_similarity = self.calculate_item_similarity()
    
    def create_user_item_matrix(self):
        transactions = self.data_processor.transactions
        transactions = transactions[transactions['status'] == 'completed']
        
        # Create user-item matrix with interaction strength
        user_item = transactions.groupby(['user_id', 'product_id']).agg({
            'quantity': 'sum',
            'price': 'mean'
        }).reset_index()
        
        user_item['interaction_strength'] = user_item['quantity'] * user_item['price']
        
        # Pivot to create matrix
        user_item_matrix = user_item.pivot_table(
            index='user_id', 
            columns='product_id', 
            values='interaction_strength', 
            fill_value=0
        )
        
        return user_item_matrix
    
    def calculate_item_similarity(self):
        # Calculate cosine similarity between items
        item_similarity = cosine_similarity(self.user_item_matrix.T)
        item_similarity_df = pd.DataFrame(
            item_similarity, 
            index=self.user_item_matrix.columns, 
            columns=self.user_item_matrix.columns
        )
        return item_similarity_df
    
    def get_recommendations(self, user_id, n_recommendations=5):
        if user_id not in self.user_item_matrix.index:
            return self.get_popular_products(n_recommendations)
        
        # Get user's purchased items
        user_items = self.user_item_matrix.loc[user_id]
        purchased_items = user_items[user_items > 0].index.tolist()
        
        if not purchased_items:
            return self.get_popular_products(n_recommendations)
        
        # Calculate recommendation scores
        scores = {}
        for item in purchased_items:
            similar_items = self.item_similarity[item].sort_values(ascending=False)
            for similar_item, score in similar_items.items():
                if similar_item not in purchased_items:
                    scores[similar_item] = scores.get(similar_item, 0) + score
        
        # Get top recommendations
        recommendations = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:n_recommendations]
        
        # Get product details
        products = self.data_processor.products
        recommended_products = []
        for product_id, score in recommendations:
            product_info = products[products['product_id'] == product_id].iloc[0]
            recommended_products.append({
                'product_id': product_id,
                'name': product_info['name'],
                'category': product_info['category'],
                'price': product_info['price'],
                'score': round(score, 4)
            })
        
        return recommended_products
    
    def get_popular_products(self, n=5):
        transactions = self.data_processor.transactions
        products = self.data_processor.products
        
        popular_products = transactions.groupby('product_id').agg({
            'quantity': 'sum'
        }).reset_index().sort_values('quantity', ascending=False).head(n)
        
        popular_products = popular_products.merge(products, on='product_id')
        
        return popular_products.to_dict('records')