# LocumTele Widgets V2 - Internal Dashboard

A comprehensive internal dashboard for managing LocumTele's widget ecosystem, with a focus on Notion-based form management and N8n webhook integration.

## 🆕 What's New in V2

### **Internal Dashboard System**
- **🗄️ Forms Database** - Complete management interface for Notion forms
- **🔗 N8n Integration** - Real-time webhook data synchronization
- **📊 Table View** - Organized display of form data with actions
- **🎨 Branded Interface** - Professional LocumTele styling

## 📁 Project Structure

```
ltGlobalWidgets/
├── internal-dashboard.html      # Main internal dashboard (NEW)
├── dashboard-integrations.html  # Original integration dashboard
├── pages/
│   ├── integrations/            # Original integration pages
│   └── widgets/                 # Widget storage (NEW)
├── forms/                       # Dynamic form system
│   ├── components/
│   │   ├── formLoader.js
│   │   ├── globalForm.js
│   │   ├── qTemplate.html
│   │   └── formStyle.css
│   ├── screeners/              # JSON configuration files
│   └── documentation/
├── calendars/                   # Calendar widgets
├── funnel/                     # Funnel pages
└── documentation/              # Brand assets and docs
```

## 🔧 New Features

### **1. Internal Dashboard (`internal-dashboard.html`)**

#### **🗄️ Database Management**
- **Single-page interface** focused on form database management
- **N8n webhook integration** for live Notion data sync
- **Table view** with comprehensive form information:
  - Form Name
  - Form ID (truncated)
  - Sections (Patient Profile, Assessment, etc.)
  - Total Question Count
  - Status indicators
  - Action buttons (View/Edit)

#### **🔄 Data Synchronization**
- **One-click refresh** via "🔄 Refresh Data" button
- **Webhook endpoint**: `https://locumtele.app.n8n.cloud/webhook/notion-questions`
- **Real-time parsing** of complex Notion data structure
- **Raw JSON display** for debugging and verification

#### **📱 Professional Interface**
- **LocumTele branding** with logo and color scheme
- **Mobile responsive** design with collapsible sidebar
- **Clean table layout** with proper spacing and borders
- **Loading states** and error handling

### **2. Data Structure Handling**

#### **Notion Form Schema Support**
```javascript
// Handles complex nested structure:
{
  "formId": "27382abf-7eae-80f3-b3ab-c6b2468f6646",
  "formName": "NAD+",
  "Patient Profile": [
    {
      "name": "Full Name",
      "questionType": "text",
      "required": true,
      // ... more question data
    }
  ],
  "Assessment": [...],
  "Medical History": [...],
  "Verification": [...]
}
```

#### **Smart Data Processing**
- **Object-to-array conversion** for table rendering
- **Section counting** across all form sections
- **Question totaling** for comprehensive metrics
- **Data caching** for cross-page consistency

### **3. Technical Architecture**

#### **Webhook Integration**
- **Single trigger point** - only database refresh calls webhook
- **Error handling** with user-friendly messages
- **Response validation** and data structure parsing
- **Global data storage** for reuse across components

#### **Modular JavaScript**
- **Self-contained** - all functionality in single HTML file
- **Clean separation** of concerns within script blocks
- **Extensible design** for future enhancements
- **Debugging tools** built-in for development

## 🚀 Getting Started

### **1. Access the Internal Dashboard**
```bash
# Open in browser
open internal-dashboard.html
```

### **2. Configure N8n Webhook (Already Done)**
The dashboard is pre-configured with:
- **Webhook URL**: `https://locumtele.app.n8n.cloud/webhook/notion-questions`
- **Headers**: Standard JSON content-type
- **Method**: GET request

### **3. Load Your Data**
1. **Click** "🔄 Refresh Data" button
2. **View** forms in organized table format
3. **Inspect** raw JSON data if needed
4. **Use** View/Edit buttons for form management

## 📊 Dashboard Features

### **Form Database Table**
| Column | Description | Example |
|--------|-------------|---------|
| **Form Name** | Display name from Notion | "NAD+" |
| **Form ID** | Truncated UUID | "27382abf..." |
| **Sections** | List of form sections | "Patient Profile, Assessment" |
| **Total Questions** | Count across all sections | "15" |
| **Status** | Active/Inactive indicator | "🟢 Active" |
| **Actions** | View and Edit buttons | "👁️ View ✏️ Edit" |

### **Data Refresh Process**
1. **Button Click** → Calls N8n webhook
2. **Data Received** → Parses complex JSON structure
3. **Table Updated** → Renders organized view
4. **Cache Stored** → Saves for future use
5. **Debug Display** → Shows raw JSON data

### **Error Handling**
- **Network errors** - Clear error messages
- **Data parsing issues** - Fallback displays
- **Empty responses** - User-friendly notifications
- **Webhook timeouts** - Retry suggestions

## 🔗 Integration Points

### **N8n Workflow**
- **Trigger**: Manual button click in dashboard
- **Endpoint**: `webhook/notion-questions`
- **Response**: Complete form data structure
- **Format**: JSON with nested sections

### **Notion Database**
- **Source**: Forms stored as Notion pages
- **Structure**: Sections as arrays of question objects
- **Metadata**: Form IDs, names, and configuration
- **Sync**: Real-time via N8n automation

## 🎨 Styling & Branding

### **Brand Integration**
- **Logo**: LocumTele branding in sidebar
- **Colors**: Brand blue (`--lt-blue`) throughout
- **Typography**: Professional sans-serif fonts
- **Layout**: Clean, medical-focused design

### **CSS Files Used**
```html
<link rel="stylesheet" href="documentation/locumtele/brand/brand.css">
<link rel="stylesheet" href="documentation/locumtele/brand/sites.css">
```

## 🔧 Development Notes

### **Key JavaScript Functions**
- `refreshDatabaseData()` - Main webhook caller
- `renderDatabaseTable()` - Table generation
- `loadDatabaseFromWebhook()` - Data fetching
- `viewFormDetails()` - Form inspection (placeholder)
- `editForm()` - Form editing (placeholder)

### **Data Flow**
```
User Click → Webhook Call → JSON Response → Data Parse → Table Render → Cache Store
```

### **Future Enhancements**
- **Form editing** - Direct Notion integration
- **Question preview** - Expandable form details
- **Export functionality** - CSV/JSON downloads
- **Analytics dashboard** - Usage metrics
- **User management** - Access controls

## 📝 Original Widget System

The V2 dashboard complements the existing widget ecosystem:

### **Dynamic Forms**
- **JSON-driven** form generation
- **Multiple question types** support
- **Conditional logic** implementation
- **Mobile optimization**

### **Calendar Widgets**
- **Specialty calendars** for different medical practices
- **Appointment booking** integration
- **Customizable styling**

### **Funnel Pages**
- **Patient acquisition** optimization
- **Lead capture** forms
- **Conversion tracking**

## 🆘 Support & Documentation

### **For Internal Use**
- **Dashboard**: Use `internal-dashboard.html` for form management
- **N8n Integration**: Webhook is pre-configured and tested
- **Data Structure**: Handles complex Notion schemas automatically

### **For Client Integration**
- **API Documentation**: See `dashboard-integrations.html`
- **Widget embedding**: Use existing form system
- **Custom forms**: JSON configuration files in `/forms/screeners/`

---

**Built with ❤️ for LocumTele internal operations**

*Last Updated: September 2025*