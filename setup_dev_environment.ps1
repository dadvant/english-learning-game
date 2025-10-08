# 🚀 סקריפט PowerShell להקמת סביבת פיתוח
# מיועד לילדים שרוצים להתחיל לפתח עם AI!

param(
    [string]$ProjectName = "english-learning-game",
    [switch]$SkipGitClone = $false
)

# צבעים לפלט יפה
function Write-Success {
    param([string]$Message)
    Write-Host "✅ $Message" -ForegroundColor Green
}

function Write-Info {
    param([string]$Message)
    Write-Host "🔄 $Message" -ForegroundColor Cyan
}

function Write-Warning {
    param([string]$Message)
    Write-Host "⚠️ $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "❌ $Message" -ForegroundColor Red
}

function Write-Header {
    param([string]$Message)
    Write-Host "`n🎯 $Message" -ForegroundColor Magenta
    Write-Host "=" * 50 -ForegroundColor Gray
}

# בדיקת דרישות מקדימות
function Test-Prerequisites {
    Write-Header "בודק דרישות מקדימות"
    
    $allGood = $true
    
    # בדיקת Python
    try {
        $pythonVersion = python --version 2>&1
        if ($pythonVersion -match "Python (\d+)\.(\d+)") {
            $major = [int]$Matches[1]
            $minor = [int]$Matches[2]
            if ($major -ge 3 -and $minor -ge 8) {
                Write-Success "Python $major.$minor מותקן"
            } else {
                Write-Error "נדרש Python 3.8 או גרסה חדשה יותר"
                $allGood = $false
            }
        }
    } catch {
        Write-Error "Python לא מותקן. הורידו מ: https://python.org"
        $allGood = $false
    }
    
    # בדיקת Git
    try {
        $gitVersion = git --version 2>&1
        if ($gitVersion -match "git version") {
            Write-Success "Git מותקן"
        } else {
            Write-Error "Git לא מותקן. הורידו מ: https://git-scm.com"
            $allGood = $false
        }
    } catch {
        Write-Error "Git לא מותקן. הורידו מ: https://git-scm.com"
        $allGood = $false
    }
    
    # בדיקת VS Code
    try {
        $codeVersion = code --version 2>&1
        if ($codeVersion -match "\d+\.\d+\.\d+") {
            Write-Success "VS Code מותקן"
        } else {
            Write-Warning "VS Code לא נמצא. מומלץ להתקין מ: https://code.visualstudio.com"
        }
    } catch {
        Write-Warning "VS Code לא נמצא. מומלץ להתקין מ: https://code.visualstudio.com"
    }
    
    return $allGood
}

# הקמת הפרויקט
function Setup-Project {
    Write-Header "מקים את הפרויקט"
    
    # יצירת תיקייה
    if (Test-Path $ProjectName) {
        Write-Warning "התיקייה $ProjectName כבר קיימת"
        $choice = Read-Host "האם להמשיך? (y/n)"
        if ($choice.ToLower() -ne "y") {
            return $false
        }
    } else {
        New-Item -ItemType Directory -Name $ProjectName | Out-Null
        Write-Success "יצרתי תיקייה: $ProjectName"
    }
    
    Set-Location $ProjectName
    
    # שכפול מ-GitHub
    if (-not $SkipGitClone) {
        Write-Info "מנסה להוריד את הפרויקט מ-GitHub..."
        try {
            git clone https://github.com/dadvant/english-learning-game.git . 2>&1 | Out-Null
            if ($LASTEXITCODE -eq 0) {
                Write-Success "הפרויקט הורד בהצלחה מ-GitHub!"
            } else {
                Write-Warning "לא ניתן להוריד מ-GitHub. יוצר פרויקט בסיסי..."
                New-BasicProject
            }
        } catch {
            Write-Warning "לא ניתן להוריד מ-GitHub. יוצר פרויקט בסיסי..."
            New-BasicProject
        }
    } else {
        New-BasicProject
    }
    
    return $true
}

# יצירת פרויקט בסיסי
function New-BasicProject {
    Write-Info "יוצר פרויקט בסיסי..."
    
    # יצירת requirements.txt
    @"
Flask==2.3.3
requests==2.31.0
"@ | Out-File -FilePath "requirements.txt" -Encoding UTF8
    
    # יצירת README
    @"
# 🎮 משחק לימוד אנגלית לעידן

## התחלה מהירה:
1. הפעילו: ``python EnglishGame.py``
2. פתחו דפדפן: ``http://localhost:5000``
3. תתחילו ללמוד!

## עיקרי הפרויקט:
- משחק לימוד אנגלית אינטראקטיבי
- 8 קטגוריות שונות
- מערכת תרגום חכמה
- ממשק ידידותי לילדים

צרו קשר לעזרה! 🚀
"@ | Out-File -FilePath "README.md" -Encoding UTF8
    
    Write-Success "פרויקט בסיסי נוצר"
}

# התקנת ספריות
function Install-Requirements {
    Write-Header "מתקין ספריות נדרשות"
    
    # יצירת סביבה וירטואלית
    Write-Info "יוצר סביבה וירטואלית..."
    try {
        python -m venv venv
        Write-Success "סביבה וירטואלית נוצרה"
    } catch {
        Write-Error "שגיאה ביצירת סביבה וירטואלית"
        return $false
    }
    
    # הפעלת סביבה וירטואלית והתקנת ספריות
    Write-Info "מתקין ספריות..."
    try {
        & ".\venv\Scripts\Activate.ps1"
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        Write-Success "ספריות הותקנו בהצלחה"
    } catch {
        Write-Error "שגיאה בהתקנת ספריות"
        return $false
    }
    
    return $true
}

