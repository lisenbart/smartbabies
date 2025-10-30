#!/usr/bin/env python3
"""
Генератор оптимізованих описів та тегів для відео SmartBabies
"""

import argparse
from datetime import datetime

# Шаблони для різних типів контенту
CONTENT_TEMPLATES = {
    'learning': {
        'title_prefix': '🔤',
        'keywords': ['alphabet', 'letters', 'learning', 'education', 'preschool'],
        'hashtags': ['#KidsEducation', '#PreschoolLearning', '#SmartBabies', '#AlphabetForKids']
    },
    'numbers': {
        'title_prefix': '🔢',
        'keywords': ['numbers', 'counting', 'math', 'preschool', 'toddler'],
        'hashtags': ['#LearnNumbers', '#CountingForKids', '#SmartBabies', '#PreschoolMath']
    },
    'colors': {
        'title_prefix': '🎨',
        'keywords': ['colors', 'learning', 'preschool', 'toddler', 'education'],
        'hashtags': ['#LearnColors', '#KidsEducation', '#SmartBabies', '#Preschool']
    },
    'songs': {
        'title_prefix': '🎵',
        'keywords': ['kids songs', 'children music', 'preschool', 'educational songs'],
        'hashtags': ['#KidsSongs', '#ChildrenMusic', '#SmartBabies', '#PreschoolSongs']
    },
    'adventure': {
        'title_prefix': '🛸',
        'keywords': ['ScoopyCap', 'adventure', 'space', 'preschool', 'learning'],
        'hashtags': ['#ScoopyCap', '#SmartBabies', '#KidsAdventure', '#Preschool']
    }
}

def generate_optimized_tags(content_type, additional_tags=None):
    """Генерація оптимізованих тегів"""
    base_tags = CONTENT_TEMPLATES.get(content_type, CONTENT_TEMPLATES['learning'])['keywords']
    
    # Загальні теги для SmartBabies
    smartbabies_tags = [
        'SmartBabies',
        'ScoopyCap',
        'preschool education',
        'toddler learning',
        'educational videos for kids',
        'kids content',
        'preschool activities',
        'early learning',
        'children education',
        'safe kids content'
    ]
    
    # Локалізація
    multilingual_tags = [
        'ukrainian kids content',
        'polish kids videos',
        'bilingual education'
    ]
    
    all_tags = base_tags + smartbabies_tags[:10] + multilingual_tags[:3]
    
    if additional_tags:
        all_tags.extend(additional_tags)
    
    # Унікальність та обмеження до 15
    unique_tags = list(dict.fromkeys(all_tags))[:15]
    
    return unique_tags

def generate_optimized_description(title, content_type, video_length_minutes=None, timestamps=None, 
                                   social_links=None, language='en'):
    """Генерація оптимізованого опису з фокусом на CTR та retention"""
    template = CONTENT_TEMPLATES.get(content_type, CONTENT_TEMPLATES['learning'])
    prefix = template['title_prefix']
    
    # Початок з ключового тексту (перші 2 рядки - найважливіші для SEO)
    # Додаємо CTA для підвищення engagement
    description = f"""{prefix} {title}

🎯 Learn with SmartBabies! Educational content designed for preschoolers and toddlers.
👍 LIKE this video if your child loves learning with ScoopyCap!

"""
    
    # Основна інформація з фокусом на користь
    description += "📚 WHAT YOUR CHILD WILL LEARN:\n"
    learning_points_detailed = {
        'learning': '• Letter recognition and phonics\n• Building vocabulary\n• Early reading skills\n• Pronunciation practice\n',
        'numbers': '• Number recognition 1-10\n• Counting skills\n• Basic math concepts\n• Pattern recognition\n',
        'colors': '• Color names and identification\n• Color matching\n• Creative expression\n• Visual learning\n',
        'songs': '• Rhythm and melody\n• Language development\n• Memory enhancement\n• Motor skills through dance\n',
        'adventure': '• Critical thinking\n• Problem-solving\n• Social-emotional skills\n• Exploration and curiosity\n'
    }
    description += learning_points_detailed.get(content_type, '• Fun educational content\n• Safe viewing experience\n• Age-appropriate learning\n')
    description += "\n🎓 Perfect for ages 2-5 years old!\n\n"
    
    # Таймкоди (якщо є)
    if timestamps:
        description += "⏱️ CHAPTERS:\n"
        for time, label in timestamps:
            description += f"{time} - {label}\n"
        description += "\n"
    elif video_length_minutes and video_length_minutes > 2:
        description += "💡 TIP: Use the chapters in this video to jump to your favorite parts!\n\n"
    
    # Що діти вивчать
    description += "✨ WHAT CHILDREN WILL LEARN:\n"
    learning_points = {
        'learning': '• Letter recognition and sounds\n• Basic vocabulary\n• Pronunciation skills\n',
        'numbers': '• Number recognition\n• Counting skills\n• Basic math concepts\n',
        'colors': '• Color names and recognition\n• Matching colors\n• Creative expression\n',
        'songs': '• Rhythm and melody\n• Language development\n• Memory skills\n',
        'adventure': '• Problem-solving\n• Curiosity and exploration\n• Social-emotional skills\n'
    }
    description += learning_points.get(content_type, '• Fun and educational content\n• Safe viewing experience\n')
    
    description += "\n"
    
    # Про SmartBabies
    description += "🛸 ABOUT SMARTBABIES:\n"
    description += """SmartBabies® creates safe, engaging educational content for preschoolers. 
Our hero ScoopyCap guides children through fun learning adventures!

👉 SUBSCRIBE NOW: https://www.youtube.com/@SmartBabies?sub_confirmation=1
🔔 Click the bell for notifications!

"""
    
    # Соціальні мережі
    if social_links:
        description += "🔗 FOLLOW US:\n"
        if social_links.get('youtube'):
            description += f"YouTube: {social_links['youtube']}\n"
        if social_links.get('facebook'):
            description += f"Facebook: {social_links.get('facebook')}\n"
        description += "\n"
    
    # Хештеги (в кінці опису)
    hashtags = template['hashtags']
    description += " ".join(hashtags)
    
    # Додаткові хештеги для покращення
    additional_hashtags = [
        '#ToddlerEducation',
        '#KidsLearning',
        '#EducationalVideos',
        '#PreschoolContent',
        '#SafeKidsContent'
    ]
    description += " " + " ".join(additional_hashtags[:3])
    
    return description

