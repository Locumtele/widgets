# Universal Form Generator System

A flexible, unified system that can generate forms from any JSON data structure. Automatically detects form structure and generates appropriate HTML with logic and validation.

## Features

- **Universal Compatibility**: Works with any JSON form data structure
- **Auto-Detection**: Automatically detects question types and form structure
- **Multiple Form Types**: Single forms, multi-step forms, and surveys
- **Comprehensive Question Types**: Text, email, phone, number, date, radio, checkbox, select, textarea, file, height, weight
- **Conditional Logic**: Built-in support for disqualification and conditional questions
- **Validation**: Real-time validation with error messages
- **Mobile Responsive**: Optimized for all device sizes
- **Accessibility**: Proper labels, ARIA attributes, and keyboard navigation

## Quick Start

### 1. Include the Files

```html
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="components/universalFormStyle.css">
</head>
<body>
    <div id="form-container"></div>
    <script src="components/universalFormLoader.js"></script>
</body>
</html>
```

### 2. Create Your Form Data

```javascript
const formData = {
    title: "Contact Form",
    subtitle: "Get in touch with us",
    category: "contact",
    questions: [
        {
            text: "Full Name",
            type: "text",
            required: true,
            placeholder: "Enter your full name"
        },
        {
            text: "Email Address",
            type: "email",
            required: true
        },
        {
            text: "Message",
            type: "textarea",
            required: true,
            placeholder: "Tell us about your inquiry"
        }
    ]
};
```

### 3. Generate the Form

```javascript
// Generate form
await window.UniversalFormLoader.generateForm(formData, 'form-container');

// Or use the helper function
await window.generateForm(formData, 'form-container');
```

## Supported Data Structures

### Simple Array Structure
```javascript
[
    {
        text: "Question 1",
        type: "text",
        required: true
    },
    {
        text: "Question 2",
        type: "radio",
        options: ["Option 1", "Option 2"]
    }
]
```

### Object with Questions Property
```javascript
{
    title: "My Form",
    questions: [
        { text: "Name", type: "text", required: true }
    ]
}
```

### Multi-Section Structure
```javascript
{
    title: "Survey",
    "Section 1": [
        { text: "Question 1", type: "text" }
    ],
    "Section 2": [
        { text: "Question 2", type: "radio", options: ["A", "B"] }
    ]
}
```

## Question Types

### Text Input
```javascript
{
    text: "Full Name",
    type: "text",
    required: true,
    placeholder: "Enter your name"
}
```

### Email Input
```javascript
{
    text: "Email Address",
    type: "email",
    required: true
}
```

### Phone Input
```javascript
{
    text: "Phone Number",
    type: "phone",
    required: true
}
```

### Number Input
```javascript
{
    text: "Age",
    type: "number",
    required: true,
    min: 18,
    max: 100
}
```

### Date Input
```javascript
{
    text: "Date of Birth",
    type: "date",
    required: true
}
```

### Radio Buttons
```javascript
{
    text: "Gender",
    type: "radio",
    required: true,
    options: ["Male", "Female", "Other"]
}
```

### Checkboxes
```javascript
{
    text: "Interests",
    type: "checkbox",
    options: ["Sports", "Music", "Reading", "Travel"]
}
```

### Select Dropdown
```javascript
{
    text: "Country",
    type: "select",
    required: true,
    options: ["USA", "Canada", "UK", "Australia"]
}
```

### Textarea
```javascript
{
    text: "Comments",
    type: "textarea",
    required: false,
    rows: 4,
    placeholder: "Enter your comments"
}
```

### File Upload
```javascript
{
    text: "Upload Document",
    type: "file",
    required: true,
    accept: "image/*,.pdf"
}
```

### Height Input (Feet and Inches)
```javascript
{
    text: "Height",
    type: "height",
    required: true
}
```

### Weight Input
```javascript
{
    text: "Weight (pounds)",
    type: "weight",
    required: true
}
```

## Advanced Features

### Disqualification Logic
```javascript
{
    text: "Do you have diabetes?",
    type: "radio",
    required: true,
    options: ["No", "Type 1", "Type 2"],
    safeAnswers: ["No"],
    disqualifyAnswers: ["Type 1", "Type 2"],
    disqualifyMessage: "This treatment is not suitable for diabetics"
}
```

### Flagging Answers
```javascript
{
    text: "Blood Pressure",
    type: "radio",
    required: true,
    options: ["Normal", "High", "Very High"],
    safeAnswers: ["Normal"],
    flagAnswers: ["High"],
    disqualifyAnswers: ["Very High"]
}
```

### Auto-Detection
The system can automatically detect question types based on text content:
- "email" → email input
- "phone" → phone input
- "date" or "birth" → date input
- "height" → height input
- "weight" → weight input
- "gender" → radio buttons
- Questions with options → radio/checkbox/select

## Multi-Step Forms

For multi-step forms, use section-based structure:

```javascript
{
    title: "Multi-Step Survey",
    "Personal Information": [
        { text: "Name", type: "text", required: true },
        { text: "Email", type: "email", required: true }
    ],
    "Preferences": [
        { text: "Favorite Color", type: "radio", options: ["Red", "Blue", "Green"] }
    ],
    "Feedback": [
        { text: "Comments", type: "textarea" }
    ]
}
```

