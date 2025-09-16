# n8n Integration Guide

This document explains how to integrate the Global Widgets formLoader with n8n for automated form processing and patient management.

## 🎯 Overview

The formLoader generates dynamic forms that submit data to your n8n webhook endpoint. The integration enables automated patient screening, data processing, and workflow automation.

## 🔄 Integration Flow

```
User fills form → Form validates data → Submits to n8n webhook → n8n processes → Redirects user
```

## 📊 Data Structure

### Form Submission Payload

The form sends JSON data to n8n with this structure:

```json
{
  "screener": "GLP1",
  "category": "Weightloss",
  "locationId": "12345",
  "locationName": "Downtown Clinic",
  "patientData": {
    "fullName": "John Doe",
    "email": "john@example.com",
    "phone": "5551234567",
    "dateOfBirth": "1990-01-01",
    "gender": "male",
    "height": "6'0\"",
    "weight": "200",
    "state": "CA",
    "pregnancy": "no",
    "medicalConditions": ["diabetes_type2"],
    "medications": ["metformin"],
    "allergies": "none",
    "exerciseLevel": "moderate",
    "tobaccoUse": "no",
    "alcoholConsumption": "1-2_daily",
    "depressionHistory": "no"
  },
  "timestamp": "2025-01-15T10:00:00.000Z",
  "formVersion": "1.0.0"
}
```

### Available Form Categories

- **Weightloss** - GLP-1, Weight Loss forms
- **Antiaging** - NAD, Anti-aging forms  
- **Hormone** - Sermorelin, Hormone forms
- **Sexual Health** - ED, Herpes forms
- **Hair & Skin** - Acne, Hair loss forms

## 🛠️ n8n Workflow Setup

### Step 1: Create Webhook Node

1. **Create New Workflow** in n8n
2. **Add Webhook Node**
3. **Configure Settings:**
   - **HTTP Method:** POST
   - **Path:** `/webhook/patient-screener`
   - **Response Mode:** Respond to Webhook
   - **Response Code:** 302 (for redirects)

### Step 2: Data Processing Nodes

#### A. Data Validation Node
```javascript
// Validate required fields
const requiredFields = ['fullName', 'email', 'phone', 'dateOfBirth'];
const missingFields = requiredFields.filter(field => !$json.patientData[field]);

if (missingFields.length > 0) {
  throw new Error(`Missing required fields: ${missingFields.join(', ')}`);
}

return $json;
```

#### B. Data Transformation Node
```javascript
// Transform data for your CRM/database
const transformedData = {
  patient_id: `PAT_${Date.now()}`,
  screener_type: $json.screener,
  category: $json.category,
  location_id: $json.locationId,
  location_name: $json.locationName,
  patient_info: {
    name: $json.patientData.fullName,
    email: $json.patientData.email,
    phone: $json.patientData.phone,
    dob: $json.patientData.dateOfBirth,
    gender: $json.patientData.gender,
    bmi: calculateBMI($json.patientData.height, $json.patientData.weight),
    state: $json.patientData.state
  },
  medical_history: {
    conditions: $json.patientData.medicalConditions || [],
    medications: $json.patientData.medications || [],
    allergies: $json.patientData.allergies,
    pregnancy: $json.patientData.pregnancy,
    tobacco: $json.patientData.tobaccoUse,
    alcohol: $json.patientData.alcoholConsumption,
    exercise: $json.patientData.exerciseLevel,
    depression: $json.patientData.depressionHistory
  },
  submission_time: $json.timestamp,
  form_version: $json.formVersion
};

function calculateBMI(height, weight) {
  // Convert height to inches and calculate BMI
  const heightInches = parseHeight(height);
  const weightLbs = parseFloat(weight);
  const bmi = (weightLbs / (heightInches * heightInches)) * 703;
  return Math.round(bmi * 10) / 10;
}

function parseHeight(heightStr) {
  // Parse "6'0\"" format to inches
  const match = heightStr.match(/(\d+)'(\d+)"/);
  if (match) {
    return parseInt(match[1]) * 12 + parseInt(match[2]);
  }
  return 70; // Default height
}

return transformedData;
```

### Step 3: Database Storage

