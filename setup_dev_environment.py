#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 סקריפט אוטומטי להקמת סביבת פיתוח למשחק לימוד אנגלית
מיועד לילדים שרוצים להתחיל לפתח עם AI!
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def run_command(cmd, description=""):
    """הרצת פקודה עם הודעות ידידותיות"""
    print(f"🔄 {description}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - הושלם בהצלחה!")
            return True
        else:
            print(f"❌ שגיאה ב{description}: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ שגיאה: {str(e)}")
        return False

def check_prerequisites():
    """בדיקת דרישות מקדימות"""
    print("🔍 בודק דרישות מקדימות...")
    
    # בדיקת Python
    try:
        python_version = sys.version_info
        if python_version.major >= 3 and python_version.minor >= 8:
            print(f"✅ Python {python_version.major}.{python_version.minor} מותקן")
        else:
            print("❌ נדרש Python 3.8 או גרסה חדשה יותר")
            return False
    except:
        print("❌ Python לא מותקן")
        return False
    
    # בדיקת Git
    if run_command("git --version", "בדיקת Git"):
        pass
    else:
        print("❌ Git לא מותקן. אנא התקינו Git מ: https://git-scm.com/")
        return False
    
    # בדיקת VS Code
    if run_command("code --version", "בדיקת VS Code"):
        pass
    else:
        print("⚠️ VS Code לא נמצא. אנא התקינו מ: https://code.visualstudio.com/")
        print("   אפשר להמשיך בלי VS Code, אבל מומלץ להתקין")
    
    return True

def setup_project():
    """הקמת הפרויקט"""
    print("\n🎯 מקים את הפרויקט...")
    
    # יצירת תיקייה
    project_dir = "english-learning-game"
    if os.path.exists(project_dir):
        print(f"📁 התיקייה {project_dir} כבר קיימת")
        choice = input("האם להמשיך? (y/n): ")
        if choice.lower() != 'y':
            return False
    else:
        os.makedirs(project_dir)
        print(f"📁 יצרתי תיקייה: {project_dir}")
    
    os.chdir(project_dir)
    
    # שכפול מ-GitHub (אם זמין)
    print("📥 מנסה להוריד את הפרויקט מ-GitHub...")
    if run_command("git clone https://github.com/dadvant/english-learning-game.git .", 
                   "הורדת הפרויקט מ-GitHub"):
        print("🎉 הפרויקט הורד בהצלחה מ-GitHub!")
    else:
        print("⚠️ לא ניתן להוריד מ-GitHub. יוצר פרויקט בסיסי...")
        create_basic_project()
    
    return True

def create_basic_project():
    """יצירת פרויקט בסיסי אם GitHub לא זמין"""
    print("🔨 יוצר פרויקט בסיסי...")
    
    # יצירת requirements.txt
    with open("requirements.txt", "w") as f:
        f.write("Flask==2.3.3\nrequests==2.31.0\n")
    
    # יצירת README בסיסי
    with open("README.md", "w", encoding="utf-8") as f:
        f.write("""# 🎮 משחק לימוד אנגלית לעידן

## התחלה מהירה:
1. הפעילו: `python EnglishGame.py`
2. פתחו דפדפן: `http://localhost:5000`
3. תתחילו ללמוד!

## עיקרי הפרויקט:
- משחק לימוד אנגלית אינטראקטיבי
- 8 קטגוריות שונות
- מערכת תרגום חכמה
- ממשק ידידותי לילדים

צרו קשר לעזרה! 🚀
""")

def install_requirements():
    """התקנת ספריות נדרשות"""
    print("\n📦 מתקין ספריות נדרשות...")
    
    # יצירת סביבה וירטואלית
    if run_command("python -m venv venv", "יצירת סביבה וירטואלית"):
        pass
    
    # הפעלת סביבה וירטואלית
    if os.name == 'nt':  # Windows
        activate_cmd = "venv\\Scripts\\activate && pip install -r requirements.txt"
    else:  # Mac/Linux
        activate_cmd = "source venv/bin/activate && pip install -r requirements.txt"
    
    run_command(activate_cmd, "התקנת ספריות")

def setup_vscode():
    """הקמת VS Code"""
    print("\n⚙️ מגדיר VS Code...")
    
    vscode_dir = ".vscode"
    if not os.path.exists(vscode_dir):
        os.makedirs(vscode_dir)
    
    # הגדרות VS Code
    settings = {
        "python.defaultInterpreterPath": "./venv/bin/python" if os.name != 'nt' else ".\\venv\\Scripts\\python.exe",
        "files.associations": {
            "*.py": "python"
        },
        "editor.fontSize": 16,
        "editor.lineNumbers": "on",
        "editor.wordWrap": "on",
        "python.linting.enabled": True,
        "python.formatting.provider": "black"
    }
    
    with open(f"{vscode_dir}/settings.json", "w") as f:
        json.dump(settings, f, indent=4)
    
    # הרחבות מומלצות
    extensions = {
        "recommendations": [
            "ms-python.python",
            "ms-vscode.vscode-json",
            "GitHub.copilot",
            "Continue.continue",
            "ritwickdey.LiveServer"
        ]
    }
    
    with open(f"{vscode_dir}/extensions.json", "w") as f:
        json.dump(extensions, f, indent=4)
    
    print("✅ VS Code מוגדר עם הרחבות מומלצות")

def open_vscode():
    """פתיחת VS Code"""
    print("\n🚀 פותח VS Code...")
    if run_command("code .", "פתיחת VS Code"):
        print("🎉 VS Code נפתח בהצלחה!")
        print("\n📋 מה לעשות עכשיו:")
        print("1. התקינו את ההרחבות המומלצות (VS Code יציע)")
        print("2. פתחו את הקובץ EnglishGame.py")
        print("3. לחצו F5 להפעלת המשחק")
        print("4. שאלו AI כל שאלה! 🤖")
    else:
        print("⚠️ לא ניתן לפתוח VS Code אוטומטית")
        print("פתחו VS Code ידנית ופתחו את התיקייה הזו")

def main():
    """פונקציה ראשית"""
    print("🎮 ברוכים הבאים להקמת סביבת הפיתוח!")
    print("=" * 50)
    
    # בדיקת דרישות
    if not check_prerequisites():
        print("\n❌ אנא התקינו את הדרישות המקדימות")
        input("לחצו Enter לסיום...")
        return
    
    # הקמת פרויקט
    if not setup_project():
        print("\n❌ הקמת הפרויקט נכשלה")
        input("לחצו Enter לסיום...")
        return
    
    # התקנת ספריות
    install_requirements()
    
    # הגדרת VS Code
    setup_vscode()
    
    # פתיחת VS Code
    open_vscode()
    
    print("\n🎉 הכל מוכן!")
    print("📖 קראו את המדריך AI_CODING_GUIDE.md למידע נוסף")
    print("🚀 בהצלחה בפיתוח!")
    
    input("\nלחצו Enter לסיום...")

if __name__ == "__main__":
    main()