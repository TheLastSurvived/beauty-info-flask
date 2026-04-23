import random
from app import app, db
from models import User, Salon, Review
from datetime import datetime, timedelta

# Список имен для генерации пользователей
first_names = [
    'Александр', 'Дмитрий', 'Максим', 'Артем', 'Егор', 'Иван', 'Андрей', 'Сергей',
    'Анна', 'Елена', 'Мария', 'Ольга', 'Татьяна', 'Наталья', 'Екатерина', 'Ирина'
]

last_names = [
    'Иванов', 'Петров', 'Сидоров', 'Смирнов', 'Кузнецов', 'Попов', 'Васильев',
    'Иванова', 'Петрова', 'Сидорова', 'Смирнова', 'Кузнецова', 'Попова', 'Васильева'
]

# Отзывы по категориям (шаблоны)
review_templates = {
    'Парикмахерская': [
        {'text': 'Отличная стрижка, мастер профессионал своего дела! Обязательно вернусь снова.', 'tags': 'профессионализм, качество, атмосфера'},
        {'text': 'Понравилось отношение к клиентам. Очень вежливый персонал, уютная обстановка.', 'tags': 'сервис, вежливость, уют'},
        {'text': 'Делала окрашивание - результат превзошел ожидания. Волосы стали как после салона в Европе!', 'tags': 'окрашивание, качество, цвет'},
        {'text': 'Нормальная парикмахерская, но цены кусаются. Стрижка средняя, не вау.', 'tags': 'стрижка, цены'},
        {'text': 'Быстро, качественно, недорого. Супер место!', 'tags': 'скорость, качество, цена'},
        {'text': 'Мастер учла все пожелания, дала отличные советы по уходу. Спасибо!', 'tags': 'консультация, уход, внимание'},
        {'text': 'Ужасная стрижка! Испортили волосы, не рекомендую.', 'tags': 'негатив, стрижка'},
        {'text': 'Отличный барбершоп для мужчин. Классические стрижки на высоте.', 'tags': 'мужская стрижка, барбершоп'},
    ],
    'Ногтевой сервис': [
        {'text': 'Маникюр держится 3 недели! Очень аккуратная работа.', 'tags': 'стойкость, аккуратность, маникюр'},
        {'text': 'Лучший мастер по наращиванию! Форма идеальная, ни одного скола.', 'tags': 'наращивание, опыт, качество'},
        {'text': 'Большой выбор дизайнов. Сделали именно то, что я хотела.', 'tags': 'дизайн, выбор, креатив'},
        {'text': 'Очень гигиенично, одноразовые инструменты. Это важно!', 'tags': 'гигиена, безопасность'},
        {'text': 'Педикюр - сказка! Ножки как у младенца.', 'tags': 'педикюр, уход'},
        {'text': 'Запись за 2 недели, очень трудно попасть. Но оно того стоит.', 'tags': 'запись, ожидание'},
        {'text': 'Сделали сложный дизайн с лепкой - великолепно выглядит!', 'tags': 'дизайн, лепка'},
    ],
    'Косметология': [
        {'text': 'Чистка лица прошла практически безболезненно. Кожа сияет!', 'tags': 'чистка, результат, кожа'},
        {'text': 'Отличный косметолог, подобрала индивидуальный уход. Акне прошло за месяц.', 'tags': 'лечение, акне, уход'},
        {'text': 'Аппаратная косметология сделала чудо - подтянула овал лица.', 'tags': 'аппаратная, лифтинг'},
        {'text': 'Дорого, но результат виден сразу. Косметика отличная.', 'tags': 'цена, качество, косметика'},
        {'text': 'Очень приятная атмосфера, расслабляющие процедуры. Рекомендую SPA-программы.', 'tags': 'атмосфера, релакс, SPA'},
        {'text': 'Сделала пилинг - лицо обгорело! Не рекомендую этого мастера.', 'tags': 'негатив, пилинг, ошибка'},
    ],
    'Мужской барбершоп': [
        {'text': 'Классическая мужская стрижка - идеально. Бритье опасной бритвой отдельный кайф!', 'tags': 'бритье, классика, стиль'},
        {'text': 'Атмосфера чисто мужская, футбол, хорошая музыка. Супер место!', 'tags': 'атмосфера, уют'},
        {'text': 'Бороду привели в порядок - теперь выгляжу на миллион.', 'tags': 'борода, уход', 'rating': 5},
        {'text': 'Стрижка норм, но ждать пришлось 40 минут даже по записи.', 'tags': 'ожидание, сервис', 'rating': 3},
    ],
    'SPA-салон': [
        {'text': 'Расслабилась на 100%. Массаж, обертывание, чай - все на высшем уровне.', 'tags': 'релакс, массаж'},
        {'text': 'Очень чисто, приятные ароматы, профессионалы своего дела.', 'tags': 'чистота, сервис'},
        {'text': 'Ходим с мужем на пару - отличный отдых. Рекомендую!', 'tags': 'парное посещение, отдых'},
    ],
    'Брови и ресницы': [
        {'text': 'Брови - огонь! Форма идеальная, цвет подошел отлично.', 'tags': 'брови, форма', 'rating': 5},
        {'text': 'Ламинирование ресниц - глаза раскрылись. Просыпаюсь красивой!', 'tags': 'ламинирование, ресницы', 'rating': 5},
        {'text': 'Очень аккуратно, без боли. Теперь только к этому мастеру.', 'tags': 'аккуратность, доверие'},
    ],
    'Тату и пирсинг': [
        {'text': 'Отличная работа, линии ровные, зажило быстро. Тату мечты!', 'tags': 'татуировка, качество'},
        {'text': 'Пирсинг сделали быстро, почти безболезненно. Все стерильно.', 'tags': 'пирсинг, безопасность'},
        {'text': 'Эскиз разработали индивидуально, учли все пожелания. Спасибо!', 'tags': 'индивидуально, креатив'},
    ],
    'Свадебный салон': [
        {'text': 'Нашла платье мечты с третьего раза. Девочки-консультанты - ангелы!', 'tags': 'свадебное платье, консультация'},
        {'text': 'Очень большой выбор, есть на любой бюджет. Рекомендую.', 'tags': 'выбор, бюджет'},
        {'text': 'Платье пришлось подгонять, но сделали идеально. Спасибо!', 'tags': 'подгонка, сервис'},
    ],
    'default': [
        {'text': 'Отличный салон! Всё понравилось, обязательно вернусь.', 'tags': 'отлично, рекомендую', 'rating': 5},
        {'text': 'Хороший сервис, приятный персонал. Понравилось.', 'tags': 'сервис, персонал', 'rating': 4},
        {'text': 'Нормально, но есть куда расти. Цены выше среднего.', 'tags': 'нормально, цены', 'rating': 3},
        {'text': 'Разочарован. Не соответствует ожиданиям.', 'tags': 'разочарование', 'rating': 2},
        {'text': 'Отвратительное обслуживание! Не рекомендую.', 'tags': 'негатив', 'rating': 1},
        {'text': 'Спасибо мастерам за красоту! Теперь постоянный клиент.', 'tags': 'благодарность, постоянство', 'rating': 5},
    ]
}

