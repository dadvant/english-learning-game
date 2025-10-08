# 🚀 סקריפט העלאה אוטומטית ל-GitHub
param(
    [Parameter(Mandatory=$true)]
    [string]$GitHubToken
)

Write-Host "🚀 מתחיל העלאה אוטומטית ל-GitHub..." -ForegroundColor Green
Write-Host "=" * 50 -ForegroundColor Yellow

# הגדרות
$repoName = "english-learning-game"
$username = "dadvant"  # שינינו מ-ofirnichtern ל-dadvant
$description = "🎮 משחק לימוד אנגלית קולביורטיבי לילדים עם AI"

# בדיקה אם הריפו קיים
Write-Host "� בודק אם Repository קיים..." -ForegroundColor Cyan
try {
    $existingRepo = Invoke-RestMethod -Uri "https://api.github.com/repos/$username/$repoName" -Headers @{
        "Authorization" = "token $GitHubToken"
        "Accept" = "application/vnd.github.v3+json"
    }
    Write-Host "✅ Repository קיים: $username/$repoName" -ForegroundColor Green
    $repoExists = $true
} catch {
    Write-Host "📁 Repository לא קיים, יוצר חדש..." -ForegroundColor Yellow
    $repoExists = $false
}

# יצירת הריפו אם לא קיים
if (-not $repoExists) {
    $createRepoBody = @{
        name = $repoName
        description = $description
        private = $false
    } | ConvertTo-Json

    try {
        Invoke-RestMethod -Uri "https://api.github.com/user/repos" -Method POST -Headers @{
            "Authorization" = "token $GitHubToken"
            "Accept" = "application/vnd.github.v3+json"
        } -Body $createRepoBody -ContentType "application/json" | Out-Null

        Write-Host "✅ Repository נוצר בהצלחה!" -ForegroundColor Green
    } catch {
        Write-Host "❌ שגיאה ביצירת Repository: $($_.Exception.Message)" -ForegroundColor Red
        exit 1
    }
}

# הגדרת Git remote
Write-Host "🔗 מגדיר Git remote..." -ForegroundColor Cyan
Set-Location "C:\Users\ofirn\OneDrive\Documents\Private\Kids Lessons\Idan"
git remote set-url origin "https://$username`:$GitHubToken@github.com/$username/$repoName.git"

# העלאת הקבצים
Write-Host "📤 מעלה קבצים ל-GitHub..." -ForegroundColor Cyan
Write-Host "   (זה עלול לקחת כמה דקות - יש 115 קבצים...)" -ForegroundColor Gray

$pushResult = git push origin main 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ כל הקבצים הועלו בהצלחה!" -ForegroundColor Green
} else {
    Write-Host "❌ שגיאה בהעלאה: $pushResult" -ForegroundColor Red
    exit 1
}

# סיכום
Write-Host "`n🎉 העלאה הושלמה בהצלחה!" -ForegroundColor Green
Write-Host "=" * 50 -ForegroundColor Yellow
Write-Host "📁 Repository: https://github.com/$username/$repoName" -ForegroundColor White
Write-Host "👥 הילדים יכולים לעשות:" -ForegroundColor Cyan
Write-Host "   git clone https://github.com/$username/$repoName.git" -ForegroundColor White
Write-Host "   .\setup_dev_environment.ps1" -ForegroundColor White
Write-Host "`n🚀 מוכנים להתחיל לפתח עם AI!" -ForegroundColor Green

# פתיחת הדפדפן
Write-Host "`n🌐 פותח את Repository בדפדפן..." -ForegroundColor Cyan
Start-Process "https://github.com/$username/$repoName"

Write-Host "`n✨ תהנו מפיתוח עם הילדים! 🤖" -ForegroundColor Magenta