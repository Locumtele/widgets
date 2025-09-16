# Quick Start Guide - Internal Team

## 🚀 Get Started in 5 Minutes

> **Note**: This guide is for our internal team using our Global Widgets form system. For external clients integrating their own forms, see [CLIENT_API_DOCUMENTATION.md](CLIENT_API_DOCUMENTATION.md).

### 1. Test Your Forms
Visit: https://locumtele.github.io/widgets/

### 2. Embed in GHL

#### Option A: Universal Loader (Recommended)
```html
<script src="https://locumtele.github.io/widgets/forms/components/globalForm.js"></script>
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
<iframe src="https://locumtele.github.io/widgets/forms/example-form.html"
    style="width:100%;height:100vh;border:0;"></iframe>

<!-- Specific medication form -->
<iframe src="https://locumtele.github.io/widgets/forms/screeners/glp1.json"
    style="width:100%;height:100vh;border:0;"></iframe>
```

### 3. n8n Integration
- **Webhook URL**: `https://locumtele.app.n8n.cloud/webhook/patient-screener`
- **Method**: POST
- **Response**: 302 redirect
- **Data**: JSON with patient info + form responses

### 4. Available Forms
- **GLP-1 Weight Loss** (`forms/screeners/glp1.json`) - 24 questions
- **NAD Anti-Aging** (`forms/screeners/nad.json`) - 17 questions  
- **Sermorelin Hormone** (`forms/screeners/sermorelin.json`) - 15 questions
- **Metformin** (`forms/screeners/metformin.json`) - Diabetes screening
- **Vitamin A** (`forms/screeners/vitamina.json`) - Vitamin therapy
- **Weight Loss** (`forms/screeners/weightloss.json`) - General weight management
- **Acne** (`forms/screeners/acne.json`) - Skin care screening
- **ED** (`forms/screeners/ed.json`) - Men's health
- **Herpes** (`forms/screeners/herpes.json`) - Sexual health
- **MCAS** (`forms/screeners/mcas.json`) - Allergy screening
- **And 10+ more specialty forms**

### 5. Customization
- Edit JSON files in `forms/screeners/` to modify questions
- Update `forms/components/qTemplate.html` for form styling
- Modify redirect URLs in the template
- Use `GlobalWidgets.getAvailableForms()` to see all available forms

### 6. Adding New Forms

1. Create a JSON file in `forms/screeners/` following this structure:

```json
{
  "screener": "YourMedication",
  "category": "CategoryName",
  "lastUpdated": "2025-01-15T10:00:00.000Z",
  "totalQuestions": 10,
  "questions": [
    {
      "id": 1,
      "section": "Patient Profile",
      "text": "Question Text",
      "type": "text|email|phone|checkbox|select|file",
      "safe": ["allowed_values"],
      "flag": ["flagged_values"],
      "disqualify": ["disqualifying_values"],
      "disqualifyMessage": "Disqualification message",
      "showCondition": "always|if_gender_female|etc",
      "category": "CategoryName"
    }
  ]
}
```

2. Use the form loader to generate the form:

```javascript
FormLoader.generateForm('forms/screeners/yourmedication.json', 'container-id');
```

## 📚 Full Documentation
- **n8n Integration**: [N8N_INTEGRATION.md](N8N_INTEGRATION.md)
- **README**: [README.md](README.md)
- **GitHub**: https://github.com/Locumtele/widgets

## 🆘 Need Help?
- Check the live examples on GitHub Pages
- Review the n8n integration guide
- Test with the example forms first
