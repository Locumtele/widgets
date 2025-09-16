# Quick Start Guide - Internal Team

## 🚀 Get Started in 5 Minutes

> **Note**: This guide is for our internal team using our Global Widgets form system. For external clients integrating their own forms, see [CLIENT_API_DOCUMENTATION.md](CLIENT_API_DOCUMENTATION.md).

### 1. Test Your Forms
Visit: https://locumtele.github.io/ltGlobalWidgets/

### 2. Embed in GHL

#### Option A: Universal Loader (Recommended)
```html
<script src="https://locumtele.github.io/ltGlobalWidgets/forms/components/globalForm.js"></script>
<script>
    // Load a specific form
    GlobalWidgets.loadForm('forms/screeners/glp1.json', 'form-container');
    
    // Or get available forms and let user choose
    const forms = GlobalWidgets.getAvailableForms();
    console.log(forms);
</script>
<div id="form-container"></div>
```

#### Option B: Iframe Integration
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
- Update `forms/components/qTemplate.html` for form styling
- Modify redirect URLs in the template
- Use `GlobalWidgets.getAvailableForms()` to see all available forms

## 📚 Full Documentation
- **n8n Integration**: [N8N_INTEGRATION.md](N8N_INTEGRATION.md)
- **README**: [README.md](README.md)
- **GitHub**: https://github.com/Locumtele/ltGlobalWidgets

## 🆘 Need Help?
- Check the live examples on GitHub Pages
- Review the n8n integration guide
- Test with the example forms first
