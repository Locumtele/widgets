# 🏥 LocumTele Medical Form System

**Last Updated**: January 21, 2025  
**Project Status**: Production Ready  
**Live Demo**: [GitHub Pages](https://locumtele.github.io/widgets/)

## 🚀 Quick Start

### Generate a Medical Form
```bash
cd python-forms
python3 regenerate_complete_form.py
```

This creates a production-ready medical screening form at `surveys/weightloss/GLP1-screener-live.html`.

### Embed in Your Website
```html
<!-- Copy the entire HTML content from the generated file -->
<!-- Paste into your GHL custom HTML widget or any website -->
```

## 📋 Project Overview

This is a complete medical form generation system for GHL (GoHighLevel) white-label healthcare businesses. The system generates dynamic, responsive medical screening forms from JSON data with advanced conditional logic, real-time BMI calculation, and comprehensive API integration. It's designed specifically for telemedicine patient screening and integrates with n8n webhooks for data processing.

### 🎯 Target Audience
- **White-label healthcare providers** using GHL
- **Telemedicine companies** needing patient screening
- **Weight loss clinics** offering GLP1 treatments
- **Men's health clinics** offering TRT treatments

## 🎯 Project Goals & Business Context

### Primary Objectives
1. **Generate medical screening forms** for various treatments (GLP1, testosterone, etc.)
2. **Integrate with GHL** as embeddable HTML widgets
3. **Stream data to n8n** for automated patient processing workflows
4. **Provide conditional logic** for medical screening requirements
5. **Calculate BMI** and apply form-specific disqualification rules
6. **Handle state-based routing** for sync vs async consultations

### Target Market
- **White-label healthcare providers** using GHL
- **Telemedicine companies** needing patient screening
- **Weight loss clinics** offering GLP1 treatments
- **Men's health clinics** offering TRT treatments

## 📁 Project Structure

```
ltGlobalWidgets/
├── README.md                           # This file - Main documentation
├── python-forms/                       # Core form generation system
│   ├── enhanced_form_generator.py      # Main form generation engine
│   ├── form_data_loader.py            # JSON data parser
│   ├── regenerate_complete_form.py    # Form generation script
│   ├── surveys/all-forms/             # Shared form sections
│   └── components/                    # Universal form components
├── surveys/                           # Generated forms and form data
│   ├── weightloss/GLP1-screener-live.html  # Production form
│   ├── weightloss/GLP1-screener.json      # Form data
│   ├── hormone/Sermorelin-screener.json   # Hormone form data
│   └── antiaging/NAD-screener.json        # Anti-aging form data
├── docs/                              # Documentation and assets
│   ├── api/                          # API documentation
│   ├── brand/                        # Brand assets and CSS
│   └── widgets/                      # Widget dashboard docs
├── widget-dashboard.html             # Widget management interface
├── forms-dashboard.html              # Forms management & embed code library
├── api-dashboard.html                # API integration dashboard
└── archive-ignore/                   # Outdated files and old systems
```

## 🔧 Technical Architecture

### Core Components

#### 1. Enhanced Form Generator (`enhanced_form_generator.py`)
**Purpose**: Main form generation engine
**Key Features**:
- Multi-section form generation (Patient Profile, Medical History, Verification, Assessment)
- Conditional logic engine for dynamic question visibility
- Real-time BMI calculation with form-specific disqualification rules
- Phone number validation with auto-formatting
- Modern UI with professional black/white theme
- Local storage for form persistence across browser sessions
- State selector with sync-only state detection
- File upload handling with validation
- Comprehensive API integration

**Critical Methods**:
- `generate_notion_form()`: Main form generation entry point
- `generate_all_sections()`: Creates all form sections
- `generate_form_javascript()`: Creates interactive JavaScript
- `generate_height_weight_group()`: Special 3-column layout with BMI display

#### 2. Form Data Loader (`form_data_loader.py`)
**Purpose**: Intelligent JSON parser and data combiner
**Key Features**:
- Loads general sections from local `surveys/all-forms/` directory
- Loads form-specific assessments from `/surveys/{category}/`
- Combines data into complete form structure
- Handles question ordering and option sorting
- Generates unique question IDs from Notion data

**Critical Methods**:
- `generate_complete_form_data()`: Combines all data sources
- `load_general_sections()`: Loads shared form sections
- `load_form_assessment()`: Loads form-specific questions
- `_convert_questions()`: Converts Notion format to internal format

#### 3. Conditional Logic System
**Purpose**: Dynamic question visibility based on user answers
**Implementation**: JavaScript functions within generated forms

**Available Conditions**:
- `always`: Question always visible
- `if_gender_female`: Shows for female patients (pregnancy questions)
- `if_allergies_yes`: Shows when allergies are indicated
- `if_other_glp1s_yes`: Shows for patients taking other GLP-1 medications
- `if_tobacco_yes` / `if_tobacco_use_yes`: Shows tobacco follow-up questions

### Data Flow Architecture

```
JSON Data Sources → Form Data Loader → Enhanced Form Generator → HTML Form
     ↓                    ↓                      ↓               ↓
surveys/all-forms/  Combines sections    Generates UI      User fills form
surveys/{category}/ Sorts questions      Adds JavaScript   JavaScript validates
                   Creates IDs          Applies styling   Sends to webhook
```

### API Integration

**Webhook Endpoint**: `https://locumtele.app.n8n.cloud/webhook/patient-screener`

**Data Structure Sent**:
```json
{
  "contact": {
    "name": "Patient Name",
    "email": "patient@email.com",
    "phone": "(555) 123-4567",
    "address": "123 Main St",
    "address2": "Apt 1",
    "city": "City",
    "state": "CA",
    "postalCode": "12345",
    "type": "patient"
  },
  "patient": {
    "rxRequested": "GLP1",
    "height": "5'10\"",
    "weight": "180",
    "BMI": "25.8"
  },
  "form": {
    "formType": "screener",
    "category": "Weightloss",
    "screener": "GLP1",
    "timestamp": "2025-01-21T...",
    "formVersion": "1.0",
    "answers": {
      "What is your exercise level?": "moderate",
      "Do you have any allergies?": "no",
      "Do you currently use tobacco or vape?": "no"
    },
    "consultType": "async"
  },
  "clinic": {
    "name": "{{location.name}}",
    "id": "{{location.id}}",
    "type": "healthcare"
  }
}
```

## 📊 Current Implementation Status

### ✅ Completed Features

#### Core Functionality
- **Multi-section forms**: 4 sections with 30 total questions
- **Form generation**: Complete HTML/CSS/JavaScript generation from JSON
- **Data loading**: Intelligent parsing of Notion-exported JSON data
- **Question ordering**: Proper sorting by `property_order` field
- **Option sorting**: "none", "none_of_the_above", "no" options placed last

#### User Experience
- **Phone validation**: 10-digit validation with real-time formatting `(555) 123-4567`
- **BMI calculation**: Real-time calculation displayed in Patient Profile section
- **Modern styling**: Professional black/white theme with gradient accents
- **Form persistence**: Local storage with intelligent cleanup
- **Progress tracking**: Visual progress bar with section indicators
- **Navigation**: Previous/Next buttons with proper validation
- **Mobile responsive**: Works perfectly on all devices

#### Medical-Specific Features
- **Conditional logic**: All major medical conditional patterns implemented
- **Disqualification logic**: Smart messaging for medical disqualification criteria
- **Pregnancy questions**: Conditional visibility for female patients
- **Allergy follow-ups**: Detail questions when allergies are indicated
- **Tobacco follow-ups**: Follow-up questions for tobacco users
- **File uploads**: Government ID and body photo uploads with validation

#### Technical Features
- **State selector**: Full US states dropdown with sync-only state detection
- **Radio button fixes**: No pre-selection on fresh loads
- **API integration**: Complete webhook data submission with proper structure
- **Error handling**: Comprehensive validation and error messaging
- **Cross-browser compatibility**: Works in all modern browsers

### 📊 Form Statistics
- **Total Questions**: 30
- **Sections**: 4 (Patient Profile, Medical History, Verification, Assessment)
- **Conditional Questions**: 3 (pregnancy, allergy details, tobacco follow-up)
- **Disqualifying Questions**: 8 with smart messaging
- **File Uploads**: 2 (government ID, body photos)
- **API Fields**: 50+ structured data points sent to webhook

## 🧪 Complete Testing Checklist

### ✅ Functional Testing
1. **Phone number formatting and validation**: Auto-formats, prevents letters, validates 10 digits
2. **Female gender → pregnancy question appears**: Conditional logic working
3. **Height/weight → BMI calculates automatically**: Real-time calculation
4. **BMI under 25 → can proceed to see value**: Form-specific disqualification rules
5. **Tobacco "yes" → follow-up question appears**: Tobacco conditional logic
6. **Disqualifying answers → modern styled messages appear**: Professional messaging
7. **Form submission → complete data sent to webhook**: API integration working
8. **State selection → proper async/sync routing**: State-based logic
9. **File uploads → validation and visual feedback**: Upload handling
10. **Form persistence → remembers progress across sessions**: Local storage working

### ✅ UI/UX Testing
- **Responsive design**: Works on desktop, tablet, mobile
- **Navigation flow**: Smooth transitions between sections
- **Visual feedback**: Clear error messages and validation states
- **Professional appearance**: Modern, medical-grade styling
- **Accessibility**: Proper form labels and keyboard navigation

### ✅ Integration Testing
- **Webhook submission**: Data successfully reaches n8n endpoint
- **Data structure**: All required fields properly formatted
- **Question text keys**: Readable question names in API data
- **Error handling**: Graceful handling of network issues
- **GHL embedding**: Form works properly when embedded in GHL

## 🔄 Development Workflow

### Current Process
1. **Update JSON data**: Modify files in `surveys/all-forms/` or `surveys/{category}/`
2. **Update generator**: Modify `enhanced_form_generator.py` for UI/logic changes
3. **Regenerate form**: Run `python3 regenerate_complete_form.py`
4. **Test**: Open `surveys/weightloss/GLP1-screener-live.html` in browser
5. **Deploy**: Copy HTML content to GHL widget

### Key Files to Modify
- **JSON data**: `surveys/all-forms/` and `surveys/{category}/` files
- **Form logic**: `enhanced_form_generator.py`
- **Data parsing**: `form_data_loader.py`
- **Generation script**: `regenerate_complete_form.py`

## 📚 Documentation Index

### 🏥 Core System Documentation
- **[Python Form Generator](python-forms/README-Python-Form-Generator.md)** - Complete technical documentation for the form generation system
- **[Quick Start Guide](python-forms/README-Quick-Start-Guide.md)** - Get up and running in minutes with simple commands
- **[Integration Guide](python-forms/README-Integration-Guide.md)** - Deploy and integrate the Python system with existing workflows
- **[Conditional Logic Reference](python-forms/README-Conditional-Logic-Reference.md)** - Complete reference for form question conditional logic

### 🎛️ Dashboard & Interface Documentation
- **[Forms Dashboard](docs/widgets/README-Forms-Dashboard.md)** - Complete guide to the embed code library and form management interface
- **[CSS Framework](docs/brand/README-CSS-Framework.md)** - Brand system and dashboard framework for creating new interfaces

### 🔌 API & Integration Documentation
- **[Patient Screening API](docs/api/README-Patient-Screening-API.md)** - External API for submitting patient screening data from custom forms

### 📋 Quick Reference
- **Main Project Overview**: This README.md file
- **Forms Dashboard**: `forms-dashboard.html` - Live embed code library
- **Widget Dashboard**: `widget-dashboard.html` - Internal management interface
- **API Dashboard**: `api-dashboard.html` - API integration dashboard

## 📚 Knowledge Base

### Critical Implementation Details

#### Conditional Logic Patterns
The system uses string matching in JavaScript to implement conditional logic:

```javascript
// Example: Tobacco follow-up
if (condition === 'if_tobacco_yes' || condition === 'if_tobacco_use_yes') {
    const tobaccoInputs = document.querySelectorAll('input[type="radio"][value="yes"]:checked');
    for (let input of tobaccoInputs) {
        const questionText = input.closest('.question-container').querySelector('label[class*="question-label"]')?.textContent;
        if (questionText && (questionText.toLowerCase().includes('tobacco') || questionText.toLowerCase().includes('vape'))) {
            shouldShow = true;
            break;
        }
    }
}
```

#### BMI Calculation & Disqualification
BMI is calculated in real-time and displayed in the Patient Profile section. Disqualification logic is form-specific:

```javascript
// BMI calculation
function calculateBMI() {
    const feet = parseInt(feetInput.value) || 0;
    const inches = parseInt(inchesInput.value) || 0;
    const weight = parseFloat(weightInput.value) || 0;

    if (feet > 0 && weight > 0) {
        const totalInches = (feet * 12) + inches;
        const heightInMeters = totalInches * 0.0254;
        const weightInKg = weight * 0.453592;
        const bmi = weightInKg / (heightInMeters * heightInMeters);

        // Display BMI
        bmiValueElement.textContent = bmi.toFixed(1);

        // Check disqualification (only for GLP1 forms)
        if (category === 'Weightloss' && form_name === 'GLP1' && bmi < 25) {
            // Show disqualification message
        }
    }
}
```

#### API Data Structure Logic
The webhook data building function dynamically finds form inputs and structures data:

```javascript
// Build comprehensive form answers object with question text as keys
const formAnswers = {};
const contactFields = ['name', 'email', 'phone', 'address', 'city', 'state', 'postal'];

const allInputs = document.querySelectorAll('input, select, textarea');
allInputs.forEach(input => {
    if (input.name && input.value) {
        // Get question text
        const questionWrapper = input.closest('.question-wrapper');
        let questionText = questionWrapper?.querySelector('label')?.textContent?.trim() || input.name;

        // Remove asterisk from required fields
        questionText = questionText.replace('*', '').trim();

        // Skip contact info fields - they're already in contact section
        const isContactField = contactFields.some(field =>
            questionText.toLowerCase().includes(field) ||
            (field === 'name' && questionText.toLowerCase().includes('full name'))
        );

        if (!isContactField) {
            // Add to answers object
            formAnswers[questionText] = input.value;
        }
    }
});
```

### Sync-Only States Logic
Certain states only support synchronous consultations:

```javascript
const syncOnlyStates = ['AL', 'AK', 'AR', 'ID', 'IA', 'KS', 'KY', 'LA', 'ME', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NM', 'ND', 'OK', 'SC', 'SD', 'TN', 'UT', 'VT', 'WV', 'WY'];

if (syncOnlyStates.includes(selectedState)) {
    finalConsultType = 'sync';
} else {
    finalConsultType = consultType; // Use original consult type
}
```

## 🚀 Deployment & Integration

### Forms Dashboard
The Forms Dashboard (`forms-dashboard.html`) provides a comprehensive management interface for medical forms:

#### 📊 Dashboard Tab - Embed Code Library
- **Shows only forms with HTML files AND embed codes ready**
- **Compact table layout** for hundreds of forms
- **Category toggle buttons** (All, Weightloss, Hormone, Anti-Aging)
- **Search functionality** for quick form finding
- **One-click embed code copying** for client deployment
- **Preview buttons** to test live surveys
- **Bulk operations** (copy all codes, deployment reports)

#### 📝 Forms Tab - Form Management
- **Shows only forms with HTML files ready**
- **Form overview** with question counts and categories
- **Question logic visualization** with color-coded safe/flag/disqualify options
- **Survey preview** in modal iframe
- **Recent submissions** tracking

#### 🎛️ Control Panel Tab - Automation
- **Safe automation controls** separated from main workflow
- **Automatic form discovery** - scans surveys directory for new JSON files
- **Real-time status checking** for HTML files and embed codes
- **HTML file status tracking** (exists/missing)
- **Embed code generation status** (ready/pending)
- **Batch operations** for efficiency

⚠️ **Note**: HTML generation and embed code creation buttons were removed due to JavaScript template literal syntax issues. HTML files must be generated manually using the Python scripts in the `python-forms/` directory.

### For GHL Integration
1. **Generate form**: `cd python-forms && python3 regenerate_complete_form.py`
2. **Extract HTML**: Copy entire content from `surveys/weightloss/GLP1-screener-live.html`
3. **Embed in GHL**: Paste as custom HTML widget
4. **Test webhook**: Verify data reaches n8n endpoint at `https://locumtele.app.n8n.cloud/webhook/patient-screener`

### For Client Deployment
1. **Open Forms Dashboard**: `forms-dashboard.html`
2. **Navigate to Dashboard tab**: Embed Code Library
3. **Search/filter forms**: Use category toggles and search bar
4. **Copy embed code**: Click "📋 Copy" button for desired form
5. **Paste in client website**: Embed code is ready for deployment

### Local Development & Testing
```bash
# Navigate to project
cd /Users/tatyanagomez/Projects/ltGlobalWidgets/python-forms/

# Generate latest form
python3 regenerate_complete_form.py

# Open for testing
open surveys/weightloss/GLP1-screener-live.html

# Monitor network tab in browser dev tools to verify API calls
```

## 🔧 Configuration & Customization

### Key Configuration Points

#### Webhook URL
```javascript
const response = await fetch('https://locumtele.app.n8n.cloud/webhook/patient-screener', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
});
```

#### Local Storage Key Format
```javascript
const storageKey = `medicalForm_${form_name}_${category}`;
// Example: "medicalForm_GLP1_Weightloss"
```

#### BMI Disqualification Rules
```javascript
// Only applies to GLP1 Weightloss forms with BMI < 25
if (category === 'Weightloss' && form_name === 'GLP1' && bmi < 25) {
    // Show disqualification
}
```

### Styling Variables
```css
/* Main theme colors */
:root {
    --primary-color: #333;
    --secondary-color: #555;
    --accent-color: #e74c3c;
    --background-gradient: linear-gradient(135deg, #fff 0%, #fef7f7 100%);
}
```

## 🛠️ Troubleshooting Guide

### Common Issues & Solutions

#### Radio Buttons Pre-selecting
**Issue**: Radio buttons showing as selected on page load
**Solution**: Clear localStorage for the form
```javascript
localStorage.removeItem('medicalForm_GLP1_Weightloss');
```

#### Phone Validation Not Working
**Issue**: Phone field accepting letters or not validating
**Solution**: Check `formatPhoneInput()` function and validation logic

#### Conditional Logic Not Triggering
**Issue**: Follow-up questions not appearing
**Solution**:
1. Check question text matching in JavaScript
2. Verify `property_show_condition` in JSON data
3. Ensure condition is added to `checkQuestionVisibility()` function

#### API Data Issues
**Issue**: Webhook not receiving expected data
**Solution**:
1. Check browser console for errors
2. Verify webhook URL is accessible
3. Check data structure in `buildWebhookData()` function

#### BMI Calculation Not Working
**Issue**: BMI not calculating or displaying
**Solution**:
1. Check height/weight input selectors
2. Verify BMI calculation formula
3. Ensure `calculateBMI()` is called on input changes

## 📈 Future Development Roadmap

### Immediate Priorities
1. **Additional forms**: Create testosterone, erectile dysfunction, other treatment forms
2. **Enhanced validation**: Add more sophisticated medical validation rules
3. **Better error handling**: More granular error messages and recovery
4. **Performance optimization**: Reduce form load time and improve responsiveness

### Medium-term Goals
1. **Form builder UI**: Visual interface for creating new forms without coding
2. **Advanced conditional logic**: More complex branching logic patterns
3. **Multi-language support**: Spanish and other language translations
4. **Analytics integration**: Track form completion rates and drop-off points

### Long-term Vision
1. **AI-powered form optimization**: Machine learning for form improvement
2. **Advanced medical algorithms**: More sophisticated medical screening logic
3. **Integration marketplace**: Connect with more healthcare platforms
4. **White-label customization**: Client-specific branding and customization

## 📞 Contact & Support

### Key Personnel
- **Primary Developer**: Tatyana Gomez
- **Project Manager**: [To be updated]
- **Medical Advisor**: [To be updated]

### Documentation Locations
- **Python Form Generator**: `/Users/tatyanagomez/Projects/ltGlobalWidgets/python-forms/README-Python-Form-Generator.md`
- **Quick Start Guide**: `/Users/tatyanagomez/Projects/ltGlobalWidgets/python-forms/README-Quick-Start-Guide.md`
- **Integration Guide**: `/Users/tatyanagomez/Projects/ltGlobalWidgets/python-forms/README-Integration-Guide.md`
- **Conditional Logic Reference**: `/Users/tatyanagomez/Projects/ltGlobalWidgets/python-forms/README-Conditional-Logic-Reference.md`
- **Forms Dashboard**: `/Users/tatyanagomez/Projects/ltGlobalWidgets/docs/widgets/README-Forms-Dashboard.md`
- **CSS Framework**: `/Users/tatyanagomez/Projects/ltGlobalWidgets/docs/brand/README-CSS-Framework.md`
- **Patient Screening API**: `/Users/tatyanagomez/Projects/ltGlobalWidgets/docs/api/README-Patient-Screening-API.md`

### Repository Information
- **Location**: Local development at `/Users/tatyanagomez/Projects/ltGlobalWidgets/`
- **Version Control**: [To be set up if needed]
- **Backup Strategy**: [To be implemented]

## 📅 Project Timeline & Milestones

### Development History
- **Initial Development**: Multi-day intensive development session
- **Core Features**: Form generation, conditional logic, BMI calculation
- **API Integration**: Webhook integration with n8n
- **UI Polish**: Modern styling, phone validation, error handling
- **Current Status**: Production-ready GLP1 form complete

### Recent Achievements (Latest Session)
- ✅ Fixed phone number validation with auto-formatting
- ✅ Updated disqualification message styling to modern design
- ✅ Fixed tobacco follow-up question conditional logic
- ✅ Corrected API data structure (rxRequested, screener showing "GLP1")
- ✅ Added full address to contact section in API data
- ✅ Restructured answers to use question text as keys, removed contact duplication
- ✅ Updated comprehensive documentation
- ✅ Created Forms Dashboard with embed code library
- ✅ Built compact table layout for hundreds of forms
- ✅ Added category toggle system and search functionality
- ✅ Implemented one-click embed code copying for client deployment

## 🔍 Code Quality & Standards

### Coding Standards
- **Python**: PEP 8 compliance for Python code
- **JavaScript**: ES6+ standards, proper error handling
- **HTML/CSS**: Semantic HTML, mobile-first responsive design
- **Documentation**: Comprehensive inline comments and external docs

### Testing Standards
- **Manual testing**: Complete functional testing checklist
- **Browser testing**: Chrome, Firefox, Safari, Edge compatibility
- **Mobile testing**: iOS Safari, Android Chrome testing
- **Integration testing**: End-to-end webhook testing

### Maintenance Standards
- **Regular updates**: Keep medical questions current with regulations
- **Performance monitoring**: Track form load times and completion rates
- **Security reviews**: Regular security assessment of data handling
- **Documentation updates**: Keep all documentation current with code changes

## 🆘 Support & Contact

### Getting Help
- **Technical Issues**: Check the troubleshooting section above
- **Form Generation**: See `python-forms/README.md` for detailed instructions
- **API Integration**: See `docs/api/api-screeners.md` for API documentation
- **Widget Management**: See `docs/widgets/README_widget.md` for dashboard usage

### Key Personnel
- **Primary Developer**: Tatyana Gomez
- **Project Manager**: [To be updated]
- **Medical Advisor**: [To be updated]

### Documentation Locations
- **Main Documentation**: This README.md file
- **Technical Details**: `python-forms/README.md`
- **API Reference**: `docs/api/api-screeners.md`
- **Widget Dashboard**: `docs/widgets/README_widget.md`
- **Conditional Logic**: `python-forms/SHOW_CONDITION_PATTERNS.md`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is part of the LocumTele GHL widget system for white-label healthcare businesses.

## 🔄 Version History

- **v1.0.0** (January 21, 2025) - Production-ready GLP1 medical form system
- **v0.9.0** - Complete form generation with conditional logic
- **v0.8.0** - BMI calculation and disqualification logic
- **v0.7.0** - API integration with n8n webhooks

---

**Document Status**: ✅ Complete and Current  
**Next Review Date**: [To be scheduled]  
**Version**: 1.0 (January 21, 2025)

This document serves as the definitive reference for the LocumTele Medical Form System project. It should be updated whenever significant changes are made to the system architecture, features, or configuration.

**Built with ❤️ for healthcare providers**