# 🚀 Exact Commands to Push to GitHub

## Step 1: Initialize Git Repository

Open PowerShell in the project folder and run:

```powershell
cd C:\Users\Mouli\OneDrive\Desktop\churn
git init
```

## Step 2: Add All Files

```powershell
git add .
```

## Step 3: Create Initial Commit

```powershell
git commit -m "Initial commit: Customer Churn Analytics System with Django REST, MongoDB, and ML"
```

## Step 4: Create GitHub Repository

1. Go to: https://github.com/new
2. Repository name: `customer-churn-analytics`
3. Description: `Production-grade customer churn prediction system with Django REST, MongoDB, and ML (87% accuracy)`
4. Choose **Public**
5. **DO NOT** check "Add a README file" (we already have one)
6. Click **"Create repository"**

## Step 5: Connect and Push to GitHub

```powershell
git remote add origin https://github.com/janakisowmya/customer-churn-analytics.git
git branch -M main
git push -u origin main
```

## ✅ That's It!

Your repository will be live at:
**https://github.com/janakisowmya/customer-churn-analytics**

---

## 🎨 After Pushing - Make It Look Professional

### Add Topics (on GitHub)
1. Go to your repository
2. Click the gear icon ⚙️ next to "About"
3. Add these topics:
   - `django`
   - `django-rest-framework`
   - `mongodb`
   - `machine-learning`
   - `customer-churn`
   - `scikit-learn`
   - `python`
   - `javascript`
   - `docker`
   - `data-science`

### Pin the Repository
1. Go to your profile: https://github.com/janakisowmya
2. Click "Customize your pins"
3. Select this repository to feature it on your profile

---

## 🚨 Troubleshooting

**Problem**: "git: command not found"
- **Solution**: Install Git from https://git-scm.com/download/win

**Problem**: Authentication error when pushing
- **Solution**: GitHub now requires a Personal Access Token instead of password
  1. Go to: https://github.com/settings/tokens
  2. Generate new token (classic)
  3. Select scopes: `repo` (all)
  4. Use the token as your password when prompted

**Problem**: Large file warning
- **Solution**: The model file (19MB) is fine. If you get errors, you can skip it with:
  ```powershell
  git rm --cached churn_model_rf.joblib
  echo "churn_model_rf.joblib" >> .gitignore
  git commit -m "Remove large model file"
  git push
  ```

---

**Ready to go! Just copy and paste the commands above.** 🎉
