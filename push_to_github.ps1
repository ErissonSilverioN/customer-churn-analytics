# Automated GitHub Push Script
# Run this after creating your GitHub repository

Write-Host "🚀 Pushing to GitHub..." -ForegroundColor Cyan
Write-Host ""

# Add remote
Write-Host "📡 Adding remote repository..." -ForegroundColor Yellow
git remote add origin https://github.com/janakisowmya/customer-churn-analytics.git

# Rename branch to main
Write-Host "🔄 Renaming branch to main..." -ForegroundColor Yellow
git branch -M main

# Push to GitHub
Write-Host "⬆️  Pushing to GitHub..." -ForegroundColor Yellow
git push -u origin main

Write-Host ""
Write-Host "✅ Done! Your repository is now live at:" -ForegroundColor Green
Write-Host "   https://github.com/janakisowmya/customer-churn-analytics" -ForegroundColor Cyan
Write-Host ""
Write-Host "🎯 Next steps:" -ForegroundColor Yellow
Write-Host "   1. Visit your repository on GitHub"
Write-Host "   2. Add topics: django, mongodb, machine-learning, etc."
Write-Host "   3. Pin it to your profile"
Write-Host ""
