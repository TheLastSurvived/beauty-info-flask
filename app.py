from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from sqlalchemy import func, or_, desc
import math
from datetime import datetime

from config import Config
from flask_migrate import Migrate
from models import db, User, Salon, Service, Review, BlogPost, BlogTag, BlogComment


app = Flask(__name__)
app.config.from_object(Config)

# Инициализация расширений
db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Пожалуйста, войдите в систему'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Контекстные процессоры
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

@app.context_processor
def inject_user():
    return {'current_user': current_user}

# Вспомогательные функции (заменили crud.py)
def get_blog_posts(skip=0, limit=10, category=None, tag=None, search=None, only_published=True):
    query = BlogPost.query
    
    if only_published:
        query = query.filter(BlogPost.is_published == True)
    
    if category:
        query = query.filter(BlogPost.category == category)
    
    if tag:
        query = query.join(BlogPost.tags).filter(BlogTag.name == tag)
    
    if search:
        search_term = f'%{search}%'
        query = query.filter(
            or_(
                BlogPost.title.ilike(search_term),
                BlogPost.content.ilike(search_term),
                BlogPost.excerpt.ilike(search_term)
            )
        )
    
    return query.order_by(desc(BlogPost.created_at)).offset(skip).limit(limit).all()

def get_blog_categories_with_counts():
    result = db.session.query(
        BlogPost.category,
        func.count(BlogPost.id).label('count')
    ).filter(
        BlogPost.is_published == True
    ).group_by(
        BlogPost.category
    ).all()
    
    return [{'name': cat, 'count': count} for cat, count in result if cat]

def get_popular_posts(limit=5):
    return BlogPost.query.filter(
        BlogPost.is_published == True
    ).order_by(
        desc(BlogPost.views_count)
    ).limit(limit).all()

def get_recent_posts(limit=5):
    return BlogPost.query.filter(
        BlogPost.is_published == True
    ).order_by(
        desc(BlogPost.created_at)
    ).limit(limit).all()

def get_popular_tags(limit=10):
    from models import post_tags
    result = db.session.query(
        BlogTag,
        func.count(post_tags.c.post_id).label('count')
    ).join(
        post_tags
    ).group_by(
        BlogTag.id
    ).order_by(
        desc('count')
    ).limit(limit).all()
    
    return result

# Главная страница
@app.route('/')
def home():
    # Статистика
    total_salons = Salon.query.count()
    total_reviews = Review.query.count()
    total_categories = db.session.query(Salon.category).distinct().count()
    
    # Средний рейтинг
    avg_rating = db.session.query(func.avg(Salon.rating)).scalar() or 0
    average_rating = round(avg_rating, 1)
    
    # Топ салоны
    top_salons = Salon.query.order_by(
        Salon.rating.desc(),
        Salon.reviews_count.desc()
    ).limit(3).all()
    
    # Категории с количеством салонов
    categories = db.session.query(
        Salon.category,
        func.count(Salon.id).label('count')
    ).group_by(Salon.category).all()
    
    categories_data = []
    for cat, count in categories:
        if cat:
            categories_data.append({
                "name": cat,
                "count": count
            })
    
    # Последние отзывы
    recent_reviews = Review.query.join(Salon).order_by(
        Review.created_at.desc()
    ).limit(4).all()
    
    # Популярные статьи блога
    blog_posts = BlogPost.query.filter(
        BlogPost.is_published == True
    ).order_by(
        BlogPost.views_count.desc()
    ).limit(3).all()
    
    # Районы с количеством салонов
    districts = db.session.query(
        Salon.district,
        func.count(Salon.id).label('count')
    ).group_by(Salon.district).all()
    
    districts_data = []
    for dist, count in districts:
        if dist:
            districts_data.append({
                "name": dist,
                "count": count
            })
    
    max_district_count = max([d["count"] for d in districts_data]) if districts_data else 1
    
    return render_template('index.html',
        title="Красота в Гродно - Информационный ресурс о салонах красоты",
        stats={
            "total_salons": total_salons,
            "total_reviews": total_reviews,
            "average_rating": average_rating,
            "total_categories": total_categories
        },
        top_salons=top_salons,
        categories=categories_data,
        recent_reviews=recent_reviews,
        blog_posts=blog_posts,
        districts=districts_data,
        max_district_count=max_district_count
    )

