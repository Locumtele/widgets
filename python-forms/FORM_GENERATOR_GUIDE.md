# 🏥 Form Generator - Quick Start Guide

Convert any JSON form to production-ready HTML in seconds!

## 🚀 Super Simple Usage

### Option 1: By Category & Form Name (Easiest)
```bash
cd python-forms
python3 generate_form.py --category weightloss --form-name GLP1
python3 generate_form.py --category antiaging --form-name NAD
python3 generate_form.py --category hormone --form-name Sermorelin
```

### Option 2: Interactive Mode (User-Friendly)
```bash
python3 generate_form.py --interactive
```
Then follow the prompts!

### Option 3: Direct JSON File
```bash
python3 generate_form.py --form ../surveys/weightloss/GLP1-screener.json
```

### Option 4: Generate All Forms at Once
```bash
python3 generate_form.py --batch-all
```

## 📋 What You Get

- ✅ **Complete HTML Form** - Ready to embed in GHL
- ✅ **All Sections** - Patient Profile, Medical History, Verification, Assessment
- ✅ **Conditional Logic** - Questions appear/hide based on answers
- ✅ **BMI Calculator** - Real-time calculation
- ✅ **Phone Validation** - Auto-formatting
- ✅ **File Uploads** - ID and photo uploads
- ✅ **API Integration** - Sends to n8n webhook
- ✅ **Mobile Responsive** - Works on all devices

## 📁 Output Location

Forms are saved in the same directory as the JSON:
- `surveys/weightloss/GLP1-screener-live.html`
- `surveys/antiaging/NAD-screener-live.html`
- `surveys/hormone/Sermorelin-screener-live.html`

## 🎯 Available Commands

```bash
# List all available forms
python3 generate_form.py --list-forms

# Get help
python3 generate_form.py --help

# Interactive mode (best for beginners)
python3 generate_form.py --interactive
```

## 🔧 For Dashboard Integration

Your dashboard can call:
```python
from generate_form import generate_by_category_and_name
success = generate_by_category_and_name("antiaging", "NAD", "async")
```

## ❗ Requirements

1. **JSON Structure** - Your JSON must have:
   - `property_category` field
   - Either `questions` array OR `property_sub_item` references

2. **Shared Sections** - Must exist in `surveys/all-forms/`:
   - `patient-profile.json`
   - `medical-history.json`
   - `verification.json`

3. **Python Dependencies** - Run once:
   ```bash
   pip install -r requirements.txt
   ```

## 🎉 That's It!

No complex setup, no configuration files. Just point it at your JSON and get a complete medical form!