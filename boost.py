from app import app, db
from models import Review, Salon
from sqlalchemy import func
import random

def boost_reviews():
    """Поднимает рейтинг отзывов на 1 балл (но не выше 5)"""
    
    with app.app_context():
        print("🚀 ПОДНЯТИЕ РЕЙТИНГА ОТЗЫВОВ")
        print("=" * 50)
        
        # Получаем все отзывы
        reviews = Review.query.all()
        print(f"Всего отзывов: {len(reviews)}")
        
        updated_count = 0
        for review in reviews:
            old_rating = review.rating
            # Поднимаем на 1 балл, но не выше 5
            new_rating = min(old_rating + 1, 5)
            
            if new_rating != old_rating:
                review.rating = new_rating
                updated_count += 1
        
        db.session.commit()
        print(f"✅ Обновлено {updated_count} отзывов")
        
        # Обновляем рейтинги салонов
        print("\n🔄 Пересчет рейтингов салонов...")
        
        for salon in Salon.query.all():
            reviews_list = Review.query.filter_by(salon_id=salon.id).all()
            if reviews_list:
                avg_rating = sum(r.rating for r in reviews_list) / len(reviews_list)
                salon.rating = round(avg_rating, 1)
                salon.reviews_count = len(reviews_list)
                print(f"  {salon.name}: {salon.rating} ⭐ ({salon.reviews_count} отзывов)")
        
        db.session.commit()
        
        # Общая статистика
        print("\n📊 НОВАЯ СТАТИСТИКА:")
        all_reviews_avg = db.session.query(func.avg(Review.rating)).scalar() or 0
        print(f"  Средний рейтинг всех отзывов: {round(all_reviews_avg, 1)}")
        
        rating_distribution = db.session.query(
            Review.rating, func.count(Review.id)
        ).group_by(Review.rating).all()
        
        print("\n  Распределение оценок:")
        for rating, count in sorted(rating_distribution):
            bar = "█" * (count // 5)
            print(f"    {rating} ⭐: {count} отзывов {bar}")
        
        print("\n✨ Готово!")

def set_minimum_rating(min_rating=4):
    """Устанавливает минимальный рейтинг для всех отзывов"""
    
    with app.app_context():
        print(f"🎯 УСТАНОВКА МИНИМАЛЬНОГО РЕЙТИНГА = {min_rating}")
        print("=" * 50)
        
        reviews = Review.query.all()
        updated_count = 0
        
        for review in reviews:
            if review.rating < min_rating:
                old_rating = review.rating
                # Поднимаем до минимального, но можно добавить случайность
                # new_rating = min_rating + random.choice([0, 0.5, 1])  # с вариациями
                new_rating = min_rating
                review.rating = new_rating
                updated_count += 1
                print(f"  Отзыв #{review.id}: {old_rating} → {new_rating}")
        
        db.session.commit()
        print(f"\n✅ Обновлено {updated_count} отзывов")
        
        # Пересчет рейтингов салонов
        print("\n🔄 Пересчет рейтингов салонов...")
        for salon in Salon.query.all():
            avg = db.session.query(func.avg(Review.rating)).filter_by(salon_id=salon.id).scalar() or 0
            count = Review.query.filter_by(salon_id=salon.id).count()
            salon.rating = round(avg, 1)
            salon.reviews_count = count
        
        db.session.commit()
        
        # Итоговая статистика
        new_avg = db.session.query(func.avg(Review.rating)).scalar() or 0
        print(f"\n📊 Новый средний рейтинг всех отзывов: {round(new_avg, 1)}")
        
        print("\n🏆 ТОП-5 САЛОНОВ:")
        top = Salon.query.order_by(Salon.rating.desc()).limit(5).all()
        for i, salon in enumerate(top, 1):
            print(f"  {i}. {salon.name} - {salon.rating} ⭐")

def smart_boost():
    """Умное повышение: низкие оценки поднимаем больше, высокие оставляем"""
    
    with app.app_context():
        print("🧠 УМНОЕ ПОВЫШЕНИЕ РЕЙТИНГА")
        print("=" * 50)
        
        reviews = Review.query.all()
        updated_count = 0
        
        for review in reviews:
            old_rating = review.rating
            
            if old_rating == 1:
                new_rating = 4  # поднимаем сильно
            elif old_rating == 2:
                new_rating = 4  # тоже поднимаем
            elif old_rating == 3:
                new_rating = 4  # до 4
            elif old_rating == 4:
                # 4 оставляем или иногда поднимаем до 4.5/5
                new_rating = random.choice([4, 4.5, 5])
            else:  # 5
                new_rating = 5
            
            # Проверяем, что рейтинг целое число (для вашей модели)
            if isinstance(review.rating, int):
                new_rating = int(new_rating)
            
            if new_rating != old_rating:
                review.rating = new_rating
                updated_count += 1
        
        db.session.commit()
        print(f"✅ Обновлено {updated_count} отзывов")
        
        # Пересчет
        for salon in Salon.query.all():
            avg = db.session.query(func.avg(Review.rating)).filter_by(salon_id=salon.id).scalar() or 0
            count = Review.query.filter_by(salon_id=salon.id).count()
            salon.rating = round(avg, 1)
        
        db.session.commit()
        
        new_avg = db.session.query(func.avg(Review.rating)).scalar() or 0
        print(f"\n📊 Новый средний рейтинг: {round(new_avg, 1)}")

if __name__ == '__main__':
    print("ВЫБЕРИТЕ ДЕЙСТВИЕ:")
    print("1. Поднять все отзывы на 1 балл (максимум 5)")
    print("2. Установить минимальный рейтинг 4 для всех отзывов")
    print("3. Умное повышение (низкие → 4, высокие оставить)")
    
    choice = input("\nВаш выбор (1-3): ")
    
    if choice == '1':
        boost_reviews()
    elif choice == '2':
        set_minimum_rating(4)
    elif choice == '3':
        smart_boost()
    else:
        print("Неверный выбор!")