# Контакты
@app.route('/contact')
def contact():
    return render_template('contact.html', 
        title="Контакты и информация - Красота в Гродно")

# Блог
@app.route('/blog')
def blog():
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', None)
    tag = request.args.get('tag', None)
    search = request.args.get('search', None)
    
    items_per_page = 6
    skip = (page - 1) * items_per_page
    
    # Получаем посты
    posts = get_blog_posts(
        skip=skip,
        limit=items_per_page,
        category=category,
        tag=tag,
        search=search,
        only_published=True
    )
    
    # Общее количество постов
    if category:
        total_items = BlogPost.query.filter_by(
            is_published=True,
            category=category
        ).count()
    elif tag:
        total_items = db.session.query(func.count(BlogPost.id)).join(
            BlogPost.tags
        ).filter(
            BlogPost.is_published == True,
            BlogTag.name == tag
        ).scalar()
    else:
        total_items = BlogPost.query.filter_by(is_published=True).count()
    
    total_pages = max(1, math.ceil(total_items / items_per_page))
    
    # Данные для сайдбара
    categories = get_blog_categories_with_counts()
    popular_posts = get_popular_posts(limit=2)
    recent_posts = get_recent_posts(limit=2)
    popular_tags_result = get_popular_tags(limit=10)
    popular_tags = [tag[0] for tag in popular_tags_result] if popular_tags_result else []
    
    return render_template('blog.html',
        title="Блог о красоте - Красота в Гродно",
        posts=posts,
        categories=categories,
        popular_posts=popular_posts,
        recent_posts=recent_posts,
        popular_tags=popular_tags,
        current_category=category,
        current_tag=tag,
        search_query=search,
        current_page=page,
        total_pages=total_pages,
        total_items=total_items
    )

# Детальная страница поста
@app.route('/blog/<slug>')
def blog_post(slug):
    post = BlogPost.query.filter_by(slug=slug).first()
    
    if not post:
        abort(404)
    
    # Увеличиваем счетчик просмотров
    post.views_count += 1
    db.session.commit()
    
    # Получаем комментарии
    comments = BlogComment.query.filter_by(
        post_id=post.id,
        is_approved=True
    ).order_by(BlogComment.created_at.desc()).all()
    
    # Предыдущий и следующий пост
    prev_post = BlogPost.query.filter(
        BlogPost.is_published == True,
        BlogPost.created_at > post.created_at
    ).order_by(BlogPost.created_at.asc()).first()
    
    next_post = BlogPost.query.filter(
        BlogPost.is_published == True,
        BlogPost.created_at < post.created_at
    ).order_by(BlogPost.created_at.desc()).first()
    
    # Похожие посты
    similar_posts = []
    
    # По категории
    category_posts = BlogPost.query.filter(
        BlogPost.is_published == True,
        BlogPost.category == post.category,
        BlogPost.id != post.id
    ).order_by(BlogPost.created_at.desc()).limit(3).all()
    
    similar_posts.extend(category_posts)
    
    # По тегам
    if post.tags:
        tag_ids = [tag.id for tag in post.tags]
        tag_posts = BlogPost.query.join(
            BlogPost.tags
        ).filter(
            BlogPost.is_published == True,
            BlogPost.id != post.id,
            BlogTag.id.in_(tag_ids)
        ).distinct().limit(3).all()
        
        existing_ids = [p.id for p in similar_posts]
        for tag_post in tag_posts:
            if tag_post.id not in existing_ids and len(similar_posts) < 6:
                similar_posts.append(tag_post)
    
    # Если мало постов
    if len(similar_posts) < 4:
        recent_posts = BlogPost.query.filter(
            BlogPost.is_published == True,
            BlogPost.id != post.id
        ).order_by(BlogPost.created_at.desc()).limit(3).all()
        
        existing_ids = [p.id for p in similar_posts]
        for recent_post in recent_posts:
            if recent_post.id not in existing_ids and len(similar_posts) < 6:
                similar_posts.append(recent_post)
    
    return render_template('blog-post.html',
        title=f"{post.title} - Красота в Гродно",
        post=post,
        comments=comments,
        similar_posts=similar_posts[:4],
        prev_post=prev_post,
        next_post=next_post,
        tags=post.tags
    )



