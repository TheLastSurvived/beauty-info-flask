import os
import sys
from app import app, db
from models import Salon, Service

# ============================================================
# ПОЛНЫЙ СПИСОК САЛОНОВ (из Заполнение.docx)
# ============================================================

salons_data = [
    # ========== 1. ПАРИКМАХЕРСКИЕ (8 шт) ==========
    {
        'name': 'Baz House',
        'category': 'Парикмахерская',
        'district': 'Октябрьский',
        'description': 'Стильные стрижки и окрашивание для всей семьи. Современный подход и уютная атмосфера.',
        'address': 'ул. Щорса, 19, этаж 2',
        'phone': '+375 (29) 266-88-82',
        'working_hours': 'Пн-Пт: 09:00-20:00, Сб: 09:00-20:00, Вс: 10:00-18:00',
        'social_instagram': 'https://www.instagram.com/baz_house_studio',
        'services': []
    },
    {
        'name': 'Agnessa hair',
        'category': 'Парикмахерская',
        'district': 'Октябрьский',
        'description': 'Индивидуальный подход к каждой прическе. Работаем с разными типами волос.',
        'address': 'проспект Янки Купалы, 63, этаж 3, офис 326',
        'phone': '+375 (29) 882-82-44',
        'working_hours': 'Пн: 13:00-20:00, Ср-Чт: 14:00-20:00, Пт: 13:00-20:00, Вс, Вт - выходной',
        'social_instagram': 'https://www.instagram.com/agnessa_hair',
        'services': []
    },
    {
        'name': 'Белые Росы',
        'category': 'Парикмахерская',
        'district': 'Октябрьский',
        'description': 'Доступные цены и качественный сервис. Стрижки, укладки, окрашивание.',
        'address': 'ул. Белые Росы, 19',
        'phone': '+375 (33) 665-90-66',
        'working_hours': 'Пн-Пт: 09:00-20:00, Сб: 09:00-18:00, Вс: 10:00-16:00',
        'social_instagram': 'https://www.instagram.com/belye_rosy_grodno/',
        'services': []
    },
    {
        'name': 'Keratin Hair',
        'category': 'Парикмахерская',
        'district': 'Ленинский',
        'description': 'Восстановление волос кератином. Лечение и уход за поврежденными волосами.',
        'address': 'ул. Октябрьская, 4, этаж 2, комната 209',
        'phone': '+375 (29) 887-39-69',
        'working_hours': 'Пн-Вс: 11:00-21:00',
        'social_instagram': 'https://www.instagram.com/keratin_hair_grodno',
        'social_vk': 'https://vk.com/dadushko_hair',
        'services': []
    },
    {
        'name': 'Салон красоты Надежды Верстак',
        'category': 'Парикмахерская',
        'district': 'Ленинский',
        'description': 'Опытный мастер с многолетним стажем. Мужские, женские, детские стрижки.',
        'address': 'ул. 17 Сентября, 49',
        'phone': '+375 (29) 800-04-64',
        'working_hours': 'Пн-Пт: 08:30-20:30, Сб-Вс: 10:00-20:30',
        'social_instagram': 'https://www.instagram.com/snv_grodno',
        'services': []
    },
    {
        'name': 'Стригут тут',
        'category': 'Парикмахерская',
        'district': 'Ленинский',
        'description': 'Быстро, качественно, недорого. Стрижки без записи и по предварительной записи.',
        'address': 'ул. Курчатова, 27',
        'phone': '+375 (29) 624-23-77',
        'working_hours': 'Пн-Пт: 09:00-21:00, Сб-Вс: 09:00-17:00',
        'social_instagram': 'https://www.instagram.com/strig.tut',
        'services': []
    },
    {
        'name': 'Ликвин',
        'category': 'Парикмахерская',
        'district': 'Ленинский',
        'description': 'Парикмахерская с многолетней историей. Классические и современные стрижки.',
        'address': 'ул. Советская, 6',
        'phone': '+375 (33) 901-38-84',
        'working_hours': 'Пн-Пт: 09:00-21:00, Сб: 10:00-17:00, Вс: выходной',
        'social_instagram': 'https://www.instagram.com/lakvin_19',
        'services': []
    },
    {
        'name': 'Мир красоты',
        'category': 'Парикмахерская',
        'district': 'Октябрьский',
        'description': 'Широкий спектр услуг. Вечерние прически, окрашивание, уход.',
        'address': 'ул. Молодёжная, 1',
        'phone': '+375 (29) 826-32-63',
        'working_hours': 'Пн-Пт: 09:00-21:00, Сб: 09:00-21:00, Вс: 09:00-18:00',
        'social_instagram': 'https://www.instagram.com/mir_krasoty_grodno/',
        'social_vk': 'https://vk.com/beauty_world_grodno',
        'social_facebook': 'https://www.facebook.com/mir.krasoty.54',
        'social_ok': 'https://ok.ru/profile/577388528588',
        'services': []
    },

    # ========== 2. НОГТЕВОЙ СЕРВИС (4 шт) ==========
    {
        'name': 'Mix Studio',
        'category': 'Ногтевой сервис',
        'district': 'Октябрьский',
        'description': 'Дизайн ногтей любой сложности. Маникюр, педикюр, наращивание.',
        'address': 'пер. Поповича, 8',
        'phone': '+375 (33) 694-97-78',
        'working_hours': 'Пн-Пт: 10:00-21:00, Сб-Вс: 10:00-15:00',
        'services': [
            {'name': 'Обработка вросшего ногтя', 'price': 30, 'category': 'Педикюр'},
            {'name': 'Комплекс маникюр без покрытия + педикюр без покрытия', 'price': 75, 'category': 'Комплексы'},
            {'name': 'Комплекс маникюр с покрытием + педикюр с покрытием гель-лаком', 'price': 95, 'category': 'Комплексы'},
            {'name': 'Маникюр с покрытием гель-лаком', 'price': 50, 'category': 'Маникюр'},
            {'name': 'Наращивание ногтей', 'price': 65, 'category': 'Наращивание'},
            {'name': 'Обработка пальцев ног + покрытие гель-лаком', 'price': 40, 'category': 'Педикюр'},
            {'name': 'Педикюр без покрытия', 'price': 45, 'category': 'Педикюр'},
            {'name': 'Зачистка онихолизиса', 'price': 25, 'category': 'Лечение'},
            {'name': 'Маникюр без покрытия', 'price': 35, 'category': 'Маникюр'},
            {'name': 'Снятие гель-лака без маникюра', 'price': 20, 'category': 'Снятие'},
            {'name': 'Педикюр с покрытием гель-лаком', 'price': 60, 'category': 'Педикюр'},
            {'name': 'Педикюр гигиенический (пальцы + стопы)', 'price': 50, 'category': 'Педикюр'},
            {'name': 'Педикюр пальцев (здоровых)', 'price': 35, 'category': 'Педикюр'},
        ]
    },
    {
        'name': 'Здоровый педикюр и маникюр',
        'category': 'Ногтевой сервис',
        'district': 'Ленинский',
        'description': 'Акцент на безопасность и гигиену. Лечебный педикюр.',
        'address': 'ул. Максима Горького, 53А, этаж 2',
        'phone': '+375 (29) 255-47-47',
        'working_hours': 'Пн-Вс: 12:00-21:00',
        'social_vk': 'https://vk.com/podolog.di_grodno',
        'services': [
            {'name': 'Маникюр с покрытием гель-лак', 'price': 63, 'category': 'Маникюр'},
            {'name': 'Педикюр с покрытием гель-лак', 'price': 73, 'category': 'Педикюр'},
            {'name': 'Подологический педикюр', 'price': 100, 'category': 'Педикюр'},
            {'name': 'Установка КС титановая нить (1 шт)', 'price': 120, 'category': 'Лечение'},
            {'name': 'Обработка стержневой мозоли с разгрузкой', 'price': 35, 'category': 'Лечение'},
            {'name': 'Обработка ВПЧ (бородавка) азотной кислотой (1 шт)', 'price': 30, 'category': 'Лечение'},
        ]
    },
    {
        'name': 'Четкая',
        'category': 'Ногтевой сервис',
        'district': 'Ленинский',
        'description': 'Идеальная форма и стойкое покрытие. Работаем быстро и аккуратно.',
        'address': 'ул. Курчатова, 27',
        'phone': '+375 (33) 993-77-33',
        'working_hours': 'Пн-Пт: 11:00-21:00, Сб: 11:00-21:00, Вс: выходной',
        'social_instagram': 'https://www.instagram.com/nail_studio_grodno',
        'services': [
            {'name': 'Наращивание ногтей', 'price': 70, 'category': 'Наращивание'},
            {'name': 'Педикюр с покрытием гель-лак', 'price': 65, 'category': 'Педикюр'},
            {'name': 'Педикюр без покрытия', 'price': 50, 'category': 'Педикюр'},
            {'name': 'Маникюр с дизайном "Френч"', 'price': 65, 'category': 'Маникюр'},
            {'name': 'Маникюр без покрытия', 'price': 35, 'category': 'Маникюр'},
            {'name': 'Маникюр с покрытием гель-лак', 'price': 55, 'category': 'Маникюр'},
            {'name': 'Мужской маникюр без покрытия', 'price': 40, 'category': 'Маникюр'},
            {'name': 'Маникюр и педикюр в 4 руки (комплекс)', 'price': 140, 'category': 'Комплексы'},
        ]
    },
    {
        'name': 'Вишня студия',
        'category': 'Ногтевой сервис',
        'district': 'Октябрьский',
        'description': 'Уютная студия с приятными ценами. Маникюр для каждого дня.',
        'address': 'ул. Антонова, 25А',
        'phone': '+375 (29) 717-62-65',
        'working_hours': 'Пн-Вс: 09:00-21:00',
        'services': [
            {'name': 'Детский маникюр', 'price': 35, 'category': 'Маникюр'},
            {'name': 'Гигиенический маникюр (инструктор)', 'price': 45, 'category': 'Маникюр'},
            {'name': 'Маникюр полный комплекс (инструктор)', 'price': 70, 'category': 'Маникюр'},
            {'name': 'Наращивание ногтей (инструктор)', 'price': 90, 'category': 'Наращивание'},
            {'name': 'Гигиенический маникюр (ведущий мастер)', 'price': 35, 'category': 'Маникюр'},
            {'name': 'Маникюр полный комплекс (ведущий мастер)', 'price': 55, 'category': 'Маникюр'},
        ]
    },

    # ========== 3. КОСМЕТОЛОГИЯ (2 шт) ==========
    {
        'name': 'Lameko-M',
        'category': 'Косметология',
        'district': 'Октябрьский',
        'description': 'Профессиональная косметология. Чистки лица, уход, аппаратная косметология.',
        'address': 'ул. Дзержинского, 58',
        'phone': '+375 (44) 502-16-44',
        'working_hours': 'Пн-Вс: 08:00-22:00',
        'social_instagram': 'https://www.instagram.com/lameko_m/',
        'social_facebook': 'https://www.facebook.com/grodnokosmetolog',
        'social_vk': 'https://vk.com/marina_shell',
        'services': [
            {'name': 'Карбокситерапия CO2', 'price': 65, 'category': 'Аппаратная косметология'},
            {'name': 'Карбокситерапия CO2 с кислотным пилингом', 'price': 85, 'category': 'Аппаратная косметология'},
            {'name': 'Безинъекционная мезотерапия Dr.Pex X5', 'price': 75, 'category': 'Мезотерапия'},
            {'name': 'Гигиеническая чистка лица "классическая"', 'price': 70, 'category': 'Чистка лица'},
            {'name': 'Глубокий моделирующий массаж лица', 'price': 50, 'category': 'Массаж лица'},
            {'name': 'Экспресс-уход за 30 минут', 'price': 55, 'category': 'Уход'},
        ]
    },
    {
        'name': 'Леди рай',
        'category': 'Косметология',
        'district': 'Ленинский',
        'description': 'Салон красоты и здоровья. Уход за лицом и телом.',
        'address': 'ул. Максима Горького, 49',
        'phone': '+375 (33) 376-33-36',
        'working_hours': 'Пн-Вс: 09:00-21:00',
        'social_instagram': 'https://www.instagram.com/lady_ray_grodno',
        'services': [
            {'name': 'Японский массаж лица "Кобидо"', 'price': 50, 'category': 'Массаж лица'},
            {'name': 'Массаж Гуаша', 'price': 45, 'category': 'Массаж лица'},
            {'name': 'Чистка лица', 'price': 55, 'category': 'Чистка лица'},
            {'name': 'Ретиноловый пилинг', 'price': 85, 'category': 'Пилинги'},
            {'name': 'Классический массаж тела', 'price': 60, 'category': 'Массаж тела'},
            {'name': 'Микронидлинг лица и шеи', 'price': 120, 'category': 'Аппаратная косметология'},
            {'name': 'Карбокситерапия', 'price': 70, 'category': 'Аппаратная косметология'},
            {'name': 'Микронидлинг лица', 'price': 60, 'category': 'Аппаратная косметология'},
        ]
    },

    # ========== 4. SPA-САЛОНЫ (3 шт) ==========
    {
        'name': 'РазоМнем',
        'category': 'SPA-салон',
        'district': 'Ленинский',
        'description': 'Расслабляющие SPA-программы. Уход за телом и душой.',
        'address': 'ул. Большая Троицкая, 16',
        'phone': '+375 (25) 904-59-49',
        'working_hours': 'Пн-Вс: 10:00-20:00',
        'social_instagram': 'https://www.instagram.com/razomnem_grodno',
        'services': []
    },
    {
        'name': 'Baunty',
        'category': 'SPA-салон',
        'district': 'Ленинский',
        'description': 'SPA-релакс в центре города. Пенные ванны, обертывания, массажи.',
        'address': 'ул. Свердлова, 12',
        'phone': '+375 (33) 675-55-88',
        'working_hours': 'Пн-Вс: 09:00-23:00',
        'social_instagram': 'https://www.instagram.com/bauntygrodno',
        'services': []
    },
    {
        'name': 'Воздух',
        'category': 'SPA-салон',
        'district': 'Ленинский',
        'description': 'Легкость и свежесть после процедур. Детокс-программы и уход за телом.',
        'address': 'ул. Большая Троицкая, 37, этаж 3',
        'phone': '+375 (33) 386-58-50',
        'working_hours': 'Пн-Вс: 10:00-20:00',
        'social_instagram': 'https://www.instagram.com/vozduh.grodno/',
        'services': []
    },

    # ========== 5. БРОВИ И РЕСНИЦЫ (7 шт) ==========
    {
        'name': 'Вейки',
        'category': 'Брови и ресницы',
        'district': 'Октябрьский',
        'description': 'Архитектура бровей, окрашивание, ламинирование. Создаем идеальный образ.',
        'address': 'ул. Валентины Макаровой, 2',
        'phone': '+375 (29) 588-81-67',
        'working_hours': 'Вт-Пт: 09:00-21:00, Сб: 09:00-20:00, Вс-Пн: выходной',
        'social_instagram': 'https://www.instagram.com/veiki_grodno',
        'services': [
            {'name': '2D LED наращивание ресниц', 'price': 50, 'category': 'Ресницы'},
            {'name': '1D LED наращивание ресниц', 'price': 45, 'category': 'Ресницы'},
            {'name': '3D LED наращивание ресниц (мокрый эффект)', 'price': 55, 'category': 'Ресницы'},
            {'name': 'Ламинирование ресниц', 'price': 55, 'category': 'Ресницы'},
            {'name': 'Ламинирование бровей (комплекс)', 'price': 50, 'category': 'Брови'},
            {'name': 'Цветные ресницы', 'price': 5, 'category': 'Ресницы'},
        ]
    },
    {
        'name': 'Brows Boss',
        'category': 'Брови и ресницы',
        'district': 'Ленинский',
        'description': 'Брови с характером. Коррекция, окрашивание, укладка.',
        'address': 'ул. Мостовая, 39, этаж 3',
        'phone': '+375 (33) 620-52-00',
        'working_hours': 'Пн-Пт: 10:00-19:00, Сб-Вс: выходной',
        'social_instagram': 'https://www.instagram.com/brows_bossdi',
        'services': [
            {'name': 'Коррекция и окрашивание бровей', 'price': 50, 'category': 'Брови'},
            {'name': 'Перманентный макияж губ', 'price': 320, 'category': 'Перманент'},
            {'name': 'Перманентный макияж бровей', 'price': 320, 'category': 'Перманент'},
        ]
    },
    {
        'name': 'Lami Zlata',
        'category': 'Брови и ресницы',
        'district': 'Октябрьский',
        'description': 'Ламинирование бровей и ресниц. Натуральный уход и стойкий результат.',
        'address': 'ул. Титова, 24, этаж 2, кабинет 15',
        'phone': '+375 (29) 289-89-10',
        'working_hours': 'Пн-Пт: 10:00-20:00, Сб-Вс: выходной',
        'social_instagram': 'https://www.instagram.com/lami_zlata',
        'services': [
            {'name': 'Ламинирование ресниц + уход + окрашивание', 'price': 45, 'category': 'Ресницы'},
            {'name': 'Окрашивание ресниц', 'price': 10, 'category': 'Ресницы'},
            {'name': 'Ламинирование и окрашивание бровей', 'price': 40, 'category': 'Брови'},
            {'name': 'Коррекция бровей женская', 'price': 15, 'category': 'Брови'},
            {'name': 'Депиляция воском (1 зона)', 'price': 7, 'category': 'Депиляция'},
            {'name': 'Ботокс для бровей', 'price': 5, 'category': 'Брови'},
        ]
    },
    {
        'name': 'Marumaru',
        'category': 'Брови и ресницы',
        'district': 'Октябрьский',
        'description': 'Деликатный сервис. Ресницы, брови, окрашивание.',
        'address': 'ул. Молодёжная, 3, этаж 1',
        'phone': '+375 (29) 289-89-10',
        'working_hours': 'Пн-Вс: 10:00-22:00',
        'social_instagram': 'https://www.instagram.com/marumaru_grodno',
        'services': [
            {'name': 'Оформление бровей (коррекция + окрашивание)', 'price': 30, 'category': 'Брови'},
            {'name': 'Ламинирование ресниц (с окрашиванием и ботоксом)', 'price': 45, 'category': 'Ресницы'},
        ]
    },
    {
        'name': 'Skris studio',
        'category': 'Брови и ресницы',
        'district': 'Ленинский',
        'description': 'Гармония и красота. Брови, ресницы, легкий макияж.',
        'address': 'ул. Ленина, 20, этаж 1',
        'phone': '+375 (29) 681-33-80',
        'working_hours': 'Пн-Вс: 09:00-21:00',
        'social_instagram': 'https://www.instagram.com/skris.studio',
        'services': [
            {'name': 'Окрашивание ресниц', 'price': 15, 'category': 'Ресницы'},
            {'name': 'Коррекция бровей', 'price': 30, 'category': 'Брови'},
            {'name': 'Коррекция бровей + окрашивание', 'price': 40, 'category': 'Брови'},
            {'name': 'Ламинирование бровей + окрашивание', 'price': 50, 'category': 'Брови'},
            {'name': 'Наращивание ресниц', 'price': 50, 'category': 'Ресницы'},
        ]
    },
    {
        'name': 'Victoria Beauty',
        'category': 'Брови и ресницы',
        'district': 'Ленинский',
        'description': 'Английский стиль и качество. Брови, ресницы, окрашивание.',
        'address': 'Советская площадь, 2А',
        'phone': '+375 (29) 874-08-62',
        'working_hours': 'Пн-Пт: 10:00-19:00, Сб-Вс: выходной',
        'social_instagram': 'https://www.instagram.com/victoria.zheshko/',
        'services': [
            {'name': 'Окрашивание бровей', 'price': 30, 'category': 'Брови'},
            {'name': 'Ламинирование бровей', 'price': 40, 'category': 'Брови'},
            {'name': 'Ламинирование ресниц', 'price': 40, 'category': 'Ресницы'},
            {'name': 'Ламинирование верхних и нижних ресниц', 'price': 50, 'category': 'Ресницы'},
        ]
    },
    {
        'name': 'Ntl.Lami',
        'category': 'Брови и ресницы',
        'district': 'Ленинский',
        'description': 'Ламинирование и уход. Долговременная укладка бровей.',
        'address': 'ул. Октябрьская, 4, этаж 3, кабинет 314',
        'phone': '+375 (29) 588-10-60',
        'working_hours': 'Пн-Пт: 12:00-20:00, Сб: 12:00-20:00, Вс: выходной',
        'social_instagram': 'https://www.instagram.com/ntl.lami',
        'services': [
            {'name': 'Ламинирование ресниц (нижние+верхние)', 'price': 70, 'category': 'Ресницы'},
            {'name': 'Ламинирование верхних ресниц', 'price': 50, 'category': 'Ресницы'},
            {'name': 'Долговременная укладка бровей с окрашиванием', 'price': 50, 'category': 'Брови'},
            {'name': 'Долговременная укладка бровей без окрашивания', 'price': 40, 'category': 'Брови'},
            {'name': 'Коррекция и окрашивание бровей', 'price': 35, 'category': 'Брови'},
            {'name': 'Коррекция бровей', 'price': 25, 'category': 'Брови'},
        ]
    },

    # ========== 6. ТАТУ И ПИРСИНГ (4 шт) ==========
    {
        'name': 'Медведь',
        'category': 'Тату и пирсинг',
        'district': 'Ленинский',
        'description': 'Тату-салон с характером. Опытные мастера, качественные краски.',
        'address': 'ул. Октябрьская, 6, этаж 1',
        'phone': '+375 (29) 787-99-07',
        'working_hours': 'Пн-Пт: 09:00-18:00, Сб: 09:00-18:00, Вс: выходной',
        'social_instagram': 'https://www.instagram.com/medvedtattoo',
        'social_vk': 'https://vk.com/medvedtattoo',
        'services': [{'name': 'Художественная татуировка', 'price': 70, 'category': 'Татуировки'}]
    },
    {
        'name': 'Мроя',
        'category': 'Тату и пирсинг',
        'district': 'Ленинский',
        'description': 'Уникальные эскизы. Любой стиль, от реализма до акварели.',
        'address': 'ул. Телеграфная, 7',
        'phone': '+375 (29) 584-59-53',
        'working_hours': 'Пн-Вс: 09:00-19:00',
        'social_instagram': 'https://www.instagram.com/mroya_tattoo/',
        'social_vk': 'https://vk.com/grodno_tattooclub',
        'services': [{'name': 'Татуировка', 'price': 80, 'category': 'Татуировки'}]
    },
    {
        'name': 'Эстектика',
        'category': 'Тату и пирсинг',
        'district': 'Ленинский',
        'description': 'Эстетичные татуировки и пирсинг. Стерильность и безопасность.',
        'address': 'ул. Мостовая, 31, этаж 2, офис 21',
        'phone': '+375 (29) 253-01-73',
        'working_hours': 'Пн-Вс: 10:00-21:00',
        'social_instagram': 'https://www.instagram.com/piercing__grodno/',
        'services': [{'name': 'Пирсинг', 'price': 25, 'category': 'Пирсинг'}]
    },
    {
        'name': 'Инкарнация',
        'category': 'Тату и пирсинг',
        'district': 'Ленинский',
        'description': 'Искусство татуировки. Создаем тату на заказ.',
        'address': 'ул. Кирова, 38, помещение 2',
        'phone': '+375 (29) 834-56-66',
        'working_hours': 'Пн-Вс: 10:00-19:00',
        'social_instagram': 'https://www.instagram.com/incarnatio.tattoostudio',
        'services': [
            {'name': 'Осветление/выведение тату', 'price': 50, 'category': 'Татуировки'},
            {'name': 'Пирсинг', 'price': 40, 'category': 'Пирсинг'},
            {'name': 'Художественная татуировка', 'price': 100, 'category': 'Татуировки'},
        ]
    },

    # ========== 7. МУЖСКОЙ БАРБЕРШОП (13 шт) ==========
    {
        'name': 'Razmova',
        'category': 'Мужской барбершоп',
        'district': 'Октябрьский',
        'description': 'Мужская классика. Стрижки, бритье, уход за бородой.',
        'address': 'ул. Лидская, 19',
        'phone': '+375 (33) 996-37-17',
        'working_hours': 'Вт-Вс: 10:00-20:00, Пн: выходной',
        'services': []
    },
    {
        'name': 'LeVeL',
        'category': 'Мужской барбершоп',
        'district': 'Ленинский',
        'description': 'Барбершоп нового уровня. Стильные стрижки и мужские процедуры.',
        'address': 'ул. Курчатова, 27, этаж 2',
        'phone': '+375 (29) 334-50-00',
        'working_hours': 'Пн-Вс: 09:00-21:00',
        'social_instagram': 'https://www.instagram.com/level_barbershop_grodno',
        'services': []
    },
    {
        'name': 'Карт-бланш',
        'category': 'Мужской барбершоп',
        'district': 'Октябрьский',
        'description': 'Свобода выбора образа. Креативные стрижки и моделирование.',
        'address': 'проспект Янки Купалы, 67',
        'phone': '+375 (29) 741-52-73',
        'working_hours': 'Пн-Вс: 10:00-22:00',
        'social_instagram': 'https://www.instagram.com/carteblanche.br/',
        'services': []
    },
    {
        'name': 'Mbarber',
        'category': 'Мужской барбершоп',
        'district': 'Октябрьский',
        'description': 'Брутальный сервис для мужчин. Бритье опасной бритвой.',
        'address': 'ул. Антонова, 4А, этаж 2, кабинет 3',
        'phone': '+375 (33) 353-62-98',
        'working_hours': 'Пн-Пт: 10:00-20:00, Сб: 10:00-20:00, Вс: выходной',
        'social_instagram': 'https://www.instagram.com/mbarber_grodno',
        'services': []
    },
    {
        'name': 'One',
        'category': 'Мужской барбершоп',
        'district': 'Ленинский',
        'description': 'Единое пространство стиля. Стрижки, борода, уход.',
        'address': 'ул. Максима Горького, 47А',
        'phone': '+375 (29) 266-42-45',
        'working_hours': 'Пн-Вс: 10:00-20:00',
        'social_instagram': 'https://www.instagram.com/one_salone_',
        'services': []
    },
    {
        'name': 'Man Side',
        'category': 'Мужской барбершоп',
        'district': 'Октябрьский',
        'description': 'Мужская сторона красоты. Комфортная атмосфера, качественный сервис.',
        'address': 'ул. Тимирязева, 10, корпус 1, этаж 4, комната 20',
        'phone': '+375 (33) 675-24-11',
        'working_hours': 'Вт-Сб: 10:00-20:00, Вс-Пн: выходной',
        'social_instagram': 'https://www.instagram.com/manside_barbershop/',
        'services': []
    },
    {
        'name': "Men's Style",
        'category': 'Мужской барбершоп',
        'district': 'Ленинский',
        'description': 'Мужской стиль и уход. Классические и современные стрижки.',
        'address': 'ул. Советская, 14, этаж 2',
        'phone': '+375 (33) 673-68-34',
        'working_hours': 'Пн-Вс: 10:00-20:00',
        'social_instagram': 'https://www.instagram.com/zlaya_sveta_',
        'services': []
    },
    {
        'name': 'Feroom',
        'category': 'Мужской барбершоп',
        'district': 'Ленинский',
        'description': 'Свобода и стиль. Барбершоп для смелых решений.',
        'address': 'ул. 1 Мая, 19',
        'phone': '+375 (29) 773-34-43',
        'working_hours': 'Пн-Вс: 10:00-20:00',
        'social_instagram': 'https://www.instagram.com/feroom.barber/',
        'services': []
    },
    {
        'name': 'ФлэтБуш',
        'category': 'Мужской барбершоп',
        'district': 'Октябрьский',
        'description': 'Американский стиль в Гродно. Классические мужские стрижки.',
        'address': 'ул. Калючинская, 6',
        'phone': '+375 (33) 685-36-66',
        'working_hours': 'Пн-Вс: 10:00-20:00',
        'social_instagram': 'https://www.instagram.com/barbershop_flatbush/',
        'services': []
    },
    {
        'name': 'Лезвие',
        'category': 'Мужской барбершоп',
        'district': 'Октябрьский',
        'description': 'Острый стиль, идеальный результат. Бритье и стрижки.',
        'address': 'ул. Щорса, 11Б, этаж 2',
        'phone': '+375 (29) 121-12-99',
        'working_hours': 'Пн-Вс: 09:00-21:00',
        'social_instagram': 'https://www.instagram.com/lezvie.grodno',
        'services': []
    },
    {
        'name': 'Перезагрузка',
        'category': 'Мужской барбершоп',
        'district': 'Ленинский',
        'description': 'Новый образ с нуля. Радикальные изменения и легкая коррекция.',
        'address': 'ул. Тельмана, 6, этаж 2',
        'phone': '+375 (29) 787-78-77',
        'working_hours': 'Пн-Вс: 10:00-20:00',
        'social_instagram': 'https://www.instagram.com/perezagruzka_studio_barbers/',
        'services': []
    },
    {
        'name': '13th',
        'category': 'Мужской барбершоп',
        'district': 'Ленинский',
        'description': 'Мистический стиль. Неформальная атмосфера и отличные стрижки.',
        'address': 'ул. Кирова, 18, помещение 2',
        'phone': '+375 (29) 294-13-13',
        'working_hours': 'Пн-Вс: 10:00-20:00',
        'social_instagram': 'https://www.instagram.com/13th.by/',
        'social_facebook': 'https://www.facebook.com/13th.by',
        'services': []
    },

    # ========== 8. СОЛЯРИЙ (2 шт) ==========
    {
        'name': 'Black Power',
        'category': 'Солярий',
        'district': 'Ленинский',
        'description': 'Мощный загар для сияющей кожи. Турбо-солярий.',
        'address': 'ул. Максима Горького, 72, этаж 5',
        'phone': '+375 (29) 888-30-60',
        'working_hours': 'Пн-Пт: 10:00-21:00, Сб-Вс: выходной',
        'social_instagram': 'https://www.instagram.com/black_power_grodno/',
        'services': [{'name': '1 минута', 'price': 2.20, 'category': 'Солярий'}]
    },
    {
        'name': 'Sweet Dream',
        'category': 'Солярий',
        'district': 'Ленинский',
        'description': 'Приятный загар в сладкой атмосфере. Косметика для загара.',
        'address': 'ул. Пушкина, 31А, этаж 2',
        'phone': '+375 (33) 995-52-78',
        'working_hours': 'Пн-Вс: 10:00-22:00',
        'social_instagram': 'https://www.instagram.com/sweet_dream_grodno',
        'services': [{'name': '1 минута', 'price': 1.70, 'category': 'Солярий'}]
    },

    # ========== 9. МАССАЖНЫЙ САЛОН (8 шт) ==========
    {
        'name': 'Массаж',
        'category': 'Массажный салон',
        'district': 'Ленинский',
        'description': 'Классический и лечебный массаж. Снятие напряжения и боли.',
        'address': 'ул. Куйбышева, 18',
        'phone': '+375 (29) 268-86-44',
        'working_hours': 'Пн-Пт: 09:30-22:00, Сб-Вс: выходной',
        'services': [
            {'name': 'Расслабляющий массаж 1 час', 'price': 70, 'category': 'Массаж'},
            {'name': 'Расслабляющий массаж 90 мин', 'price': 100, 'category': 'Массаж'},
            {'name': 'Массаж при болях в пояснице', 'price': 60, 'category': 'Лечебный массаж'},
        ]
    },
    {
        'name': 'На Виленской',
        'category': 'Массажный салон',
        'district': 'Ленинский',
        'description': 'Расслабляющий массаж в уютной обстановке. Антистресс-программы.',
        'address': 'ул. Большая Троицкая, 2Б',
        'phone': '+375 (33) 635-13-51',
        'working_hours': 'Пн-Сб: 09:00-21:00, Вс: выходной',
        'social_instagram': 'https://www.instagram.com/spa_navilenskoi/',
        'services': [
            {'name': 'Шоколадный массаж тела', 'price': 70, 'category': 'Массаж'},
            {'name': 'Хиромассаж тела (испанский массаж)', 'price': 80, 'category': 'Массаж'},
        ]
    },
    {
        'name': 'Массажный салон',
        'category': 'Массажный салон',
        'district': 'Октябрьский',
        'description': 'Профессиональный массаж для здоровья спины.',
        'address': 'ул. Тимирязева, 10, корпус 1, этаж 3, офис 15',
        'phone': '+375 (33) 380-96-57',
        'working_hours': 'Пн-Сб: 09:00-21:00, Вс: выходной',
        'social_instagram': 'https://www.instagram.com/massage.ketrin.g',
        'services': [
            {'name': 'Массаж лица', 'price': 50, 'category': 'Массаж лица'},
            {'name': 'Буккальный массаж лица', 'price': 60, 'category': 'Массаж лица'},
            {'name': 'Расслабляющий массаж тела', 'price': 70, 'category': 'Массаж'},
            {'name': 'Ультразвуковой пилинг', 'price': 50, 'category': 'Пилинг'},
        ]
    },
    {
        'name': 'Ph Beauty №1',
        'category': 'Массажный салон',
        'district': 'Ленинский',
        'description': 'Beauty-массаж. Лимфодренаж, антицеллюлитный, релакс.',
        'address': 'ул. Большая Троицкая, 37, этаж 2',
        'phone': '+375 (29) 887-19-90',
        'working_hours': 'Пн-Пт: 09:00-20:00, Сб: 09:00-14:00, Вс: выходной',
        'social_instagram': 'https://www.instagram.com/ph.beauty.salon/',
        'services': []
    },
    {
        'name': 'Pro Massage',
        'category': 'Массажный салон',
        'district': 'Октябрьский',
        'description': 'Профессиональный подход к здоровью. Спортивный и лечебный массаж.',
        'address': 'ул. Титова, 24, этаж 2, офис 19',
        'phone': '+375 (29) 517-84-42',
        'working_hours': 'Пн-Пт: 09:00-19:00, Сб: 10:00-16:00, Вс: выходной',
        'social_instagram': 'https://www.instagram.com/pro_massage_grodno',
        'services': []
    },
    {
        'name': 'Z.Efir',
        'category': 'Массажный салон',
        'district': 'Октябрьский',
        'description': 'Эфир легкости. Массаж для души и тела.',
        'address': 'ул. Советских Пограничников, 17',
        'phone': '+375 (29) 789-19-04',
        'working_hours': 'Пн-Вс: 09:00-21:00',
        'social_instagram': 'https://www.instagram.com/z.efir_massage/',
        'services': []
    },
    {
        'name': 'Далони',
        'category': 'Массажный салон',
        'district': 'Ленинский',
        'description': 'Исцеляющие руки. Массаж, остеопатия, восстановление.',
        'address': 'ул. 17 Сентября, 49, этаж 1',
        'phone': '+375 (33) 688-33-43',
        'working_hours': 'Пн-Пт: 09:00-22:00, Сб-Вс: выходной',
        'social_instagram': 'https://www.instagram.com/daloni_rimma/',
        'services': []
    },
    {
        'name': 'Массаж',
        'category': 'Массажный салон',
        'district': 'Октябрьский',
        'description': 'Доступный массаж в удобное время. Классика и спорт.',
        'address': 'проспект Клецкова, 15А',
        'phone': '+375 (44) 786-94-94',
        'working_hours': 'Пн-Вс: 09:00-21:00',
        'services': []
    },

    # ========== 10. ЭПИЛЯЦИЯ И ДЕПИЛЯЦИЯ (4 шт) ==========
    {
        'name': 'Студия эстетической косметологии',
        'category': 'Эпиляция и депиляция',
        'district': 'Октябрьский',
        'description': 'Эпиляция сахаром и воском. Гладкая кожа без раздражения.',
        'address': 'проспект Космонавтов, 2/1, этаж 2',
        'phone': '+375 (33) 657-41-49',
        'working_hours': 'Пн-Пт: 09:00-21:00, Сб: 09:00-16:00, Вс: выходной',
        'social_instagram': 'https://www.instagram.com/olga_sokolyan/',
        'services': []
    },
    {
        'name': 'RedMak',
        'category': 'Эпиляция и депиляция',
        'district': 'Октябрьский',
        'description': 'Качественная эпиляция. Быстро и надолго.',
        'address': 'проспект Тимирязева, 10, корпус 1',
        'phone': '+375 (29) 738-80-60',
        'working_hours': 'Пн-Вс: 09:00-21:00',
        'social_instagram': 'https://www.instagram.com/Redmak_epil',
        'services': []
    },
    {
        'name': 'Эпиклиника',
        'category': 'Эпиляция и депиляция',
        'district': 'Октябрьский',
        'description': 'Клиника эпиляции. Лазерная и восковая депиляция.',
        'address': 'ул. Лидская, 34, этаж 2',
        'phone': '+375 (29) 725-11-39',
        'working_hours': 'Пн-Сб: 08:00-21:00, Сб: 09:00-17:00, Вс: выходной',
        'services': []
    },
    {
        'name': 'Депиляция',
        'category': 'Эпиляция и депиляция',
        'district': 'Ленинский',
        'description': 'Процедуры депиляции в центре города. Доступные цены.',
        'address': 'ул. Ленина, 6',
        'phone': '+375 (29) 884-66-55',
        'working_hours': 'Пн-Вс: 10:00-21:00',
        'social_instagram': 'https://www.instagram.com/valerija_shugaring',
        'services': []
    },

    # ========== 11. СВАДЕБНЫЙ САЛОН (10 шт) ==========
    {
        'name': 'Есения',
        'category': 'Свадебный салон',
        'district': 'Ленинский',
        'description': 'Свадебные платья и аксессуары. Поможем создать идеальный образ.',
        'address': 'ул. Кирова, 11, этаж 2',
        'phone': '+375 (29) 586-09-76',
        'working_hours': 'Пн-Пт: 11:00-19:00, Сб: 11:00-17:00, Вс: выходной',
        'social_instagram': 'https://www.instagram.com/eseniyasvadba/',
        'services': [
            {'name': 'Прокат платьев', 'price': 100, 'category': 'Прокат'},
            {'name': 'Индивидуальный пошив платья', 'price': 200, 'category': 'Пошив'},
        ]
    },
    {
        'name': 'Ниаггара',
        'category': 'Свадебный салон',
        'district': 'Ленинский',
        'description': 'Роскошные свадебные наряды. Платья на любой бюджет.',
        'address': 'ул. Социалистическая, 56',
        'phone': '+375 (29) 281-22-07',
        'working_hours': 'Пн-Пт: 11:00-19:00, Сб: 11:00-16:00, Вс: выходной',
        'social_instagram': 'https://www.instagram.com/niaggara_wedding_by/',
        'services': [{'name': 'Прокат платьев', 'price': 120, 'category': 'Прокат'}]
    },
    {
        'name': 'Маргарита',
        'category': 'Свадебный салон',
        'district': 'Октябрьский',
        'description': 'Свадебные платья и вечерние наряды. Индивидуальный подход.',
        'address': 'ул. Советских Пограничников, 91',
        'phone': '+375 (29) 580-09-23',
        'working_hours': 'Пн-Вс: 09:00-21:00',
        'social_vk': 'https://vk.com/club140532339',
        'services': [{'name': 'Прокат платьев', 'price': 135, 'category': 'Прокат'}]
    },
    {
        'name': 'Брайд',
        'category': 'Свадебный салон',
        'district': 'Ленинский',
        'description': 'Свадебный салон для невест. Платья, вуали, украшения.',
        'address': 'ул. Карла Маркса, 5, этаж 2',
        'phone': '+375 (29) 887-24-55',
        'working_hours': 'Пн-Пт: 12:30-19:00, Сб: 11:00-16:00, Вс: выходной',
        'social_instagram': 'https://www.instagram.com/bride_grodno/',
        'services': [{'name': 'Прокат платьев', 'price': 200, 'category': 'Прокат'}]
    },
    {
        'name': 'Женева',
        'category': 'Свадебный салон',
        'district': 'Ленинский',
        'description': 'Европейский стиль и качество. Свадебные платья премиум-класса.',
        'address': 'ул. Мостовая, 31, этаж 2, помещение 31',
        'phone': '+375 (33) 686-80-50',
        'working_hours': 'Вт-Сб: 12:00-20:00, Вс-Пн: выходной',
        'social_instagram': 'https://www.instagram.com/salon_genewa/',
        'services': [
            {'name': 'Прокат платьев', 'price': 150, 'category': 'Прокат'},
            {'name': 'Прокат аксессуаров', 'price': 35, 'category': 'Прокат'},
        ]
    },
    {
        'name': 'Veigo',
        'category': 'Свадебный салон',
        'district': 'Ленинский',
        'description': 'Современная свадебная мода. Легкие и элегантные платья.',
        'address': 'ул. Карла Маркса, 25',
        'phone': '+375 (29) 283-79-67',
        'working_hours': 'Пн-Пт: 10:00-19:00, Сб: 10:00-16:00, Вс: выходной',
        'social_instagram': 'https://www.instagram.com/salon_veigo/',
        'services': [{'name': 'Прокат платьев', 'price': 300, 'category': 'Прокат'}]
    },
    {
        'name': 'Грация',
        'category': 'Свадебный салон',
        'district': 'Ленинский',
        'description': 'Изящные свадебные наряды. Платья, фаты, аксессуары.',
        'address': 'ул. Городничанская, 36',
        'phone': '+375 (15) 245-00-15',
        'working_hours': 'Пн-Пт: 11:00-19:00, Сб: 11:00-15:00, Вс: выходной',
        'social_instagram': 'https://www.instagram.com/salongracia.grodno/',
        'social_vk': 'https://vk.com/salongracia.grodno',
        'services': [
            {'name': 'Прокат платьев', 'price': 350, 'category': 'Прокат'},
            {'name': 'Прокат мужских костюмов', 'price': 150, 'category': 'Прокат'},
        ]
    },
    {
        'name': 'Dominik',
        'category': 'Свадебный салон',
        'district': 'Ленинский',
        'description': 'Эксклюзивные модели. Поможем выбрать платье мечты.',
        'address': 'ул. Максима Горького, 91, зал Д, улица Северная, место 15с',
        'phone': '+375 (29) 135-09-35',
        'working_hours': 'Вт-Вс: 10:00-18:00, Пн: выходной',
        'social_instagram': 'https://www.instagram.com/dominik_salon/',
        'social_vk': 'https://vk.com/salon_dominik',
        'services': [{'name': 'Прокат платьев', 'price': 330, 'category': 'Прокат'}]
    },
    {
        'name': 'Lusso',
        'category': 'Свадебный салон',
        'district': 'Ленинский',
        'description': 'Роскошь и стиль. Свадебные платья и вечерние наряды.',
        'address': 'ул. Кирова, 5, этаж 2',
        'phone': '+375 (29) 282-23-02',
        'working_hours': 'Пн-Пт: 12:00-19:00, Сб: 12:00-17:00, Вс: выходной',
        'social_instagram': 'https://www.instagram.com/lussogrodno/',
        'services': [
            {'name': 'Прокат платьев', 'price': 150, 'category': 'Прокат'},
            {'name': 'Индивидуальный пошив', 'price': 200, 'category': 'Пошив'},
        ]
    },
    {
        'name': 'Мерри',
        'category': 'Свадебный салон',
        'district': 'Ленинский',
        'description': 'Счастливые невесты начинают здесь. Демократичные цены, отличный выбор.',
        'address': 'ул. Кирова, 30',
        'phone': '+375 (29) 395-54-97',
        'working_hours': 'Пн: 11:00-16:00, Ср-Пт: 11:00-19:00, Сб: 11:00-16:00',
        'social_instagram': 'https://www.instagram.com/grodno_merri/',
        'services': [
            {'name': 'Прокат платьев', 'price': 100, 'category': 'Прокат'},
            {'name': 'Вечерние платья на покупку', 'price': 450, 'category': 'Продажа'},
        ]
    },

    # ========== 12. САЛОН ПОЛНОГО ЦИКЛА (17 шт) ==========
    {
        'name': 'IzzySalon',
        'category': 'Салон красоты полного цикла',
        'district': 'Ленинский',
        'description': 'Всё в одном месте: стрижки, маникюр, косметология. Комплексный уход.',
        'address': 'ул. Максима Горького, 104',
        'phone': '+375 (29) 766-99-22',
        'working_hours': 'Пн-Пт: 09:00-21:00, Сб: 08:00-16:00, Вс: выходной',
        'social_instagram': 'https://www.instagram.com/izzysalon_grodno/',
        'services': [
            {'name': 'Стрижка женская', 'price': 40, 'category': 'Парикмахерские услуги'},
            {'name': 'Стрижка мужская', 'price': 35, 'category': 'Парикмахерские услуги'},
            {'name': 'Стрижка детская', 'price': 25, 'category': 'Парикмахерские услуги'},
            {'name': 'Окрашивание волос в один тон', 'price': 135, 'category': 'Парикмахерские услуги'},
            {'name': 'Маникюр с покрытием гель-лак', 'price': 55, 'category': 'Ногтевой сервис'},
            {'name': 'Педикюр с покрытием гель-лак', 'price': 70, 'category': 'Ногтевой сервис'},
            {'name': 'Чистка лица', 'price': 70, 'category': 'Косметология'},
            {'name': 'Перманентный макияж бровей', 'price': 250, 'category': 'Перманент'},
            {'name': 'Перманентный макияж губ', 'price': 250, 'category': 'Перманент'},
        ]
    },
    {
        'name': 'Грейс',
        'category': 'Салон красоты полного цикла',
        'district': 'Октябрьский',
        'description': 'Красота без границ. Полный спектр услуг для женщин и мужчин.',
        'address': 'ул. Дзержинского, 125А',
        'phone': '+375 (33) 310-50-20',
        'working_hours': 'Пн-Вс: 10:00-20:00',
        'social_instagram': 'https://www.instagram.com/studiokrasoty_grace/',
        'services': [
            {'name': 'Женская стрижка', 'price': 35, 'category': 'Парикмахерские услуги'},
            {'name': 'Вечерний макияж', 'price': 90, 'category': 'Макияж'},
            {'name': 'Ламинирование ресниц', 'price': 45, 'category': 'Брови и ресницы'},
            {'name': 'Окрашивание волос', 'price': 80, 'category': 'Парикмахерские услуги'},
            {'name': 'Коррекция бровей', 'price': 25, 'category': 'Брови и ресницы'},
        ]
    },
    {
        'name': 'Персона',
        'category': 'Салон красоты полного цикла',
        'district': 'Октябрьский',
        'description': 'Индивидуальный подход к каждому клиенту. Все виды beauty-услуг.',
        'address': 'ул. Советских Пограничников, 91',
        'phone': '+375 (29) 889-04-96',
        'working_hours': 'Пн-Сб: 09:00-21:00, Вс: 09:00-17:00',
        'social_instagram': 'https://www.instagram.com/persona_grodno',
        'social_facebook': 'https://www.facebook.com/persona.grodno/',
        'services': []
    },
    {
        'name': 'Тиффани',
        'category': 'Салон красоты полного цикла',
        'district': 'Ленинский',
        'description': 'Элегантность и стиль. Парикмахерские, косметологические и ногтевые услуги.',
        'address': 'ул. Карла Маркса, 15, этаж 1',
        'phone': '+375 (29) 554-47-77',
        'working_hours': 'Пн-Пт: 09:00-20:00, Сб: 09:00-14:00, Вс: выходной',
        'social_instagram': 'https://www.instagram.com/tiffany_grodno/',
        'services': []
    },
    {
        'name': 'Бьюти комплекс',
        'category': 'Салон красоты полного цикла',
        'district': 'Октябрьский',
        'description': 'Масштабный салон красоты. Большой выбор процедур.',
        'address': 'ул. Дзержинского, 40',
        'phone': '+375 (29) 223-87-77',
        'working_hours': 'Пн-Пт: 09:00-21:00, Сб-Вс: выходной',
        'services': []
    },
    {
        'name': 'Бьюти старт',
        'category': 'Салон красоты полного цикла',
        'district': 'Октябрьский',
        'description': 'Начни свой путь к красоте. Доступные цены, качественный сервис.',
        'address': 'ул. Валентины Макаровой, 1, этаж 1',
        'phone': '+375 (29) 765-93-53',
        'working_hours': 'Пн-Пт: 12:00-20:00, Сб: 10:00-13:00, Вс: выходной',
        'social_instagram': 'https://www.instagram.com/beautystart_grodno/',
        'services': []
    },
    {
        'name': 'Doza Club',
        'category': 'Салон красоты полного цикла',
        'district': 'Октябрьский',
        'description': 'Клуб красоты. Современные методики и уютная атмосфера.',
        'address': 'проспект Янки Купалы, 2В, этаж 2, помещение 3',
        'phone': '+375 (29) 809-69-69',
        'working_hours': 'Пн-Вс: 09:00-21:00',
        'services': []
    },
    {
        'name': 'NovaЯ',
        'category': 'Салон красоты полного цикла',
        'district': 'Октябрьский',
        'description': 'Новая версия тебя. Преображение и уход.',
        'address': 'ул. Розанова, 34, этаж 1',
        'phone': '+375 (29) 292-92-15',
        'working_hours': 'Пн-Пт: 09:30-21:00, Сб: 09:30-21:00, Вс: выходной',
        'social_instagram': 'https://www.instagram.com/studia.krasoty_novaja/',
        'services': []
    },
    {
        'name': 'Ollissalon',
        'category': 'Салон красоты полного цикла',
        'district': 'Ленинский',
        'description': 'Салон красоты с душой. Индивидуальный подход к каждому.',
        'address': 'ул. Большая Троицкая, 48',
        'phone': '+375 (29) 287-06-04',
        'working_hours': 'Пн-Пт: 10:00-20:00, Сб-Вс: 10:00-16:00',
        'social_instagram': 'https://www.instagram.com/ollissalon',
        'services': []
    },
    {
        'name': 'Diva',
        'category': 'Салон красоты полного цикла',
        'district': 'Ленинский',
        'description': 'Чувствуй себя дивой. Профессиональный сервис и внимание к деталям.',
        'address': 'ул. 1 Мая, 20',
        'phone': '+375 (29) 283-05-01',
        'working_hours': 'Пн-Пт: 09:00-21:00, Сб-Вс: выходной',
        'social_instagram': 'https://www.instagram.com/diva.grodno',
        'services': []
    },
    {
        'name': 'Red Fantasy room',
        'category': 'Салон красоты полного цикла',
        'district': 'Октябрьский',
        'description': 'Красная фантазия стиля. Яркие образы и нестандартные решения.',
        'address': 'ул. Кленовая, 37',
        'phone': '+375 (33) 354-65-46',
        'working_hours': 'Пн-Пт: 09:00-20:00, Сб: 09:00-15:00, Вс: выходной',
        'social_instagram': 'https://www.instagram.com/redfantasy_room',
        'services': []
    },
    {
        'name': 'Honey Day',
        'category': 'Салон красоты полного цикла',
        'district': 'Ленинский',
        'description': 'Сладкий день красоты. Полный спектр услуг в комфортной обстановке.',
        'address': 'ул. Мостовая, 39, этаж 3',
        'phone': '+375 (44) 584-25-25',
        'working_hours': 'Пн-Пт: 09:00-20:00, Сб: 09:00-20:00, Вс: 09:00-16:00',
        'social_instagram': 'https://www.instagram.com/honeyday_grodno/',
        'services': []
    },
    {
        'name': 'Elegance',
        'category': 'Салон красоты полного цикла',
        'district': 'Ленинский',
        'description': 'Элегантность в каждой детали. Премиальный сервис и уход.',
        'address': 'ул. Стефана Батория, 8Б, этаж 2',
        'phone': '+375 (29) 507-00-88',
        'working_hours': 'Пн-Сб: 10:00-20:00, Вс: 10:00-16:00',
        'social_instagram': 'https://www.instagram.com/elegance.grodno',
        'services': []
    },
    {
        'name': 'Монэ',
        'category': 'Салон красоты полного цикла',
        'district': 'Ленинский',
        'description': 'Салон красоты нового формата. Современные тренды и технологии.',
        'address': 'ул. Бульвар Ленинского Комсомола, 15',
        'phone': '+375 (33) 310-37-38',
        'working_hours': 'Пн-Пт: 10:00-20:00, Сб: 10:00-18:00, Вс: 11:00-17:00',
        'social_instagram': 'https://www.instagram.com/mone.beautystudio',
        'services': []
    },
    {
        'name': 'Монро',
        'category': 'Салон красоты полного цикла',
        'district': 'Октябрьский',
        'description': 'Стиль, вдохновленный легендой. Классика и современность.',
        'address': 'проспект Клецкова, 64, помещение 2',
        'phone': '+375 (29) 777-72-31',
        'working_hours': 'Пн-Пт: 09:00-21:00, Сб: 09:00-21:00, Вс: выходной',
        'social_instagram': 'https://www.instagram.com/monroe.by/',
        'services': []
    },
]