## Customization Options

```javascript
await window.UniversalFormLoader.generateForm(formData, 'container-id', {
    showProgress: true,        // Show progress bar for multi-step forms
    allowBackNavigation: true, // Allow back navigation
    submitText: 'Submit Form', // Custom submit button text
    theme: 'default'          // Theme (future feature)
});
```

## Styling

The system includes comprehensive CSS that works out of the box. You can customize by overriding CSS classes:

- `.universal-form-container` - Main container
- `.form-header` - Form title and subtitle
- `.question` - Individual question styling
- `.option-group` - Radio/checkbox groups
- `.nav-button` - Navigation buttons
- `.error-message` - Error styling
- `.disqualification-message` - Disqualification styling

## Mobile Optimization

- Responsive design that works on all screen sizes
- Touch-friendly input targets (44px minimum)
- Prevents zoom on iOS input focus
- Optimized layouts for mobile devices

## Browser Support

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+
- Mobile browsers (iOS Safari, Chrome Mobile)

## API Reference

### UniversalFormLoader Class

#### Methods

- `generateForm(formData, containerId, options)` - Generate form from data
- `analyzeFormStructure(formData)` - Analyze form structure
- `buildFormHTML(options)` - Build form HTML
- `generateQuestionHTML(question)` - Generate question HTML
- `initializeForm()` - Initialize form functionality

#### Properties

- `currentFormData` - Current form data
- `formConfig` - Analyzed form configuration
- `questionIdCounter` - Counter for unique question IDs

## Examples

See `universal-form-demo.html` for comprehensive examples including:
- Simple contact form
- Medical screening form
- Multi-step survey
- Complex assessment form

## Complete Form Flow

The Universal Form System implements a complete patient journey:

### 1. Form Submission
- Collects form data and stores in `sessionStorage`
- Redirects to state selector (NO webhook submission yet)
- Shows success message before redirect

### 2. State Selection
- Gets form data from `sessionStorage`
- Submits webhook data in proper format to `https://locumtele.app.n8n.cloud/webhook/patient-screener`
- Redirects to correct fee page with URL parameters

### 3. Fee Page Autofill
- Fee pages receive URL parameters: `name`, `email`, `phone`, `state`, `category`, `consult_type`
- Include `fee-page-autofill.js` script to automatically populate contact fields
- Supports multiple field naming conventions

### Webhook Data Format

The system sends data in this exact format:

```json
{
  "contact": {
    "name": "string",
    "email": "string", 
    "gender": "string",
    "dateOfBirth": "string (YYYY-MM-DD)",
    "phone": "string",
    "address1": "string",
    "city": "string",
    "state": "string",
    "postalCode": "string",
    "timezone": "string",
    "type": "patient"
  },
  "patient": {
    "patientId": "string",
    "contactId": "string", 
    "rxRequested": "string",
    "height": "string",
    "weight": "string",
    "BMI": "string",
    "pregnancy": "string",
    "conditions": ["string"],
    "medications": ["string"],
    "allergies": "string",
    "activityLevel": "string",
    "tobaccoUse": "string",
    "alcoholUse": "string",
    "otcConsumption": ["string"],
    "mentalHealth": "string"
  },
  "form": {
    "formType": "string",
    "category": "string", 
    "screener": "string",
    "screenerData": "string",
    "timestamp": "string (ISO 8601)",
    "formVersion": "string"
  },
  "clinic": {
    "name": "string",
    "id": "string",
    "email": "string", 
    "phone": "string",
    "type": "healthcare"
  }
}
```

### Fee Page Integration

Add this script to your fee pages for automatic contact info population:

```html
<script src="https://locumtele.github.io/widgets/forms/components/fee-page-autofill.js"></script>
```

The script automatically finds and fills:
- Name fields (by name, id, placeholder, or label)
- Email fields (by type, name, id, placeholder, or label)  
- Phone fields (by type, name, id, placeholder, or label)
- State fields (by name, id, placeholder, or label)

## Integration

### With Existing Systems

```javascript
// Load form data from API
const response = await fetch('/api/form-data');
const formData = await response.json();

// Generate form
await window.UniversalFormLoader.generateForm(formData, 'form-container');
```

### With Form Submission

The system automatically handles the complete flow:
1. Form submission → State selector
2. State selection → Webhook + Fee page redirect
3. Fee page → Auto-fill contact info

## Troubleshooting

### Common Issues

1. **Form not displaying**: Check that the container element exists
2. **Questions not rendering**: Verify question data structure
3. **Validation not working**: Ensure required fields are marked correctly
4. **Mobile issues**: Check viewport meta tag is present

### Debug Mode

Enable debug logging:
```javascript
console.log('Form data:', formData);
console.log('Form config:', this.formConfig);
```

## Contributing

To extend the system:

1. Add new question types in `generateInputField()`
2. Add new validation rules in `validateField()`
3. Add new conditional logic in `checkConditionalLogic()`
4. Add new styling in `universalFormStyle.css`

## License

This system is part of the ltGlobalWidgets project.