# Поиск в блоге
@app.route('/api/blog/search')
def blog_search():
    query = request.args.get('q', '').strip()
    
    if len(query) < 1:
        return jsonify({'results': []})
    
    posts = BlogPost.query.filter(
        BlogPost.is_published == True,
        or_(
            BlogPost.title.ilike(f'%{query}%'),
            BlogPost.content.ilike(f'%{query}%'),
            BlogPost.excerpt.ilike(f'%{query}%')
        )
    ).limit(5).all()
    
    results = []
    for post in posts:
        results.append({
            'id': post.id,
            'title': post.title,
            'excerpt': post.excerpt[:100] if post.excerpt else '',
            'slug': post.slug,
            'category': post.category,
            'image_url': post.image_url
        })
    
    return jsonify({'results': results})

# Каталог
@app.route('/catalog')
def catalog():
    category = request.args.get('category', None)
    district = request.args.get('district', None)
    min_rating = request.args.get('min_rating', None)
    sort_by = request.args.get('sort_by', 'popular')
    page = request.args.get('page', 1, type=int)
    
    # Базовый запрос
    query = Salon.query
    
    # Применяем фильтры
    if category:
        query = query.filter(func.lower(Salon.category) == func.lower(category))
    if district:
        query = query.filter(func.lower(Salon.district) == func.lower(district))
    
    if min_rating and min_rating != '':
        try:
            rating_value = float(min_rating)
            query = query.filter(Salon.rating >= rating_value)
        except ValueError:
            pass
    
    # Применяем сортировку
    if sort_by == 'rating':
        query = query.order_by(Salon.rating.desc())
    elif sort_by == 'reviews':
        query = query.order_by(Salon.reviews_count.desc())
    elif sort_by == 'name':
        query = query.order_by(Salon.name.asc())
    else:
        query = query.order_by(Salon.rating.desc(), Salon.reviews_count.desc())
    
    # Пагинация
    items_per_page = 6
    total_items = query.count()
    total_pages = max(1, math.ceil(total_items / items_per_page))
    
    # Корректируем номер страницы
    page = min(page, total_pages)
    
    # Получаем элементы
    salons = query.offset((page - 1) * items_per_page).limit(items_per_page).all()
    
    # Уникальные категории и районы
    categories = [cat[0] for cat in db.session.query(Salon.category).distinct().all() if cat[0]]
    districts = [dist[0] for dist in db.session.query(Salon.district).distinct().all() if dist[0]]
    
    # Подсчет с учетом фильтров
    category_counts = {}
    district_counts = {}
    
    for cat in categories:
        cat_query = Salon.query.filter(func.lower(Salon.category) == func.lower(cat))
        if district:
            cat_query = cat_query.filter(func.lower(Salon.district) == func.lower(district))
        if min_rating and min_rating != '':
            try:
                rating_value = float(min_rating)
                cat_query = cat_query.filter(Salon.rating >= rating_value)
            except ValueError:
                pass
        category_counts[cat] = cat_query.count()
    
    for dist in districts:
        dist_query = Salon.query.filter(func.lower(Salon.district) == func.lower(dist))
        if category:
            dist_query = dist_query.filter(func.lower(Salon.category) == func.lower(category))
        if min_rating and min_rating != '':
            try:
                rating_value = float(min_rating)
                dist_query = dist_query.filter(Salon.rating >= rating_value)
            except ValueError:
                pass
        district_counts[dist] = dist_query.count()
    
    # Подсчет для "Все категории" и "Все районы"
    all_categories_query = Salon.query
    all_districts_query = Salon.query
    
    if district:
        all_categories_query = all_categories_query.filter(
            func.lower(Salon.district) == func.lower(district)
        )
    if min_rating and min_rating != '':
        try:
            rating_value = float(min_rating)
            all_categories_query = all_categories_query.filter(Salon.rating >= rating_value)
            all_districts_query = all_districts_query.filter(Salon.rating >= rating_value)
        except ValueError:
            pass
    
    if category:
        all_districts_query = all_districts_query.filter(
            func.lower(Salon.category) == func.lower(category)
        )
    
    all_categories_count = all_categories_query.count()
    all_districts_count = all_districts_query.count()
    
    return render_template('catalog.html',
        title="Каталог салонов",
        salons=salons,
        categories=categories,
        districts=districts,
        all_categories_count=all_categories_count,
        all_districts_count=all_districts_count,
        category_counts=category_counts,
        district_counts=district_counts,
        current_category=category,
        current_district=district,
        current_rating=min_rating if min_rating else '',
        current_sort=sort_by,
        current_page=page,
        total_pages=total_pages,
        total_items=total_items,
        items_per_page=items_per_page
    )

