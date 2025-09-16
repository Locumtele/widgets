# Patient Screening API Documentation

## Overview

This API allows clinics to submit patient screening data from their own custom forms to our centralized processing system. The API accepts data from any screening category and processes it through a standardized webhook endpoint.

## 🎯 Use Cases

- **Custom Form Integration**: Submit data from your own patient screening forms
- **Third-party Form Builders**: Integrate with Typeform, Gravity Forms, etc.
- **Mobile Apps**: Submit screening data from custom mobile applications
- **Existing Systems**: Connect your current patient management system

## 🚀 Quick Integration Examples

### HTML/JavaScript Form
```html
<form id="patient-form">
    <input type="text" name="fullName" placeholder="Full Name" required>
    <input type="email" name="email" placeholder="Email" required>
    <input type="tel" name="phone" placeholder="Phone" required>
    <input type="date" name="dateOfBirth" required>
    <select name="gender" required>
        <option value="">Select Gender</option>
        <option value="male">Male</option>
        <option value="female">Female</option>
    </select>
    <button type="submit">Submit Screening</button>
</form>

<script>
document.getElementById('patient-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());
    
    // Add metadata
    data.timestamp = new Date().toISOString();
    data.formVersion = '1.0';
    data.screeningCategory = 'custom';
    
    try {
        const response = await fetch('https://locumtele.app.n8n.cloud/webhook/patient-screener', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            // Redirect to success page
            window.location.href = response.url;
        }
    } catch (error) {
        console.error('Submission failed:', error);
    }
});
</script>
```

### WordPress/Gravity Forms Integration
```php
// Add to your theme's functions.php
add_action('gform_after_submission', 'submit_to_patient_api', 10, 2);

function submit_to_patient_api($entry, $form) {
    $data = array(
        'patientData' => array(
            'fullName' => rgar($entry, '1'), // Field ID 1
            'email' => rgar($entry, '2'),     // Field ID 2
            'phone' => rgar($entry, '3'),     // Field ID 3
            'dateOfBirth' => rgar($entry, '4'), // Field ID 4
            'gender' => rgar($entry, '5'),    // Field ID 5
        ),
        'timestamp' => current_time('c'),
        'formVersion' => '1.0',
        'screeningCategory' => 'custom'
    );
    
    wp_remote_post('https://locumtele.app.n8n.cloud/webhook/patient-screener', array(
        'headers' => array('Content-Type' => 'application/json'),
        'body' => json_encode($data),
        'timeout' => 30
    ));
}
```

### Typeform Integration
```javascript
// Add to Typeform's webhook settings
// Webhook URL: https://locumtele.app.n8n.cloud/webhook/patient-screener
// Method: POST

// Transform Typeform data to our format
function transformTypeformData(typeformData) {
    return {
        patientData: {
            fullName: typeformData.form_response.answers.find(a => a.field.ref === 'full_name')?.text,
            email: typeformData.form_response.answers.find(a => a.field.ref === 'email')?.email,
            phone: typeformData.form_response.answers.find(a => a.field.ref === 'phone')?.phone_number,
            dateOfBirth: typeformData.form_response.answers.find(a => a.field.ref === 'dob')?.date,
            gender: typeformData.form_response.answers.find(a => a.field.ref === 'gender')?.choice?.label
        },
        timestamp: new Date().toISOString(),
        formVersion: '1.0',
        screeningCategory: 'typeform'
    };
}
```

## Base URL

```
https://locumtele.app.n8n.cloud/webhook/patient-screener
```

## Authentication

Currently, no authentication is required. Rate limiting is applied to prevent abuse.

## Endpoint

### Submit Patient Screening Data

**POST** `/webhook/patient-screener`

Submit patient screening data for any category of medical screening.

#### Request Headers

```
Content-Type: application/json
```

#### Request Body

The API accepts a structured JSON payload organized into logical sections:

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

#### Field Descriptions

