# image_utils.py - ПОЛНОСТЬЮ ИСПРАВЛЕННАЯ ВЕРСИЯ
import os
from PIL import Image
from flask import current_app
import uuid
import re


# Проверка разрешенного расширения файла
def allowed_file(filename):
    """Проверка разрешенного расширения файла"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


# Генерация уникального имени файла на основе оригинального
def get_unique_filename(original_filename):
    """Генерация уникального имени файла"""
    ext = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else 'jpg'
    unique_id = str(uuid.uuid4())[:8]
    # Очищаем оригинальное имя от недопустимых символов
    name = re.sub(r'[^\w\-_.]', '_', original_filename.rsplit('.', 1)[0])
    name = name[:50]  # Ограничиваем длину
    return f"{name}_{unique_id}.{ext}"


# Создание миниатюры (уменьшенной копии) изображения
def create_thumbnail_image(image_path, thumbnail_path, size):
    """Создание миниатюры изображения"""
    try:
        with Image.open(image_path) as img:
            # Конвертируем в RGB если необходимо (для JPEG)
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            # Создаем миниатюру
            img.thumbnail(size, Image.Resampling.LANCZOS)
            img.save(thumbnail_path, 'JPEG', quality=85, optimize=True)
            return True
    except Exception as e:
        current_app.logger.error(f"Ошибка создания миниатюры: {e}")
        return False


# Оптимизация изображения - сжатие и изменение размера
def optimize_uploaded_image(image_path, max_size=(1200, 1200), quality=85):
    """Оптимизация изображения"""
    try:
        with Image.open(image_path) as img:
            # Конвертируем в RGB если необходимо
            if img.mode in ('RGBA', 'P'):
                rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = rgb_img
            
            # Изменяем размер если изображение слишком большое
            if img.width > max_size[0] or img.height > max_size[1]:
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Сохраняем с оптимизацией
            img.save(image_path, 'JPEG', quality=quality, optimize=True)
            return True
    except Exception as e:
        current_app.logger.error(f"Ошибка оптимизации изображения: {e}")
        return False


# Основная функция сохранения загруженного изображения
def save_uploaded_image(file, subfolder='salons', make_thumb=True, thumb_size=(300, 200)):
    """
    Сохранение загруженного файла
    Возвращает путь к файлу и путь к миниатюре (если создана)
    
    Параметры:
    - file: загруженный файл
    - subfolder: подпапка для сохранения ('salons', 'blog', 'editor')
    - make_thumb: создавать ли миниатюру
    - thumb_size: размер миниатюры
    """
    if not file or not allowed_file(file.filename):
        return None, None
    
    # Создаем директорию если не существует
    upload_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], subfolder)
    os.makedirs(upload_folder, exist_ok=True)
    
    # Генерируем уникальное имя файла
    filename = get_unique_filename(file.filename)
    filepath = os.path.join(upload_folder, filename)
    
    # Сохраняем файл
    file.save(filepath)
    
    # Оптимизируем изображение
    optimize_uploaded_image(filepath, 
                   max_size=(current_app.config['IMAGE_MAX_WIDTH'], 
                            current_app.config['IMAGE_MAX_HEIGHT']),
                   quality=current_app.config['IMAGE_QUALITY'])
    
    # Создаем миниатюру если нужно
    thumbnail_path = None
    if make_thumb:
        thumb_filename = f"thumb_{filename}"
        thumb_filepath = os.path.join(upload_folder, thumb_filename)
        if create_thumbnail_image(filepath, thumb_filepath, thumb_size):
            thumbnail_path = f"/{current_app.config['UPLOAD_FOLDER']}/{subfolder}/{thumb_filename}"
    
    # Возвращаем URL для доступа
    file_url = f"/{current_app.config['UPLOAD_FOLDER']}/{subfolder}/{filename}"
    
    return file_url, thumbnail_path


# Удаление изображения и его миниатюры по URL
def delete_uploaded_image(image_url):
    """Удаление изображения и его миниатюры"""
    if not image_url or not image_url.startswith('/static/uploads/'):
        return False
    
    # Получаем путь к файлу
    filepath = os.path.join(current_app.root_path, image_url.lstrip('/'))
    
    # Удаляем основной файл
    if os.path.exists(filepath):
        os.remove(filepath)
    
    # Удаляем миниатюру если есть
    dirname = os.path.dirname(filepath)
    basename = os.path.basename(filepath)
    thumb_path = os.path.join(dirname, f"thumb_{basename}")
    if os.path.exists(thumb_path):
        os.remove(thumb_path)
    
    return True