# 🔄 Quick Start - Синхронізація розмов

## 🎯 Головна ідея

Cursor **НЕ синхронізує** розмови автоматично між Cloud Agent і локальним Cursor.  
Але ми створили систему для **передачі контексту** через Git!

---

## ⚡ Швидкий старт

### Сценарій 1: З Cloud Agent → на Windows

**1. Тут (Cloud Agent) збережіть контекст:**
```bash
./save_context.sh "Додав функцію X"
nano chat_exports/context/context_*.md  # Відредагуйте, додайте нотатки
git add . && git commit -m "Save context" && git push
```

**2. На Windows стягніть зміни:**
```cmd
git pull
```

**3. У новому чаті Cursor на Windows напишіть:**
```
Привіт! Прочитай @chat_exports/context/context_2026-09-18_115221.md 
та @TODO.md і продовж роботу
```

---

### Сценарій 2: З Windows → на Cloud Agent

**1. На Windows збережіть контекст:**
```cmd
save_context.bat "Зробив feature Y"
REM Відредагуйте файл у Notepad
git add . && git commit -m "Save context" && git push
```

**2. Тут (Cloud Agent) стягніть:**
```bash
git pull
```

**3. У новому чаті тут напишіть:**
```
Привіт! Прочитай @chat_exports/context/context_2026-09-18_120000.md 
та @TODO.md і продовж роботу
```

---

## 📋 Що треба оновлювати

### 1. **TODO.md** (найважливіше!)
Завжди оновлюйте перед комітом:
- Що зробили ✅
- Що в процесі 🔄
- Що далі ⏭️

### 2. **Файли контексту**
Створюйте коли перемикаєтесь між пристроями:
```bash
./save_context.sh "Short description"
```

### 3. **Детальні commit messages**
```bash
git commit -m "Add authentication

- Implemented JWT token generation
- Added password hashing with bcrypt
- TODO: Add email validation
- TODO: Write tests

Context: User wants OAuth2 later, started with basic auth first"
```

---

## 🎓 Корисні команди

### Знайти останній контекст
```bash
ls -lt chat_exports/context/ | head -3
```

### Прочитати TODO
```bash
cat TODO.md
```

### Історія комітів
```bash
git log --oneline -5
```

### Швидкий sync цикл
```bash
# Зберегти контекст і запушити
./save_context.sh "description" && \
nano chat_exports/context/context_*.md && \
git add . && git commit -m "Save context" && git push
```

---

## 📚 Детальна документація

Читайте повну інструкцію: [SYNC_GUIDE.md](SYNC_GUIDE.md)

---

## ✅ Чеклист перед перемиканням

- [ ] Закомітив всі зміни
- [ ] Оновив TODO.md
- [ ] Створив файл контексту (`save_context.sh` або `.bat`)
- [ ] Додав нотатки в контекст файл
- [ ] Запушив: `git push`

На іншому пристрої:

- [ ] Стягнув зміни: `git pull`
- [ ] Прочитав TODO.md
- [ ] Прочитав останній context файл
- [ ] Сказав AI прочитати контекст через @mentions

---

**💡 Головне правило:** Завжди оновлюйте `TODO.md` - це ваша "єдина правда" про стан проекту!
