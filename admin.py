from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, current_app, jsonify
from flask_login import login_required, current_user
from sqlalchemy import func, desc
from functools import wraps
from models import db, User, Salon, Service, Review, BlogPost, BlogTag, BlogComment
from datetime import datetime
from image_utils import save_uploaded_image, delete_uploaded_image

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Декоратор для проверки прав администратора
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

# Главная страница админки
@admin_bp.route('/')
@login_required
@admin_required
def index():
    # Статистика
    stats = {
        'users': User.query.count(),
        'salons': Salon.query.count(),
        'reviews': Review.query.count(),
        'blog_posts': BlogPost.query.count(),
        'blog_comments': BlogComment.query.count(),
        'services': Service.query.count(),
        'tags': BlogTag.query.count()
    }
    
    # Последние пользователи
    recent_users = User.query.order_by(desc(User.created_at)).limit(5).all()
    
    # Последние отзывы
    recent_reviews = Review.query.order_by(desc(Review.created_at)).limit(5).all()
    
    # Последние посты блога
    recent_posts = BlogPost.query.order_by(desc(BlogPost.created_at)).limit(5).all()
    
    # Саланы без отзывов
    salons_without_reviews = Salon.query.filter(Salon.reviews_count == 0).count()
    
    # Средний рейтинг салонов
    avg_salon_rating = db.session.query(func.avg(Salon.rating)).scalar() or 0
    
    return render_template('admin/index.html',
        title='Панель управления',
        stats=stats,
        recent_users=recent_users,
        recent_reviews=recent_reviews,
        recent_posts=recent_posts,
        salons_without_reviews=salons_without_reviews,
        avg_salon_rating=round(avg_salon_rating, 1)
    )

# ==================== ЗАГРУЗКА ИЗОБРАЖЕНИЙ ====================

@admin_bp.route('/upload/salon-image', methods=['POST'])
@login_required
@admin_required
def upload_salon_image():
    """AJAX загрузка изображения для салона"""
    if 'image' not in request.files:
        return jsonify({'error': 'Файл не выбран'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'Файл не выбран'}), 400
    
    # Сохраняем файл
    image_url, thumbnail_url = save_uploaded_image(
    file, 
    subfolder='salons',
    make_thumb=True,
    thumb_size=(300, 200)
    )
    
    if image_url:
        return jsonify({
            'success': True,
            'image_url': image_url,
            'thumbnail_url': thumbnail_url
        })
    else:
        return jsonify({'error': 'Неподдерживаемый формат файла'}), 400

# AJAX загрузка изображения для блога
@admin_bp.route('/upload/blog-image', methods=['POST'])
@login_required
@admin_required
def upload_blog_image():
    """AJAX загрузка изображения для блога"""
    if 'image' not in request.files:
        return jsonify({'error': 'Файл не выбран'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'Файл не выбран'}), 400
    
    # Сохраняем файл
    image_url, thumbnail_url = save_uploaded_image(
        file, 
        subfolder='blog',
        create_thumb=True,
        thumbnail_size=(400, 300)
    )
    
    if image_url:
        return jsonify({
            'success': True,
            'image_url': image_url,
            'thumbnail_url': thumbnail_url
        })
    else:
        return jsonify({'error': 'Неподдерживаемый формат файла'}), 400

