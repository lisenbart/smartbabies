@echo off
REM Скрипт для швидкого збереження контексту роботи (Windows)
REM Використання: save_context.bat "Ваш коментар про що робили"

setlocal EnableDelayedExpansion

REM Отримуємо дату та час
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
set "TIMESTAMP=%datetime:~0,4%-%datetime:~4,2%-%datetime:~6,2%_%datetime:~8,6%"

set "CONTEXT_FILE=chat_exports\context\context_%TIMESTAMP%.md"
set "COMMENT=%~1"
if "%COMMENT%"=="" set "COMMENT=Manual context save"

echo 💾 Зберігаю контекст роботи...

REM Створюємо файл контексту
(
echo # Context saved at %date% %time%
echo.
echo **Comment:** %COMMENT%
echo.
echo ---
echo.
echo ## 📊 Git Status
echo.
echo ### Recent commits ^(last 5^)
echo ```
git log --oneline -5
echo ```
echo.
echo ### Current branch
echo ```
git branch --show-current
echo ```
echo.
echo ### Changed files
echo ```
git status --short
echo ```
echo.
echo ### Uncommitted changes
echo ```
git diff --stat
echo ```
echo.
echo ---
echo.
echo ## 📁 Project Structure
echo ```
dir /b /s | findstr /v ".git node_modules" 2^>nul
echo ```
echo.
echo ---
echo.
echo ## 📝 Current TODO items
if exist "TODO.md" (
    type TODO.md
) else (
    echo No TODO.md file found
)
echo.
echo ---
echo.
echo ## 🎯 What to do next
echo.
echo [✏️ ЗАПОВНІТЬ ЦЕ ВРУЧНУ - що потрібно робити далі]
echo.
echo - [ ] Task 1
echo - [ ] Task 2
echo - [ ] Task 3
echo.
echo ## 💡 Important notes
echo.
echo [✏️ ЗАПОВНІТЬ ЦЕ ВРУЧНУ - важливі деталі, які треба пам'ятати]
echo.
echo - Context: [опис контексту]
echo - Decisions made: [які рішення прийняті]
echo - Known issues: [відомі проблеми]
echo.
echo ## 🔗 Related files
echo.
echo [✏️ ЗАПОВНІТЬ ЦЕ ВРУЧНУ - які файли обговорювались]
echo.
echo - `path/to/file1.js` - [опис]
echo - `path/to/file2.js` - [опис]
echo.
echo ---
echo.
echo ## 🚀 How to continue
echo.
echo На іншому пристрої/в іншому чаті:
echo.
echo 1. Pull changes: `git pull`
echo 2. Read this file: `@chat_exports/context/context_%TIMESTAMP%.md`
echo 3. In chat say: "Continue work from context file @chat_exports/context/context_%TIMESTAMP%.md"
) > "%CONTEXT_FILE%"

echo.
echo ✅ Context saved to: %CONTEXT_FILE%
echo.
echo 📝 Next steps:
echo    1. Edit the file to add your notes:
echo       notepad %CONTEXT_FILE%
echo.
echo    2. Commit and push:
echo       git add %CONTEXT_FILE%
echo       git commit -m "Save context: %COMMENT%"
echo       git push
echo.
echo 🔗 Or open the file now?
echo.

choice /C YN /M "Open file in Notepad"
if errorlevel 2 goto :skip_edit
if errorlevel 1 goto :open_edit

:open_edit
notepad "%CONTEXT_FILE%"

:skip_edit
echo.
echo 💡 Don't forget to commit and push!
pause
