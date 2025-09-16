# Locumtele Widgets

A comprehensive collection of medical widgets designed for healthcare providers, including dynamic forms, calendar integrations, and funnel pages.

## 🚀 Live Demo

Visit the [GitHub Pages site](https://locumtele.github.io/widgets/) to see all widgets in action.

## 📋 Widget Types

### 📝 Dynamic Forms
- **Medical Screening Forms**: Patient intake and assessment forms
- **JSON-Driven**: Generate forms dynamically from configuration files
- **Multiple Question Types**: Text, email, phone, checkbox, select, file inputs
- **Conditional Logic**: Show/hide questions based on user responses
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

### Universal Loader (Recommended)
```html
<script src="https://locumtele.github.io/widgets/forms/components/globalForm.js"></script>
<script>
    // Load a form
    GlobalWidgets.loadForm('forms/screeners/glp1.json', 'form-container');
    
    // Get available widgets
    const widgets = GlobalWidgets.getAvailableForms();
</script>
<div id="form-container"></div>
```

## 📚 Documentation

### For Form Integration
- **[Quick Start Guide](forms/documentation/QUICK_START.md)** - Get started with forms in 5 minutes
- **[n8n Integration](forms/documentation/N8N_INTEGRATION.md)** - Internal team automation setup
- **[Client API Docs](forms/documentation/CLIENT_API_DOCUMENTATION.md)** - For external clients with custom forms

### Available Forms
- **GLP-1 Weight Loss** - Weight management screening
- **NAD Anti-Aging** - Anti-aging therapy assessment  
- **Sermorelin Hormone** - Hormone therapy screening
- **And 10+ more specialty forms**

### Examples
- `forms/example-form.html` - Basic form selector
- `forms/advanced-example.html` - Advanced demo with metadata

## 📁 Project Structure

```
locumtele-widgets/
├── forms/                       # Dynamic form system
│   ├── components/              # Form system components
│   │   ├── formLoader.js       # Main form generator
│   │   ├── globalForm.js       # Universal form loader
│   │   ├── qTemplate.html      # Master form template
│   │   ├── formStyle.css       # Form styling
│   │   └── ghl-redirect.js     # GoHighLevel integration
│   ├── documentation/           # Form documentation
│   │   ├── CLIENT_API_DOCUMENTATION.md
│   │   ├── N8N_INTEGRATION.md
│   │   └── QUICK_START.md
│   ├── example-form.html       # Basic usage example
│   ├── advanced-example.html   # Advanced demo
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

### Universal Loader (Recommended)
The easiest way to integrate widgets is using the universal loader:

```html
<script src="https://locumtele.github.io/widgets/forms/components/globalForm.js"></script>
<script>
    // Load a form
    GlobalWidgets.loadForm('forms/screeners/glp1.json', 'form-container');
    
    // Get available forms
    const forms = GlobalWidgets.getAvailableForms();
    console.log(forms);
    
    // Load form data without rendering
    GlobalWidgets.loadFormData('forms/screeners/nad.json').then(data => {
        console.log('Form data:', data);
    });
</script>
```

### Direct Form Integration
For more control, use the formLoader directly:

```html
<script src="https://locumtele.github.io/widgets/forms/components/formLoader.js"></script>
<script>
    FormLoader.generateForm('forms/screeners/glp1.json', 'form-container');
</script>
```

### Calendars
```html
<iframe src="https://locumtele.github.io/widgets/calendars/weightloss.html"
    style="width:100%;height:800px;border:0;"></iframe>
```

### Forms (Iframe)
```html
<iframe src="https://locumtele.github.io/widgets/forms/example-form.html"
    style="width:100%;height:100vh;border:0;"></iframe>
```

### Footer Scripts
```html
<script src="https://locumtele.github.io/widgets/funnel/footerScreener.html"></script>
```

### Medication Forms (Iframe)
```html
<iframe src="https://locumtele.github.io/widgets/forms/screeners/semaglutide.html"
    style="width:100%;height:100vh;border:0;"></iframe>
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

- **v1.0.0** - Initial release with dynamic form loader
- **v1.1.0** - Added mobile optimizations
- **v1.2.0** - Enhanced validation and conditional logic

---

**Built with ❤️ for healthcare providers**
