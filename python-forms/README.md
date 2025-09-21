# 🏥 LocumTele Medical Form Generator System

A complete Python-based medical form generation system for GHL white-label healthcare businesses. Generates dynamic, responsive medical screening forms from JSON data with advanced conditional logic, BMI calculation, and comprehensive API integration.

## 🚀 Quick Start

### Installation

```bash
cd python-forms
pip install -r requirements.txt
```

### Generate a Complete Medical Form

```bash
python3 regenerate_complete_form.py
```

This will generate `GLP1_Weightloss_Screening_COMPLETE.html` - a complete medical screening form ready for testing.

## 📁 Project Structure

```
python-forms/
├── enhanced_form_generator.py       # Core medical form generation engine
├── form_data_loader.py             # JSON data loader from forms directory
├── regenerate_complete_form.py     # Form regeneration script
├── GLP1_Weightloss_Screening_COMPLETE.html  # Generated form output
├── SHOW_CONDITION_PATTERNS.md      # Conditional logic documentation
├── forms/                          # JSON data source
│   ├── general/                   # Shared sections (Patient Profile, Medical History, etc.)
│   └── screener/                  # Form-specific assessments
└── README.md                      # This file
```

## 🔧 Core Components

### 1. Enhanced Form Generator (`enhanced_form_generator.py`)

Advanced medical form generator with complete healthcare-specific functionality.

**Key Features:**
- **Multi-section forms**: Patient Profile, Medical History, Verification, Assessment
- **Conditional logic**: Dynamic question visibility (pregnancy, allergies, tobacco follow-ups)
- **BMI calculation**: Real-time BMI calculation with form-specific disqualification rules
- **Phone validation**: 10-digit validation with auto-formatting `(555) 123-4567`
- **Modern UI**: Black/white theme with professional styling
- **Local storage**: Form persistence across browser sessions
- **State selector**: Full US states dropdown with sync-only state detection
- **File uploads**: Government ID and photo uploads with validation
- **Disqualification logic**: Smart messaging for medical disqualification criteria
- **API integration**: Complete webhook data submission to n8n

**Usage:**
```python
from enhanced_form_generator import EnhancedFormGenerator
from form_data_loader import FormDataLoader

# Load form data from JSON files
loader = FormDataLoader()
form_data = loader.generate_complete_form_data("Weightloss", "GLP1", "async")

# Generate complete form
generator = EnhancedFormGenerator()
html = generator.generate_notion_form(form_data)

# Save to file
with open("medical_form.html", "w") as f:
    f.write(html)
```

### 2. Form Data Loader (`form_data_loader.py`)

Intelligent JSON parser that combines general sections with form-specific assessments.

**Features:**
- **Dynamic loading**: Reads from `/forms/general/` and `/forms/screener/` directories
- **Question ordering**: Proper sorting by `property_order` field
- **Option sorting**: Places "none", "none_of_the_above", "no" options last
- **ID generation**: Creates unique question IDs from Notion data
- **Section combination**: Merges general sections with form-specific questions

**Supported Sections:**
- **Patient Profile**: Name, email, phone, DOB, gender, height/weight
- **Medical History**: Exercise, allergies, tobacco use, medications
- **Verification**: Address, ID upload
- **Assessment**: Form-specific medical questions and conditions

### 3. Conditional Logic System

Advanced conditional logic for medical forms with comprehensive patterns.

**Available Conditions:**
- `always`: Question always visible
- `if_gender_female`: Shows for female patients (pregnancy questions)
- `if_allergies_yes`: Shows when allergies are indicated
- `if_other_glp1s_yes`: Shows for patients taking other GLP-1 medications
- `if_tobacco_yes` / `if_tobacco_use_yes`: Shows tobacco follow-up questions

**Implementation:**
```javascript
// Example: Pregnancy question only for females
{
  "property_show_condition": "if_gender_female",
  "property_question_text": "Are you currently pregnant or breastfeeding?"
}
```

## 🌐 Generated Form Features

### Form Functionality
- **4 sections**: Patient Profile → Medical History → Verification → Assessment
- **30 total questions**: Comprehensive medical screening
- **Progress tracking**: Visual progress bar with section indicators
- **Navigation**: Previous/Next buttons with proper validation
- **Mobile responsive**: Works perfectly on all devices

### Medical-Specific Features
- **BMI calculation**: Automatic calculation displayed in Patient Profile
- **Disqualification logic**: Smart disqualification with clear messaging
- **Phone formatting**: Real-time formatting with 10-digit validation
- **Date validation**: Age verification for medical compliance
- **File uploads**: Secure government ID and photo upload handling

