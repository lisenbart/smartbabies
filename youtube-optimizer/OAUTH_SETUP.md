# 🔐 Інструкція з налаштування OAuth для оновлення відео

Для **автоматичного оновлення** метаданих відео через API потрібна OAuth автентифікація.

## ⚡ Швидкий старт

### Крок 1: Створіть OAuth Client ID

1. Перейдіть на https://console.cloud.google.com/
2. Виберіть проект (той самий де створили API ключ)
3. Перейдіть: **APIs & Services** → **Credentials**

### Крок 2: Налаштуйте OAuth Consent Screen (якщо ще не налаштовано)

Якщо бачите попередження про OAuth consent screen:

1. Натисніть **"Configure Consent Screen"**
2. **User Type:** Виберіть **"External"** → **Create**
3. **App information:**
   - App name: `SmartBabies Optimizer`
   - User support email: ваш email
   - Developer contact information: ваш email
4. Натисніть **Save and Continue**
5. **Scopes:** Пропустіть (натисніть **Save and Continue**)
6. **Test users:** Пропустіть (натисніть **Save and Continue**)
7. Натисніть **Back to Dashboard**

### Крок 3: Створіть OAuth Client ID

1. Поверніться до **Credentials**
2. Натисніть **"+ CREATE CREDENTIALS"** → **"OAuth client ID"**
3. **Application type:** Виберіть **"Desktop app"**
4. **Name:** `SmartBabies Desktop Client`
5. Натисніть **Create**
6. Завантажте JSON файл (відкриється вікно з кнопкою Download)

### Крок 4: Покладіть файл в проект

1. Перейменуйте завантажений JSON файл в **`client_secret.json`**
2. Перемістіть його в папку `/youtube-optimizer/`

### Крок 5: Запустіть автентифікацію

**Що потрібно зробити в терміналі:**

1. Відкрийте термінал (Terminal на Mac або Cursor's вбудований термінал)

2. Перейдіть в папку проекту:
   ```bash
   cd /Users/dmytrolisenbart/Desktop/Cursor/smartbabies/youtube-optimizer
   ```

3. Запустіть скрипт автентифікації:
   ```bash
   python3 auth_setup.py
   ```

**Що відбудеться:**

1. Скрипт перевірить наявність файлу `client_secret.json`
   - Якщо немає → покаже повну інструкцію як його отримати
   - Якщо є → продовжить далі

2. Відкриється браузер автоматично з Google сторінкою входу

3. Увійдіть в Google акаунт:
   - ✅ **Важливо:** використовуйте той Google акаунт, який має права на канал SmartBabies!
   - Це може бути ваш особистий Google акаунт або акаунт команди

4. Побачите запит на надання прав:
   ```
   "SmartBabies Optimizer wants to access your Google Account"
   ```
   - Натисніть **"Allow"** або **"Дозволити"**

5. Після успішної авторизації:
   - Браузер покаже: "The authentication flow has completed"
   - В терміналі з'явиться: "✅ Авторизація успішна!"
   - Створиться файл `token.pickle` (він зберігає ваш токен доступу)

**Як перевірити що все працює:**
```bash
ls -la token.pickle
```
Якщо бачите файл - все готово!

✅ **Готово!** Тепер можете використовувати `update_videos.py`

## 🚀 Використання

### Прев'ю (без змін):
```bash
python3 update_videos.py
```
Покаже що буде змінено, але нічого не оновить.

### Реальне оновлення:
```bash
python3 update_videos.py --apply
```

### Оновити тільки проблемні відео:
```bash
python3 update_videos.py --apply --priority
```

### Тестування на кількох відео:
```bash
python3 update_videos.py --apply --limit 5
```

## ⚠️ Важливо

- **OAuth токен** зберігається в `token.pickle` - не діліться цим файлом!
- Якщо токен прострочиться - просто запустіть `auth_setup.py` знову
- Для оновлення всіх 186 відео це може зайняти 5-10 хвилин (затримки для rate limits)

## 🔒 Безпека

- `client_secret.json` - додайте в `.gitignore` (вже додано)
- `token.pickle` - додайте в `.gitignore` (вже додано)
- Не комітьте ці файли в git!

## ❓ Проблеми?

**Помилка "Access denied":**
- Переконайтеся що використовуєте правильний Google акаунт (той що має права на канал)

**Помилка 403 Forbidden:**
- Переконайтеся що OAuth consent screen налаштовано
- Перевірте що обрано правильні scopes в `auth_setup.py`

**Токен прострочився:**
- Просто запустіть `auth_setup.py` знову - він автоматично оновить токен

