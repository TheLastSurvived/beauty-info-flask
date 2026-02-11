# seed_reviews_comments.py - заполнение отзывов и комментариев
import sys
import os
import random
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

SQLALCHEMY_DATABASE_URL = "sqlite:///./instance/database.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
import models

# Данные для генерации
REVIEW_AUTHORS = [
    "Анна", "Мария", "Екатерина", "Ольга", "Ирина", "Наталья", "Татьяна", "Виктория",
    "Александр", "Сергей", "Дмитрий", "Андрей", "Михаил", "Алексей", "Владимир", "Иван",
    "Юлия", "Елена", "Людмила", "Светлана", "Галина", "Валентина", "Лариса", "Маргарита",
    "Артем", "Константин", "Николай", "Павел", "Роман", "Станислав"
]

# Тексты отзывов к салонам
SALON_REVIEWS_POSITIVE = [
    "Отличный салон! Мастер внимательно выслушал все пожелания и сделал даже лучше, чем я ожидала.",
    "Очень довольна результатом. Профессионалы своего дела, работают качественно и аккуратно.",
    "Приятная атмосфера, чистота и порядок. Персонал вежливый и внимательный. Буду рекомендовать друзьям.",
    "Впервые посетила этот салон и осталась в восторге. Отличное соотношение цены и качества.",
    "Хожу сюда уже несколько лет, всегда довольна. Мастера постоянно совершенствуются, следят за трендами.",
    "Прекрасный сервис! Все сделано быстро и качественно. Особенно понравилось отношение к клиенту.",
    "После посещения этого салона чувствую себя обновленной. Процедуры выполнены на высшем уровне.",
    "Удобное расположение, приятные цены. Обслуживание на высоте. Обязательно вернусь еще.",
    "Мастер проявил настоящий профессионализм. Результат превзошел все ожидания. Спасибо огромное!",
    "Чисто, уютно, комфортно. Идеальное место для того, чтобы привести себя в порядок и расслабиться.",
    "Очень качественные услуги. Видно, что мастера любят свою работу и делают ее с душой.",
    "Была на нескольких процедурах, все выполнено безупречно. Теперь это мой любимый салон.",
    "Отличные специалисты, современное оборудование. Чувствуется забота о клиентах.",
    "Пришла с проблемой, ушла с решением. Мастер дал ценные советы по уходу. Очень благодарна!",
    "Салон соответствует всем моим требованиям: качество, чистота, вежливость персонала. 5 звезд!"
]

SALON_REVIEWS_NEUTRAL = [
    "В целом неплохо, но есть небольшие недочеты. Мастер немного торопился.",
    "Услуга выполнена качественно, но ожидала большего внимания к деталям.",
    "Нормальный салон, цены средние. Ничего особенного, но и нареканий нет.",
    "Сделали все как просила, но атмосфера могла бы быть более дружелюбной.",
    "Результат удовлетворительный, но процесс занял больше времени, чем обещали.",
    "В принципе все нормально, но есть салоны и получше в этом районе.",
    "Сделали свою работу, но без особого энтузиазма. В целом можно сходить.",
    "Цены немного завышены для такого уровня сервиса, но качество на приемлемом уровне."
]

SALON_REVIEWS_NEGATIVE = [
    "Не понравилось. Мастер был невнимателен, результат не соответствует ожиданиям.",
    "Очень долго ждала своей очереди, хотя записывалась заранее. Сервис оставляет желать лучшего.",
    "Цены высокие, а качество услуг среднее. Есть более достойные варианты в городе.",
    "Не рекомендую. Сделали некачественно, пришлось переделывать в другом салоне.",
    "Персонал грубый и невнимательный. Атмосфера неприятная. Больше не пойду.",
    "Обещали одно, сделали другое. Очень разочарована. Деньги потрачены зря.",
    "Грязно и неуютно. Инструменты выглядели нестерильными. Не советую посещать."
]

# Теги для отзывов
REVIEW_TAGS = [
    "профессионализм", "чистота", "уют", "качество", "сервис", 
    "результат", "цены", "атмосфера", "мастера", "оборудование",
    "внимательность", "скорость", "вежливость", "комфорт", "гигиена",
    "индивидуальный подход", "современные технологии", "удобство", "рекомендации"
]

