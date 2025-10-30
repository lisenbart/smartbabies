#!/usr/bin/env python3
"""
Оптимізація метаданих YouTube каналу
Фокус: Збільшення підписників та виведення в топ пошуку
"""

import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
from auth_setup import get_youtube_service

load_dotenv()

# Channel ID для SmartBabies
CHANNEL_ID = 'UCPBKtZdTxxqxU3c8iR44uhw'

def get_optimized_channel_description():
    """Генерує оптимізований опис каналу для SEO та підписників"""
    
    description = """🛸 SmartBabies® - Preschool Educational Content | Learn with ScoopyCap

Welcome to SmartBabies! We create safe, engaging, and educational videos for preschoolers and toddlers (ages 2-5). Join our friendly space explorer ScoopyCap on fun learning adventures!

🎯 WHAT WE OFFER:
• 📚 ABC & Alphabet Learning
• 🔢 Numbers & Counting
• 🎨 Colors & Shapes Recognition
• 🎵 Nursery Rhymes & Kids Songs
• 🛸 Adventure Stories with ScoopyCap
• 🌟 Safe, Age-Appropriate Content

👶 PERFECT FOR:
• Toddlers (2-3 years)
• Preschoolers (3-5 years)
• Parents looking for educational content
• Early childhood educators

✨ WHY SUBSCRIBE:
✅ New educational videos every week
✅ Safe, ad-free viewing experience
✅ Bilingual content (English, Ukrainian, Polish)
✅ Award-winning animation director
✅ Evidence-based learning approaches

📺 POPULAR PLAYLISTS:
🎵 Songs & Music: Best Nursery Rhymes Collection
🔤 Learning ABC: Alphabet & Phonics Series
🎨 Colors & Shapes: Visual Learning Adventures
🛸 ScoopyCap Adventures: Fun Stories for Kids

🔗 CONNECT WITH US:
YouTube: /@SmartBabies
Facebook: /Smart-Babies-108947580525633

📧 Business Inquiries: smartbabies.app@gmail.com

🎓 Created by award-winning animation director Dmytro Lisenbart
Over 30+ years of experience in children's content production

#KidsEducation #PreschoolLearning #SmartBabies #ScoopyCap #ToddlerEducation #KidsLearning #EducationalVideos #PreschoolContent #SafeKidsContent #NurseryRhymes #KidsSongs #LearnABC #PreschoolVideos #KidsContent #EarlyLearning #ToddlerVideos #KidsEntertainment #EducationalContent #PreschoolActivities #KidsShows"""
    
    return description

def get_optimized_channel_keywords():
    """Оптимізовані ключові слова для каналу"""
    keywords = [
        'SmartBabies',
        'ScoopyCap',
        'preschool education',
        'toddler learning',
        'educational videos for kids',
        'kids content',
        'preschool activities',
        'early learning',
        'children education',
        'safe kids content',
        'nursery rhymes',
        'kids songs',
        'alphabet learning',
        'numbers for kids',
        'colors for toddlers',
        'preschool videos',
        'educational cartoons',
        'kids animation',
        'toddler content',
        'preschool curriculum',
        'early childhood education',
        'bilingual education',
        'ukrainian kids content',
        'polish kids videos'
    ]
    return ','.join(keywords)

def get_channel_branding_recommendations():
    """Рекомендації для оформлення каналу"""
    recommendations = {
        'channel_art': {
            'title': 'Banner (Channel Art)',
            'recommendations': [
                'Розмір: 2560x1440 пікселів',
                'Включити: ScoopyCap, назву SmartBabies, емодзі',
                'Кольори: яскраві, привабливі для дітей',
                'Текст: "Learn & Play with SmartBabies"',
                'Call-to-action: "Subscribe for new videos!"'
            ]
        },
        'profile_picture': {
            'title': 'Profile Picture',
            'recommendations': [
                'Розмір: 800x800 пікселів (кругле)',
                'Включити: ScoopyCap або логотип SmartBabies',
                'Чіткий на маленькому розмірі',
                'Узгоджений з брендингом'
            ]
        },
        'video_watermark': {
            'title': 'Video Watermark (Subscribe Button)',
            'recommendations': [
                'Додати subscribe watermark на всі відео',
                'Позиція: нижній правий кут',
                'Показувати з 10-ї секунди',
                'Чіткий та не нав\'язливий'
            ]
        },
        'sections': {
            'title': 'Channel Sections (Playlists на головній)',
            'recommendations': [
                'Верхній розділ: "Popular Videos" (5-10 найкращих)',
                'Другий: "Songs & Music Playlist"',
                'Третій: "ABC Learning Series"',
                'Четвертий: "Newest Videos"',
                'П\'ятий: "ScoopyCap Adventures"'
            ]
        }
    }
    return recommendations

