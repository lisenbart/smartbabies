#!/usr/bin/env python3
"""
Масова оптимізація та оновлення метаданих відео на YouTube
Підвищує SEO, CTR та retention для збільшення переглядів
"""

import json
import os
import sys
import time
from datetime import datetime
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
from auth_setup import get_youtube_service
from optimize_videos import get_channel_id, get_all_videos, detect_content_type, generate_optimization_report
from generate_description import generate_optimized_description, generate_optimized_tags
from get_playlists import get_playlists_for_channel

load_dotenv()

def optimize_title(title, content_type):
    """Оптимізує заголовок для максимального CTR БЕЗ обрізання слів"""
    # Спочатку виправляємо обрізані назви
    optimized = title.strip()
    
    # Відновлюємо відомі обрізані слова ПЕРЕД видаленням "..."
    if 'presents: ...' in optimized:
        optimized = optimized.replace('presents: ...', 'presents: Adventure')
    if 'на Хе...' in optimized:
        optimized = optimized.replace('на Хе...', 'на Хеловін')
    if optimized.endswith('Хе...'):
        optimized = optimized.replace('Хе...', 'Хеловін')
    if 'Хе...' in optimized:
        optimized = optimized.replace('Хе...', 'Хеловін')
    if optimized.endswith('Alpa'):
        optimized = optimized.replace('Alpa', 'Alphabet')
    if optimized.endswith('Ghos'):
        optimized = optimized + 'ts'
    if optimized.endswith('Watch'):
        optimized = optimized + ' Now'
    if optimized.endswith('presents:'):
        optimized = optimized + ' Adventure'
    # Українські слова
    if optimized.endswith('Хе'):
        optimized = optimized.replace('Хе', 'Хеловін')
    if optimized.endswith('привидів?'):
        optimized = optimized + ' Хеловін'
    if optimized.endswith('на Хе'):
        optimized = optimized.replace('на Хе', 'на Хеловін')
    if optimized.endswith('на'):
        optimized = optimized + ' Хеловін'
    
    # Видаляємо "..." в кінці тільки якщо залишилися
    if optimized.endswith('...'):
        optimized = optimized[:-3].strip()
    
    # Додаємо емодзі якщо немає
    emoji_map = {
        'learning': '🔤',
        'numbers': '🔢',
        'colors': '🎨',
        'songs': '🎵',
        'adventure': '🛸'
    }
    emoji = emoji_map.get(content_type, '🎯')
    
    if not any(ord(c) > 127 for c in optimized[:2]):  # Якщо немає емодзі на початку
        optimized = f"{emoji} {optimized}"
    
    # Додаємо бренд якщо немає
    if 'SmartBabies' not in optimized and 'ScoopyCap' not in optimized:
        # Вставляємо після емодзі або на початку
        if ' | ' in optimized:
            parts = optimized.split(' | ', 1)
            optimized = f"{parts[0]} | SmartBabies {parts[1]}"
        else:
            optimized = f"{optimized} | SmartBabies"
    
    # Розумне скорочення БЕЗ обрізання слів
    if len(optimized) > 100:  # YouTube дозволяє до 100 символів
        # Видаляємо зайві слова, але зберігаємо цілісність
        words = optimized.split()
        
        # Видаляємо зайві слова з кінця, але зберігаємо важливі
        important_words = ['SmartBabies', 'ScoopyCap', 'Learn', 'Kids', 'Preschool', 'Alphabet', 'Ghosts', 'Хеловін']
        while len(' '.join(words)) > 100 and len(words) > 3:
            # Не видаляємо важливі слова
            last_word = words[-1]
            if not any(important in last_word for important in important_words):
                words.pop()
            else:
                # Якщо останнє слово важливе, видаляємо попереднє
                if len(words) > 4:
                    words.pop(-2)
                else:
                    break
        
        optimized = ' '.join(words)
    
    return optimized

