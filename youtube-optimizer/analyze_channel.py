#!/usr/bin/env python3
"""
Аналізатор YouTube каналу SmartBabies
Аналізує поточну оптимізацію та дає рекомендації
"""

import os
import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

load_dotenv()

# Конфігурація
API_KEY = os.getenv('YOUTUBE_API_KEY')
CHANNEL_HANDLE = os.getenv('CHANNEL_ID', '@SmartBabies')

def get_channel_id(youtube, handle):
    """Отримує Channel ID з handle (@SmartBabies)"""
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
        print(f'Помилка пошуку каналу: {e}')
        return None

def analyze_channel(youtube, channel_id):
    """Аналізує інформацію про канал"""
    try:
        request = youtube.channels().list(
            part='snippet,statistics,contentDetails',
            id=channel_id
        )
        response = request.execute()
        
        if not response['items']:
            print('Канал не знайдено')
            return None
            
        channel = response['items'][0]
        stats = channel['statistics']
        snippet = channel['snippet']
        
        return {
            'title': snippet['title'],
            'description': snippet['description'],
            'subscribers': int(stats.get('subscriberCount', 0)),
            'total_views': int(stats.get('viewCount', 0)),
            'video_count': int(stats.get('videoCount', 0)),
            'custom_url': snippet.get('customUrl', ''),
            'published_at': snippet['publishedAt'],
            'keywords': snippet.get('keywords', ''),
            'country': snippet.get('country', ''),
            'playlist_id': channel['contentDetails']['relatedPlaylists']['uploads']
        }
    except HttpError as e:
        print(f'Помилка отримання даних каналу: {e}')
        return None

def get_recent_videos(youtube, playlist_id, max_results=10):
    """Отримує останні відео з каналу"""
    try:
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
                video_data = get_video_details(youtube, video_id)
                if video_data:
                    videos.append(video_data)
            
            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break
                
        return videos[:max_results]
    except HttpError as e:
        print(f'Помилка отримання відео: {e}')
        return []

def get_video_details(youtube, video_id):
    """Отримує детальну інформацію про відео"""
    try:
        request = youtube.videos().list(
            part='snippet,statistics,contentDetails',
            id=video_id
        )
        response = request.execute()
        
        if not response['items']:
            return None
            
        video = response['items'][0]
        snippet = video['snippet']
        stats = video['statistics']
        
        return {
            'id': video_id,
            'title': snippet['title'],
            'description': snippet['description'],
            'tags': snippet.get('tags', []),
            'published_at': snippet['publishedAt'],
            'views': int(stats.get('viewCount', 0)),
            'likes': int(stats.get('likeCount', 0)),
            'comments': int(stats.get('commentCount', 0)),
            'duration': video['contentDetails']['duration'],
            'category_id': snippet.get('categoryId', ''),
            'thumbnails': snippet.get('thumbnails', {}),
            'has_custom_thumbnail': 'high' in snippet.get('thumbnails', {})
        }
    except HttpError as e:
        print(f'Помилка отримання даних відео {video_id}: {e}')
        return None

def analyze_video_seo(video):
    """Аналізує SEO оптимізацію відео"""
    issues = []
    recommendations = []
    
    title = video['title']
    description = video['description']
    tags = video.get('tags', [])
    
    # Аналіз заголовку
    if len(title) < 30:
        issues.append('Заголовок занадто короткий (мінімум 30 символів)')
    elif len(title) > 60:
        issues.append('Заголовок занадто довгий (макс 60 символів для повного відображення)')
    
    if 'SmartBabies' not in title and 'ScoopyCap' not in title:
        recommendations.append('Додайте назву бренду до заголовку')
    
    # Аналіз опису
    desc_length = len(description)
    if desc_length < 200:
        issues.append(f'Опис занадто короткий ({desc_length} символів, мінімум 200)')
        recommendations.append('Розширте опис до мінімум 200 символів')
    elif desc_length < 1000:
        recommendations.append('Ідеальний опис для SEO має 1000+ символів')
    
    # Перевірка наявності посилань
    if 'http' not in description:
        recommendations.append('Додайте посилання на ваш сайт/соцмережі в опис')
    
    # Перевірка тегів
    if len(tags) < 10:
        issues.append(f'Занадто мало тегів ({len(tags)}, рекомендується 10-15)')
    elif len(tags) > 15:
        issues.append(f'Занадто багато тегів ({len(tags)}, максимум 15)')
    
    # Перевірка таймкодів
    if '# ' not in description and '0:00' not in description:
        recommendations.append('Додайте таймкоди до опису для кращої навігації')
    
    # Перевірка хештегів
    hashtags = [word for word in description.split() if word.startswith('#')]
    if len(hashtags) < 3:
        recommendations.append('Додайте хештеги (3-5 штук) в опис відео')
    
    return {
        'issues': issues,
        'recommendations': recommendations,
        'seo_score': max(0, 100 - (len(issues) * 15 + len(recommendations) * 5))
    }

