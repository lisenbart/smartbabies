# 🔐 Покрокова інструкція: Запуск автентифікації

## 📋 Передумови

Переконайтеся що у вас є:
- ✅ Файл `client_secret.json` в папці `youtube-optimizer/`
- ✅ Python 3 встановлений
- ✅ Всі бібліотеки встановлені (`pip install -r requirements.txt`)

---

## 🎬 Покрокова інструкція:

### 1️⃣ Відкрийте термінал

На Mac:
- Натисніть `Cmd + Space`
- Введіть "Terminal"
- Натисніть Enter

Або використовуйте вбудований термінал в Cursor (View → Terminal)

### 2️⃣ Перейдіть в папку проекту

```bash
cd /Users/dmytrolisenbart/Desktop/Cursor/smartbabies/youtube-optimizer
```

**Перевірка:** Ви повинні бачити файли:
```bash
ls
```
Ви маєте побачити: `auth_setup.py`, `update_videos.py`, тощо

### 3️⃣ Перевірте наявність client_secret.json

```bash
ls client_secret.json
```

**Якщо файлу немає:**
- Скрипт сам покаже інструкцію як його отримати
- Або читайте Кроки 1-4 в `OAUTH_SETUP.md`

**Якщо файл є:**
- Продовжуйте до кроку 4

### 4️⃣ Запустіть автентифікацію

```bash
python3 auth_setup.py
```

### 5️⃣ Що побачите в терміналі:

```
🔐 Налаштування OAuth автентифікації...

Перевіряю наявність client_secret.json...
✅ client_secret.json знайдено!

🔐 Запускаю автентифікацію...
Відкриється браузер для авторизації...
Please visit this URL to authorize this application: https://accounts.google.com/o/oauth2/auth?...
```

### 6️⃣ Браузер відкриється автоматично

Ви побачите:
1. **Сторінку входу Google**
   - Введіть email та пароль вашого Google акаунта
   - ✅ **Важливо:** Використовуйте акаунт з правами на канал SmartBabies!

2. **Запит на надання прав:**
   ```
   SmartBabies Optimizer wants to access your Google Account
   
   This will allow SmartBabies Optimizer to:
   • View and manage your YouTube account
   ```
   
   - Натисніть **"Allow"** або **"Дозволити"**

3. **Підтвердження:**
   ```
   The authentication flow has completed.
   You may close this window.
   ```

### 7️⃣ Поверніться до терміналу

Після авторизації в терміналі з'явиться:

```
✅ Авторизація успішна!
✅ Токен збережено в token.pickle

Тепер ви можете використовувати update_videos.py для оновлення відео!
```

### 8️⃣ Перевірка успішності

```bash
ls -la token.pickle
```

Ви маєте побачити файл `token.pickle` - це означає що все працює!

---

## ✅ Готово!

Тепер можете запускати оновлення відео:

```bash
# Прев'ю (без змін)
python3 update_videos.py

# Реальне оновлення
python3 update_videos.py --apply
```

---

## ❓ Можливі проблеми:

### Проблема: "client_secret.json не знайдено"
**Рішення:**
- Переконайтеся що файл в папці `youtube-optimizer/`
- Перевірте що він називається саме `client_secret.json` (не `.txt` чи інший формат)

### Проблема: "Access denied" або "Permission denied"
**Рішення:**
- Переконайтеся що використовуєте правильний Google акаунт
- Акаунт повинен мати права Editor або Owner на YouTube каналі

### Проблема: Браузер не відкрився
**Рішення:**
- Скопіюйте URL з терміналу
- Вставте вручну в браузер
- Після авторизації скопіюйте код повернення в термінал

### Проблема: "Module not found"
**Рішення:**
```bash
pip install -r requirements.txt
```

---

## 📝 Візуальний приклад:

```
$ cd /Users/dmytrolisenbart/Desktop/Cursor/smartbabies/youtube-optimizer

$ python3 auth_setup.py
🔐 Налаштування OAuth автентифікації...
✅ client_secret.json знайдено!
🔐 Запускаю автентифікацію...
Please visit this URL to authorize this application:
https://accounts.google.com/o/oauth2/auth?...

[Автоматично відкривається браузер]
[Ви входите в Google]
[Натискаєте "Allow"]

✅ Авторизація успішна!
✅ Токен збережено в token.pickle

$ ls token.pickle
token.pickle
```

Готово! 🎉


