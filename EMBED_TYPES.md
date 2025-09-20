# Embed Types Documentation

## Overview

Three different embed types for different use cases in the LocumTele widget system.

## 🎯 Embed Type 1: Form Only

**Purpose:** Simple form that redirects to state selection  
**Use Case:** Basic screening forms that need state selection

### Flow:
1. User fills form
2. Form submits → Stores data in `sessionStorage`
3. Redirects to `{{rootdomain}}/{{category}}-state`
4. State selector handles the rest

### Implementation:
```html
<!-- Include Universal Form System -->
<link rel="stylesheet" href="https://locumtele.github.io/widgets/forms/components/universalFormStyle.css">
<script src="https://locumtele.github.io/widgets/forms/components/universalFormLoader.js"></script>

<script>
const formData = {
    title: "Medical Screening",
    category: "weightloss", // or "antiaging", "hormone", etc.
    questions: [
        { text: "Full Name", type: "text", required: true },
        { text: "Email", type: "email", required: true },
        { text: "Phone", type: "phone", required: true }
    ]
};

await window.generateForm(formData, 'form-container');
</script>
<div id="form-container"></div>
```

### Redirect Pattern:
- `example.com/weightloss-state`
- `example.com/antiaging-state`
- `example.com/hormone-state`

---

## 🎯 Embed Type 2: State Selector with API

**Purpose:** State selector that calls API to determine consult type  
**Use Case:** When you need API-driven consult type determination

### Flow:
1. User selects state
2. Calls `https://locumtele.app.n8n.cloud/webhook/patient-screener`
3. API returns consult type (sync/async)
4. Redirects to `{{rootdomain}}/{{category}}-{{consultType}}-fee`

### Implementation:
```html
<!-- Include state selector -->
<iframe src="https://locumtele.github.io/widgets/forms/state-selector.html?category=weightloss&location_id=123&location_name=Clinic%20Name" 
        style="width:100%;height:600px;border:0;"></iframe>
```

### API Data Format:
```json
{
  "contact": {
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "5551234567",
    "state": "CA",
    "type": "patient"
  },
  "patient": {
    "rxRequested": "weightloss",
    "height": "6'0\"",
    "weight": "200",
    "BMI": "28.5"
  },
  "form": {
    "formType": "weightloss",
    "category": "weightloss",
    "timestamp": "2025-01-15T10:00:00.000Z"
  },
  "clinic": {
    "name": "Clinic Name",
    "id": "123",
    "type": "healthcare"
  }
}
```

### API Response:
```json
{
  "consultType": "async", // or "sync"
  "redirectUrl": "optional_redirect_url"
}
```

### Redirect Patterns:
- `example.com/weightloss-async-fee`
- `example.com/weightloss-sync-fee`
- `example.com/antiaging-async-fee`

---

## 🎯 Embed Type 3: Sync Calendar

**Purpose:** Calendar booking that redirects to consult booked page  
**Use Case:** Direct calendar integration for sync consultations

### Flow:
1. User books appointment
2. Redirects to `{{rootdomain}}/{{category}}-consult-booked`

### Implementation:
```html
<!-- Include calendar widget -->
<iframe src="https://locumtele.github.io/widgets/calendars/weightloss.html" 
        style="width:100%;height:800px;border:0;"></iframe>
```

### Redirect Patterns:
- `example.com/weightloss-consult-booked`
- `example.com/antiaging-consult-booked`
- `example.com/hormone-consult-booked`

---

## 🔧 Configuration

### URL Parameters for State Selector:
- `category` - Form category (weightloss, antiaging, hormone, etc.)
- `location_id` - Clinic location ID
- `location_name` - Clinic location name
- `location_email` - Clinic email (optional)
- `location_phone` - Clinic phone (optional)

### Example:
```
https://locumtele.github.io/widgets/forms/state-selector.html?category=weightloss&location_id=123&location_name=Downtown%20Clinic
```

## 📊 Data Flow Summary

### Embed 1 (Form Only):
```
Form → sessionStorage → {{rootdomain}}/{{category}}-state
```

### Embed 2 (State + API):
```
State Selection → API Call → {{rootdomain}}/{{category}}-{{consultType}}-fee
```

### Embed 3 (Calendar):
```
Calendar Booking → {{rootdomain}}/{{category}}-consult-booked
```

## 🚫 Sync-Only States

These states always redirect to sync consultations:
- AR, DC, DE, ID, KS, LA, MS, NM, RI, WV, NC, SC, ME

## 🔗 API Endpoint

**URL:** `https://locumtele.app.n8n.cloud/webhook/patient-screener`  
**Method:** POST  
**Content-Type:** application/json  
**Response:** JSON with consultType and optional redirectUrl
