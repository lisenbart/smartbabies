# YouTube Channel Optimizer для SmartBabies

Інструмент для аналізу та оптимізації YouTube каналу SmartBabies.

## 🚀 Швидкий старт

### 1. Отримання YouTube API ключа

1. Перейдіть на [Google Cloud Console](https://console.cloud.google.com/)
2. Створіть новий проект або виберіть існуючий
3. Увімкніть **YouTube Data API v3**:
   - Перейдіть в "APIs & Services" → "Library"
   - Пошукайте "YouTube Data API v3"
   - Натисніть "Enable"
4. Створіть API ключ:
   - "APIs & Services" → "Credentials"
   - "Create Credentials" → "API Key"
   - Скопіюйте ключ та збережіть його безпечно

5. ⚠️ **ВАЖЛИВО: Обмежте доступ ключа для безпеки**
   
   Після створення ключа ви побачите попередження "This key is unrestricted". 
   Обов'язково обмежте його:
   
   **Крок 1:** Натисніть "Restrict key" або оберіть ваш ключ у списку
   
   **Крок 2:** В розділі "API restrictions":
   - Оберіть "Restrict key"
   - Поставте галочку біля **"YouTube Data API v3"**
   - Натисніть "Save"
   
   **Крок 3:** (Опціонально, але рекомендовано) В розділі "Application restrictions":
   - Можете залишити "None" для тестування
   - Або обмежити за IP-адресами, якщо використовуєте на сервері
   
   ✅ **Чому це важливо:** 
   - Захищає від неавторизованого використання
   - Не дозволяє іншим використовувати ваш ключ
   - Зменшує ризик перевищення квот

### 2. Встановлення залежностей

```bash
pip install -r requirements.txt
```

### 3. Налаштування

Створіть файл `.env` в папці `youtube-optimizer/`:

```env
YOUTUBE_API_KEY=ваш_api_ключ_тут
CHANNEL_ID=@SmartBabies
```

## 📊 Використання

### 1. Аналіз каналу (без змін)

```bash
python analyze_channel.py
```

### 2. Отримання рекомендацій по оптимізації

```bash
python optimize_videos.py
```

### 3. ⚡ **МАСОВЕ ОНОВЛЕННЯ ВСІХ ВІДЕО** (основна функція)

**Крок 1:** Налаштуйте OAuth (один раз):
```bash
python auth_setup.py
```
Детальна інструкція в [OAUTH_SETUP.md](OAUTH_SETUP.md)

**Крок 2:** Перевірте що буде змінено (прев'ю):
```bash
python update_videos.py
```

**Крок 3:** Застосуйте оптимізацію до всіх відео:
```bash
python update_videos.py --apply
```

**Оновити тільки проблемні відео:**
```bash
python update_videos.py --apply --priority
```

**Тестування на 5 відео:**
```bash
python update_videos.py --apply --limit 5
```

### 4. Генерація оптимізованих описів для нових відео

```bash
python generate_description.py --topic "ABC learning" --type learning
```

## 📝 Функції

- ✅ Аналіз поточних метаданих відео
- ✅ Рекомендації з SEO оптимізації
- ✅ Генерація оптимізованих тегів та описів
- ✅ Аналіз конкурентів у ніші
- ✅ Підбір оптимальних ключових слів

