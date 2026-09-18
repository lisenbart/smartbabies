# 🔄 Синхронізація проекту ПЕРШОСВІТ між Windows і Cloud Agent

## 📍 Поточна ситуація

- **Windows:** Проект в `E:\ПЕРШОСВІТ`
- **Cloud Agent:** Зараз в `/workspace` (репозиторій smartbabies)
- **Мета:** Працювати над ПЕРШОСВІТ з обох місць

---

## 🎯 Рішення 1: ПЕРШОСВІТ як окремий Git репозиторій (РЕКОМЕНДОВАНО)

### Крок 1: На Windows створіть Git репозиторій

```cmd
cd E:\ПЕРШОСВІТ

REM Перевірте чи вже є git
dir .git

REM Якщо немає - ініціалізуйте
git init
git branch -M main
```

### Крок 2: Створіть репозиторій на GitHub

1. Відкрийте https://github.com/new
2. Назвіть репозиторій: `pershopsvit` або `ПЕРШОСВІТ`
3. НЕ додавайте README/LICENSE (якщо вже є файли)

### Крок 3: Підключіть remote і запуште

```cmd
cd E:\ПЕРШОСВІТ

git remote add origin https://github.com/ВАШ-USERNAME/pershopsvit.git

REM Додайте всі файли
git add .
git commit -m "Initial commit: ПЕРШОСВІТ project"
git push -u origin main
```

### Крок 4: Додайте інструменти синхронізації

```cmd
cd E:\ПЕРШОСVІТ

REM Скачайте скрипти з smartbabies
curl -o save_context.bat https://raw.githubusercontent.com/lisenbart/smartbabies/main/save_context.bat
curl -o TODO.md https://raw.githubusercontent.com/lisenbart/smartbabies/main/TODO.md
curl -o .gitignore https://raw.githubusercontent.com/lisenbart/smartbabies/main/.gitignore

REM Створіть папку для контексту
mkdir chat_exports\context

REM Закомітьте
git add .
git commit -m "Add sync tools"
git push
```

### Крок 5: На Cloud Agent клонуйте проект

```bash
cd /workspace
git clone https://github.com/ВАШ-USERNAME/pershopsvit.git ПЕРШОСВІТ
cd ПЕРШОСВІТ
ls -la
```

### Крок 6: Працюйте з синхронізацією!

**На Windows перед закінченням роботи:**
```cmd
cd E:\ПЕРШОСВІТ
save_context.bat "Налаштував канал, зробив X і Y"
notepad chat_exports\context\context_*.md  REM додайте деталі
git add .
git commit -m "Update: channel configuration"
git push
```

**На Cloud Agent для продовження:**
```bash
cd /workspace/ПЕРШОСВІТ
git pull
# У чаті Cursor: "Прочитай @TODO.md та @chat_exports/context/context_*.md і продовж роботу над ПЕРШОСВІТ"
```

---

## 🎯 Рішення 2: ПЕРШОСВІТ як підпапка в smartbabies

Якщо хочете все в одному місці:

### На Windows:

```cmd
cd C:\path\to\smartbabies

REM Створіть папку
mkdir ПЕРШОСВІТ

REM Скопіюйте файли
xcopy E:\ПЕРШОСВІТ ПЕРШОСВІТ\ /E /I /H /Y

REM Оновіть TODO.md
notepad TODO.md

REM Збережіть контекст
save_context.bat "Додав папку ПЕРШОСВІТ з проектом каналу"

REM Закомітьте
git add ПЕРШОСВІТ/
git add TODO.md
git commit -m "Add ПЕРШОСВІТ project as subfolder"
git push
```

### На Cloud Agent:

```bash
cd /workspace
git pull
ls -la ПЕРШОСВІТ/
# Файли тут!
```

---

## 🎯 Рішення 3: Симлінк (для досвідчених)

Якщо smartbabies клонований на Windows в іншому місці:

```cmd
cd C:\path\to\smartbabies
mklink /D ПЕРШОСВІТ E:\ПЕРШОСВІТ
```

Тепер зміни в `E:\ПЕРШОСВІТ` автоматично видно в smartbabies як підпапку.

---

## 💡 Рекомендація

**Використовуйте Рішення 1** (окремий репозиторій) якщо:
- ✅ ПЕРШОСВІТ - великий проект
- ✅ Хочете окрему історію комітів
- ✅ Можливо інші люди працюватимуть над ним

**Використовуйте Рішення 2** (підпапка) якщо:
- ✅ ПЕРШОСВІТ - частина smartbabies
- ✅ Хочете все в одному місці
- ✅ Маленький проект/конфігурація

---

## 🔄 Робочий процес після налаштування

### Щодня на Windows:

```cmd
cd E:\ПЕРШОСВІТ  REM (або cd smartbabies\ПЕРШОСВІТ)

REM Стягніть зміни
git pull

REM ... працюєте ...

REM Перед закінченням
save_context.bat "Короткий опис що зробили"
notepad chat_exports\context\context_*.md
notepad TODO.md

git add .
git commit -m "Descriptive message"
git push
```

### На Cloud Agent:

```bash
cd /workspace/ПЕРШОСВІТ  # (або cd /workspace, залежно від структури)

git pull

# У чаті Cursor:
# "Привіт! Прочитай @TODO.md та @chat_exports/context/context_[latest].md 
# і продовж роботу над каналом ПЕРШОСВІТ"

# ... працюєте ...

./save_context.sh "Що зробили"
nano chat_exports/context/context_*.md
nano TODO.md

git add .
git commit -m "Descriptive message"
git push
```

---

## 📋 Чеклист налаштування

### Початкове налаштування:
- [ ] Вирішили: окремий репо чи підпапка?
- [ ] Створили GitHub репозиторій (якщо окремий)
- [ ] Ініціалізували git в `E:\ПЕРШОСВІТ`
- [ ] Зробили перший push
- [ ] Клонували на Cloud Agent
- [ ] Скопіювали sync інструменти (save_context.bat, TODO.md)
- [ ] Створили chat_exports/context/ папку
- [ ] Протестували: Windows → push → Cloud Agent → pull

### Щоденна робота:
- [ ] git pull перед початком
- [ ] Працювати
- [ ] Оновити TODO.md
- [ ] save_context.bat/sh перед закінченням
- [ ] git add/commit/push
- [ ] На іншому пристрої: git pull
- [ ] Прочитати контекст через @ в чаті

---

## 🆘 Якщо щось пішло не так

### Git не ініціалізований на Windows:
```cmd
cd E:\ПЕРШОСВІТ
git init
git branch -M main
```

### Git є, але немає remote:
```cmd
git remote add origin https://github.com/USERNAME/pershopsvit.git
```

### Забули яка структура:
```cmd
cd E:\ПЕРШОСВІТ
git remote -v
```

Це покаже чи є remote і який URL.

---

## 📞 Наступні кроки

1. **Скажіть мені:**
   - Чи є `.git` в `E:\ПЕРШОСВІТ` зараз?
   - Окремий репозиторій чи підпапка?
   - Яке ім'я репозиторію хочете?

2. **Я допоможу:**
   - Створити правильну структуру
   - Налаштувати синхронізацію
   - Зробити перший sync test

---

**Готовий допомогти налаштувати прямо зараз!** 🚀