def create_enhanced_description(title, content_type, current_desc, video_id, playlists_cache=None, youtube_api=None):
    """Створює покращений опис з фокусом на retention та CTR"""
    
    # Базовий опис (без посилання на сайт - тимчасово недоступний)
    social_links = {
        'youtube': 'https://www.youtube.com/@SmartBabies',
        'facebook': 'https://www.facebook.com/Smart-Babies-108947580525633/'
        # 'website' прибрано - тимчасово недоступний
    }
    
    description = generate_optimized_description(
        title,
        content_type,
        social_links=social_links
    )
    
    # Додаємо call-to-action на початку (підвищує retention)
    cta_text = f"""🎯 Press LIKE if your child enjoyed this video! 
💬 Comment below what your little one learned today!

"""
    
    # Вставляємо CTA після першого абзацу
    lines = description.split('\n')
    if len(lines) > 3:
        description = '\n'.join(lines[:3]) + '\n' + cta_text + '\n'.join(lines[3:])
    
    # Отримуємо реальні плейлисти
    if playlists_cache is None and youtube_api:
        try:
            playlists_cache = get_playlists_for_channel(youtube_api)
        except:
            playlists_cache = {}
    
    # Додаємо реальні посилання на плейлисти
    description += "\n\n📚 MORE SMARTBABIES CONTENT:\n"
    
    if playlists_cache:
        # Використовуємо специфічний плейлист для типу контенту
        if content_type == 'songs' and 'songs' in playlists_cache:
            songs_playlist = playlists_cache['songs']
            description += f"🎵 Songs & Music: {songs_playlist['url']}\n"
        elif 'songs' in playlists_cache:
            description += f"🎵 Songs & Music: {playlists_cache['songs']['url']}\n"
        else:
            description += "🎵 Songs & Music: https://www.youtube.com/@SmartBabies/playlists\n"
        
        if content_type == 'learning' and 'learning' in playlists_cache:
            learning_playlist = playlists_cache['learning']
            description += f"🔤 Learning ABC: {learning_playlist['url']}\n"
        elif 'learning' in playlists_cache:
            description += f"🔤 Learning ABC: {playlists_cache['learning']['url']}\n"
        else:
            description += "🔤 Learning ABC: https://www.youtube.com/@SmartBabies/playlists\n"
        
        if content_type == 'colors' and 'colors' in playlists_cache:
            colors_playlist = playlists_cache['colors']
            description += f"🎨 Colors & Shapes: {colors_playlist['url']}\n"
        elif 'colors' in playlists_cache:
            description += f"🎨 Colors & Shapes: {playlists_cache['colors']['url']}\n"
        elif 'songs' in playlists_cache:
            # Якщо немає окремого для colors, використовуємо загальний
            description += f"🎨 Colors & Shapes: {playlists_cache['songs']['url']}\n"
        else:
            description += "🎨 Colors & Shapes: https://www.youtube.com/@SmartBabies/playlists\n"
    else:
        # Fallback якщо не вдалося отримати плейлисти
        description += "🎵 Songs & Music: https://www.youtube.com/@SmartBabies/playlists\n"
        description += "🔤 Learning ABC: https://www.youtube.com/@SmartBabies/playlists\n"
        description += "🎨 Colors & Shapes: https://www.youtube.com/@SmartBabies/playlists\n"
    
    # Додаємо більше релевантних хештегів для discovery
    relevant_hashtags = [
        '#KidsEducation',
        '#PreschoolLearning',
        '#SmartBabies',
        '#ScoopyCap',
        '#ToddlerEducation',
        '#KidsLearning',
        '#EducationalVideos',
        '#PreschoolContent',
        '#SafeKidsContent',
        '#KidsContent',
        '#LearningForKids',
        '#PreschoolVideos'
    ]
    
    # Додаємо локалізовані хештеги
    if 'ukrainian' in current_desc.lower() or 'україн' in current_desc.lower():
        relevant_hashtags.extend(['#УкраїнськіДіти', '#ОсвітаДітей'])
    
    if 'polish' in current_desc.lower() or 'polski' in current_desc.lower():
        relevant_hashtags.extend(['#EdukacjaDzieci', '#PolskieDzieci'])
    
    description += "\n" + " ".join(relevant_hashtags[:10])
    
    return description