# Детальная страница салона
@app.route('/catalog/<int:salon_id>')
def salon_detail(salon_id):
    salon = Salon.query.get_or_404(salon_id)
    
    # Получаем услуги
    services = Service.query.filter_by(salon_id=salon_id).all()
    
    # Группируем услуги по категориям
    services_by_category = {}
    for service in services:
        if service.category not in services_by_category:
            services_by_category[service.category] = []
        services_by_category[service.category].append(service)
    
    # Получаем отзывы
    reviews = Review.query.filter_by(salon_id=salon_id).all()
    
    return render_template('salon-detail.html',
        title=salon.name,
        salon=salon,
        services=services,
        services_by_category=services_by_category,
        reviews=reviews
    )

# Поиск в каталоге
@app.route('/catalog/search', methods=['POST'])
def catalog_search():
    search_query = request.form.get('search_query', '').strip()
    page = request.form.get('page', 1, type=int)
    
    if search_query:
        search_term = f'%{search_query}%'
        base_query = Salon.query.filter(
            or_(
                func.lower(Salon.name).ilike(func.lower(search_term)),
                func.lower(Salon.description).ilike(func.lower(search_term)),
                func.lower(Salon.address).ilike(func.lower(search_term)),
                func.lower(Salon.district).ilike(func.lower(search_term)),
                func.lower(Salon.category).ilike(func.lower(search_term))
            )
        )
        
        # Пагинация
        items_per_page = 6
        total_items = base_query.count()
        total_pages = max(1, math.ceil(total_items / items_per_page))
        
        page = min(page, total_pages)
        salons = base_query.offset((page - 1) * items_per_page).limit(items_per_page).all()
        
        categories = [cat[0] for cat in db.session.query(Salon.category).distinct().all() if cat[0]]
        districts = [dist[0] for dist in db.session.query(Salon.district).distinct().all() if dist[0]]
        
        category_counts = {}
        district_counts = {}
        
        for cat in categories:
            category_counts[cat] = Salon.query.filter(
                func.lower(Salon.category) == func.lower(cat)
            ).count()
        
        for dist in districts:
            district_counts[dist] = Salon.query.filter(
                func.lower(Salon.district) == func.lower(dist)
            ).count()
        
        return render_template('catalog.html',
            title=f'Результаты поиска: {search_query}',
            salons=salons,
            categories=categories,
            districts=districts,
            category_counts=category_counts,
            district_counts=district_counts,
            search_query=search_query,
            current_page=page,
            total_pages=total_pages,
            total_items=total_items,
            items_per_page=items_per_page
        )
    
    return redirect(url_for('catalog'))

# Автодополнение поиска
@app.route('/api/search/autocomplete')
def search_autocomplete():
    query = request.args.get('q', '').strip()
    
    if len(query) < 1:
        return jsonify({'results': []})
    
    search_term = f'%{query}%'
    
    # Ищем салоны
    salons = Salon.query.filter(
        func.lower(Salon.name).ilike(func.lower(search_term))
    ).limit(10).all()
    
    # Ищем категории
    categories = [cat[0] for cat in db.session.query(Salon.category).filter(
        func.lower(Salon.category).ilike(func.lower(search_term))
    ).distinct().limit(5).all() if cat[0]]
    
    # Ищем районы
    districts = [dist[0] for dist in db.session.query(Salon.district).filter(
        func.lower(Salon.district).ilike(func.lower(search_term))
    ).distinct().limit(5).all() if dist[0]]
    
    results = []
    
    # Добавляем салоны
    for salon in salons:
        results.append({
            'type': 'salon',
            'id': salon.id,
            'name': salon.name,
            'rating': salon.rating,
            'category': salon.category,
            'icon': 'bi-shop'
        })
    
    # Добавляем категории
    for category in categories:
        results.append({
            'type': 'category',
            'name': category,
            'icon': 'bi-tag'
        })
    
    # Добавляем районы
    for district in districts:
        results.append({
            'type': 'district',
            'name': district,
            'icon': 'bi-geo-alt'
        })
    
    return jsonify({'results': results})

