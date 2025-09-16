# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. Test Your Forms
Visit: https://locumtele.github.io/ltGlobalWidgets/

### 2. Embed in GHL
```html
<!-- Basic form selector -->
<iframe src="https://locumtele.github.io/ltGlobalWidgets/forms/example-form.html"
    style="width:100%;height:100vh;border:0;"></iframe>

<!-- Specific medication form -->
<iframe src="https://locumtele.github.io/ltGlobalWidgets/forms/screeners/glp1.json"
    style="width:100%;height:100vh;border:0;"></iframe>
```

### 3. n8n Integration
- **Webhook URL**: `https://locumtele.app.n8n.cloud/webhook/patient-screener`
- **Method**: POST
- **Response**: 302 redirect
- **Data**: JSON with patient info + form responses

### 4. Available Forms
- **GLP-1 Weight Loss** (24 questions)
- **NAD Anti-Aging** (17 questions)
- **Sermorelin Hormone** (15 questions)
- **Acne, CBD, ED, Herpes** and 10+ more

### 5. Customization
- Edit JSON files in `forms/screeners/` to modify questions
- Update `forms/qTemplate.html` for form styling
- Modify redirect URLs in the template

## 📚 Full Documentation
- **n8n Integration**: [N8N_INTEGRATION.md](N8N_INTEGRATION.md)
- **README**: [README.md](README.md)
- **GitHub**: https://github.com/Locumtele/ltGlobalWidgets

## 🆘 Need Help?
- Check the live examples on GitHub Pages
- Review the n8n integration guide
- Test with the example forms first
