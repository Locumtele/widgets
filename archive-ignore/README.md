# Locumtele Widgets

A comprehensive collection of medical widgets designed for healthcare providers, featuring three embed types for different integration needs.

## 🚀 Live Demo

Visit the [GitHub Pages site](https://locumtele.github.io/widgets/) to see all widgets in action.

## 🎯 Three Embed Types

### 📝 Embed Type 1: Form Only
- **Purpose**: Simple screening forms that redirect to state selection
- **Flow**: Form → `{{rootdomain}}/{{category}}-state`
- **Use Case**: Basic patient screening with state selection

### 🗺️ Embed Type 2: State Selector with API
- **Purpose**: State selection with API-driven consult type determination
- **Flow**: State Selection → API Call → `{{rootdomain}}/{{category}}-{{consultType}}-fee`
- **Use Case**: When consult type needs to be determined by API

### 📅 Embed Type 3: Sync Calendar
- **Purpose**: Direct calendar booking for sync consultations
- **Flow**: Calendar Booking → `{{rootdomain}}/{{category}}-consult-booked`
- **Use Case**: Direct appointment scheduling

## 📋 Universal Form System

### ✨ Key Features
- **Any Data Structure**: Generate forms from any JSON data structure
- **Auto-Detection**: Automatically detects question types and form structure
- **Answer Logic**: Safe, flag, and disqualify answer handling
- **Mobile Optimized**: Responsive design with iOS zoom prevention
- **Multiple Question Types**: Text, email, phone, radio, checkbox, select, textarea, file, height, weight
- **Conditional Logic**: Real-time validation and disqualification handling

## 🛠️ Quick Start

### Embed Type 1: Form Only
```html
<link rel="stylesheet" href="https://locumtele.github.io/widgets/forms/components/universalFormStyle.css">
<script src="https://locumtele.github.io/widgets/forms/components/universalFormLoader.js"></script>
<script>
    const formData = {
        title: "Medical Screening",
        category: "weightloss", // weightloss, antiaging, hormone, etc.
        questions: [
            { text: "Name", type: "text", required: true },
            { text: "Email", type: "email", required: true },
            { text: "Do you have diabetes?", type: "radio", options: ["No", "Yes"], 
              safeAnswers: ["No"], disqualifyAnswers: ["Yes"] }
        ]
    };
    
    await window.generateForm(formData, 'form-container');
</script>
<div id="form-container"></div>
```

### Embed Type 2: State Selector with API
```html
<iframe src="https://locumtele.github.io/widgets/forms/state-selector.html?category=weightloss&location_id=123&location_name=Clinic%20Name" 
        style="width:100%;height:600px;border:0;"></iframe>
```

### Embed Type 3: Sync Calendar
```html
<iframe src="https://locumtele.github.io/widgets/calendars/weightloss.html" 
        style="width:100%;height:800px;border:0;"></iframe>
```

## 📚 Documentation

### Universal Form System
- **[Universal Forms Guide](forms/README-universal-forms.md)** - Complete documentation for the universal form system
- **[Demo Page](forms/universal-form-demo.html)** - Interactive demo with examples

### Additional Documentation
- **[Client API Docs](docs/api/api-screeners.md)** - For external clients with custom forms
- **[Widget Dashboard](widget-dashboard.html)** - Internal widget management interface
- **[Embed Types Guide](docs/EMBED_TYPES.md)** - Three embed types documentation
- **[API Dashboard](api-dashboard.html)** - API integration dashboard

### Examples
- `forms/universal-form-demo.html` - Interactive demo with multiple form types
- `glp1-screening-form.html` - Example of complex medical screening form

## 📁 Project Structure

```
ltGlobalWidgets/
├── README.md                    # Main project documentation
├── api-dashboard.html           # API integration dashboard
├── widget-dashboard.html        # Widget management dashboard
├── forms/                       # Universal form system
│   ├── components/              # Form system components
│   │   ├── universalFormLoader.js    # Universal form generator
│   │   └── universalFormStyle.css    # Universal styling
│   ├── universal-form-demo.html      # Interactive demo
│   ├── README-universal-forms.md     # Complete documentation
│   └── state-selector.html           # State selection for forms
├── docs/                        # Documentation and examples
│   ├── EMBED_TYPES.md           # Three embed types documentation
│   ├── README_widget.md         # Widget dashboard documentation
│   ├── pages/                   # Dashboard and widget pages
│   │   ├── integrations/        # Integration dashboard
│   │   └── widgets/             # Widget management dashboard
│   └── examples/                # Test files and examples
└── documentation/               # Brand assets and documentation
    ├── clinics/                 # Client API documentation
    └── docs/brand/              # Brand CSS system
```

## 🔧 Customization

### Forms
- **JSON Configuration**: Create custom forms using JSON files
- **Template System**: Modify `forms/components/qTemplate.html` for styling
- **Styling**: Update `forms/components/formStyle.css` for appearance
- **See**: [Quick Start Guide](forms/documentation/QUICK_START.md) for detailed instructions

### Calendars
- **Coming Soon**: Calendar customization options
- **Integration**: GoHighLevel calendar integration
- **Branding**: Customizable for different clinics

### General
- **API Integration**: Update webhook endpoints as needed
- **Mobile Support**: All widgets are mobile-optimized

## 🌐 Embedding Widgets

### Universal Form System (Recommended)
The easiest way to integrate forms is using the universal form system:

```html
<link rel="stylesheet" href="https://locumtele.github.io/widgets/forms/components/universalFormStyle.css">
<script src="https://locumtele.github.io/widgets/forms/components/universalFormLoader.js"></script>
<script>
    // Your form data (any structure!)
    const formData = {
        title: "Medical Screening",
        questions: [
            { text: "Name", type: "text", required: true },
            { text: "Email", type: "email", required: true }
        ]
    };
    
    // Generate form
    await window.generateForm(formData, 'form-container');
</script>
```

### Multi-Step Forms
```html
<script>
    const surveyData = {
        title: "Patient Survey",
        "Personal Info": [
            { text: "Name", type: "text", required: true }
        ],
        "Medical History": [
            { text: "Allergies", type: "textarea" }
        ]
    };
    
    await window.generateForm(surveyData, 'form-container');
</script>
```

### Calendars
```html
<iframe src="https://locumtele.github.io/widgets/calendars/weightloss.html"
    style="width:100%;height:800px;border:0;"></iframe>
```

### Forms (Iframe)
```html
<!-- Form selector with multiple options -->
<iframe src="https://locumtele.github.io/widgets/forms/example-form.html"
    style="width:100%;height:100vh;border:0;"></iframe>

<!-- Specific medication form -->
<iframe src="https://locumtele.github.io/widgets/forms/screeners/semaglutide.html"
    style="width:100%;height:100vh;border:0;"></iframe>
```

### Footer Scripts
```html
<script src="https://locumtele.github.io/widgets/funnel/footerScreener.html"></script>
```

## 🎨 Customization

### Form Styling
Modify `forms/components/formStyle.css` to customize form appearance.

### Template Customization
Edit `forms/components/qTemplate.html` to modify the base form template.

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

- **v2.0.0** - Universal Form System - Generate forms from any JSON data structure
- **v1.2.0** - Enhanced validation and conditional logic
- **v1.1.0** - Added mobile optimizations
- **v1.0.0** - Initial release with dynamic form loader

---

**Built with ❤️ for healthcare providers**
