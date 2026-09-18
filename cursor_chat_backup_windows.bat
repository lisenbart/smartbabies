@echo off
REM Скрипт для резервного копіювання чатів Cursor на Windows
REM Використання: cursor_chat_backup_windows.bat

setlocal EnableDelayedExpansion

set "BACKUP_DIR=%USERPROFILE%\Desktop\Cursor\cursor_backups"
set "CURSOR_DATA_DIR=%APPDATA%\Cursor"

REM Отримуємо дату та час для імені папки
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
set "TIMESTAMP=%datetime:~0,8%_%datetime:~8,6%"
set "BACKUP_PATH=%BACKUP_DIR%\backup_%TIMESTAMP%"

echo 🔍 Створюю резервну копію даних Cursor...
echo 📁 Папка для бекапів: %BACKUP_DIR%

REM Створюємо папку для бекапів
if not exist "%BACKUP_PATH%" mkdir "%BACKUP_PATH%"

echo.
echo 📋 Копіюю важливі файли...

REM Копіюємо глобальне сховище
if exist "%CURSOR_DATA_DIR%\User\globalStorage" (
    echo   ✓ globalStorage
    xcopy "%CURSOR_DATA_DIR%\User\globalStorage" "%BACKUP_PATH%\globalStorage\" /E /I /H /Y >nul
)

REM Копіюємо workspace storage
if exist "%CURSOR_DATA_DIR%\User\workspaceStorage" (
    echo   ✓ workspaceStorage
    xcopy "%CURSOR_DATA_DIR%\User\workspaceStorage" "%BACKUP_PATH%\workspaceStorage\" /E /I /H /Y >nul
)

REM Копіюємо localStorage
if exist "%CURSOR_DATA_DIR%\Local Storage" (
    echo   ✓ Local Storage
    xcopy "%CURSOR_DATA_DIR%\Local Storage" "%BACKUP_PATH%\Local Storage\" /E /I /H /Y >nul
)

REM Копіюємо session storage
if exist "%CURSOR_DATA_DIR%\Session Storage" (
    echo   ✓ Session Storage
    xcopy "%CURSOR_DATA_DIR%\Session Storage" "%BACKUP_PATH%\Session Storage\" /E /I /H /Y >nul
)

REM Копіюємо Preferences
if exist "%CURSOR_DATA_DIR%\Preferences" (
    echo   ✓ Preferences
    copy "%CURSOR_DATA_DIR%\Preferences" "%BACKUP_PATH%\" >nul
)

REM Створюємо інформаційний файл
echo CURSOR CHAT BACKUP > "%BACKUP_PATH%\BACKUP_INFO.txt"
echo ================= >> "%BACKUP_PATH%\BACKUP_INFO.txt"
echo Дата створення: %date% %time% >> "%BACKUP_PATH%\BACKUP_INFO.txt"
echo Версія скрипта: 1.0 (Windows) >> "%BACKUP_PATH%\BACKUP_INFO.txt"
echo. >> "%BACKUP_PATH%\BACKUP_INFO.txt"
echo Цей бекап містить: >> "%BACKUP_PATH%\BACKUP_INFO.txt"
echo - globalStorage - глобальні налаштування та дані >> "%BACKUP_PATH%\BACKUP_INFO.txt"
echo - workspaceStorage - дані робочих просторів >> "%BACKUP_PATH%\BACKUP_INFO.txt"
echo - Local Storage - локальне сховище >> "%BACKUP_PATH%\BACKUP_INFO.txt"
echo - Session Storage - сховище сесій >> "%BACKUP_PATH%\BACKUP_INFO.txt"
echo - Preferences - налаштування програми >> "%BACKUP_PATH%\BACKUP_INFO.txt"
echo. >> "%BACKUP_PATH%\BACKUP_INFO.txt"
echo Щоб відновити: >> "%BACKUP_PATH%\BACKUP_INFO.txt"
echo 1. Закрийте Cursor >> "%BACKUP_PATH%\BACKUP_INFO.txt"
echo 2. Скопіюйте файли з backup_%TIMESTAMP% назад у: >> "%BACKUP_PATH%\BACKUP_INFO.txt"
echo    %APPDATA%\Cursor\User\ >> "%BACKUP_PATH%\BACKUP_INFO.txt"
echo 3. Відкрийте Cursor знову >> "%BACKUP_PATH%\BACKUP_INFO.txt"
echo. >> "%BACKUP_PATH%\BACKUP_INFO.txt"
echo ВАЖЛИВО: Перед відновленням зробіть бекап поточних файлів! >> "%BACKUP_PATH%\BACKUP_INFO.txt"

echo.
echo ✅ Резервну копію створено!
echo 📂 Розташування: %BACKUP_PATH%
echo.
echo 📝 Рекомендації:
echo    1. Запускайте цей скрипт регулярно
echo    2. Зберігайте бекапи в хмару (OneDrive, Dropbox, тощо)
echo    3. Перед великими оновленнями Cursor робіть бекап

REM Відкриваємо папку з бекапом
explorer "%BACKUP_PATH%"

pause
