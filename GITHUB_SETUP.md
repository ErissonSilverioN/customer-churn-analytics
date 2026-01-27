# GitHub Repository Setup Guide

## 📋 Steps to Push to GitHub

### 1. Initialize Git Repository

```bash
cd c:\Users\Mouli\OneDrive\Desktop\churn
git init
```

### 2. Add All Files

```bash
git add .
```

### 3. Create Initial Commit

```bash
git commit -m "Initial commit: Customer Churn Analytics System

- Django REST Framework backend with MongoDB
- Machine Learning prediction service (87% accuracy)
- Modern JavaScript frontend with glassmorphism design
- Docker containerization
- 85%+ test coverage
- Complete documentation and screenshots"
```

### 4. Create GitHub Repository

1. Go to [GitHub](https://github.com)
2. Click the **"+"** icon → **"New repository"**
3. Repository name: `customer-churn-analytics`
4. Description: `Production-grade customer churn prediction system with Django REST, MongoDB, and ML (87% accuracy)`
5. Choose **Public** or **Private**
6. **DO NOT** initialize with README (we already have one)
7. Click **"Create repository"**

### 5. Connect to GitHub

Replace `yourusername` with your GitHub username:

```bash
git remote add origin https://github.com/yourusername/customer-churn-analytics.git
git branch -M main
git push -u origin main
```

### 6. Update README Links

After pushing, update these in `README.md`:
- Replace `yourusername` with your actual GitHub username
- Add your LinkedIn profile link
- Update the repository URL in clone command

Then commit and push the changes:
```bash
git add README.md
git commit -m "Update README with actual GitHub links"
git push
```

---

## 🎨 Optional: Add Topics to Repository

On GitHub, add these topics to make your repo more discoverable:
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

---

## 📊 Optional: Enable GitHub Pages

To host the frontend dashboard on GitHub Pages:

1. Go to repository **Settings** → **Pages**
2. Source: **Deploy from a branch**
3. Branch: **main** → Folder: **/ (root)**
4. Click **Save**
5. Your dashboard will be available at: `https://yourusername.github.io/customer-churn-analytics/frontend/`

---

## ✅ Verification

After pushing, verify on GitHub:
- [ ] All files are uploaded
- [ ] README displays correctly with images
- [ ] Screenshots are visible
- [ ] License is detected
- [ ] Repository has a description
- [ ] Topics are added

---

## 🚀 Next Steps

1. **Add a .github/workflows** folder for CI/CD
2. **Create issues** for future enhancements
3. **Add a CONTRIBUTING.md** file
4. **Pin the repository** on your GitHub profile
5. **Share on LinkedIn** with project highlights

---

**Your repository is now ready to impress recruiters and showcase your skills!** 🎉
