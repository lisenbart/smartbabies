#!/usr/bin/env python3
"""
Скрипт для виправлення обрізаних назв відео
Відновлює повні назви без обрізання слів
"""

import json
import os
import time
from datetime import datetime
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
from auth_setup import get_youtube_service

load_dotenv()

def fix_truncated_title(title):
    """Відновлює обрізану назву до повної"""
    # Видаляємо "..." в кінці
    if title.endswith('...'):
        title = title[:-3].strip()
    
    # Видаляємо "..." в середині (якщо є)
    if '...' in title:
        # Знаходимо останнє повне слово перед "..."
        parts = title.split('...')
        if len(parts) > 1:
            # Беремо першу частину і додаємо логічне завершення
            first_part = parts[0].strip()
            if first_part.endswith('Alpa'):
                return first_part.replace('Alpa', 'Alphabet')
            elif first_part.endswith('Miss Polly Had A Doll'):
                return first_part + 'y'
            elif first_part.endswith('Five Little Ghosts'):
                return first_part + ' 👻'
            elif first_part.endswith('Captain Scoopy Cap presents'):
                return first_part + ' Adventure'
            # Українські слова
            elif first_part.endswith('Хе'):
                return first_part.replace('Хе', 'Хеловін')
            elif 'Хе...' in first_part:
                return first_part.replace('Хе...', 'Хеловін')
            elif first_part.endswith('привидів?'):
                return first_part + ' Хеловін'
            else:
                return first_part
    
    return title

def get_original_title_from_description(description):
    """Намагається відновити оригінальну назву з опису"""
    lines = description.split('\n')
    for line in lines[:5]:  # Перші 5 рядків
        line = line.strip()
        if line and not line.startswith('http') and not line.startswith('#'):
            # Якщо це схоже на назву (не посилання, не хештег)
            if len(line) > 10 and not line.startswith('🎯'):
                return line
    return None

def fix_video_title(youtube, video_id, current_title, description):
    """Виправляє назву конкретного відео"""
    try:
        # Отримуємо поточні дані відео
        video_response = youtube.videos().list(
            part='snippet',
            id=video_id
        ).execute()
        
        if not video_response['items']:
            print(f"  ⚠️  Відео {video_id} не знайдено")
            return False
        
        video = video_response['items'][0]
        snippet = video['snippet']
        
        # Відновлюємо назву
        fixed_title = fix_truncated_title(current_title)
        
        # Якщо назва все ще виглядає обрізаною, намагаємося відновити з опису
        if '...' in fixed_title or len(fixed_title) < 20:
            original_from_desc = get_original_title_from_description(description)
            if original_from_desc and len(original_from_desc) > len(fixed_title):
                fixed_title = original_from_desc
        
        # Додаємо емодзі та бренд якщо потрібно
        if not any(ord(c) > 127 for c in fixed_title[:2]):
            # Визначаємо тип контенту для емодзі
            if 'alphabet' in fixed_title.lower() or 'abc' in fixed_title.lower():
                emoji = '🔤'
            elif 'number' in fixed_title.lower() or 'count' in fixed_title.lower():
                emoji = '🔢'
            elif 'color' in fixed_title.lower():
                emoji = '🎨'
            elif 'song' in fixed_title.lower() or 'music' in fixed_title.lower():
                emoji = '🎵'
            elif 'scoopycap' in fixed_title.lower() or 'adventure' in fixed_title.lower():
                emoji = '🛸'
            else:
                emoji = '🎯'
            
            fixed_title = f"{emoji} {fixed_title}"
        
        # Додаємо бренд якщо немає
        if 'SmartBabies' not in fixed_title and 'ScoopyCap' not in fixed_title:
            if ' | ' in fixed_title:
                parts = fixed_title.split(' | ', 1)
                fixed_title = f"{parts[0]} | SmartBabies {parts[1]}"
            else:
                fixed_title = f"{fixed_title} | SmartBabies"
        
        # Оновлюємо назву
        snippet['title'] = fixed_title
        
        update_response = youtube.videos().update(
            part='snippet',
            body={
                'id': video_id,
                'snippet': snippet
            }
        ).execute()
        
        return True, fixed_title
        
    except HttpError as e:
        print(f"  ❌ Помилка оновлення відео {video_id}: {e}")
        return False, current_title

