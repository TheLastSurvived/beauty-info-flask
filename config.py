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

    # Настройки загрузки изображений
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
    # Настройки для оптимизации изображений
    IMAGE_QUALITY = 85
    IMAGE_MAX_WIDTH = 1200
    IMAGE_MAX_HEIGHT = 1200
    THUMBNAIL_SIZE = (300, 200)
    BLOG_IMAGE_SIZE = (800, 600)
    SALON_IMAGE_SIZE = (600, 400)