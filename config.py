import os
from datetime import timedelta

class Config:
    # Базовые настройки
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-in-production'
    
    # База данных
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Настройки безопасности
    SECURITY_PASSWORD_SALT = 'your-password-salt-change-in-production'
    
    # Настройки приложения
    ITEMS_PER_PAGE = 6
    BLOG_POSTS_PER_PAGE = 6
    TOP_SALONS_LIMIT = 3
    RECENT_REVIEWS_LIMIT = 4
    BLOG_POSTS_HOME_LIMIT = 3