# הגדרת VS Code
function Setup-VSCode {
    Write-Header "מגדיר VS Code"
    
    # יצירת תיקיית .vscode
    if (-not (Test-Path ".vscode")) {
        New-Item -ItemType Directory -Name ".vscode" | Out-Null
    }
    
    # הגדרות VS Code
    $settings = @{
        "python.defaultInterpreterPath" = ".\venv\Scripts\python.exe"
        "files.associations" = @{
            "*.py" = "python"
        }
        "editor.fontSize" = 16
        "editor.lineNumbers" = "on"
        "editor.wordWrap" = "on"
        "python.linting.enabled" = $true
        "python.formatting.provider" = "black"
        "python.analysis.typeCheckingMode" = "basic"
    } | ConvertTo-Json -Depth 3
    
    $settings | Out-File -FilePath ".vscode\settings.json" -Encoding UTF8
    
    # הרחבות מומלצות
    $extensions = @{
        "recommendations" = @(
            "ms-python.python",
            "ms-vscode.vscode-json",
            "GitHub.copilot",
            "Continue.continue",
            "ritwickdey.LiveServer",
            "ms-python.debugpy"
        )
    } | ConvertTo-Json -Depth 2
    
    $extensions | Out-File -FilePath ".vscode\extensions.json" -Encoding UTF8
    
    # הגדרות debug
    $launch = @{
        "version" = "0.2.0"
        "configurations" = @(
            @{
                "name" = "🎮 Run English Game"
                "type" = "python"
                "request" = "launch"
                "program" = "${workspaceFolder}\EnglishGame.py"
                "console" = "integratedTerminal"
                "cwd" = "${workspaceFolder}"
            }
        )
    } | ConvertTo-Json -Depth 3
    
    $launch | Out-File -FilePath ".vscode\launch.json" -Encoding UTF8
    
    # משימות
    $tasks = @{
        "version" = "2.0.0"
        "tasks" = @(
            @{
                "label" = "🎮 Start Game Server"
                "type" = "shell"
                "command" = "python"
                "args" = @("EnglishGame.py")
                "group" = "build"
                "presentation" = @{
                    "echo" = $true
                    "reveal" = "always"
                    "focus" = $false
                    "panel" = "new"
                }
                "isBackground" = $true
            }
        )
    } | ConvertTo-Json -Depth 4
    
    $tasks | Out-File -FilePath ".vscode\tasks.json" -Encoding UTF8
    
    Write-Success "VS Code מוגדר עם הרחבות והגדרות מומלצות"
}

# פתיחת VS Code
function Open-VSCode {
    Write-Header "פותח VS Code"
    
    try {
        code .
        Write-Success "VS Code נפתח בהצלחה!"
        Write-Host "`n📋 מה לעשות עכשיו:" -ForegroundColor Yellow
        Write-Host "1. התקינו את ההרחבות המומלצות (VS Code יציע)" -ForegroundColor White
        Write-Host "2. פתחו את הקובץ EnglishGame.py" -ForegroundColor White
        Write-Host "3. לחצו F5 להפעלת המשחק" -ForegroundColor White
        Write-Host "4. שאלו AI כל שאלה! 🤖" -ForegroundColor White
    } catch {
        Write-Warning "לא ניתן לפתוח VS Code אוטומטית"
        Write-Host "פתחו VS Code ידנית ופתחו את התיקייה הזו" -ForegroundColor White
    }
}

# יצירת קיצורי דרך
function New-Shortcuts {
    Write-Header "יוצר קיצורי דרך"
    
    # קיצור דרך להפעלת המשחק
    $startGameScript = @"
@echo off
cd /d "%~dp0"
call venv\Scripts\activate.bat
python EnglishGame.py
pause
"@
    $startGameScript | Out-File -FilePath "start_game.bat" -Encoding ASCII
    
    # קיצור דרך לפתיחת VS Code
    $openVSCodeScript = @"
@echo off
cd /d "%~dp0"
code .
"@
    $openVSCodeScript | Out-File -FilePath "open_vscode.bat" -Encoding ASCII
    
    Write-Success "קיצורי דרך נוצרו: start_game.bat, open_vscode.bat"
}

# פונקציה ראשית
function Main {
    Clear-Host
    Write-Host "🎮 ברוכים הבאים להקמת סביבת הפיתוח!" -ForegroundColor Magenta
    Write-Host "=" * 50 -ForegroundColor Gray
    
    # בדיקת דרישות
    if (-not (Test-Prerequisites)) {
        Write-Error "אנא התקינו את הדרישות המקדימות"
        Read-Host "לחצו Enter לסיום"
        return
    }
    
    # הקמת פרויקט
    if (-not (Setup-Project)) {
        Write-Error "הקמת הפרויקט נכשלה"
        Read-Host "לחצו Enter לסיום"
        return
    }
    
    # התקנת ספריות
    Install-Requirements
    
    # הגדרת VS Code
    Setup-VSCode
    
    # יצירת קיצורי דרך
    New-Shortcuts
    
    # פתיחת VS Code
    Open-VSCode
    
    Write-Host "`n🎉 הכל מוכן!" -ForegroundColor Green
    Write-Host "📖 קראו את המדריך AI_CODING_GUIDE.md למידע נוסף" -ForegroundColor Cyan
    Write-Host "🚀 בהצלחה בפיתוח!" -ForegroundColor Yellow
    
    Read-Host "`nלחצו Enter לסיום"
}

# הפעלה
Main