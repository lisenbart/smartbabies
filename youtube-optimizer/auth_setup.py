#!/usr/bin/env python3
"""
Налаштування OAuth автентифікації для YouTube API
Потрібно для оновлення метаданих відео
"""

import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

# Scope для редагування відео
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

def get_credentials():
    """
    Отримує валідні credentials для YouTube API.
    Створює OAuth flow якщо потрібно.
    """
    creds = None
    token_file = 'token.pickle'
    
    # Перевірка чи є збережений токен
    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)
    
    # Якщо немає валідних credentials, запускаємо OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('client_secret.json'):
                print("❌ Помилка: Файл client_secret.json не знайдено!")
                print("\n📝 Щоб отримати client_secret.json:")
                print("1. Перейдіть на https://console.cloud.google.com/")
                print("2. Виберіть ваш проект")
                print("3. APIs & Services → Credentials")
                print("4. Create Credentials → OAuth client ID")
                print("5. Application type: Desktop app")
                print("6. Завантажте JSON файл та перейменуйте в client_secret.json")
                return None
            
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Зберігаємо credentials для майбутнього використання
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)
    
    return creds

def get_youtube_service():
    """Повертає авторизований YouTube сервіс"""
    creds = get_credentials()
    if not creds:
        return None
    return build('youtube', 'v3', credentials=creds)

if __name__ == '__main__':
    print("🔐 Налаштування OAuth автентифікації...")
    print("\nПеревіряю наявність client_secret.json...")
    
    if not os.path.exists('client_secret.json'):
        print("\n❌ Файл client_secret.json не знайдено!")
        print("\n📋 Інструкція:")
        print("="*70)
        print("""
1. Перейдіть на https://console.cloud.google.com/
2. Виберіть ваш проект (той самий де створили API ключ)
3. Перейдіть: APIs & Services → Credentials
4. Натисніть "Create Credentials" → "OAuth client ID"
5. Якщо проситиме створити OAuth consent screen:
   - User Type: External
   - App name: SmartBabies Optimizer
   - User support email: ваш email
   - Developer email: ваш email
   - Save and Continue (scopes пропустіть)
   - Save and Continue (test users пропустіть)
   - Back to Dashboard

6. Поверніться до Credentials → Create Credentials → OAuth client ID
7. Application type: Desktop app
8. Name: SmartBabies Desktop Client
9. Create
10. Завантажте JSON файл
11. Перейменуйте його в client_secret.json
12. Покладіть в папку youtube-optimizer/
        """)
        print("="*70)
    else:
        print("✅ client_secret.json знайдено!")
        print("\n🔐 Запускаю автентифікацію...")
        print("Відкриється браузер для авторизації...")
        
        service = get_youtube_service()
        if service:
            print("\n✅ Авторизація успішна!")
            print("✅ Токен збережено в token.pickle")
            print("\nТепер ви можете використовувати update_videos.py для оновлення відео!")