# Регистрация
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        
        # Валидация
        if not email or not password:
            flash('Пожалуйста, заполните все обязательные поля', 'error')
            return render_template('register.html', title='Регистрация')
        
        if len(password) < 6:
            flash('Пароль должен содержать не менее 6 символов', 'error')
            return render_template('register.html', title='Регистрация')
        
        # Проверяем, существует ли пользователь
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Пользователь с таким email уже существует', 'error')
            return render_template('register.html', title='Регистрация')
        
        # Создаем пользователя
        user = User(
            email=email,
            first_name=first_name if first_name else None,
            last_name=last_name if last_name else None
        )
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            
            # Автоматически входим после регистрации
            login_user(user)
            flash('Регистрация прошла успешно!', 'success')
            return redirect(url_for('home'))
            
        except Exception as e:
            db.session.rollback()
            flash('Ошибка при регистрации. Пожалуйста, попробуйте позже.', 'error')
            return render_template('register.html', title='Регистрация')
    
    return render_template('register.html', title='Регистрация')

# Вход
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        remember = request.form.get('remember', False)
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user, remember=bool(remember))
            next_page = request.args.get('next')
            flash(f'Добро пожаловать, {user.first_name or user.email}!', 'success')
            return redirect(next_page or url_for('home'))
        else:
            flash('Неверный email или пароль', 'error')
    
    return render_template('login.html', title='Вход')

# Выход
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы успешно вышли из системы', 'success')
    return redirect(url_for('home'))



# Обработка ошибки 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title='Страница не найдена'), 404

# Обработка ошибки 500
@app.errorhandler(500)
def internal_error(e):
    db.session.rollback()
    return render_template('500.html', title='Внутренняя ошибка сервера'), 500


# Форма для добавления отзыва
@app.route('/catalog/<int:salon_id>/review', methods=['POST'])
@login_required
def add_review(salon_id):
    salon = Salon.query.get_or_404(salon_id)
    
    rating = request.form.get('rating', type=int)
    text = request.form.get('text', '').strip()
    tags = request.form.get('tags', '').strip()
    
    if not rating or not text:
        flash('Пожалуйста, заполните все обязательные поля', 'error')
        return redirect(url_for('salon_detail', salon_id=salon_id))
    
    if rating < 1 or rating > 5:
        flash('Рейтинг должен быть от 1 до 5', 'error')
        return redirect(url_for('salon_detail', salon_id=salon_id))
    
    # Создаем отзыв
    review = Review(
        salon_id=salon.id,
        user_id=current_user.id,
        author_name=current_user.first_name or current_user.email.split('@')[0],
        rating=rating,
        text=text,
        tags=tags
    )
    
    db.session.add(review)
    
    # Обновляем рейтинг салона
    salon.reviews_count += 1
    all_reviews = Review.query.filter_by(salon_id=salon.id).all()
    if all_reviews:
        avg_rating = sum(r.rating for r in all_reviews) / len(all_reviews)
        salon.rating = round(avg_rating, 1)
    
    db.session.commit()
    
    flash('Спасибо за ваш отзыв! Он успешно добавлен.', 'success')
    return redirect(url_for('salon_detail', salon_id=salon_id) + '#reviews')

