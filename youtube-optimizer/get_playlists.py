#!/usr/bin/env python3
"""
Отримує реальні плейлисти з YouTube каналу для використання в описах
"""

import os
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

def get_channel_playlists(youtube, channel_id):
    """Отримує всі плейлисти каналу"""
    try:
        playlists = []
        next_page_token = None
        
        while True:
            request = youtube.playlists().list(
                part='snippet',
                channelId=channel_id,
                maxResults=50,
                pageToken=next_page_token
            )
            response = request.execute()
            
            for item in response['items']:
                playlists.append({
                    'id': item['id'],
                    'title': item['snippet']['title'],
                    'url': f"https://www.youtube.com/playlist?list={item['id']}"
                })
            
            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break
                
        return playlists
    except Exception as e:
        print(f'Помилка отримання плейлистів: {e}')
        return []

def find_best_playlist(playlists, content_type):
    """Знаходить найкращий плейлист для типу контенту"""
    # Ключові слова для пошуку
    keywords_map = {
        'songs': ['song', 'music', 'nursery rhyme', 'rhyme', 'sing'],
        'learning': ['abc', 'learn', 'alphabet', 'education', 'learn'],
        'numbers': ['number', 'count', 'math'],
        'colors': ['color', 'shape', 'colour'],
        'adventure': ['scoopy', 'adventure', 'story']
    }
    
    keywords = keywords_map.get(content_type, ['song', 'kids'])
    
    best_match = None
    best_score = 0
    
    for playlist in playlists:
        title_lower = playlist['title'].lower()
        score = sum(1 for keyword in keywords if keyword in title_lower)
        
        # Додатковий бонус для "top", "best", "popular"
        if any(word in title_lower for word in ['top', 'best', 'popular', 'favorite']):
            score += 1
            
        if score > best_score:
            best_score = score
            best_match = playlist
    
    return best_match

def get_playlists_for_channel(youtube, channel_handle='@SmartBabies'):
    """Отримує плейлисти для каналу та повертає найкращі для кожного типу контенту"""
    # Отримуємо channel ID
    request = youtube.search().list(
        part='snippet',
        q=channel_handle,
        type='channel',
        maxResults=1
    )
    response = request.execute()
    
    if not response['items']:
        return {}
    
    channel_id = response['items'][0]['snippet']['channelId']
    
    # Отримуємо всі плейлисти
    playlists = get_channel_playlists(youtube, channel_id)
    
    # Знаходимо найкращі для кожного типу
    best_playlists = {}
    for content_type in ['songs', 'learning', 'numbers', 'colors', 'adventure']:
        best = find_best_playlist(playlists, content_type)
        if best:
            best_playlists[content_type] = best
    
    # Якщо не знайшли для конкретного типу, використовуємо загальний
    if 'songs' in best_playlists:
        best_playlists.setdefault('learning', best_playlists['songs'])
        best_playlists.setdefault('numbers', best_playlists['songs'])
        best_playlists.setdefault('colors', best_playlists['songs'])
    
    return best_playlists

if __name__ == '__main__':
    api_key = os.getenv('YOUTUBE_API_KEY')
    if not api_key:
        print("❌ YOUTUBE_API_KEY не знайдено")
        exit(1)
    
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    print("🔍 Отримую плейлисти каналу...")
    playlists = get_playlists_for_channel(youtube)
    
    print("\n📚 Рекомендовані плейлисти для описів:")
    print("="*70)
    for content_type, playlist in playlists.items():
        print(f"{content_type:10}: {playlist['title'][:50]:50} | {playlist['url']}")