def update_channel_metadata(youtube, preview_mode=True):
    """Оновлює метадані каналу"""
    try:
        # Отримуємо поточні дані каналу
        request = youtube.channels().list(
            part='snippet',
            id=CHANNEL_ID
        )
        response = request.execute()
        
        if not response['items']:
            print("❌ Канал не знайдено")
            return False
        
        channel = response['items'][0]
        snippet = channel['snippet']
        
        # Зберігаємо поточні дані для порівняння
        current_desc = snippet.get('description', '')
        current_keywords = snippet.get('keywords', '')
        
        # Нові оптимізовані дані
        new_description = get_optimized_channel_description()
        new_keywords = get_optimized_channel_keywords()
        
        print("\n" + "="*70)
        print("📊 АНАЛІЗ ПОТОЧНОГО ОФОРМЛЕННЯ КАНАЛУ")
        print("="*70)
        
        print(f"\n📝 ОПИС КАНАЛУ:")
        print(f"   Поточний: {len(current_desc)} символів")
        print(f"   Новий: {len(new_description)} символів")
        print(f"   Різниця: {len(new_description) - len(current_desc)} символів")
        
        if len(current_desc) < 200:
            print("   ⚠️  Поточний опис занадто короткий для SEO (рекомендується 200+ символів)")
        
        print(f"\n🏷️  КЛЮЧОВІ СЛОВА:")
        print(f"   Поточні: {len(current_keywords.split(',')) if current_keywords else 0} ключових слів")
        print(f"   Нові: {len(new_keywords.split(','))} ключових слів")
        
        # Порівняння
        improvements = []
        if len(new_description) > len(current_desc):
            improvements.append(f"✅ Опис розширено на {len(new_description) - len(current_desc)} символів")
        if len(new_keywords.split(',')) > len(current_keywords.split(',')) if current_keywords else True:
            improvements.append("✅ Додано більше ключових слів")
        if 'ScoopyCap' not in current_desc:
            improvements.append("✅ Додано згадку про ScoopyCap (бренд)")
        if 'Subscribe' not in current_desc:
            improvements.append("✅ Додано call-to-action для підписки")
        
        if improvements:
            print(f"\n✨ ПОКРАЩЕННЯ:")
            for imp in improvements:
                print(f"   {imp}")
        
        # Показуємо новий опис
        print(f"\n📄 НОВИЙ ОПИС КАНАЛУ (перші 500 символів):")
        print("-"*70)
        print(new_description[:500] + "...")
        print("-"*70)
        
        if not preview_mode:
            print("\n🔄 Оновлюю метадані каналу...")
            snippet['description'] = new_description
            snippet['keywords'] = new_keywords
            snippet['defaultLanguage'] = 'en'
            
            update_request = youtube.channels().update(
                part='snippet',
                body={
                    'id': CHANNEL_ID,
                    'snippet': snippet
                }
            )
            update_request.execute()
            print("✅ Канал успішно оновлено!")
            return True
        else:
            print("\n⚠️  РЕЖИМ ПРЕВ'Ю: Нічого не змінено")
            print("Для застосування змін запустіть з --apply")
            return True
        
    except HttpError as e:
        print(f"❌ Помилка: {e}")
        if e.resp.status == 403:
            print("⚠️  Перевірте права доступу OAuth токену")
        return False

def print_branding_recommendations():
    """Виводить рекомендації з оформлення"""
    recommendations = get_channel_branding_recommendations()
    
    print("\n" + "="*70)
    print("🎨 РЕКОМЕНДАЦІЇ З ОФОРМЛЕННЯ КАНАЛУ")
    print("="*70)
    
    for key, rec in recommendations.items():
        print(f"\n{rec['title']}:")
        for item in rec['recommendations']:
            print(f"  • {item}")