# Обновленная функция добавления комментария с авторизацией
@app.route('/blog/<slug>/comment', methods=['POST'])
def add_comment(slug):
    post = BlogPost.query.filter_by(slug=slug).first()
    
    if not post:
        flash('Пост не найден', 'error')
        return redirect(url_for('blog'))
    
    # Если пользователь авторизован, используем его данные
    if current_user.is_authenticated:
        author_name = current_user.first_name or current_user.email.split('@')[0]
        author_email = current_user.email
        user_id = current_user.id
    else:
        author_name = request.form.get('author_name', '').strip()
        author_email = request.form.get('author_email', '').strip()
        user_id = None
    
    content = request.form.get('content', '').strip()
    
    if not author_name or not content:
        flash('Пожалуйста, заполните все обязательные поля', 'error')
        return redirect(url_for('blog_post', slug=slug))
    
    # Проверяем email для неавторизованных пользователей
    if not current_user.is_authenticated and author_email:
        import re
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, author_email):
            flash('Пожалуйста, введите корректный email', 'error')
            return redirect(url_for('blog_post', slug=slug))
    
    comment = BlogComment(
        post_id=post.id,
        user_id=user_id,
        author_name=author_name,
        author_email=author_email,
        content=content,
        is_approved=current_user.is_authenticated  # Автоматически одобряем для авторизованных
    )
    
    db.session.add(comment)
    db.session.commit()
    
    flash('Комментарий добавлен' + (' и опубликован' if current_user.is_authenticated else ' и будет опубликован после проверки'), 'success')
    return redirect(url_for('blog_post', slug=slug) + '#comments')

# Удаление отзыва
@app.route('/review/<int:review_id>/delete', methods=['POST'])
@login_required
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)
    
    # Проверяем права
    if review.user_id != current_user.id and not current_user.is_admin:
        abort(403)
    
    salon_id = review.salon_id
    db.session.delete(review)
    
    # Обновляем рейтинг салона
    salon = Salon.query.get(salon_id)
    salon.reviews_count = max(0, salon.reviews_count - 1)
    
    all_reviews = Review.query.filter_by(salon_id=salon_id).all()
    if all_reviews:
        avg_rating = sum(r.rating for r in all_reviews) / len(all_reviews)
        salon.rating = round(avg_rating, 1)
    else:
        salon.rating = 0.0
    
    db.session.commit()
    
    flash('Отзыв успешно удален', 'success')
    return redirect(url_for('salon_detail', salon_id=salon_id))

# Удаление комментария
@app.route('/comment/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = BlogComment.query.get_or_404(comment_id)
    
    # Проверяем права
    if comment.user_id != current_user.id and not current_user.is_admin:
        abort(403)
    
    post_slug = comment.post.slug
    db.session.delete(comment)
    db.session.commit()
    
    flash('Комментарий успешно удален', 'success')
    return redirect(url_for('blog_post', slug=post_slug))

# Обновленный профиль пользователя
@app.route('/profile')
@login_required
def profile():
    # Получаем отзывы пользователя
    user_reviews = Review.query.filter_by(
        user_id=current_user.id
    ).order_by(Review.created_at.desc()).limit(10).all()
    
    # Получаем комментарии пользователя
    user_comments = BlogComment.query.filter_by(
        user_id=current_user.id
    ).order_by(BlogComment.created_at.desc()).limit(10).all()
    
    return render_template('profile.html', 
        title='Мой профиль - Красота в Гродно',
        user_reviews=user_reviews,
        user_comments=user_comments
    )

# Обновление профиля
@app.route('/profile/update', methods=['POST'])
@login_required
def update_profile():
    user = current_user
    
    # Получаем данные из формы
    first_name = request.form.get('first_name', '').strip()
    last_name = request.form.get('last_name', '').strip()
    phone = request.form.get('phone', '').strip()
    
    # Обновляем данные
    user.first_name = first_name if first_name else None
    user.last_name = last_name if last_name else None
    user.phone = phone if phone else None
    
    # Обработка смены пароля
    current_password = request.form.get('current_password', '').strip()
    new_password = request.form.get('new_password', '').strip()
    confirm_password = request.form.get('confirm_password', '').strip()
    
    if current_password and new_password:
        if not user.check_password(current_password):
            flash('Текущий пароль неверен', 'error')
            return redirect(url_for('profile'))
        
        if new_password != confirm_password:
            flash('Новый пароль и подтверждение не совпадают', 'error')
            return redirect(url_for('profile'))
        
        if len(new_password) < 6:
            flash('Пароль должен содержать не менее 6 символов', 'error')
            return redirect(url_for('profile'))
        
        user.set_password(new_password)
        flash('Пароль успешно изменен', 'success')
    
    try:
        db.session.commit()
        flash('Профиль успешно обновлен', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Ошибка при обновлении профиля', 'error')
    
    return redirect(url_for('profile'))


if __name__ == '__main__':
    
    with app.app_context():
        db.create_all()
    
    app.run(debug=True, host='127.0.0.1', port=8000)