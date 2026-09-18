# 🔄 Як синхронізувати розмови між Cloud Agent і Windows Cursor

## ❌ Погана новина
Cursor **НЕ синхронізує** розмови автоматично між пристроями.  
Кожна розмова - це окрема сесія.

## ✅ Добра новина
Ми створили систему передачі контексту через Git! 🎉

---

## 🚀 Як це працює

### Крок 1️⃣: Збережіть контекст перед перемиканням

**На Cloud Agent (Linux):**
```bash
./save_context.sh "Що ви робили"
```

**На Windows:**
```cmd
save_context.bat "Що ви робили"
```

### Крок 2️⃣: Відредагуйте файл контексту

Скрипт створить файл `chat_exports/context/context_ДАТА_ЧАС.md`

Відкрийте його та заповніть:
- 🎯 Що треба зробити далі
- 💡 Важливі нотатки
- 🔗 Які файли обговорювались

### Крок 3️⃣: Закомітьте та запуште

```bash
git add .
git commit -m "Save context"
git push
```

### Крок 4️⃣: На іншому пристрої стягніть зміни

```bash
git pull
```

### Крок 5️⃣: У новому чаті Cursor прикріпіть контекст

Напишіть:
```
Привіт! Прочитай @TODO.md та 
@chat_exports/context/context_2026-09-18_115221.md 
і продовж роботу звідти
```

AI прочитає файли і продовжить з того місця! ✨

---

## 📚 Детальні інструкції

- **Швидкий старт:** [QUICKSTART_SYNC.md](QUICKSTART_SYNC.md)
- **Повна документація:** [chat_exports/SYNC_GUIDE.md](chat_exports/SYNC_GUIDE.md)
- **Windows бекап:** [CURSOR_CHAT_BACKUP_GUIDE_WINDOWS.md](CURSOR_CHAT_BACKUP_GUIDE_WINDOWS.md)

---

## 💡 Головне правило

**Завжди оновлюйте `TODO.md`** - це ваша "єдина правда" про стан проекту!

AI може прочитати його через `@TODO.md` в будь-якій розмові.

---

## 🎯 Що у нас є

| Файл | Призначення |
|------|-------------|
| `save_context.sh` | Збереження контексту (Linux/macOS) |
| `save_context.bat` | Збереження контексту (Windows) |
| `TODO.md` | Центральний файл стану проекту |
| `QUICKSTART_SYNC.md` | Швидкий посібник |
| `SYNC_GUIDE.md` | Детальна документація |
| `chat_exports/context/` | Папка з файлами контексту |

---

**Приклад використання:**

```bash
# На Cloud Agent
./save_context.sh "Додав аутентифікацію"
nano chat_exports/context/context_*.md  # Додайте нотатки
git add . && git commit -m "Context" && git push

# На Windows
git pull
# У Cursor: "Привіт! Прочитай @chat_exports/context/context_2026-09-18_115221.md та продовж"
```

---

✨ **Готово! Тепер ви можете "синхронізувати" розмови між пристроями через контекстні файли!**
