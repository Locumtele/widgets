# 🐍 LocumTele Python Form System

A complete Python implementation of the LocumTele Universal Form System, providing form generation, state selection, and embed handling capabilities.

## 🚀 Quick Start

### Installation

```bash
cd python-forms
pip install -r requirements.txt
```

### Run the Flask App

```bash
python flask_app.py
```

Visit `http://localhost:5000` to see the demo interface.

## 📁 Project Structure

```
python-forms/
├── universal_form_generator.py  # Core form generation logic
├── state_selector.py           # State selection with API integration
├── embed_handler.py            # Three embed types handler
├── flask_app.py               # Flask web application
├── requirements.txt           # Python dependencies
└── README.md                 # This file
```

## 🔧 Core Components

### 1. Universal Form Generator (`universal_form_generator.py`)

Generates forms from any JSON data structure with automatic type detection and validation.

**Features:**
- Automatic question type detection
- Support for all question types (text, email, radio, checkbox, etc.)
- Answer logic handling (safe, flag, disqualify)
- Mobile-responsive HTML generation
- Multi-step form support

**Usage:**
```python
from universal_form_generator import UniversalFormGenerator

generator = UniversalFormGenerator()
form_data = {
    "title": "Medical Screening",
    "questions": [
        {"text": "Name", "type": "text", "required": True},
        {"text": "Email", "type": "email", "required": True}
    ]
}
html = generator.generate_form(form_data, 'form-container')
```

### 2. State Selector (`state_selector.py`)

Handles state selection with API-driven consult type determination.

**Features:**
- All 50 US states + DC support
- Sync-only state detection
- API integration with N8n webhook
- Dynamic root domain detection
- BMI calculation
- Form data mapping

**Usage:**
```python
from state_selector import StateSelector

selector = StateSelector()
redirect_url = selector.process_state_selection(
    state_code="CA",
    form_data=form_data,
    category="weightloss"
)
```

### 3. Embed Handler (`embed_handler.py`)

Manages the three different embed types for the widget system.

**Embed Types:**
1. **Form Only**: Form → `{{rootdomain}}/{{category}}-state`
2. **State + API**: State → API → `{{rootdomain}}/{{category}}-{{consultType}}-fee`
3. **Sync Calendar**: Calendar → `{{rootdomain}}/{{category}}-consult-booked`

**Usage:**
```python
from embed_handler import EmbedHandler

handler = EmbedHandler()

# Embed Type 1
result = handler.embed_type_1_form_only(form_data, "weightloss")

# Embed Type 2
result = handler.embed_type_2_state_api("CA", form_data, "weightloss")

# Embed Type 3
result = handler.embed_type_3_sync_calendar("weightloss")
```

## 🌐 Flask Web Application

The Flask app provides a complete web interface and API for the form system.

### Available Endpoints

- **`/`** - Main page with embed type selection
- **`/embed/type1`** - Form Only demo
- **`/embed/type2`** - State + API demo  
- **`/embed/type3`** - Sync Calendar demo
- **`/demo/form`** - Form generation demo
- **`/demo/state`** - State selection demo
- **`/api/info`** - API information
- **`/api/generate-form`** - Form generation API
- **`/api/process-state`** - State processing API

### API Usage

#### Generate Form
```bash
curl -X POST http://localhost:5000/api/generate-form \
  -H "Content-Type: application/json" \
  -d '{
    "form_data": {
      "title": "Test Form",
      "questions": [
        {"text": "Name", "type": "text", "required": true}
      ]
    }
  }'
```

#### Process State
```bash
curl -X POST http://localhost:5000/api/process-state \
  -H "Content-Type: application/json" \
  -d '{
    "state_code": "CA",
    "form_data": {"fullName": "John Doe", "email": "john@example.com"},
    "category": "weightloss"
  }'
```

## 🎯 Key Features

### Form Generation
- **Universal**: Works with any JSON structure
- **Smart Detection**: Automatically detects question types
- **Answer Logic**: Handles safe, flag, and disqualify answers
- **Responsive**: Mobile-first design
- **Accessible**: Proper form labels and validation

### State Selection
- **API Integration**: Calls N8n webhook for consult type
- **State Logic**: Sync-only states automatically use sync consultations
- **Data Mapping**: Handles various field name variations
- **BMI Calculation**: Automatic BMI calculation from height/weight

### Embed Types
- **Type 1**: Simple form submission with state redirect
- **Type 2**: State selection with API-driven consult type
- **Type 3**: Direct calendar booking for sync consultations

## 🔄 Integration with JavaScript System

This Python system is designed to work alongside the existing JavaScript implementation:

- **Same API endpoints**: Uses the same N8n webhook
- **Same data formats**: Compatible with existing form data structures
- **Same redirect patterns**: Follows the same URL patterns
- **Same CSS**: Uses the same styling system

## 🚀 Deployment

### Local Development
```bash
python flask_app.py
```

### Production Deployment
```bash
# Using gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 flask_app:app

# Using Docker
docker build -t python-forms .
docker run -p 5000:5000 python-forms
```

## 📊 Advantages of Python Implementation

1. **Cleaner Logic**: More readable and maintainable code
2. **Better Error Handling**: Comprehensive exception handling
3. **Type Safety**: Type hints for better development experience
4. **API Server**: Built-in web API for integration
5. **Testing**: Easier to write unit tests
6. **Scalability**: Better for server-side processing
7. **Data Processing**: More powerful data manipulation capabilities

## 🔧 Configuration

### Environment Variables
- `FLASK_ENV`: Set to 'production' for production deployment
- `WEBHOOK_URL`: Override the default N8n webhook URL
- `DEFAULT_ROOT_DOMAIN`: Set default root domain for redirects

### Customization
- Modify `universal_form_generator.py` for form generation logic
- Update `state_selector.py` for state-specific rules
- Customize `embed_handler.py` for different embed flows

## 📝 Examples

See the Flask app demos at `http://localhost:5000` for complete examples of all functionality.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is part of the LocumTele widget system.