def generate_title_suggestions(content_topic, content_type):
    """Генерація варіантів оптимізованих заголовків"""
    template = CONTENT_TEMPLATES.get(content_type, CONTENT_TEMPLATES['learning'])
    prefix = template['title_prefix']
    
    suggestions = [
        f"{prefix} {content_topic} | SmartBabies - Learn with ScoopyCap",
        f"{prefix} Learn {content_topic} | Educational Video for Kids | SmartBabies",
        f"{prefix} {content_topic} for Preschoolers | SmartBabies - Safe Kids Content",
        f"{prefix} {content_topic} | Fun Learning for Toddlers | SmartBabies",
        f"ScoopyCap's {content_topic} Adventure | SmartBabies - Preschool Education"
    ]
    
    return suggestions

def main():
    parser = argparse.ArgumentParser(description='Генератор оптимізованих описів для YouTube')
    parser.add_argument('--topic', required=True, help='Тема відео (наприклад: "ABC Learning")')
    parser.add_argument('--type', default='learning', 
                       choices=['learning', 'numbers', 'colors', 'songs', 'adventure'],
                       help='Тип контенту')
    parser.add_argument('--length', type=int, help='Довжина відео в хвилинах')
    parser.add_argument('--output', default='output_description.txt', help='Файл для збереження')
    
    args = parser.parse_args()
    
    print("\n" + "="*70)
    print("📝 ГЕНЕРАЦІЯ ОПТИМІЗОВАНОГО ОПИСУ")
    print("="*70)
    
    # Генерація заголовків
    print("\n📌 ВАРІАНТИ ЗАГОЛОВКІВ:")
    title_suggestions = generate_title_suggestions(args.topic, args.type)
    for i, title in enumerate(title_suggestions, 1):
        print(f"{i}. {title} ({len(title)} символів)")
    
    # Генерація опису
    social_links = {
        'youtube': 'https://www.youtube.com/@SmartBabies',
        'facebook': 'https://www.facebook.com/Smart-Babies-108947580525633/'
    }
    
    description = generate_optimized_description(
        args.topic,
        args.type,
        video_length_minutes=args.length,
        social_links=social_links
    )
    
    print(f"\n📄 ОПИС ({len(description)} символів):")
    print("-"*70)
    print(description)
    print("-"*70)
    
    # Генерація тегів
    tags = generate_optimized_tags(args.type)
    print(f"\n🏷️  ТЕГИ ({len(tags)} тегів):")
    print(", ".join(tags))
    
    # Збереження
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write("="*70 + "\n")
        f.write("ОПТИМІЗОВАНИЙ ОПИС ДЛЯ YOUTUBE\n")
        f.write(f"Дата створення: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write("="*70 + "\n\n")
        f.write("ЗАГОЛОВКИ:\n")
        for i, title in enumerate(title_suggestions, 1):
            f.write(f"{i}. {title}\n")
        f.write("\n" + "="*70 + "\n")
        f.write("ОПИС:\n")
        f.write("="*70 + "\n\n")
        f.write(description)
        f.write("\n\n" + "="*70 + "\n")
        f.write("ТЕГИ:\n")
        f.write("="*70 + "\n")
        f.write(", ".join(tags))
        f.write("\n")
    
    print(f"\n💾 Результати збережено в {args.output}")

if __name__ == '__main__':
    main()

