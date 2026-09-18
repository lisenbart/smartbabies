# 🔒 Як зберегти чати Cursor на Windows - Повний гайд

## Важливо!

Cursor автоматично зберігає чати локально на Windows, але іноді вони можуть зникати після оновлень або при проблемах. Ось як їх захистити:

## 📋 Швидкий старт

### 1. Автоматичне резервне копіювання

Запустіть скрипт резервного копіювання:

1. Відкрийте Command Prompt або PowerShell
2. Перейдіть у папку з проектом
3. Запустіть:
   ```cmd
   cursor_chat_backup_windows.bat
   ```

Скрипт створює повну резервну копію всіх даних Cursor, включаючи чати.

**Рекомендація:** Запускайте скрипт щодня або перед закриттям Cursor.

### 2. Де знаходяться чати на Windows?

Cursor зберігає чати в наступних місцях:

```
%APPDATA%\Cursor\User\globalStorage\
%APPDATA%\Cursor\User\workspaceStorage\
%APPDATA%\Cursor\Local Storage\
```

Повний шлях зазвичай виглядає так:
```
C:\Users\[YourUsername]\AppData\Roaming\Cursor\User\globalStorage\
```

### 3. Як швидко знайти папку?

1. Натисніть `Win + R`
2. Введіть: `%APPDATA%\Cursor`
3. Натисніть Enter

## 🔄 Відновлення чатів

Якщо чати зникли:

1. **Закрийте Cursor повністю** (через Task Manager, якщо потрібно)

2. **Знайдіть ваш бекап:**
   ```cmd
   cd %USERPROFILE%\Desktop\Cursor\cursor_backups
   dir /o-d  # показати найновіший бекап
   ```

3. **Відновіть файли:**
   ```cmd
   # Зробіть бекап поточних файлів на всяк випадок!
   xcopy %APPDATA%\Cursor\User\globalStorage %USERPROFILE%\Desktop\cursor_current_backup\ /E /I /H
   
   # Відновіть з бекапу (замініть YYYYMMDD_HHMMSS на дату вашого бекапу)
   xcopy %USERPROFILE%\Desktop\Cursor\cursor_backups\backup_YYYYMMDD_HHMMSS\globalStorage\* %APPDATA%\Cursor\User\globalStorage\ /E /H /Y
   ```

4. **Відкрийте Cursor** - чати повинні повернутися

## 💡 Альтернативні способи збереження

### Спосіб 1: Експорт через інтерфейс Cursor

1. Відкрийте чат в Cursor
2. Виділіть весь текст переписки (Ctrl+A, Ctrl+C)
3. Збережіть в текстовий файл або документ

### Спосіб 2: Автоматичний бекап через Task Scheduler

Налаштуйте автоматичний бекап у Windows Task Scheduler:

1. Відкрийте Task Scheduler (`taskschd.msc`)
2. Створіть нову задачу
3. Встановіть тригер (наприклад, щодня о 3:00)
4. Дія: Запустити програму `cursor_chat_backup_windows.bat`

### Спосіб 3: Синхронізація з хмарою

Зберігайте папку з бекапами в OneDrive або Dropbox:

```cmd
# Створіть симлінк (потрібні права адміністратора)
mklink /D "%USERPROFILE%\OneDrive\cursor_backups" "%USERPROFILE%\Desktop\Cursor\cursor_backups"
```

Або просто скопіюйте папку `cursor_backups` в OneDrive/Dropbox вручну.

## 🔗 Як перенести чати в Cloud Agent / GitHub

### Варіант 1: Через Git

```bash
# У вашому проекті створіть папку
mkdir chat_exports

# Скопіюйте файли бекапу
xcopy %USERPROFILE%\Desktop\Cursor\cursor_backups\backup_[latest]\ chat_exports\ /E

# Додайте в git (якщо файли не занадто великі)
git add chat_exports/
git commit -m "Add chat history backup"
git push
```

### Варіант 2: Експорт як текст

Створіть скрипт PowerShell для експорту чатів у читабельний формат:

```powershell
# Збережіть цей код як export_chats.ps1
$backupPath = "$env:USERPROFILE\Desktop\Cursor\cursor_backups"
$exportPath = "$env:USERPROFILE\Desktop\Cursor\chat_exports"

New-Item -ItemType Directory -Force -Path $exportPath

# Знайдіть найновіший бекап
$latestBackup = Get-ChildItem $backupPath | Sort-Object LastWriteTime -Descending | Select-Object -First 1

# Скопіюйте SQLite бази даних та інші файли чатів
Copy-Item -Recurse -Force "$($latestBackup.FullName)\*" $exportPath

Write-Host "✅ Чати експортовано в: $exportPath"
```

### Варіант 3: Ручний експорт важливих розмов

1. Відкрийте кожен важливий чат у Cursor
2. Скопіюйте текст (Ctrl+A, Ctrl+C)
3. Створіть Markdown файли:
   ```
   chat_exports/
     ├── chat_2024_01_15_project_setup.md
     ├── chat_2024_01_16_bug_fixes.md
     └── chat_2024_01_17_new_features.md
   ```
4. Додайте в Git та запуште

## ⚠️ Чому чати могли зникнути?

- Оновлення Cursor
- Переустановка програми
- Очищення кешу Windows
- Проблеми з файловою системою
- Антивірус видалив файли
- Невідповідність версій

## 🛡️ Профілактика

1. ✅ Робіть бекапи регулярно
2. ✅ Зберігайте бекапи в хмарі (OneDrive, Google Drive)
3. ✅ Перед оновленнями Cursor робіть бекап
4. ✅ Не видаляйте папку `%APPDATA%\Cursor` вручну
5. ✅ Додайте папку Cursor в виключення антивіруса

## 🔍 Перевірка бекапів

Перевірте, чи існують ваші бекапи:

```cmd
dir %USERPROFILE%\Desktop\Cursor\cursor_backups\ /s
```

## 📊 Розмір даних Cursor

Подивіться, скільки місця займають ваші дані:

```powershell
Get-ChildItem "$env:APPDATA\Cursor" -Recurse | Measure-Object -Property Length -Sum | Select-Object @{Name="Size (MB)"; Expression={[math]::Round($_.Sum / 1MB, 2)}}
```

## 📞 Якщо нічого не допомагає

1. Перевірте, чи Cursor синхронізується з акаунтом (якщо є cloud sync)
2. Зверніться до підтримки Cursor
3. Перевірте логи Cursor: `%APPDATA%\Cursor\logs\`
4. Спробуйте відновити попередню версію папки через Windows (права кнопка → Properties → Previous Versions)

## 🎯 Краткий чек-лист

- [ ] Запущено скрипт `cursor_chat_backup_windows.bat`
- [ ] Створено перший бекап
- [ ] Знайдено папку з чатами (`%APPDATA%\Cursor`)
- [ ] Налаштовано автоматичні бекапи (опціонально)
- [ ] Бекапи синхронізовані з хмарою (опціонально)
- [ ] Експортовано важливі розмови в проект (опціонально)

## 🔄 Інтеграція з Git проектом

Якщо ви хочете зберігати чати разом з проектом:

1. **Створіть `.gitignore` правило** (якщо файли занадто великі):
   ```
   # У .gitignore
   chat_exports/*.db
   chat_exports/*.db-*
   ```

2. **Або зберігайте тільки текстові експорти**:
   ```
   chat_exports/
     ├── README.md  # опис структури
     └── conversations/
         ├── 2024-01-15-project-setup.md
         └── 2024-01-16-features.md
   ```

3. **Додайте README для chat_exports**:
   ```markdown
   # Chat History
   
   Цей каталог містить історію важливих розмов з Cursor AI.
   
   ## Структура
   - `conversations/` - експортовані розмови в Markdown
   - `backups/` - повні бекапи даних Cursor (не в git)
   ```

---

**Створено:** %date%  
**Платформа:** Windows  
**Версія:** 1.0
