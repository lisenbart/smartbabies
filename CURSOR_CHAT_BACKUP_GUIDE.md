# 🔒 Як зберегти чати Cursor - Повний гайд

## Важливо!

Cursor автоматично зберігає чати локально, але іноді вони можуть зникати після оновлень або при проблемах. Ось як їх захистити:

## 📋 Швидкий старт

### 1. Автоматичне резервне копіювання

Запустіть скрипт резервного копіювання:

```bash
chmod +x cursor_chat_backup.sh
./cursor_chat_backup.sh
```

Скрипт створює повну резервну копію всіх даних Cursor, включаючи чати.

**Рекомендація:** Запускайте скрипт щодня або перед закриттям Cursor.

### 2. Де знаходяться чати?

Cursor зберігає чати в наступних місцях на macOS:

```
~/Library/Application Support/Cursor/User/globalStorage/
~/Library/Application Support/Cursor/User/workspaceStorage/
~/Library/Application Support/Cursor/Local Storage/
```

## 🔄 Відновлення чатів

Якщо чати зникли:

1. **Закрийте Cursor повністю** (не просто вікно, а виходьте з програми)

2. **Знайдіть ваш бекап:**
   ```bash
   cd ~/Desktop/Cursor/cursor_backups
   ls -lt  # показати найновіший бекап
   ```

3. **Відновіть файли:**
   ```bash
   # Зробіть бекап поточних файлів на всяк випадок!
   cp -r ~/Library/Application\ Support/Cursor/User/globalStorage ~/Desktop/cursor_current_backup
   
   # Відновіть з бекапу
   cp -r ~/Desktop/Cursor/cursor_backups/backup_YYYYMMDD_HHMMSS/globalStorage/* \
         ~/Library/Application\ Support/Cursor/User/globalStorage/
   ```

4. **Відкрийте Cursor** - чати повинні повернутися

## 💡 Альтернативні способи збереження

### Способ 1: Експорт через інтерфейс Cursor

1. Відкрийте чат в Cursor
2. Скопіюйте весь текст переписки вручну (Cmd+A, Cmd+C)
3. Збережіть в текстовий файл або документ

### Спосіб 2: Автоматичний бекап через cron

Додайте в cron для автоматичного бекапу:

```bash
crontab -e

# Додайте цей рядок для бекапу кожного дня о 03:00
0 3 * * * /Users/dmytrolisenbart/Desktop/Cursor/smartbabies/cursor_chat_backup.sh >> ~/cursor_backup.log 2>&1
```

### Спосіб 3: Синхронізація з хмарою

Зберігайте папку з бекапами в iCloud або Dropbox:

```bash
# Створіть симлінк для автоматичної синхронізації
ln -s ~/Desktop/Cursor/cursor_backups ~/iCloud\ Drive/cursor_backups
```

## ⚠️ Чому чати могли зникнути?

- Оновлення Cursor
- Переустановка програми
- Очищення кешу системи
- Проблеми з файловою системою
- Невідповідність версій

## 🛡️ Профілактика

1. ✅ Робіть бекапи регулярно
2. ✅ Зберігайте бекапи в хмарі
3. ✅ Перед оновленнями Cursor робіть бекап
4. ✅ Не видаляйте папку `~/Library/Application Support/Cursor/` вручну

## 🔍 Перевірка бекапів

Перевірте, чи існують ваші бекапи:

```bash
ls -lh ~/Desktop/Cursor/cursor_backups/
```

## 📞 Якщо нічого не допомагає

1. Перевірте, чи Cursor синхронізується з акаунтом (якщо є)
2. Зверніться до підтримки Cursor
3. Перевірте логи Cursor: `~/Library/Application Support/Cursor/logs/`

## 🎯 Краткий чек-лист

- [ ] Створено скрипт бекапу
- [ ] Запущено перший бекап
- [ ] Налаштовано автоматичні бекапи (опціонально)
- [ ] Бекапи синхронізовані з хмарою (опціонально)
- [ ] Відомо розташування файлів чатів

---

**Створено:** $(date)  
**Проект:** SmartBabies