##### Contact Section (Required)

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `contact.name` | string | Patient's full name | "John Doe" |
| `contact.email` | string | Patient's email address | "john@example.com" |
| `contact.gender` | string | Patient's gender | "male", "female" |
| `contact.dateOfBirth` | string | Patient's date of birth | "1990-01-01" |
| `contact.phone` | string | Patient's phone number | "5551234567" |
| `contact.type` | string | Contact type (always "patient") | "patient" |

##### Contact Section (Optional)

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `contact.address1` | string | Patient's street address | "123 Main St" |
| `contact.city` | string | Patient's city | "Los Angeles" |
| `contact.state` | string | Patient's state | "CA" |
| `contact.postalCode` | string | Patient's ZIP code | "90210" |
| `contact.timezone` | string | Patient's timezone | "America/Los_Angeles" |

##### Patient Section (Optional)

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `patient.patientId` | string | Your internal patient ID | "PAT_12345" |
| `patient.contactId` | string | Contact ID in your system | "CONT_67890" |
| `patient.rxRequested` | string | Medication requested | "semaglutide", "sermorelin" |
| `patient.height` | string | Patient's height | "6'0\"", "72 inches" |
| `patient.weight` | string | Patient's weight | "200", "200 lbs" |
| `patient.BMI` | string | Calculated BMI | "28.5" |
| `patient.pregnancy` | string | Pregnancy status | "yes", "no" |
| `patient.conditions` | array | Medical conditions | ["diabetes_type2", "hypertension"] |
| `patient.medications` | array | Current medications | ["metformin", "lisinopril"] |
| `patient.allergies` | string | Known allergies | "none", "penicillin" |
| `patient.activityLevel` | string | Exercise level | "low", "moderate", "high" |
| `patient.tobaccoUse` | string | Tobacco use status | "yes", "no" |
| `patient.alcoholUse` | string | Alcohol consumption | "none", "1-2_daily" |
| `patient.otcConsumption` | array | Over-the-counter medications | ["vitamin_d", "multivitamin"] |
| `patient.mentalHealth` | string | Mental health history | "depression", "anxiety", "none" |

##### Form Section (Required)

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `form.formType` | string | Type of form | "screener", "reassessment" |
| `form.category` | string | Screening category | "weightloss", "hormone", "skincare", "sexual", "hair-skin", "antiaging" |
| `form.screener` | string | Specific screener name | "GLP1", "sermorelin", "acne" |
| `form.screenerData` | string | Raw question-answer data | "Height: 6'0\". Weight: 200 lbs. Medical Conditions: diabetes_type2." |
| `form.timestamp` | string | Submission timestamp | "2025-01-15T10:00:00.000Z" |
| `form.formVersion` | string | Form version | "1.0.0" |

##### Clinic Section (Required)

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `clinic.name` | string | Your clinic's name | "Downtown Medical Center" |
| `clinic.id` | string | Your clinic's unique identifier | "12345" |
| `clinic.email` | string | Clinic contact email | "info@downtownmedical.com" |
| `clinic.phone` | string | Clinic phone number | "555-123-4567" |
| `clinic.type` | string | Clinic type (always "healthcare") | "healthcare" |

#### Screener Data Format

The `form.screenerData` field should contain all the question-answer pairs from your form in a simple text format:

```
Question 1: Answer 1. Question 2: Answer 2. Question 3: Answer 3.
```

**Examples:**

**Weightloss Screener:**
```
Previous GLP-1 Experience: none. Weight Loss Goals: 30 pounds. Previous Weight Loss Attempts: yes. HbA1C Level: 6.2. Family History Diabetes: yes. Insurance Coverage: PPO. Preferred Injection Site: abdomen. Current Diet: low-carb.
```

**Hormone Screener:**
```
Previous Hormone Therapy: no. Cancer History: no. Athlete Status: no. Thyroid Issues: none. Hormone Levels Testosterone: 450. Hormone Levels Estradiol: 25. Sleep Quality: poor. Energy Levels: low. Muscle Mass Concerns: yes.
```