#### A. Airtable Integration
```javascript
// Airtable node configuration
{
  "operation": "create",
  "baseId": "your_base_id",
  "tableId": "your_table_id",
  "fields": {
    "Patient ID": $json.patient_id,
    "Screener Type": $json.screener_type,
    "Category": $json.category,
    "Name": $json.patient_info.name,
    "Email": $json.patient_info.email,
    "Phone": $json.patient_info.phone,
    "DOB": $json.patient_info.dob,
    "Gender": $json.patient_info.gender,
    "BMI": $json.patient_info.bmi,
    "State": $json.patient_info.state,
    "Medical Conditions": $json.medical_history.conditions.join(', '),
    "Medications": $json.medical_history.medications.join(', '),
    "Allergies": $json.medical_history.allergies,
    "Submission Time": $json.submission_time
  }
}
```

#### B. Google Sheets Integration
```javascript
// Google Sheets node configuration
{
  "operation": "append",
  "spreadsheetId": "your_spreadsheet_id",
  "range": "Sheet1!A:Z",
  "values": [
    [
      $json.patient_id,
      $json.screener_type,
      $json.category,
      $json.patient_info.name,
      $json.patient_info.email,
      $json.patient_info.phone,
      $json.patient_info.dob,
      $json.patient_info.gender,
      $json.patient_info.bmi,
      $json.patient_info.state,
      $json.medical_history.conditions.join(', '),
      $json.medical_history.medications.join(', '),
      $json.medical_history.allergies,
      $json.submission_time
    ]
  ]
}
```

### Step 4: Notification System

#### A. Email Notifications
```javascript
// Email node configuration
{
  "to": "admin@yourdomain.com",
  "subject": `New ${$json.category} Screening - ${$json.patient_info.name}`,
  "html": `
    <h2>New Patient Screening</h2>
    <p><strong>Patient:</strong> ${$json.patient_info.name}</p>
    <p><strong>Email:</strong> ${$json.patient_info.email}</p>
    <p><strong>Phone:</strong> ${$json.patient_info.phone}</p>
    <p><strong>Screener:</strong> ${$json.screener_type}</p>
    <p><strong>Category:</strong> ${$json.category}</p>
    <p><strong>BMI:</strong> ${$json.patient_info.bmi}</p>
    <p><strong>Medical Conditions:</strong> ${$json.medical_history.conditions.join(', ')}</p>
    <p><strong>Submission Time:</strong> ${$json.submission_time}</p>
  `
}
```

#### B. Slack Notifications
```javascript
// Slack node configuration
{
  "channel": "#patient-screening",
  "text": `New ${$json.category} screening from ${$json.patient_info.name}`,
  "blocks": [
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": `*New Patient Screening*\n*Patient:* ${$json.patient_info.name}\n*Email:* ${$json.patient_info.email}\n*Phone:* ${$json.patient_info.phone}\n*Screener:* ${$json.screener_type}\n*Category:* ${$json.category}\n*BMI:* ${$json.patient_info.bmi}`
      }
    }
  ]
}
```

### Step 5: Redirect Logic

#### A. Category-Based Redirects
```javascript
// Redirect node configuration
const category = $json.category;
const locationId = $json.locationId;
const locationName = $json.locationName;

const redirectUrls = {
  'Weightloss': `https://yourdomain.com/weightloss-consult?locationId=${locationId}&locationName=${encodeURIComponent(locationName)}`,
  'Antiaging': `https://yourdomain.com/antiaging-consult?locationId=${locationId}&locationName=${encodeURIComponent(locationName)}`,
  'Hormone': `https://yourdomain.com/hormone-consult?locationId=${locationId}&locationName=${encodeURIComponent(locationName)}`,
  'Sexual Health': `https://yourdomain.com/sexualhealth-consult?locationId=${locationId}&locationName=${encodeURIComponent(locationName)}`,
  'Hair & Skin': `https://yourdomain.com/hairskin-consult?locationId=${locationId}&locationName=${encodeURIComponent(locationName)}`
};

const redirectUrl = redirectUrls[category] || 'https://yourdomain.com/thank-you';

return {
  statusCode: 302,
  headers: {
    'Location': redirectUrl
  }
};
```

#### B. Conditional Redirects
```javascript
// Advanced redirect logic based on patient data
const bmi = $json.patient_info.bmi;
const conditions = $json.medical_history.conditions;
const category = $json.category;

let redirectUrl = 'https://yourdomain.com/thank-you';

// Weight loss specific logic
if (category === 'Weightloss') {
  if (bmi >= 30) {
    redirectUrl = `https://yourdomain.com/weightloss-consult?tier=premium&locationId=${$json.locationId}`;
  } else if (bmi >= 25) {
    redirectUrl = `https://yourdomain.com/weightloss-consult?tier=standard&locationId=${$json.locationId}`;
  } else {
    redirectUrl = `https://yourdomain.com/weightloss-consult?tier=basic&locationId=${$json.locationId}`;
  }
}

