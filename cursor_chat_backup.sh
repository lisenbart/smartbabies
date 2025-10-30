#!/bin/bash

# Скрипт для резервного копіювання чатів та даних Cursor
# Використання: ./cursor_chat_backup.sh

set -e

BACKUP_DIR="$HOME/Desktop/Cursor/cursor_backups"
CURSOR_DATA_DIR="$HOME/Library/Application Support/Cursor"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_PATH="$BACKUP_DIR/backup_$TIMESTAMP"

echo "🔍 Створюю резервну копію даних Cursor..."
echo "📁 Папка для бекапів: $BACKUP_DIR"

# Створюємо папку для бекапів
mkdir -p "$BACKUP_PATH"

echo ""
echo "📋 Копіюю важливі файли..."

# Копіюємо глобальне сховище (містить налаштування та можливо чати)
if [ -d "$CURSOR_DATA_DIR/User/globalStorage" ]; then
    echo "  ✓ globalStorage"
    cp -r "$CURSOR_DATA_DIR/User/globalStorage" "$BACKUP_PATH/"
fi

# Копіюємо workspace storage (містить дані робочих просторів)
if [ -d "$CURSOR_DATA_DIR/User/workspaceStorage" ]; then
    echo "  ✓ workspaceStorage"
    cp -r "$CURSOR_DATA_DIR/User/workspaceStorage" "$BACKUP_PATH/"
fi

# Копіюємо localStorage (може містити дані чатів)
if [ -d "$CURSOR_DATA_DIR/Local Storage" ]; then
    echo "  ✓ Local Storage"
    cp -r "$CURSOR_DATA_DIR/Local Storage" "$BACKUP_PATH/"
fi

# Копіюємо session storage
if [ -d "$CURSOR_DATA_DIR/Session Storage" ]; then
    echo "  ✓ Session Storage"
    cp -r "$CURSOR_DATA_DIR/Session Storage" "$BACKUP_PATH/"
fi

# Копіюємо Preferences
if [ -f "$CURSOR_DATA_DIR/Preferences" ]; then
    echo "  ✓ Preferences"
    cp "$CURSOR_DATA_DIR/Preferences" "$BACKUP_PATH/"
fi

# Створюємо інформаційний файл
cat > "$BACKUP_PATH/BACKUP_INFO.txt" << EOF
CURSOR CHAT BACKUP
=================
Дата створення: $(date)
Версія скрипта: 1.0

Цей бекап містить:
- globalStorage - глобальні налаштування та дані (можливо чати)
- workspaceStorage - дані робочих просторів
- Local Storage - локальне сховище браузера
- Session Storage - сховище сесій
- Preferences - налаштування програми

Щоб відновити:
1. Закрийте Cursor
2. Скопіюйте файли з backup_$TIMESTAMP назад у:
   ~/Library/Application Support/Cursor/User/
3. Відкрийте Cursor знову

ВАЖЛИВО: Перед відновленням зробіть бекап поточних файлів!
EOF

echo ""
echo "✅ Резервну копію створено!"
echo "📂 Розташування: $BACKUP_PATH"
echo ""
echo "📝 Рекомендації:"
echo "   1. Запускайте цей скрипт регулярно"
echo "   2. Зберігайте бекапи в хмару (iCloud, Dropbox, тощо)"
echo "   3. Перед великими оновленнями Cursor робіть бекап"

# Показуємо розмір бекапу
SIZE=$(du -sh "$BACKUP_PATH" | cut -f1)
echo ""
echo "💾 Розмір бекапу: $SIZE"


