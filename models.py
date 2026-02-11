from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()

# Ассоциативная таблица для связи многие-ко-многим (посты и теги)
post_tags = db.Table('post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('blog_posts.id', ondelete='CASCADE'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('blog_tags.id', ondelete='CASCADE'), primary_key=True)
)

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    password_hash = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

    is_admin = db.Column(db.Boolean, default=False) 
    
    # Дополнительные поля
    phone = db.Column(db.String(20))
    avatar_url = db.Column(db.String(300))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Salon(db.Model):
    __tablename__ = 'salons'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    category = db.Column(db.String(100))
    description = db.Column(db.Text)
    address = db.Column(db.String(300))
    district = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    working_hours = db.Column(db.String(200))
    rating = db.Column(db.Float, default=0.0)
    reviews_count = db.Column(db.Integer, default=0)
    is_verified = db.Column(db.Boolean, default=False)
    image_url = db.Column(db.String(300), default='/static/img/default.png')
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    # Связи
    services = db.relationship('Service', backref='salon', lazy=True, cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='salon', lazy=True, cascade='all, delete-orphan')

class Service(db.Model):
    __tablename__ = 'services'
    
    id = db.Column(db.Integer, primary_key=True)
    salon_id = db.Column(db.Integer, db.ForeignKey('salons.id'))
    category = db.Column(db.String(100))
    name = db.Column(db.String(200))
    description = db.Column(db.Text)
    price = db.Column(db.Integer)

class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    salon_id = db.Column(db.Integer, db.ForeignKey('salons.id'))
    author_name = db.Column(db.String(100))
    rating = db.Column(db.Integer)
    text = db.Column(db.Text)
    tags = db.Column(db.String(300))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    user = db.relationship('User', backref='reviews', lazy=True)  # Добавлено

class BlogPost(db.Model):
    __tablename__ = 'blog_posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True)
    excerpt = db.Column(db.String(500))
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), default='Администратор')
    image_url = db.Column(db.String(300), default='/static/img/default.png')
    category = db.Column(db.String(50))
    is_published = db.Column(db.Boolean, default=True)
    views_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Связи
    comments = db.relationship('BlogComment', backref='post', lazy=True, cascade='all, delete-orphan')
    tags = db.relationship('BlogTag', secondary=post_tags, backref=db.backref('posts', lazy=True))

class BlogTag(db.Model):
    __tablename__ = 'blog_tags'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    slug = db.Column(db.String(30), unique=True)

class BlogComment(db.Model):
    __tablename__ = 'blog_comments'
    
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('blog_posts.id', ondelete='CASCADE'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    author_name = db.Column(db.String(100), nullable=False)
    author_email = db.Column(db.String(100))
    content = db.Column(db.Text, nullable=False)
    is_approved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    user = db.relationship('User', backref='blog_comments', lazy=True)  # Добавлено
    