### API Integration
- **Webhook URL**: `https://locumtele.app.n8n.cloud/webhook/patient-screener`
- **Complete data structure**: Contact, patient, form, clinic information
- **Question text keys**: Answers use readable question text instead of IDs
- **Address handling**: Full address in contact section
- **State-based routing**: Automatic sync/async consultation type determination

### Data Structure Sent to API
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

## 🎯 Current Implementation Status

### ✅ Completed Features
- **Phone validation**: 10-digit validation with auto-formatting
- **BMI calculation**: Real-time calculation in Patient Profile section
- **Conditional logic**: All major medical conditional patterns
- **Modern styling**: Professional black/white theme with gradient accents
- **API integration**: Complete webhook data submission
- **Form persistence**: Local storage with intelligent cleanup
- **State selector**: Full US states with sync-only detection
- **Radio button fixes**: No pre-selection on fresh loads
- **Disqualification styling**: Modern, professional messaging
- **Tobacco follow-up**: Proper conditional logic for tobacco questions

### 📊 Form Statistics
- **Total Questions**: 30
- **Sections**: 4 (Patient Profile, Medical History, Verification, Assessment)
- **Conditional Questions**: 3 (pregnancy, allergy details, tobacco follow-up)
- **Disqualifying Questions**: 8 with smart messaging
- **File Uploads**: 2 (government ID, body photos)

### 🧪 Testing Checklist
1. ✅ Phone number formatting and validation
2. ✅ Female gender → pregnancy question appears
3. ✅ Height/weight → BMI calculates automatically
4. ✅ BMI under 25 → can proceed to see value in Assessment
5. ✅ Tobacco "yes" → follow-up question appears
6. ✅ Disqualifying answers → modern styled messages appear
7. ✅ Form submission → complete data sent to webhook
8. ✅ State selection → proper async/sync routing
9. ✅ File uploads → validation and visual feedback
10. ✅ Form persistence → remembers progress across sessions

## 🔄 Development Workflow

### Making Changes
1. **Update JSON data**: Modify files in `/forms/general/` or `/forms/screener/`
2. **Update generator**: Modify `enhanced_form_generator.py` for UI/logic changes
3. **Regenerate form**: Run `python3 regenerate_complete_form.py`
4. **Test**: Open generated HTML file in browser

### Adding New Conditional Logic
1. **Update JSON**: Add `property_show_condition` to question
2. **Update JavaScript**: Add condition to `checkQuestionVisibility()` function
3. **Document**: Update `SHOW_CONDITION_PATTERNS.md`

### Adding New Forms
1. **Create JSON**: Add new file to `/forms/screener/` directory
2. **Update loader**: Modify `form_data_loader.py` if needed
3. **Generate**: Use existing generation system

## 🚀 Deployment

### For GHL Integration
1. **Generate form**: `python3 regenerate_complete_form.py`
2. **Extract HTML**: Copy content from generated `.html` file
3. **Embed in GHL**: Use as custom HTML widget
4. **Test webhook**: Verify data reaches n8n endpoint

### Local Development
```bash
# Generate and test form
python3 regenerate_complete_form.py
open GLP1_Weightloss_Screening_COMPLETE.html

# Monitor changes
# Edit files → regenerate → test → repeat
```

## 📝 Documentation Files

- **`SHOW_CONDITION_PATTERNS.md`**: Complete conditional logic documentation
- **`README.md`**: This comprehensive guide
- **Form generator comments**: Inline documentation in code
- **JSON examples**: Sample data structures in `/forms/` directory

## 🔧 Configuration

### Key Settings
- **Webhook URL**: `https://locumtele.app.n8n.cloud/webhook/patient-screener`
- **Sync-only states**: Hardcoded list in form generator
- **BMI disqualification**: Only applies to GLP1 forms (< 25 BMI)
- **Local storage key**: `medicalForm_{form_name}_{category}`

### Customization Points
- **Styling**: CSS variables in form generator
- **Validation rules**: JavaScript validation functions
- **API structure**: Webhook data building function
- **Question types**: Form input generation methods

## 🤝 Maintenance

### Regular Tasks
- **JSON updates**: Keep form questions current with medical requirements
- **Validation updates**: Update phone/email validation as needed
- **Style updates**: Maintain modern, professional appearance
- **API monitoring**: Ensure webhook integration stays functional

### Troubleshooting
- **Radio pre-selection**: Clear localStorage if issues persist
- **Phone formatting**: Check `formatPhoneInput()` function
- **Conditional logic**: Verify question text matching in JavaScript
- **API data**: Check browser console for webhook submission errors

## 📄 License

This project is part of the LocumTele GHL widget system for white-label healthcare businesses.