// Hormone specific logic
if (category === 'Hormone') {
  if (conditions.includes('cancer')) {
    redirectUrl = `https://yourdomain.com/hormone-consult?status=ineligible&locationId=${$json.locationId}`;
  } else {
    redirectUrl = `https://yourdomain.com/hormone-consult?status=eligible&locationId=${$json.locationId}`;
  }
}

return {
  statusCode: 302,
  headers: {
    'Location': redirectUrl
  }
};
```

## 🧪 Testing & Debugging

### 1. Test Form Submission
```bash
# Test the webhook directly
curl -X POST https://locumtele.app.n8n.cloud/webhook/patient-screener \
  -H "Content-Type: application/json" \
  -d '{
    "screener": "GLP1",
    "category": "Weightloss",
    "locationId": "12345",
    "locationName": "Test Clinic",
    "patientData": {
      "fullName": "Test Patient",
      "email": "test@example.com",
      "phone": "5551234567",
      "dateOfBirth": "1990-01-01",
      "gender": "male",
      "height": "6'\''0\"",
      "weight": "200",
      "state": "CA"
    },
    "timestamp": "2025-01-15T10:00:00.000Z"
  }'
```

### 2. Check n8n Execution Logs
- Monitor webhook node executions
- Verify data structure matches expectations
- Test redirect functionality
- Check error handling

### 3. Common Issues & Solutions

#### CORS Errors
```javascript
// Add CORS headers in n8n webhook response
return {
  statusCode: 200,
  headers: {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type'
  }
};
```

#### Data Format Issues
- Ensure JSON structure matches n8n expectations
- Validate required fields before processing
- Handle missing or null values gracefully

#### Redirect Problems
- Test redirect URLs are accessible
- Ensure proper URL encoding
- Handle redirect failures gracefully

## 📈 Advanced Features

### 1. Real-time Validation
```javascript
// Validate patient eligibility in real-time
const age = calculateAge($json.patientData.dateOfBirth);
const bmi = calculateBMI($json.patientData.height, $json.patientData.weight);

if (age < 18) {
  return {
    statusCode: 400,
    body: { error: 'Patient must be 18 or older' }
  };
}

if ($json.category === 'Weightloss' && bmi < 25) {
  return {
    statusCode: 400,
    body: { error: 'BMI must be 25 or higher for weight loss program' }
  };
}
```

### 2. A/B Testing
```javascript
// A/B test different form versions
const formVersion = Math.random() < 0.5 ? 'A' : 'B';
const redirectUrl = `https://yourdomain.com/consult?version=${formVersion}&locationId=${$json.locationId}`;

return {
  statusCode: 302,
  headers: { 'Location': redirectUrl }
};
```

### 3. Multi-step Workflows
```javascript
// Trigger follow-up workflows
const followUpWorkflows = {
  'Weightloss': 'weightloss-followup-workflow',
  'Antiaging': 'antiaging-followup-workflow',
  'Hormone': 'hormone-followup-workflow'
};

// Trigger the appropriate follow-up workflow
const workflowId = followUpWorkflows[$json.category];
if (workflowId) {
  // Trigger follow-up workflow
  await n8n.workflows.trigger(workflowId, {
    patientId: $json.patient_id,
    category: $json.category,
    patientData: $json.patient_info
  });
}
```

## 🔒 Security Considerations

### 1. Data Validation
- Validate all incoming data
- Sanitize user inputs
- Check for malicious content

### 2. Rate Limiting
- Implement rate limiting on webhook
- Prevent spam submissions
- Monitor for abuse

### 3. Data Privacy
- Encrypt sensitive data
- Comply with HIPAA regulations
- Secure data transmission

## 📋 Checklist

- [ ] **Webhook Node** - Configured and tested
- [ ] **Data Validation** - Required fields validated
- [ ] **Data Transformation** - Data formatted for your systems
- [ ] **Database Storage** - Patient data stored securely
- [ ] **Notifications** - Email/Slack alerts configured
- [ ] **Redirects** - Category-based redirects working
- [ ] **Error Handling** - Graceful error handling implemented
- [ ] **Testing** - End-to-end testing completed
- [ ] **Monitoring** - Logs and alerts configured
- [ ] **Security** - Data validation and privacy measures in place

## 🚀 Deployment

1. **Test in n8n** - Run through the complete workflow
2. **Deploy to production** - Activate the workflow
3. **Monitor performance** - Check execution logs and metrics
4. **Optimize as needed** - Improve based on real usage data

---

**Need Help?** Check the n8n documentation or create an issue in the repository for support.