def import_salons():
    """Импорт салонов и их услуг"""
    
    existing_count = Salon.query.count()
    if existing_count > 0:
        print(f"⚠️ В базе уже есть {existing_count} салонов.")
        response = input("Хотите удалить существующие салоны и импортировать заново? (y/n): ")
        if response.lower() != 'y':
            print("Импорт отменен.")
            return
        Salon.query.delete()
        db.session.commit()
        print("✅ Существующие салоны удалены.")
    
    count = 0
    for data in salons_data:
        # Собираем соцсети в описание
        social_links = []
        if data.get('social_instagram'):
            social_links.append(f"📷 Instagram: {data['social_instagram']}")
        if data.get('social_vk'):
            social_links.append(f"📘 VK: {data['social_vk']}")
        if data.get('social_facebook'):
            social_links.append(f"📘 Facebook: {data['social_facebook']}")
        if data.get('social_ok'):
            social_links.append(f"📘 Одноклассники: {data['social_ok']}")
        
        description = data['description']
        if social_links:
            description += "\n\n🌐 Социальные сети:\n" + "\n".join(social_links)
        
        salon = Salon(
            name=data['name'],
            category=data['category'],
            district=data['district'],
            description=description[:1000],
            address=data.get('address', ''),
            phone=data.get('phone', ''),
            working_hours=data.get('working_hours', ''),
            image_url='/static/img/default.png',
            is_verified=True,
            rating=0.0,
            reviews_count=0,
            # Социальные сети
            social_instagram=data.get('social_instagram'),
            social_vk=data.get('social_vk'),
            social_facebook=data.get('social_facebook'),
            social_telegram=data.get('social_telegram')
        )
        db.session.add(salon)
        db.session.flush()
        
        for service_data in data.get('services', []):
            price = service_data['price']
            if isinstance(price, (int, float)):
                price = int(price)
            
            service = Service(
                salon_id=salon.id,
                category=service_data.get('category', 'Основные услуги'),
                name=service_data['name'],
                price=price,
                description=''
            )
            db.session.add(service)
        
        count += 1
        print(f"  ✅ {data['name']} ({len(data.get('services', []))} услуг)")
    
    db.session.commit()
    print(f"\n🎉 Импорт завершен! Добавлено {count} салонов.")
    print(f"📊 Статистика по категориям:")
    
    from sqlalchemy import func
    stats = db.session.query(Salon.category, func.count(Salon.id)).group_by(Salon.category).all()
    for cat, cnt in sorted(stats, key=lambda x: x[1], reverse=True):
        print(f"     {cat}: {cnt}")

def main():
    with app.app_context():
        print("🚀 Начинаю импорт данных из Заполнение.docx...")
        import_salons()
        print("\n✨ Готово!")

if __name__ == '__main__':
    main()