def update_video_metadata(youtube, video_id, optimized_title, optimized_description, optimized_tags):
    """Оновлює метадані відео через YouTube API"""
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
        
        # Оновлюємо метадані
        snippet['title'] = optimized_title
        snippet['description'] = optimized_description
        snippet['tags'] = optimized_tags[:15]  # YouTube обмежує до 15
        
        # Оновлюємо відео
        update_response = youtube.videos().update(
            part='snippet',
            body={
                'id': video_id,
                'snippet': snippet
            }
        ).execute()
        
        return True
        
    except HttpError as e:
        print(f"  ❌ Помилка оновлення відео {video_id}: {e}")
        if e.resp.status == 403:
            print("  ⚠️  Перевірте права доступу OAuth токену")
        return False

def batch_update_videos(youtube, videos_data, preview_mode=True, limit=None):
    """
    Масове оновлення відео
    
    Args:
        youtube: YouTube API сервіс
        videos_data: список словників з даними відео
        preview_mode: якщо True, тільки показує що буде змінено
        limit: максимальна кількість відео для оновлення
    """
    if limit:
        videos_data = videos_data[:limit]
    
    total = len(videos_data)
    updated = 0
    failed = 0
    
    print(f"\n{'='*70}")
    print(f"🚀 {'PREVIEW' if preview_mode else 'ОНОВЛЕННЯ'} МЕТАДАНИХ ВІДЕО")
    print(f"{'='*70}")
    print(f"📊 Всього відео: {total}")
    
    if preview_mode:
        print("\n⚠️  РЕЖИМ ПРЕВ'Ю: Нічого не буде змінено в YouTube")
        print("Для реального оновлення запустіть з --apply\n")
    
    # Отримуємо реальні плейлисти один раз (для використання API ключа)
    print("📚 Отримую реальні плейлисти каналу...")
    playlists_cache = {}
    try:
        from dotenv import load_dotenv
        import os
        load_dotenv()
        api_key = os.getenv('YOUTUBE_API_KEY')
        if api_key:
            youtube_read = build('youtube', 'v3', developerKey=api_key)
            playlists_cache = get_playlists_for_channel(youtube_read)
            print(f"✅ Знайдено {len(playlists_cache)} плейлистів для використання")
    except Exception as e:
        print(f"⚠️  Не вдалося отримати плейлисти: {e}")
        print("   Будуть використовуватись загальні посилання\n")
    
    changes_log = []
    
    for i, video_info in enumerate(videos_data, 1):
        video_id = video_info['video_id']
        current_title = video_info['current']['title']
        current_desc_len = video_info['current']['description_length']
        current_tags_count = video_info['current']['tags_count']
        
        # Генеруємо оптимізовані версії
        content_type = video_info['content_type']
        optimized_title = optimize_title(current_title, content_type)
        optimized_description = create_enhanced_description(
            optimized_title,
            content_type,
            video_info.get('current_description', ''),
            video_id,
            playlists_cache=playlists_cache
        )
        optimized_tags = video_info['optimized']['tags']
        
        print(f"\n[{i}/{total}] {current_title[:50]}...")
        print(f"  ID: {video_id}")
        
        # Показуємо зміни
        title_changed = current_title != optimized_title
        desc_changed = len(optimized_description) != current_desc_len
        tags_changed = len(optimized_tags) != current_tags_count
        
        if title_changed:
            print(f"  📝 Заголовок:")
            print(f"     Було: {current_title[:60]} ({len(current_title)} символів)")
            print(f"     Стане: {optimized_title} ({len(optimized_title)} символів)")
        
        if desc_changed:
            print(f"  📄 Опис:")
            print(f"     Було: {current_desc_len} символів")
            print(f"     Стане: {len(optimized_description)} символів")
        
        if tags_changed:
            print(f"  🏷️  Теги:")
            print(f"     Було: {current_tags_count} тегів")
            print(f"     Стане: {len(optimized_tags)} тегів")
        
        if not title_changed and not desc_changed and not tags_changed:
            print(f"  ✓ Вже оптимізовано")
            continue
        
        if not preview_mode:
            print(f"  🔄 Оновлюю...")
            success = update_video_metadata(
                youtube,
                video_id,
                optimized_title,
                optimized_description,
                optimized_tags
            )
            
            if success:
                updated += 1
                print(f"  ✅ Оновлено успішно!")
                time.sleep(1)  # Затримка щоб не перевищити rate limits
            else:
                failed += 1
                print(f"  ❌ Помилка оновлення")
        
        changes_log.append({
            'video_id': video_id,
            'title': current_title,
            'optimized_title': optimized_title,
            'title_changed': title_changed,
            'description_length_changed': desc_changed,
            'tags_count_changed': tags_changed
        })
    
    # Збереження логу
    log_file = f"update_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'preview_mode': preview_mode,
            'total': total,
            'updated': updated if not preview_mode else 0,
            'failed': failed if not preview_mode else 0,
            'changes': changes_log
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*70}")
    if preview_mode:
        print(f"📋 Прев'ю завершено! Лог збережено в {log_file}")
        print(f"\n💡 Для застосування змін запустіть:")
        print(f"   python3 update_videos.py --apply")
    else:
        print(f"✅ Оновлення завершено!")
        print(f"   Успішно оновлено: {updated}")
        print(f"   Помилок: {failed}")
        print(f"   Лог збережено в {log_file}")
    print(f"{'='*70}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Масова оптимізація метаданих відео YouTube'
    )
    parser.add_argument(
        '--apply',
        action='store_true',
        help='Застосувати зміни (без цього працює тільки прев\'ю)'
    )
    parser.add_argument(
        '--limit',
        type=int,
        help='Обмежити кількість відео для оновлення (для тестування)'
    )
    parser.add_argument(
        '--priority',
        action='store_true',
        help='Оновити тільки відео з високим пріоритетом (3+ проблем)'
    )
    
    args = parser.parse_args()
    
    print("🔍 Аналізую канал та підготую оптимізовані метадані...")
    
    # Отримуємо API ключ для читання даних
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
    
    # Отримуємо всі відео
    print(f"📥 Отримую дані відео...")
    videos = get_all_videos(youtube_read, channel_id, max_results=200)
    
    if not videos:
        print("❌ Відео не знайдено")
        return
    
    print(f"✅ Знайдено {len(videos)} відео")
    
    # Генеруємо оптимізаційний звіт
    print(f"🔧 Аналізую та оптимізую метадані...")
    report = generate_optimization_report(videos)
    
    # Отримуємо описи для кращої оптимізації
    for video_info in report['videos']:
        video_id = video_info['video_id']
        video_response = youtube_read.videos().list(
            part='snippet',
            id=video_id
        ).execute()
        if video_response['items']:
            video_info['current_description'] = video_response['items'][0]['snippet']['description']
    
    # Фільтруємо за пріоритетом якщо потрібно
    if args.priority:
        report['videos'] = [v for v in report['videos'] if v['priority'] >= 3]
        print(f"📊 Після фільтрації: {len(report['videos'])} відео з високим пріоритетом")
    
    # Отримуємо OAuth сервіс для редагування (тільки якщо не preview)
    youtube_write = None
    if args.apply:
        print("\n🔐 Авторизація для редагування...")
        youtube_write = get_youtube_service()
        if not youtube_write:
            print("\n❌ Не вдалося авторизуватися")
            print("📝 Запустіть спочатку: python3 auth_setup.py")
            return
    
    # Виконуємо оновлення
    batch_update_videos(
        youtube_write or youtube_read,  # Використовуємо write тільки для реальних оновлень
        report['videos'],
        preview_mode=not args.apply,
        limit=args.limit
    )

if __name__ == '__main__':
    main()

