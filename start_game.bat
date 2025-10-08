@echo off
title 🎮 משחק לימוד אנגלית של עידן
echo.
echo 🎮 משחק לימוד אנגלית של עידן 🎮
echo ===================================
echo.

REM בדיקה שהקובץ קיים
if not exist "EnglishGame.py" (
    echo ❌ הקובץ EnglishGame.py לא נמצא!
    echo בדקו שאתם בתיקייה הנכונה
    pause
    exit /b 1
)

echo ▶️  מפעיל את השרת...
echo.
echo 🌐 לאחר שהשרת יעלה, פתחו דפדפן וגשו ל:
echo    http://localhost:5000
echo.
echo 💡 לעצירת השרת: לחצו Ctrl+C
echo.

python EnglishGame.py

echo.
echo 👋 המשחק נסגר. תודה ששיחקתם!
pause