# Global Widgets Project

A comprehensive collection of medical screening forms, calendar widgets, and funnel pages designed for healthcare providers using GoHighLevel (GHL) platforms.

## 🚀 Live Demo

Visit the [GitHub Pages site](https://yourusername.github.io/ltGlobalWidgets/) to see all widgets in action.

## 📋 Features

### 🏥 Dynamic Form Loader
- **JSON-Driven Forms**: Generate forms dynamically from JSON configuration files
- **Multiple Question Types**: Support for text, email, phone, checkbox, select, file inputs
- **Conditional Logic**: Show/hide questions based on user responses
- **Mobile Optimized**: Responsive design with iOS zoom prevention
- **Real-time Validation**: Client-side validation with error messages
- **API Integration**: Seamless integration with n8n webhooks

### 📅 Calendar Widgets
- Weight Loss
- Anti-Aging
- Hormones
- Sexual Health
- Hair & Skin
- General 

### 📝 Medical Screening Forms
- **GLP-1 Weight Loss** (24 questions)
- **NAD Anti-Aging** (17 questions)
- **Sermorelin Hormone** (15 questions)

### 🔧 Universal Loader
- **global.js** - Optional universal loader for easy widget integration
- **index.html** - Optional landing page with widget directory

## 🛠️ Quick Start

### Basic Usage

```html
<!-- Include the form loader -->
<script src="https://yourusername.github.io/ltGlobalWidgets/forms/formLoader.js"></script>

<!-- Auto-load a form -->
<div id="form-container" data-form-loader data-json-path="forms/screeners/glp1.json"></div>
```

### Programmatic Usage

```javascript
// Load a specific form
await FormLoader.generateForm('forms/screeners/glp1.json', 'form-container');

// Load form data only
const formData = await FormLoader.loadFormData('forms/screeners/nad.json');
```

### Available Forms

The formLoader.js script dynamically generates forms from JSON configuration files:

- **GLP-1 Weight Loss** (`forms/screeners/glp1.json`) - 24 questions
- **NAD Anti-Aging** (`forms/screeners/nad.json`) - 17 questions  
- **Sermorelin Hormone** (`forms/screeners/sermorelin.json`) - 15 questions

### Form Loader Examples

- `forms/example-form.html` - Basic form selector
- `forms/advanced-example.html` - Advanced demo with metadata

## 📁 Project Structure

```
ltGlobalWidgets/
├── forms/                       # Dynamic form system
│   ├── formLoader.js           # Main form generator
│   ├── example-form.html       # Basic usage example
│   ├── advanced-example.html   # Advanced demo
│   ├── qTemplate.html          # Master form template
│   ├── formStyle.css           # Form styling
│   ├── screeners/              # JSON configuration files
│   │   ├── glp1.json
│   │   ├── nad.json
│   │   └── sermorelin.json
│   └── reassessments/          # Reassessment forms
├── calendars/                   # Calendar widgets
│   ├── weightloss.html
│   ├── antiaging.html
│   ├── hormones.html
│   ├── sexualhealth.html
│   ├── hairskin.html
│   └── general.html
├── funnel/                      # Funnel pages
│   ├── footerScreener.html
│   └── map.html
├── global.js                    # Universal loader (optional)
└── index.html                   # Landing page (optional)
```

## 🔧 Configuration

### Adding New Forms

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

## 🌐 Embedding Widgets

### Calendars
```html
<iframe src="https://yourusername.github.io/ltGlobalWidgets/calendars/weightloss.html"
    style="width:100%;height:800px;border:0;"></iframe>
```

### Forms
```html
<iframe src="https://yourusername.github.io/ltGlobalWidgets/forms/example-form.html"
    style="width:100%;height:100vh;border:0;"></iframe>
```

### Footer Scripts
```html
<script src="https://yourusername.github.io/ltGlobalWidgets/funnel/footerScreener.html"></script>
```

### Medication Forms
```html
<iframe src="https://yourusername.github.io/ltGlobalWidgets/forms/screeners/semaglutide.html"
    style="width:100%;height:100vh;border:0;"></iframe>
```

### Universal Loader
```html
<script src="https://yourusername.github.io/ltGlobalWidgets/global.js"></script>
```

## 🎨 Customization

### Form Styling
Modify `forms/formStyle.css` to customize form appearance.

### Template Customization
Edit `forms/qTemplate.html` to modify the base form template.

### API Integration
Update the API endpoint in the form template's JavaScript section.

## 📱 Mobile Support

- Responsive design for all screen sizes
- iOS zoom prevention on form inputs
- Touch-friendly interface elements
- Optimized for mobile form completion

## 🔒 Security

- Client-side validation only
- No sensitive data stored locally
- Secure API integration with n8n webhooks
- HTTPS-only deployment

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support, email support@yourdomain.com or create an issue in this repository.

## 🔄 Version History

- **v1.0.0** - Initial release with dynamic form loader
- **v1.1.0** - Added mobile optimizations
- **v1.2.0** - Enhanced validation and conditional logic

---

**Built with ❤️ for healthcare providers**