# Загрузка изображения для редактора
@admin_bp.route('/upload/editor-image', methods=['POST'])
@login_required
@admin_required
def upload_editor_image():
    """Загрузка изображения для редактора контента (TinyMCE/Summernote)"""
    if 'file' not in request.files:
        return jsonify({'error': 'Файл не выбран'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Файл не выбран'}), 400
    
    # Сохраняем файл
    image_url, _ = save_uploaded_image(
        file, 
        subfolder='editor',
        create_thumb=False
    )
    
    if image_url:
        return jsonify({
            'location': image_url
        })
    else:
        return jsonify({'error': 'Неподдерживаемый формат файла'}), 400



# ==================== УПРАВЛЕНИЕ САЛОНАМИ ====================

@admin_bp.route('/salons')
@login_required
@admin_required
def salons():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    per_page = 10
    
    query = Salon.query
    if search:
        query = query.filter(Salon.name.ilike(f'%{search}%'))
    
    pagination = query.order_by(desc(Salon.created_at)).paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('admin/salons.html',
        title='Управление салонами',
        salons=pagination.items,
        pagination=pagination,
        search=search
    )

@admin_bp.route('/salons/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_salon():
    if request.method == 'POST':
        # Обработка загруженного изображения
        image_url = '/static/img/default.png'
        if 'image_file' in request.files:
            file = request.files['image_file']
            if file and file.filename:
                uploaded_url, _ = save_uploaded_image(file, subfolder='salons', make_thumb=True)
                if uploaded_url:
                    image_url = uploaded_url
        
        salon = Salon(
            name=request.form.get('name'),
            category=request.form.get('category'),
            description=request.form.get('description'),
            address=request.form.get('address'),
            district=request.form.get('district'),
            phone=request.form.get('phone'),
            working_hours=request.form.get('working_hours'),
            image_url=image_url,
            is_verified='is_verified' in request.form,
            # Социальные сети
            social_instagram=request.form.get('social_instagram'),
            social_vk=request.form.get('social_vk'),
            social_facebook=request.form.get('social_facebook'),
            social_telegram=request.form.get('social_telegram')
        )
        
        db.session.add(salon)
        db.session.commit()
        flash('Салон успешно добавлен', 'success')
        return redirect(url_for('admin.salons'))
    
    categories = ['Парикмахерская', 'Ногтевой сервис', 'Косметология', 'SPA-салон', 
                  'Брови и ресницы', 'Тату и пирсинг', 'Мужской барбершоп', 'Солярий',
                  'Массажный салон', 'Эпиляция и депиляция', 'Свадебный салон',
                   'Салон красоты полного цикла']
    districts = ['Ленинский', 'Октябрьский']
    
    return render_template('admin/salon-form.html',
        title='Добавить салон',
        salon=None,
        categories=categories,
        districts=districts
    )


@admin_bp.route('/salons/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_salon(id):
    salon = Salon.query.get_or_404(id)
    
    if request.method == 'POST':
        # Обработка загруженного изображения
        if 'image_file' in request.files:
            file = request.files['image_file']
            if file and file.filename:
                # Удаляем старое изображение если оно не дефолтное
                if salon.image_url and not salon.image_url.startswith('/static/img/default'):
                    delete_uploaded_image(salon.image_url)
                
                uploaded_url, _ = save_uploaded_image(file, subfolder='salons', make_thumb=True)
                if uploaded_url:
                    salon.image_url = uploaded_url
        
        salon.name = request.form.get('name')
        salon.category = request.form.get('category')
        salon.description = request.form.get('description')
        salon.address = request.form.get('address')
        salon.district = request.form.get('district')
        salon.phone = request.form.get('phone')
        salon.working_hours = request.form.get('working_hours')
        salon.is_verified = 'is_verified' in request.form
        # Социальные сети
        salon.social_instagram = request.form.get('social_instagram')
        salon.social_vk = request.form.get('social_vk')
        salon.social_facebook = request.form.get('social_facebook')
        salon.social_telegram = request.form.get('social_telegram')
        
        db.session.commit()
        flash('Салон успешно обновлен', 'success')
        return redirect(url_for('admin.salons'))
    
    categories = ['Парикмахерская', 'Ногтевой сервис', 'Косметология', 'SPA-салон', 
                  'Брови и ресницы', 'Тату и пирсинг', 'Мужской барбершоп', 'Солярий',
                  'Массажный салон', 'Эпиляция и депиляция', 'Свадебный салон',
                   'Салон красоты полного цикла']
    districts = ['Ленинский', 'Октябрьский']
    
    return render_template('admin/salon-form.html',
        title='Редактировать салон',
        salon=salon,
        categories=categories,
        districts=districts
    )

@admin_bp.route('/salons/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_salon(id):
    salon = Salon.query.get_or_404(id)
    db.session.delete(salon)
    db.session.commit()
    flash('Салон успешно удален', 'success')
    return redirect(url_for('admin.salons'))

# ==================== УПРАВЛЕНИЕ УСЛУГАМИ ====================

@admin_bp.route('/services')
@login_required
@admin_required
def services():
    page = request.args.get('page', 1, type=int)
    salon_id = request.args.get('salon_id', type=int)
    per_page = 15
    
    query = Service.query
    if salon_id:
        query = query.filter(Service.salon_id == salon_id)
    
    pagination = query.order_by(Service.salon_id, Service.category).paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('admin/services.html',
        title='Управление услугами',
        services=pagination.items,
        pagination=pagination,
        salon_id=salon_id
    )

@admin_bp.route('/services/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_service():
    if request.method == 'POST':
        service = Service(
            salon_id=request.form.get('salon_id'),
            category=request.form.get('category'),
            name=request.form.get('name'),
            description=request.form.get('description'),
            price=request.form.get('price', type=int)
        )
        
        db.session.add(service)
        db.session.commit()
        flash('Услуга успешно добавлена', 'success')
        return redirect(url_for('admin.services'))
    
    salons = Salon.query.order_by(Salon.name).all()
    categories = ['Парикмахерские услуги', 'Маникюр', 'Педикюр', 'Косметология', 
                  'Массаж', 'SPA-процедуры', 'Эпиляция', 'Визаж', 'Брови и ресницы']
    
    return render_template('admin/service-form.html',
        title='Добавить услугу',
        service=None,
        salons=salons,
        categories=categories
    )

@admin_bp.route('/services/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_service(id):
    service = Service.query.get_or_404(id)
    
    if request.method == 'POST':
        service.salon_id = request.form.get('salon_id')
        service.category = request.form.get('category')
        service.name = request.form.get('name')
        service.description = request.form.get('description')
        service.price = request.form.get('price', type=int)
        
        db.session.commit()
        flash('Услуга успешно обновлена', 'success')
        return redirect(url_for('admin.services'))
    
    salons = Salon.query.order_by(Salon.name).all()
    categories = ['Парикмахерские услуги', 'Маникюр', 'Педикюр', 'Косметология', 
                  'Массаж', 'SPA-процедуры', 'Эпиляция', 'Визаж', 'Брови и ресницы']
    
    return render_template('admin/service-form.html',
        title='Редактировать услугу',
        service=service,
        salons=salons,
        categories=categories
    )

@admin_bp.route('/services/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_service(id):
    service = Service.query.get_or_404(id)
    db.session.delete(service)
    db.session.commit()
    flash('Услуга успешно удалена', 'success')
    return redirect(url_for('admin.services'))

# ==================== УПРАВЛЕНИЕ ПОЛЬЗОВАТЕЛЯМИ ====================

@admin_bp.route('/users')
@login_required
@admin_required
def users():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    per_page = 15
    
    query = User.query
    if search:
        query = query.filter(
            db.or_(
                User.email.ilike(f'%{search}%'),
                User.first_name.ilike(f'%{search}%'),
                User.last_name.ilike(f'%{search}%')
            )
        )
    
    pagination = query.order_by(desc(User.created_at)).paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('admin/users.html',
        title='Управление пользователями',
        users=pagination.items,
        pagination=pagination,
        search=search
    )

@admin_bp.route('/users/<int:id>/toggle-admin', methods=['POST'])
@login_required
@admin_required
def toggle_admin(id):
    user = User.query.get_or_404(id)
    if user.id == current_user.id:
        flash('Вы не можете изменить свои права администратора', 'error')
    else:
        user.is_admin = not user.is_admin
        db.session.commit()
        flash(f'Права администратора {"предоставлены" if user.is_admin else "отозваны"} для {user.email}', 'success')
    
    return redirect(url_for('admin.users'))

@admin_bp.route('/users/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(id):
    user = User.query.get_or_404(id)
    if user.id == current_user.id:
        flash('Вы не можете удалить свою учетную запись', 'error')
    else:
        db.session.delete(user)
        db.session.commit()
        flash(f'Пользователь {user.email} успешно удален', 'success')
    
    return redirect(url_for('admin.users'))

# ==================== УПРАВЛЕНИЕ ОТЗЫВАМИ ====================

@admin_bp.route('/reviews')
@login_required
@admin_required
def reviews():
    page = request.args.get('page', 1, type=int)
    per_page = 15
    
    pagination = Review.query.order_by(desc(Review.created_at)).paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('admin/reviews.html',
        title='Управление отзывами',
        reviews=pagination.items,
        pagination=pagination
    )

@admin_bp.route('/reviews/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_review(id):
    review = Review.query.get_or_404(id)
    salon_id = review.salon_id
    
    db.session.delete(review)
    
    # Обновляем рейтинг салона
    salon = Salon.query.get(salon_id)
    if salon:
        all_reviews = Review.query.filter_by(salon_id=salon_id).all()
        if all_reviews:
            avg_rating = sum(r.rating for r in all_reviews) / len(all_reviews)
            salon.rating = round(avg_rating, 1)
        else:
            salon.rating = 0.0
        salon.reviews_count = len(all_reviews)
    
    db.session.commit()
    flash('Отзыв успешно удален', 'success')
    return redirect(url_for('admin.reviews'))

# ==================== УПРАВЛЕНИЕ БЛОГОМ ====================

@admin_bp.route('/blog/posts')
@login_required
@admin_required
def blog_posts():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    per_page = 10
    
    query = BlogPost.query
    if search:
        query = query.filter(
            db.or_(
                BlogPost.title.ilike(f'%{search}%'),
                BlogPost.content.ilike(f'%{search}%')
            )
        )
    
    pagination = query.order_by(desc(BlogPost.created_at)).paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('admin/blog-posts.html',
        title='Управление статьями',
        posts=pagination.items,
        pagination=pagination,
        search=search
    )

@admin_bp.route('/blog/posts/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_blog_post():
    if request.method == 'POST':
        import re
        slug = request.form.get('title')
        slug = re.sub(r'[^\w\s-]', '', slug.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        
        existing = BlogPost.query.filter_by(slug=slug).first()
        if existing:
            slug = f"{slug}-{datetime.now().timestamp()}"
        
        # Обработка загруженного изображения
        image_url = '/static/img/blog-default.jpg'
        if 'image_file' in request.files:
            file = request.files['image_file']
            if file and file.filename:
                uploaded_url, _ = save_uploaded_image(file, subfolder='blog', make_thumb=True)
                if uploaded_url:
                    image_url = uploaded_url

        elif request.form.get('image_url'):
            image_url = request.form.get('image_url')
        
        post = BlogPost(
            title=request.form.get('title'),
            slug=slug,
            excerpt=request.form.get('excerpt'),
            content=request.form.get('content'),
            author=request.form.get('author', 'Администратор'),
            category=request.form.get('category'),
            image_url=image_url,
            is_published='is_published' in request.form
        )
        
        db.session.add(post)
        db.session.commit()
        
        # Добавляем теги
        tags_str = request.form.get('tags', '')
        if tags_str:
            tag_names = [t.strip().lower() for t in tags_str.split(',') if t.strip()]
            for tag_name in tag_names:
                tag = BlogTag.query.filter_by(name=tag_name).first()
                if not tag:
                    tag_slug = re.sub(r'[^\w\s-]', '', tag_name.lower())
                    tag_slug = re.sub(r'[-\s]+', '-', tag_slug)
                    tag = BlogTag(name=tag_name, slug=tag_slug)
                    db.session.add(tag)
                    db.session.flush()
                if tag not in post.tags:
                    post.tags.append(tag)
            db.session.commit()
        
        flash('Статья успешно добавлена', 'success')
        return redirect(url_for('admin.blog_posts'))
    
    categories = ['Красота и уход', 'Тренды', 'Советы', 'Здоровье', 'Новости']
    
    return render_template('admin/blog-post-form.html',
        title='Добавить статью',
        post=None,
        categories=categories
    )


@admin_bp.route('/delete-image', methods=['POST'])
@login_required
@admin_required
def delete_image_route():
    """Удаление изображения"""
    data = request.get_json()
    image_url = data.get('image_url')
    
    if image_url and delete_uploaded_image(image_url):
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'Не удалось удалить изображение'}), 400


@admin_bp.route('/blog/posts/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_blog_post(id):
    post = BlogPost.query.get_or_404(id)
    
    if request.method == 'POST':
        import re
        
        # Обработка загруженного изображения
        if 'image_file' in request.files:
            file = request.files['image_file']
            if file and file.filename:
                # Удаляем старое изображение если оно не дефолтное
                if post.image_url and not post.image_url.startswith('/static/img/blog-default'):
                    delete_uploaded_image(post.image_url)
                
                uploaded_url, _ = save_uploaded_image(file, subfolder='blog', make_thumb=True)
                if uploaded_url:
                    post.image_url = uploaded_url


        elif request.form.get('image_url'):
            post.image_url = request.form.get('image_url')
        
        post.title = request.form.get('title')
        post.excerpt = request.form.get('excerpt')
        post.content = request.form.get('content')
        post.author = request.form.get('author', 'Администратор')
        post.category = request.form.get('category')
        post.is_published = 'is_published' in request.form
        post.updated_at = datetime.now()
        
        # Обновляем теги
        post.tags.clear()
        tags_str = request.form.get('tags', '')
        if tags_str:
            tag_names = [t.strip().lower() for t in tags_str.split(',') if t.strip()]
            for tag_name in tag_names:
                tag = BlogTag.query.filter_by(name=tag_name).first()
                if not tag:
                    tag_slug = re.sub(r'[^\w\s-]', '', tag_name.lower())
                    tag_slug = re.sub(r'[-\s]+', '-', tag_slug)
                    tag = BlogTag(name=tag_name, slug=tag_slug)
                    db.session.add(tag)
                    db.session.flush()
                if tag not in post.tags:
                    post.tags.append(tag)
        
        db.session.commit()
        flash('Статья успешно обновлена', 'success')
        return redirect(url_for('admin.blog_posts'))
    
    categories = ['Красота и уход', 'Тренды', 'Советы', 'Здоровье', 'Новости']
    current_tags = ', '.join([tag.name for tag in post.tags])
    
    return render_template('admin/blog-post-form.html',
        title='Редактировать статью',
        post=post,
        categories=categories,
        current_tags=current_tags
    )

@admin_bp.route('/blog/posts/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_blog_post(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    flash('Статья успешно удалена', 'success')
    return redirect(url_for('admin.blog_posts'))

@admin_bp.route('/blog/comments')
@login_required
@admin_required
def blog_comments():
    page = request.args.get('page', 1, type=int)
    per_page = 15
    
    pagination = BlogComment.query.order_by(desc(BlogComment.created_at)).paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('admin/blog-comments.html',
        title='Управление комментариями',
        comments=pagination.items,
        pagination=pagination
    )

@admin_bp.route('/blog/comments/<int:id>/approve', methods=['POST'])
@login_required
@admin_required
def approve_comment(id):
    comment = BlogComment.query.get_or_404(id)
    comment.is_approved = True
    db.session.commit()
    flash('Комментарий опубликован', 'success')
    return redirect(url_for('admin.blog_comments'))

@admin_bp.route('/blog/comments/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_blog_comment(id):
    comment = BlogComment.query.get_or_404(id)
    db.session.delete(comment)
    db.session.commit()
    flash('Комментарий удален', 'success')
    return redirect(url_for('admin.blog_comments'))

@admin_bp.route('/blog/tags')
@login_required
@admin_required
def blog_tags():
    tags = BlogTag.query.order_by(BlogTag.name).all()
    
    # Подсчет количества постов для каждого тега
    from models import post_tags
    for tag in tags:
        tag.post_count = db.session.query(func.count(post_tags.c.post_id)).filter(
            post_tags.c.tag_id == tag.id
        ).scalar() or 0
    
    return render_template('admin/blog-tags.html',
        title='Управление тегами',
        tags=tags
    )

@admin_bp.route('/blog/tags/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_blog_tag(id):
    tag = BlogTag.query.get_or_404(id)
    db.session.delete(tag)
    db.session.commit()
    flash('Тег успешно удален', 'success')
    return redirect(url_for('admin.blog_tags'))