def print_seo_recommendations():
    """Рекомендації для SEO та пошукової видимості"""
    print("\n" + "="*70)
    print("🔍 РЕКОМЕНДАЦІЇ ДЛЯ ПОШУКОВОЇ ВИДИМОСТІ")
    print("="*70)
    
    recommendations = [
        "1. Ключові слова в назві каналу: 'SmartBabies Preschool Education'",
        "2. Створіть кастомний URL: youtube.com/@SmartBabies (вже є)",
        "3. Додайте категорію: Education",
        "4. Використовуйте ключові слова в назвах плейлистів",
        "5. Регулярно оновлюйте Featured Video на головній",
        "6. Створіть пінірований коментар з посиланням на найкращі відео",
        "7. Додайте посилання на канал в описі кожного відео",
        "8. Використовуйте однакові хештеги в описі каналу та відео"
    ]
    
    for rec in recommendations:
        print(f"  {rec}")

def print_subscriber_growth_strategies():
    """Стратегії для збільшення підписників"""
    print("\n" + "="*70)
    print("👥 СТРАТЕГІЇ ДЛЯ ЗБІЛЬШЕННЯ ПІДПИСНИКІВ")
    print("="*70)
    
    strategies = [
        {
            'title': '1. Call-to-Action в відео',
            'tips': [
                'Просити підписатись в перші 15 секунд (коли найбільша увага)',
                'Використовувати візуальні підказки (subscribe button animation)',
                'Згадувати переваги підписки: "New videos every week!"'
            ]
        },
        {
            'title': '2. Ендскріни (End Screens)',
            'tips': [
                'Додати end screen на всі відео',
                'Показувати інші відео для перегляду',
                'Додати subscribe button в end screen'
            ]
        },
        {
            'title': '3. Перехрестні посилання',
            'tips': [
                'Створіть плейлист "Best of SmartBabies"',
                'Пініте його на головній сторінці каналу',
                'Додайте посилання в опис кожного відео'
            ]
        },
        {
            'title': '4. Контент-стратегія',
            'tips': [
                'Регулярність: 2-3 відео на тиждень',
                'Серійність: створити серії (ABC Series, Numbers Series)',
                'Тренди: використовувати поточні тренди в освіті'
            ]
        },
        {
            'title': '5. Співпраця та колабори',
            'tips': [
                'Співпраця з іншими каналами для дітей',
                'Участь в YouTube Shorts',
                'Cross-promotion в соцмережах'
            ]
        },
        {
            'title': '6. Оптимізація перших 48 годин',
            'tips': [
                'Публікувати в оптимальний час (для вашої аудиторії)',
                'Швидко відповідати на коментарі',
                'Поширювати в соцмережах одразу після публікації'
            ]
        }
    ]
    
    for strategy in strategies:
        print(f"\n{strategy['title']}:")
        for tip in strategy['tips']:
            print(f"  • {tip}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Оптимізація YouTube каналу')
    parser.add_argument('--apply', action='store_true', help='Застосувати зміни')
    
    args = parser.parse_args()
    
    print("🔍 АНАЛІЗУЮ КАНАЛ SMARTBABIES...")
    
    youtube = None
    if args.apply:
        print("\n🔐 Авторизація для редагування...")
        youtube = get_youtube_service()
        if not youtube:
            print("\n❌ Не вдалося авторизуватися")
            print("📝 Запустіть спочатку: python3 auth_setup.py")
            return
    
    # Отримуємо API ключ для читання
    api_key = os.getenv('YOUTUBE_API_KEY')
    if not api_key:
        print("❌ YOUTUBE_API_KEY не знайдено")
        return
    
    youtube_read = build('youtube', 'v3', developerKey=api_key)
    
    # Аналіз та оновлення
    update_channel_metadata(youtube or youtube_read, preview_mode=not args.apply)
    
    # Рекомендації
    print_branding_recommendations()
    print_seo_recommendations()
    print_subscriber_growth_strategies()
    
    print("\n" + "="*70)
    print("✅ АНАЛІЗ ЗАВЕРШЕНО")
    print("="*70)

if __name__ == '__main__':
    main()