# Тексты комментариев к блогу
BLOG_COMMENTS = [
    "Отличная статья! Очень полезная и информативная. Спасибо автору!",
    "Много нового узнала из этой статьи. Буду применять советы на практике.",
    "Очень актуальная тема. Жду продолжения на эту же тему!",
    "Статья написана понятным языком, все разложено по полочкам. Спасибо!",
    "Как раз то, что я искала! Очень своевременная информация.",
    "Интересный подход, никогда раньше об этом не задумывалась. Спасибо за идеи!",
    "Отличные советы, буду рекомендовать статью друзьям и знакомым.",
    "Очень понравилась структура статьи - все четко и по делу, без воды.",
    "Автор молодец! Поднял важную тему и дал практические рекомендации.",
    "Читала с большим интересом. Узнала много полезного для себя.",
    "Статья заслуживает внимания. Много полезных лайфхаков и советов.",
    "Спасибо за подробное объяснение. Теперь все понятно!",
    "Очень профессионально написано. Видно, что автор разбирается в теме.",
    "Отличный материал! Сохранила статью в закладках для повторного чтения.",
    "Полезная информация, особенно для новичков в этой теме.",
    "Очень впечатлила статья. Много практических советов, которые можно применить сразу.",
    "Спасибо за качественный контент! Читаю ваш блог регулярно.",
    "Статья ответила на все мои вопросы по этой теме. Благодарю!",
    "Очень доступно объяснено. Даже сложные моменты стали понятными.",
    "Отличная работа! Жду новых статей от этого автора.",
    "Много полезных нюансов, о которых я раньше не знала. Спасибо!",
    "Статья помогла решить мою проблему. Очень благодарна автору!",
    "Информативно и интересно. Читала на одном дыхании.",
    "Хорошо структурированная статья с практическими примерами. Супер!",
    "Спасибо за экспертный взгляд на проблему. Много ценных инсайтов."
]

# Электронные почты для комментариев
COMMENT_EMAILS = [
    "anna@example.com", "maria@example.com", "irina@example.com", "olga@example.com",
    "ekaterina@example.com", "natalia@example.com", "tatyana@example.com", "victoria@example.com",
    "alexander@example.com", "sergey@example.com", "dmitry@example.com", "andrey@example.com",
    "mikhail@example.com", "alexey@example.com", "vladimir@example.com", "ivan@example.com",
    "yulia@example.com", "elena@example.com", "svetlana@example.com", "galina@example.com"
]