**Skincare Screener:**
```
Previous Acne Treatments: benzoyl_peroxide. Sun Exposure: moderate. Acne Severity: moderate. Quality of Life Impact: moderate. Skin Type: oily. Previous Retinoid Use: no. Sunscreen Usage: daily. Makeup Usage: daily. Stress Level: high.
```

## Response

### Success Response

**Status Code:** `302 Found`

**Headers:**
```
Location: https://yourdomain.com/consult?category={category}&locationId={locationId}
```

The API will redirect the user to an appropriate consultation page based on the screening category.

### Error Response

**Status Code:** `400 Bad Request`

**Response Body:**
```json
{
  "error": "string",
  "message": "string",
  "missingFields": ["string"]
}
```

#### Common Error Codes

| Status Code | Description |
|-------------|-------------|
| 400 | Bad Request - Invalid or missing required fields |
| 422 | Unprocessable Entity - Data validation failed |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error - Server processing error |

## Example Requests

### Weightloss Screening (GLP-1)

```bash
curl -X POST https://locumtele.app.n8n.cloud/webhook/patient-screener \
  -H "Content-Type: application/json" \
  -d '{
    "contact": {
      "name": "John Doe",
      "email": "john@example.com",
      "gender": "male",
      "dateOfBirth": "1990-01-01",
      "phone": "5551234567",
      "address1": "123 Main St",
      "city": "Los Angeles",
      "state": "CA",
      "postalCode": "90210",
      "timezone": "America/Los_Angeles",
      "type": "patient"
    },
    "patient": {
      "patientId": "PAT_12345",
      "contactId": "CONT_67890",
      "rxRequested": "semaglutide",
      "height": "6'\''0\"",
      "weight": "200",
      "BMI": "28.5",
      "pregnancy": "no",
      "conditions": ["diabetes_type2"],
      "medications": ["metformin"],
      "allergies": "none",
      "activityLevel": "moderate",
      "tobaccoUse": "no",
      "alcoholUse": "1-2_daily",
      "otcConsumption": ["multivitamin"],
      "mentalHealth": "none"
    },
    "form": {
      "formType": "screener",
      "category": "weightloss",
      "screener": "GLP1",
      "screenerData": "Previous GLP-1 Experience: none. Weight Loss Goals: 30 pounds. Previous Weight Loss Attempts: yes. HbA1C Level: 6.2. Family History Diabetes: yes. Insurance Coverage: PPO. Preferred Injection Site: abdomen. Current Diet: low-carb.",
      "timestamp": "2025-01-15T10:00:00.000Z",
      "formVersion": "1.0.0"
    },
    "clinic": {
      "name": "Downtown Medical Center",
      "id": "12345",
      "email": "info@downtownmedical.com",
      "phone": "555-123-4567",
      "type": "healthcare"
    }
  }'
```

### Hormone Screening (Sermorelin)

```bash
curl -X POST https://locumtele.app.n8n.cloud/webhook/patient-screener \
  -H "Content-Type: application/json" \
  -d '{
    "contact": {
      "name": "Jane Smith",
      "email": "jane@example.com",
      "gender": "female",
      "dateOfBirth": "1985-05-15",
      "phone": "5559876543",
      "address1": "456 Oak Ave",
      "city": "Austin",
      "state": "TX",
      "postalCode": "73301",
      "timezone": "America/Chicago",
      "type": "patient"
    },
    "patient": {
      "patientId": "PAT_67890",
      "contactId": "CONT_12345",
      "rxRequested": "sermorelin",
      "height": "5'\''6\"",
      "weight": "140",
      "BMI": "22.6",
      "pregnancy": "no",
      "conditions": [],
      "medications": [],
      "allergies": "none",
      "activityLevel": "high",
      "tobaccoUse": "no",
      "alcoholUse": "none",
      "otcConsumption": ["vitamin_d"],
      "mentalHealth": "none"
    },
    "form": {
      "formType": "screener",
      "category": "hormone",
      "screener": "sermorelin",
      "screenerData": "Previous Hormone Therapy: no. Cancer History: no. Athlete Status: no. Thyroid Issues: none. Hormone Levels Testosterone: 450. Hormone Levels Estradiol: 25. Sleep Quality: poor. Energy Levels: low. Muscle Mass Concerns: yes.",
      "timestamp": "2025-01-15T10:00:00.000Z",
      "formVersion": "1.0.0"
    },
    "clinic": {
      "name": "Downtown Medical Center",
      "id": "12345",
      "email": "info@downtownmedical.com",
      "phone": "555-123-4567",
      "type": "healthcare"
    }
  }'
```

