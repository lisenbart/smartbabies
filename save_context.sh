#!/bin/bash

# Скрипт для швидкого збереження контексту роботи
# Використання: ./save_context.sh "Ваш коментар про що робили"

set -e

TIMESTAMP=$(date +"%Y-%m-%d_%H%M%S")
CONTEXT_FILE="chat_exports/context/context_$TIMESTAMP.md"
COMMENT="${1:-Manual context save}"

echo "💾 Зберігаю контекст роботи..."

cat > "$CONTEXT_FILE" << EOF
# Context saved at $(date)

**Comment:** $COMMENT

---

## 📊 Git Status

### Recent commits (last 5)
\`\`\`
$(git log --oneline -5)
\`\`\`

### Current branch
\`\`\`
$(git branch --show-current)
\`\`\`

### Changed files
\`\`\`
$(git status --short)
\`\`\`

### Uncommitted changes
\`\`\`
$(git diff --stat)
\`\`\`

---

## 📁 Project Structure
\`\`\`
$(tree -L 2 -I 'node_modules|.git' || ls -la)
\`\`\`

---

## 📝 Current TODO items
$(if [ -f "TODO.md" ]; then cat TODO.md; else echo "No TODO.md file found"; fi)

---

## 🎯 What to do next

[✏️ ЗАПОВНІТЬ ЦЕ ВРУЧНУ - що потрібно робити далі]

- [ ] Task 1
- [ ] Task 2
- [ ] Task 3

## 💡 Important notes

[✏️ ЗАПОВНІТЬ ЦЕ ВРУЧНУ - важливі деталі, які треба пам'ятати]

- Context: [опис контексту]
- Decisions made: [які рішення прийняті]
- Known issues: [відомі проблеми]

## 🔗 Related files

[✏️ ЗАПОВНІТЬ ЦЕ ВРУЧНУ - які файли обговорювались]

- \`path/to/file1.js\` - [опис]
- \`path/to/file2.js\` - [опис]

---

## 🚀 How to continue

На іншому пристрої/в іншому чаті:

1. Pull changes: \`git pull\`
2. Read this file: \`@chat_exports/context/context_$TIMESTAMP.md\`
3. In chat say: "Continue work from context file @chat_exports/context/context_$TIMESTAMP.md"

EOF

echo ""
echo "✅ Context saved to: $CONTEXT_FILE"
echo ""
echo "📝 Next steps:"
echo "   1. Edit the file to add your notes:"
echo "      nano $CONTEXT_FILE"
echo ""
echo "   2. Commit and push:"
echo "      git add $CONTEXT_FILE"
echo "      git commit -m \"Save context: $COMMENT\""
echo "      git push"
echo ""
echo "🔗 Or run the full cycle:"
echo "   nano $CONTEXT_FILE && git add $CONTEXT_FILE && git commit -m \"Context: $COMMENT\" && git push"

# Відкрити файл в редакторі (якщо є EDITOR)
if [ ! -z "$EDITOR" ]; then
    echo ""
    echo "📂 Opening file in editor..."
    $EDITOR "$CONTEXT_FILE"
fi