def seed_reviews_and_comments():
    """Основная функция заполнения отзывов и комментариев"""
    db = SessionLocal()
    
    try:
        print("🔄 Начинаем заполнение отзывов и комментариев...")
        
        # Получаем существующие данные
        users = db.query(models.User).all()
        salons = db.query(models.Salon).all()
        posts = db.query(models.BlogPost).all()
        
        if not salons:
            print("❌ Нет салонов в базе. Сначала запустите seed_salons.py")
            return
        
        if not posts:
            print("❌ Нет постов в блоге. Сначала запустите seed_blog.py")
            return
        
        print(f"📊 Найдено: {len(salons)} салонов, {len(posts)} постов, {len(users)} пользователей")
        
        # 1. Очищаем существующие отзывы и комментарии (опционально)
        print("🧹 Очищаем существующие отзывы и комментарии...")
        db.query(models.Review).delete()
        db.query(models.BlogComment).delete()
        db.commit()
        
        # 2. Создаем отзывы к салонам
        print("⭐ Создаем отзывы для салонов...")
        
        for salon in salons:
            # Количество отзывов зависит от рейтинга салона
            if salon.rating >= 4.0:
                num_reviews = random.randint(8, 15)  # У популярных салонов больше отзывов
            elif salon.rating >= 3.0:
                num_reviews = random.randint(5, 10)
            else:
                num_reviews = random.randint(2, 6)
            
            # Обновляем счетчик отзывов
            salon.reviews_count = num_reviews
            
            # Создаем отзывы
            for i in range(num_reviews):
                # Распределение оценок в зависимости от рейтинга салона
                if salon.rating >= 4.5:
                    rating_weights = [0.02, 0.03, 0.05, 0.2, 0.7]  # 70% пятерок
                elif salon.rating >= 4.0:
                    rating_weights = [0.05, 0.05, 0.1, 0.3, 0.5]   # 50% пятерок
                elif salon.rating >= 3.5:
                    rating_weights = [0.1, 0.1, 0.2, 0.3, 0.3]     # 30% пятерок
                elif salon.rating >= 3.0:
                    rating_weights = [0.15, 0.15, 0.3, 0.25, 0.15] # 15% пятерок
                else:
                    rating_weights = [0.3, 0.3, 0.2, 0.15, 0.05]   # 5% пятерок
                
                rating = random.choices([1, 2, 3, 4, 5], weights=rating_weights)[0]
                
                # Выбираем текст отзыва в зависимости от оценки
                if rating >= 4:
                    text = random.choice(SALON_REVIEWS_POSITIVE)
                elif rating == 3:
                    text = random.choice(SALON_REVIEWS_NEUTRAL)
                else:
                    text = random.choice(SALON_REVIEWS_NEGATIVE)
                
                # Случайный пользователь (или аноним)
                user = random.choice(users) if users and random.random() > 0.3 else None
                
                # Случайная дата отзыва (в течение последних 2 лет)
                days_ago = random.randint(1, 730)
                created_at = datetime.now() - timedelta(days=days_ago)
                
                # Случайные теги (2-4 тега)
                tags = ", ".join(random.sample(REVIEW_TAGS, random.randint(2, 4)))
                
                review = models.Review(
                    salon_id=salon.id,
                    author_name=random.choice(REVIEW_AUTHORS) if not user else f"{user.first_name} {user.last_name}",
                    rating=rating,
                    text=text,
                    tags=tags,
                    created_at=created_at,
                    user_id=user.id if user else None
                )
                db.add(review)
            
            # Обновляем рейтинг салона на основе отзывов
            db.flush()
        
        db.commit()
        print(f"✅ Создано отзывов: {db.query(models.Review).count()}")
        
        # 3. Создаем комментарии к постам блога
        print("💬 Создаем комментарии к постам блога...")
        
        for post in posts:
            # Количество комментариев зависит от популярности поста
            if post.views_count >= 3000:
                num_comments = random.randint(8, 15)
            elif post.views_count >= 1000:
                num_comments = random.randint(5, 10)
            else:
                num_comments = random.randint(2, 6)
            
            for i in range(num_comments):
                # Случайный пользователь (или аноним)
                user = random.choice(users) if users and random.random() > 0.4 else None
                
                # Случайная дата комментария (от 0 до 60 дней после публикации)
                days_after = random.randint(0, 60)
                comment_date = post.created_at + timedelta(days=days_after)
                
                # 90% комментариев одобрены
                is_approved = random.random() > 0.1
                
                comment = models.BlogComment(
                    post_id=post.id,
                    author_name=random.choice(REVIEW_AUTHORS) if not user else f"{user.first_name} {user.last_name}",
                    author_email=random.choice(COMMENT_EMAILS) if not user else user.email,
                    content=random.choice(BLOG_COMMENTS),
                    is_approved=is_approved,
                    created_at=comment_date,
                    user_id=user.id if user else None
                )
                db.add(comment)
        
        db.commit()
        print(f"✅ Создано комментариев: {db.query(models.BlogComment).count()}")
        
        # 4. Обновляем статистику салонов
        print("📈 Обновляем статистику салонов...")
        
        for salon in salons:
            # Получаем все отзывы салона
            salon_reviews = db.query(models.Review).filter(models.Review.salon_id == salon.id).all()
            
            if salon_reviews:
                # Пересчитываем средний рейтинг
                total_rating = sum(review.rating for review in salon_reviews)
                avg_rating = total_rating / len(salon_reviews)
                
                salon.rating = round(avg_rating, 1)
                salon.reviews_count = len(salon_reviews)
        
        db.commit()
        
        # 5. Выводим статистику
        print("\n" + "="*50)
        print("✅ Отзывы и комментарии успешно созданы!")
        print("="*50)
        
        # Общая статистика
        total_reviews = db.query(models.Review).count()
        total_comments = db.query(models.BlogComment).count()
        approved_comments = db.query(models.BlogComment).filter(models.BlogComment.is_approved == True).count()
        
        print(f"📊 Общая статистика:")
        print(f"   • Отзывов о салонах: {total_reviews}")
        print(f"   • Комментариев к блогу: {total_comments}")
        print(f"   • Одобренных комментариев: {approved_comments} ({approved_comments/total_comments*100:.1f}%)")
        
        # Статистика по рейтингам
        print(f"\n⭐ Распределение оценок в отзывах:")
        for rating in range(1, 6):
            count = db.query(models.Review).filter(models.Review.rating == rating).count()
            percentage = count / total_reviews * 100 if total_reviews > 0 else 0
            stars = "★" * rating
            print(f"   {stars} ({rating}): {count} отзывов ({percentage:.1f}%)")
        
        # Топ салонов по количеству отзывов
        print(f"\n🏆 Топ салонов по количеству отзывов:")
        from sqlalchemy import func
        top_salons_reviews = db.query(
            models.Salon.name,
            models.Salon.district,
            models.Salon.rating,
            func.count(models.Review.id).label('review_count')
        ).join(models.Review).group_by(models.Salon.id).order_by(func.count(models.Review.id).desc()).limit(5).all()
        
        for i, salon in enumerate(top_salons_reviews, 1):
            print(f"   {i}. {salon.name} ({salon.district}) - {salon.review_count} отзывов, рейтинг {salon.rating}")
        
        # Топ постов по количеству комментариев
        print(f"\n📝 Топ постов блога по количеству комментариев:")
        top_posts = db.query(
            models.BlogPost.title,
            func.count(models.BlogComment.id).label('comment_count')
        ).join(models.BlogComment).group_by(models.BlogPost.id).order_by(func.count(models.BlogComment.id).desc()).limit(5).all()
        
        for i, post in enumerate(top_posts, 1):
            print(f"   {i}. {post.title[:40]}... - {post.comment_count} комментариев")
        
        print("="*50)
        
        print("\n✨ Заполнение базы данных завершено успешно!")
        
    except Exception as e:
        print(f"\n❌ Ошибка при заполнении базы данных: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        raise e
    finally:
        db.close()

def create_test_users(db):
    """Создает тестовых пользователей, если их нет"""
    test_users = [
        {
            "email": "user1@example.com",
            "first_name": "Анна",
            "last_name": "Иванова",
            "password": "password123",
            "phone": "+79001112233"
        },
        {
            "email": "user2@example.com",
            "first_name": "Сергей",
            "last_name": "Петров",
            "password": "password123",
            "phone": "+79002223344"
        },
        {
            "email": "user3@example.com",
            "first_name": "Мария",
            "last_name": "Сидорова",
            "password": "password123",
            "phone": "+79003334455"
        },
        {
            "email": "admin@example.com",
            "first_name": "Администратор",
            "last_name": "Системы",
            "password": "admin123",
            "phone": "+79004445566"
        }
    ]
    
    for user_data in test_users:
        existing_user = db.query(models.User).filter(models.User.email == user_data["email"]).first()
        if not existing_user:
            user = models.User(
                email=user_data["email"],
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                phone=user_data["phone"],
                avatar_url="/static/img/avatar.png"
            )
            user.set_password(user_data["password"])
            db.add(user)
            print(f"👤 Создан пользователь: {user_data['email']}")
    
    db.commit()

if __name__ == "__main__":
    db = SessionLocal()
    
    # Создаем тестовых пользователей, если их нет
    print("👤 Проверяем наличие пользователей...")
    if not db.query(models.User).first():
        print("👤 Создаем тестовых пользователей...")
        create_test_users(db)
    else:
        print("👤 Пользователи уже существуют в базе")
    
    db.close()
    
    # Запускаем заполнение отзывов и комментариев
    seed_reviews_and_comments()

input()