def print_analysis_report(channel_data, videos):
    """Виводить звіт аналізу"""
    print("\n" + "="*70)
    print("📊 АНАЛІЗ КАНАЛУ SMARTBABIES")
    print("="*70)
    
    if not channel_data:
        print("❌ Не вдалося отримати дані каналу")
        return
    
    print(f"\n📺 Канал: {channel_data['title']}")
    print(f"👥 Підписники: {channel_data['subscribers']:,}")
    print(f"👀 Всього переглядів: {channel_data['total_views']:,}")
    print(f"🎬 Кількість відео: {channel_data['video_count']}")
    
    if channel_data['description']:
        desc_len = len(channel_data['description'])
        print(f"\n📝 Опис каналу: {desc_len} символів")
        if desc_len < 200:
            print("⚠️  Опис каналу занадто короткий (рекомендується 200+ символів)")
    
    print("\n" + "="*70)
    print("🎥 АНАЛІЗ ВІДЕО")
    print("="*70)
    
    total_seo_score = 0
    
    for i, video in enumerate(videos, 1):
        print(f"\n--- Відео {i}: {video['title'][:60]}... ---")
        print(f"Перегляди: {video['views']:,} | Лайки: {video['likes']:,}")
        
        seo_analysis = analyze_video_seo(video)
        total_seo_score += seo_analysis['seo_score']
        
        print(f"📈 SEO Score: {seo_analysis['seo_score']}/100")
        
        if seo_analysis['issues']:
            print("\n❌ Проблеми:")
            for issue in seo_analysis['issues']:
                print(f"  • {issue}")
        
        if seo_analysis['recommendations']:
            print("\n💡 Рекомендації:")
            for rec in seo_analysis['recommendations']:
                print(f"  • {rec}")
        
        print(f"\nТеги ({len(video.get('tags', []))}): {', '.join(video.get('tags', [])[:5])}")
    
    avg_seo = total_seo_score / len(videos) if videos else 0
    print("\n" + "="*70)
    print(f"📊 СЕРЕДНІЙ SEO SCORE: {avg_seo:.1f}/100")
    print("="*70)

def main():
    if not API_KEY:
        print("❌ Помилка: YOUTUBE_API_KEY не знайдено в .env файлі")
        print("📝 Створіть .env файл та додайте ваш API ключ")
        return
    
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    
    print("🔍 Шукаю канал SmartBabies...")
    channel_id = get_channel_id(youtube, CHANNEL_HANDLE)
    
    if not channel_id:
        print(f"❌ Канал {CHANNEL_HANDLE} не знайдено")
        return
    
    print(f"✅ Канал знайдено! ID: {channel_id}")
    print("📊 Аналізую канал...")
    
    channel_data = analyze_channel(youtube, channel_id)
    
    if not channel_data:
        print("❌ Не вдалося отримати дані каналу")
        return
    
    print("🎥 Аналізую останні відео...")
    videos = get_recent_videos(youtube, channel_data['playlist_id'], max_results=10)
    
    print_analysis_report(channel_data, videos)
    
    # Збереження результатів
    report = {
        'channel': channel_data,
        'videos': videos,
        'analysis': [analyze_video_seo(v) for v in videos]
    }
    
    with open('analysis_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print("\n💾 Результати збережено в analysis_report.json")

if __name__ == '__main__':
    main()

