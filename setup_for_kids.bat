@echo off
echo 🎮 התקנת משחק לימוד אנגלית 🎮
echo ================================

echo בודק אם Python מותקן...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python לא מותקן! 
    echo אנא הורידו Python מ: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python מותקן!

echo מתקין ספריות נחוצות...
pip install flask >nul 2>&1
if errorlevel 1 (
    echo ❌ שגיאה בהתקנת Flask
    echo מנסה עם python -m pip...
    python -m pip install flask
)

echo ✅ Flask הותקן!

echo יוצר תמונות למשחק...
python create_images.py

echo יוצר נתוני שחקן ראשוניים...
if not exist players_data.json (
    echo {} > players_data.json
)

echo 🎉 ההתקנה הושלמה בהצלחה!
echo 
echo להפעלת המשחק הריצו: python EnglishGame.py
echo או פשוט לחצו כפול על start_game.bat
echo 
pause