#!/usr/bin/env python3
"""
Інструмент для масової оптимізації метаданих відео
Генерує рекомендації та оптимізовані версії описів/тегів
"""

import json
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
from generate_description import generate_optimized_description, generate_optimized_tags

load_dotenv()

API_KEY = os.getenv('YOUTUBE_API_KEY')
CHANNEL_HANDLE = os.getenv('CHANNEL_ID', '@SmartBabies')

def get_channel_id(youtube, handle):
    """Отримує Channel ID з handle"""
    try:
        request = youtube.search().list(
            part='snippet',
            q=handle,
            type='channel',
            maxResults=1
        )
        response = request.execute()
        if response['items']:
            return response['items'][0]['snippet']['channelId']
        return None
    except HttpError as e:
        print(f'Помилка: {e}')
        return None

def get_all_videos(youtube, channel_id, max_results=50):
    """Отримує всі відео каналу"""
    try:
        # Отримуємо playlist ID з uploads
        request = youtube.channels().list(
            part='contentDetails',
            id=channel_id
        )
        response = request.execute()
        
        if not response['items']:
            return []
        
        playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        
        videos = []
        next_page_token = None
        
        while len(videos) < max_results:
            request = youtube.playlistItems().list(
                part='snippet,contentDetails',
                playlistId=playlist_id,
                maxResults=min(50, max_results - len(videos)),
                pageToken=next_page_token
            )
            response = request.execute()
            
            for item in response['items']:
                video_id = item['contentDetails']['videoId']
                video_request = youtube.videos().list(
                    part='snippet,statistics',
                    id=video_id
                )
                video_response = video_request.execute()
                if video_response['items']:
                    videos.append(video_response['items'][0])
            
            next_page_token = response.get('nextPageToken')
            if not next_page_token or len(videos) >= max_results:
                break
                
        return videos[:max_results]
    except HttpError as e:
        print(f'Помилка: {e}')
        return []

def detect_content_type(title, description, tags):
    """Визначає тип контенту на основі назви та опису"""
    text = (title + " " + description + " " + " ".join(tags)).lower()
    
    if any(word in text for word in ['number', 'count', 'math', 'цифр']):
        return 'numbers'
    elif any(word in text for word in ['color', 'colour', 'кольор']):
        return 'colors'
    elif any(word in text for word in ['song', 'music', 'пісня', 'музик']):
        return 'songs'
    elif any(word in text for word in ['adventure', 'scoopycap', 'space', 'пригода']):
        return 'adventure'
    else:
        return 'learning'

def generate_optimization_report(videos):
    """Генерує звіт з рекомендаціями по оптимізації"""
    report = {
        'total_videos': len(videos),
        'videos': []
    }
    
    for video in videos:
        snippet = video['snippet']
        stats = video.get('statistics', {})
        
        title = snippet['title']
        description = snippet['description']
        tags = snippet.get('tags', [])
        video_id = video['id']
        
        # Визначаємо тип контенту
        content_type = detect_content_type(title, description, tags)
        
        # Зберігаємо поточний опис для подальшого використання
        current_description = description
        
        # Аналізуємо поточний стан
        issues = []
        
        # Перевірка заголовку
        if len(title) < 30:
            issues.append({'type': 'title_short', 'message': f'Заголовок занадто короткий ({len(title)} символів)'})
        if 'SmartBabies' not in title and 'ScoopyCap' not in title:
            issues.append({'type': 'brand_missing', 'message': 'Відсутня назва бренду в заголовку'})
        
        # Перевірка опису
        desc_length = len(description)
        if desc_length < 200:
            issues.append({'type': 'description_short', 'message': f'Опис занадто короткий ({desc_length} символів)'})
        if 'http' not in description:
            issues.append({'type': 'links_missing', 'message': 'Відсутні посилання в описі'})
        
        # Перевірка тегів
        if len(tags) < 10:
            issues.append({'type': 'tags_few', 'message': f'Занадто мало тегів ({len(tags)})'})
        elif len(tags) > 15:
            issues.append({'type': 'tags_many', 'message': f'Занадто багато тегів ({len(tags)})'})
        
        # Генеруємо оптимізовані версії
        optimized_description = generate_optimized_description(
            title,
            content_type,
            social_links={
                'youtube': 'https://www.youtube.com/@SmartBabies',
                'facebook': 'https://www.facebook.com/Smart-Babies-108947580525633/'
            }
        )
        
        optimized_tags = generate_optimized_tags(content_type, tags[:5])
        
        # Генеруємо покращені заголовки
        improved_titles = []
        if 'SmartBabies' not in title:
            improved_titles.append(f"🔤 {title} | SmartBabies - Learn with ScoopyCap")
        if len(title) < 40:
            improved_titles.append(f"{title} - Educational Video for Preschoolers | SmartBabies")
        
        video_report = {
            'video_id': video_id,
            'current': {
                'title': title,
                'description_length': desc_length,
                'tags_count': len(tags),
                'tags': tags,
                'views': int(stats.get('viewCount', 0)),
                'likes': int(stats.get('likeCount', 0))
            },
            'current_description': current_description,  # Додаємо для update_videos.py
            'content_type': content_type,
            'issues': issues,
            'optimized': {
                'description': optimized_description,
                'description_length': len(optimized_description),
                'tags': optimized_tags,
                'tags_count': len(optimized_tags),
                'improved_titles': improved_titles
            },
            'priority': len(issues)  # Більше проблем = вищий пріоритет
        }
        
        report['videos'].append(video_report)
    
    # Сортуємо за пріоритетом
    report['videos'].sort(key=lambda x: (-x['priority'], -x['current']['views']), reverse=True)
    
    return report