def generate_users(num_users=30):
    """Генерация случайных пользователей"""
    users = []
    
    # Администратор (уже может быть)
    admin = User.query.filter_by(email='admin@example.com').first()
    if not admin:
        admin = User(
            email='admin@example.com',
            first_name='Администратор',
            last_name='Системы',
            is_admin=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        users.append(admin)
        print("  ✅ Создан администратор: admin@example.com / admin123")
    
    for i in range(num_users):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        email = f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 999)}@example.com"
        
        user = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_admin=False,
            phone=f"+375 (29) {random.randint(1111111, 9999999)}" if random.random() > 0.3 else None
        )
        user.set_password('password123')
        db.session.add(user)
        users.append(user)
    
    db.session.commit()
    print(f"  ✅ Создано {num_users} обычных пользователей (пароль: password123)")
    return users

def generate_reviews(min_reviews_per_salon=2, max_reviews_per_salon=10):
    """Генерация отзывов для салонов"""
    salons = Salon.query.all()
    users = User.query.filter_by(is_admin=False).all()
    
    if not users:
        print("⚠️ Нет пользователей. Сначала создайте пользователей!")
        return
    
    total_reviews = 0
    
    for salon in salons:
        # Определяем количество отзывов для салона
        num_reviews = random.randint(min_reviews_per_salon, max_reviews_per_salon)
        
        # Получаем шаблоны для категории салона
        category_templates = review_templates.get(salon.category, review_templates['default'])
        
        # Создаем отзывы
        reviews_for_this = []
        for i in range(num_reviews):
            # Выбираем случайные даты за последние 6 месяцев
            days_ago = random.randint(1, 180)
            created_at = datetime.now() - timedelta(days=days_ago)
            
            # Выбираем шаблон
            template = random.choice(category_templates)
            
            # Рейтинг (с нормальным распределением)
            if 'rating' in template:
                rating = template['rating']
            else:
                # 60% положительные, 30% средние, 10% негативные
                r = random.random()
                if r < 0.6:
                    rating = random.choice([4, 5])
                elif r < 0.9:
                    rating = 3
                else:
                    rating = random.choice([1, 2])
            
            # Выбираем случайного пользователя
            user = random.choice(users)
            
            # Немного модифицируем текст под конкретный салон
            text = template['text']
            if random.random() > 0.7:
                praise_words = ['Очень рекомендую!', 'Супер место!', 'Лучший в городе!', 'Приду еще!']
                text += ' ' + random.choice(praise_words)
            
            review = Review(
                salon_id=salon.id,
                user_id=user.id,
                author_name=f"{user.first_name} {user.last_name}" if user.last_name else user.first_name,
                rating=rating,
                text=text,
                tags=template['tags'],
                created_at=created_at
            )
            db.session.add(review)
            reviews_for_this.append(review)
        
        # Обновляем рейтинг салона
        if reviews_for_this:
            all_reviews = Review.query.filter_by(salon_id=salon.id).all()
            if all_reviews:
                avg_rating = sum(r.rating for r in all_reviews) / len(all_reviews)
                salon.rating = round(avg_rating, 1)
            salon.reviews_count = len(all_reviews)
        
        total_reviews += num_reviews
        print(f"  📝 {salon.name}: добавлено {num_reviews} отзывов, рейтинг {salon.rating}")
    
    db.session.commit()
    print(f"\n✅ Всего добавлено отзывов: {total_reviews}")
    
    # Статистика по рейтингам
    print("\n📊 Статистика рейтингов:")
    stats = db.session.query(Review.rating, db.func.count(Review.id)).group_by(Review.rating).all()
    for rating, count in sorted(stats):
        emoji = "⭐" * rating + "☆" * (5 - rating)
        print(f"   {emoji} {rating} звезд(ы): {count} отзывов")

