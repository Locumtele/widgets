# Locumtele Widgets

A comprehensive collection of medical widgets designed for healthcare providers, including dynamic forms, calendar integrations, and funnel pages.

## 🚀 Live Demo

Visit the [GitHub Pages site](https://locumtele.github.io/widgets/) to see all widgets in action.

## 📋 Widget Types

### 📝 Universal Form System
- **Any Data Structure**: Generate forms from any JSON data structure
- **Auto-Detection**: Automatically detects question types and form structure
- **Multiple Form Types**: Single forms, multi-step forms, and surveys
- **Comprehensive Question Types**: Text, email, phone, number, date, radio, checkbox, select, textarea, file, height, weight
- **Advanced Logic**: Disqualification handling, conditional questions, validation
- **Mobile Optimized**: Responsive design with iOS zoom prevention
- **API Integration**: Seamless integration with n8n webhooks

### 📅 Calendar Widgets
- **Specialty Calendars**: Weight Loss, Anti-Aging, Hormones
- **Appointment Booking**: Integrated scheduling solutions
- **Customizable**: Tailored for different medical specialties

### 🔄 Funnel Pages
- **Patient Acquisition**: Conversion-optimized landing pages
- **Lead Capture**: Integrated form and calendar solutions
- **Customizable**: Branded for different clinics

## 🛠️ Quick Start

### Universal Form System (Recommended)
```html
<link rel="stylesheet" href="https://locumtele.github.io/widgets/forms/components/universalFormStyle.css">
<script src="https://locumtele.github.io/widgets/forms/components/universalFormLoader.js"></script>
<script>
    // Your form data (any structure!)
    const formData = {
        title: "Medical Screening",
        questions: [
            { text: "Name", type: "text", required: true },
            { text: "Email", type: "email", required: true },
            { text: "Do you have diabetes?", type: "radio", options: ["No", "Yes"], 
              safeAnswers: ["No"], disqualifyAnswers: ["Yes"] }
        ]
    };
    
    // Generate form
    await window.generateForm(formData, 'form-container');
</script>
<div id="form-container"></div>
```

## 📚 Documentation

### Universal Form System
- **[Universal Forms Guide](forms/README-universal-forms.md)** - Complete documentation for the universal form system
- **[Demo Page](forms/universal-form-demo.html)** - Interactive demo with examples
- **[Cleanup Summary](forms/CLEANUP-SUMMARY.md)** - What changed in the latest update

### Legacy Documentation
- **[n8n Integration](forms/documentation/N8N_INTEGRATION.md)** - Internal team automation setup
- **[Client API Docs](forms/documentation/CLIENT_API_DOCUMENTATION.md)** - For external clients with custom forms

### Examples
- `forms/universal-form-demo.html` - Interactive demo with multiple form types
- `glp1-screening-form.html` - Example of complex medical screening form

## 📁 Project Structure

```
ltGlobalWidgets/
├── forms/                       # Universal form system
│   ├── components/              # Form system components
│   │   ├── universalFormLoader.js    # Universal form generator
│   │   ├── universalFormStyle.css    # Universal styling
│   │   └── ghl-redirect.js           # GoHighLevel integration
│   ├── universal-form-demo.html      # Interactive demo
│   ├── README-universal-forms.md     # Complete documentation
│   └── CLEANUP-SUMMARY.md            # What changed
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
└── index.html                   # Landing page (optional)
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
