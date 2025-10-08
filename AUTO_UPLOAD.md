# 🚀 העלאה אוטומטית ל-GitHub

## ⚡ הדרך הקלה ביותר - סקריפט אוטומטי!

### שלב 1: קבלו Personal Access Token
1. גשו ל: https://github.com/settings/tokens
2. לחצו **"Generate new token (classic)"**
3. שם: `english-learning-game-upload`
4. הרשאות: ✅ `repo` (כל הזכויות לריפו)
5. לחצו **"Generate token"**
6. **העתיקו את ה-token** (מופיע רק פעם אחת!)

### שלב 2: הריצו את הסקריפט האוטומטי

```powershell
# פתחו PowerShell כמנהל והריצו:
cd "C:\Users\ofirn\OneDrive\Documents\Private\Kids Lessons\Idan"

# החליפו YOUR_TOKEN כאן עם ה-token האמיתי שלכם
.\upload_to_github.ps1 -GitHubToken "YOUR_TOKEN_HERE"
```

### מה הסקריפט עושה אוטומטית:
- ✅ יוצר repository חדש ב-GitHub
- ✅ מעלה את כל 115 הקבצים
- ✅ מגדיר את כל ההרשאות
- ✅ פותח את הדפדפן לריפו החדש

## 🎯 אחרי ההעלאה:
- הריפו יהיה זמין ב: `https://github.com/ofirnichtern/english-learning-game`
- הילדים יוכלו לעשות `git clone` ולהתחיל לפתח
- כל המדריכים יהיו שם מוכנים

## 💡 אם יש בעיות:
1. וודאו שה-token נכון וטרי
2. הריצו כמנהל (Run as Administrator)
3. אם הריפו כבר קיים, הסקריפט יעלה אליו

## 🔒 בטיחות:
- ה-token נשמר רק בזיכרון במהלך ההעלאה
- לא נשמר בקבצים או ב-Git
- ניתן למחוק את ה-token מ-GitHub אחרי ההעלאה

**מוכנים? קבלו token והריצו את הסקריפט!** 🚀