def clear_reviews():
    """Очистка всех отзывов и сброс рейтингов"""
    print("⚠️ Очистка всех отзывов...")
    Review.query.delete()
    
    # Сбрасываем рейтинги у салонов
    for salon in Salon.query.all():
        salon.rating = 0.0
        salon.reviews_count = 0
    
    db.session.commit()
    print("✅ Отзывы удалены, рейтинги сброшены")

def clear_users():
    """Очистка пользователей (кроме админа)"""
    print("⚠️ Очистка обычных пользователей...")
    User.query.filter_by(is_admin=False).delete()
    db.session.commit()
    print("✅ Обычные пользователи удалены")

def main():
    with app.app_context():
        print("🚀 Генерация пользователей и отзывов...")
        print("=" * 50)
        
        # Проверяем, есть ли салоны
        salon_count = Salon.query.count()
        if salon_count == 0:
            print("❌ Нет салонов в базе! Сначала импортируйте салоны.")
            return
        
        print(f"📊 В базе {salon_count} салонов")
        
        # Очищаем старые отзывы и обычных пользователей
        response = input("Очистить существующие отзывы и обычных пользователей? (y/n): ")
        if response.lower() == 'y':
            clear_reviews()
            clear_users()
        
        # Создаем пользователей
        print("\n👥 Создание пользователей...")
        users = generate_users(num_users=30)
        
        # Генерируем отзывы
        print("\n✍️ Генерация отзывов...")
        generate_reviews(min_reviews_per_salon=2, max_reviews_per_salon=15)
        
        print("\n✨ Готово!")
        print("\n📝 Для входа в систему:")
        print("   Администратор: admin@example.com / admin123")
        print("   Пользователь: любой из созданных / password123")

if __name__ == '__main__':
    main()