def find_truncated_videos(youtube, channel_id, max_results=200):
    """Знаходить відео з обрізаними назвами"""
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
                    part='snippet',
                    id=video_id
                )
                video_response = video_request.execute()
                if video_response['items']:
                    video = video_response['items'][0]
                    title = video['snippet']['title']
                    description = video['snippet']['description']
                    
                    # Перевіряємо чи назва обрізана
                    if '...' in title or (len(title) < 30 and 'SmartBabies' not in title):
                        videos.append({
                            'video_id': video_id,
                            'title': title,
                            'description': description
                        })
            
            next_page_token = response.get('nextPageToken')
            if not next_page_token or len(videos) >= max_results:
                break
                
        return videos
    except HttpError as e:
        print(f'Помилка: {e}')
        return []

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

def main():
    print("🔍 Пошук відео з обрізаними назвами...")
    
    # Отримуємо API ключ для читання
    api_key = os.getenv('YOUTUBE_API_KEY')
    if not api_key:
        print("❌ YOUTUBE_API_KEY не знайдено в .env")
        return
    
    # Створюємо сервіс для читання
    youtube_read = build('youtube', 'v3', developerKey=api_key)
    channel_handle = os.getenv('CHANNEL_ID', '@SmartBabies')
    
    channel_id = get_channel_id(youtube_read, channel_handle)
    if not channel_id:
        print(f"❌ Канал {channel_handle} не знайдено")
        return
    
    # Знаходимо обрізані відео
    truncated_videos = find_truncated_videos(youtube_read, channel_id)
    
    if not truncated_videos:
        print("✅ Відео з обрізаними назвами не знайдено!")
        return
    
    print(f"⚠️  Знайдено {len(truncated_videos)} відео з обрізаними назвами:")
    
    for i, video in enumerate(truncated_videos, 1):
        print(f"\n[{i}] {video['title']}")
        print(f"    ID: {video['video_id']}")
        print(f"    URL: https://www.youtube.com/watch?v={video['video_id']}")
    
    # Питаємо чи виправити
    response = input(f"\n❓ Виправити ці {len(truncated_videos)} відео? (y/n): ")
    if response.lower() != 'y':
        print("❌ Скасовано")
        return
    
    # Отримуємо OAuth сервіс для редагування
    print("\n🔐 Авторизація для редагування...")
    youtube_write = get_youtube_service()
    if not youtube_write:
        print("❌ Не вдалося авторизуватися")
        print("📝 Запустіть спочатку: python3 auth_setup.py")
        return
    
    # Виправляємо відео
    print(f"\n🔧 Виправляю назви...")
    fixed_count = 0
    failed_count = 0
    changes_log = []
    
    for i, video in enumerate(truncated_videos, 1):
        video_id = video['video_id']
        current_title = video['title']
        description = video['description']
        
        print(f"\n[{i}/{len(truncated_videos)}] Виправляю: {current_title[:50]}...")
        
        success, new_title = fix_video_title(
            youtube_write, 
            video_id, 
            current_title, 
            description
        )
        
        if success:
            fixed_count += 1
            print(f"  ✅ Виправлено: {new_title}")
            changes_log.append({
                'video_id': video_id,
                'old_title': current_title,
                'new_title': new_title,
                'url': f"https://www.youtube.com/watch?v={video_id}"
            })
        else:
            failed_count += 1
            print(f"  ❌ Помилка виправлення")
        
        time.sleep(1)  # Затримка щоб не перевищити rate limits
    
    # Збереження логу
    log_file = f"fix_titles_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'total_found': len(truncated_videos),
            'fixed': fixed_count,
            'failed': failed_count,
            'changes': changes_log
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*70}")
    print(f"✅ Виправлення завершено!")
    print(f"   Виправлено: {fixed_count}")
    print(f"   Помилок: {failed_count}")
    print(f"   Лог збережено в {log_file}")
    print(f"{'='*70}")

if __name__ == '__main__':
    main()
