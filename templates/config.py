# Database configuration
DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'ecommerce_bigdata',
    'user': 'admin',
    'password': 'password'
}

# Redis configuration for caching
REDIS_CONFIG = {
    'host': 'localhost',
    'port': 6379,
    'db': 0
}

# API keys (would be stored securely in a real application)
API_KEYS = {
    'payment_gateway': 'pk_test_123456',
    'analytics_service': 'analytics_789012'
}

# Application settings
DEBUG = True
THREADS_PER_PAGE = 2
CSRF_ENABLED = True
CSRF_SESSION_KEY = "secret"
SECRET_KEY = "super_secret_key"

# Feature flags
FEATURE_FLAGS = {
    'recommendation_engine': True,
    'real_time_analytics': True,
    'personalized_pricing': False
}