### Skincare Screening (Acne)

```bash
curl -X POST https://locumtele.app.n8n.cloud/webhook/patient-screener \
  -H "Content-Type: application/json" \
  -d '{
    "contact": {
      "name": "Alex Johnson",
      "email": "alex@example.com",
      "gender": "female",
      "dateOfBirth": "1995-08-20",
      "phone": "5554567890",
      "address1": "789 Pine St",
      "city": "New York",
      "state": "NY",
      "postalCode": "10001",
      "timezone": "America/New_York",
      "type": "patient"
    },
    "patient": {
      "patientId": "PAT_11111",
      "contactId": "CONT_22222",
      "rxRequested": "tretinoin",
      "height": "5'\''4\"",
      "weight": "125",
      "BMI": "21.5",
      "pregnancy": "no",
      "conditions": [],
      "medications": ["birth_control"],
      "allergies": "none",
      "activityLevel": "moderate",
      "tobaccoUse": "no",
      "alcoholUse": "occasional",
      "otcConsumption": ["niacinamide"],
      "mentalHealth": "none"
    },
    "form": {
      "formType": "screener",
      "category": "skincare",
      "screener": "acne",
      "screenerData": "Previous Acne Treatments: benzoyl_peroxide. Sun Exposure: moderate. Acne Severity: moderate. Quality of Life Impact: moderate. Skin Type: oily. Previous Retinoid Use: no. Sunscreen Usage: daily. Makeup Usage: daily. Stress Level: high.",
      "timestamp": "2025-01-15T10:00:00.000Z",
      "formVersion": "1.0.0"
    },
    "clinic": {
      "name": "Downtown Medical Center",
      "id": "12345",
      "email": "info@downtownmedical.com",
      "phone": "555-123-4567",
      "type": "healthcare"
    }
  }'
```

## Data Processing

### What Happens After Submission

1. **Data Validation** - All required fields are validated
2. **Question Parsing** - The screenerData is parsed to extract individual question-answer pairs
3. **Category Processing** - Data is processed based on screening category
4. **Patient Record Creation** - A unique patient record is generated with parsed data
5. **Notification** - Your clinic receives notification of the new screening
6. **Redirect** - Patient is redirected to appropriate consultation page

### Data Storage

Patient data is securely stored and processed according to HIPAA compliance standards. Data is encrypted in transit and at rest.

## Rate Limits

- **Requests per minute:** 60
- **Requests per hour:** 1000
- **Requests per day:** 10000

Rate limit headers are included in responses:
```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 59
X-RateLimit-Reset: 1640995200
```

## Testing

### Test Endpoint

Use the same endpoint for testing. Test data is processed normally but marked for testing purposes.

### Validation

Before going live, test your integration with sample data to ensure:
- All required fields are included
- Data formats are correct
- Custom fields are properly structured
- Error handling works as expected

## Support

For technical support or questions about the API:

- **Email:** api-support@locumtele.com
- **Documentation:** [Link to full documentation]
- **Status Page:** [Link to API status page]

## Changelog

### Version 1.0.0 (2025-01-15)
- Initial API release
- Support for all screening categories
- Standardized webhook endpoint
- Category-specific custom fields

---

**Last Updated:** January 15, 2025