def print_optimization_report(report):
    """Виводить звіт з рекомендаціями"""
    print("\n" + "="*70)
    print("🔧 РЕКОМЕНДАЦІЇ З ОПТИМІЗАЦІЇ")
    print("="*70)
    print(f"\n📊 Проаналізовано відео: {report['total_videos']}")
    
    high_priority = [v for v in report['videos'] if v['priority'] >= 3]
    if high_priority:
        print(f"\n⚠️  Відео з високим пріоритетом оптимізації: {len(high_priority)}")
    
    print("\n" + "="*70)
    
    for i, video in enumerate(report['videos'][:10], 1):  # Показуємо топ 10
        print(f"\n{'='*70}")
        print(f"ВІДЕО #{i}: {video['current']['title'][:60]}")
        print(f"{'='*70}")
        print(f"📺 ID: {video['video_id']}")
        print(f"👀 Перегляди: {video['current']['views']:,}")
        print(f"👍 Лайки: {video['current']['likes']:,}")
        print(f"📝 Тип контенту: {video['content_type']}")
        print(f"⚡ Пріоритет оптимізації: {'🔴 Високий' if video['priority'] >= 3 else '🟡 Середній' if video['priority'] >= 1 else '🟢 Низький'}")
        
        if video['issues']:
            print(f"\n❌ ПРОБЛЕМИ ({len(video['issues'])}):")
            for issue in video['issues']:
                print(f"  • {issue['message']}")
        
        if video['optimized']['improved_titles']:
            print(f"\n💡 ПОКРАЩЕНІ ЗАГОЛОВКИ:")
            for title in video['optimized']['improved_titles']:
                print(f"  • {title} ({len(title)} символів)")
        
        print(f"\n📈 ПОКРАЩЕННЯ:")
        print(f"  • Опис: {video['current']['description_length']} → {video['optimized']['description_length']} символів (+{video['optimized']['description_length'] - video['current']['description_length']})")
        print(f"  • Теги: {video['current']['tags_count']} → {video['optimized']['tags_count']}")
        
        print(f"\n🏷️  ОПТИМІЗОВАНІ ТЕГИ:")
        print(f"  {', '.join(video['optimized']['tags'][:10])}")

def main():
    if not API_KEY:
        print("❌ Помилка: YOUTUBE_API_KEY не знайдено")
        return
    
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    
    print("🔍 Отримую дані каналу...")
    channel_id = get_channel_id(youtube, CHANNEL_HANDLE)
    
    if not channel_id:
        print(f"❌ Канал {CHANNEL_HANDLE} не знайдено")
        return
    
    print(f"✅ Канал знайдено!")
    print("🎥 Аналізую відео...")
    
    videos = get_all_videos(youtube, channel_id, max_results=50)
    
    if not videos:
        print("❌ Відео не знайдено")
        return
    
    print(f"✅ Знайдено {len(videos)} відео")
    print("🔧 Генерую рекомендації...")
    
    report = generate_optimization_report(videos)
    
    print_optimization_report(report)
    
    # Збереження
    with open('optimization_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    # Генерація файлів з оптимізованими описами
    print("\n💾 Зберігаю результати...")
    
    for video in report['videos'][:20]:  # Перші 20 відео
        filename = f"optimized_{video['video_id']}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"ВІДЕО: {video['current']['title']}\n")
            f.write(f"ID: {video['video_id']}\n")
            f.write("="*70 + "\n\n")
            f.write("ОПТИМІЗОВАНИЙ ОПИС:\n")
            f.write("="*70 + "\n\n")
            f.write(video['optimized']['description'])
            f.write("\n\n" + "="*70 + "\n")
            f.write("ОПТИМІЗОВАНІ ТЕГИ:\n")
            f.write("="*70 + "\n")
            f.write(", ".join(video['optimized']['tags']))
            f.write("\n")
    
    print(f"✅ Створено {min(20, len(report['videos']))} файлів з оптимізованими описами")
    print("✅ Повний звіт збережено в optimization_report.json")

if __name__ == '__main__':
    main()

