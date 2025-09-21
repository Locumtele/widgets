# Widget Dashboard Documentation

## Overview
The Widget Dashboard ecosystem consists of multiple specialized dashboards for different aspects of LocumTele's widget system:

- **`widget-dashboard.html`** - Internal widget management and N8n webhook integrations
- **`forms-dashboard.html`** - Forms management, question logic, and embed code library
- **`api-dashboard.html`** - API integration and documentation

This document covers the **Forms Dashboard** (`forms-dashboard.html`), which provides a comprehensive interface for medical form management and client deployment.

## Features

### 📊 Dashboard Tab - Embed Code Library
- **Compact Table Layout**: Space-efficient design for hundreds of forms
- **Category Toggle Buttons**: Filter by All, Weightloss, Hormone, Anti-Aging
- **Search Functionality**: Real-time search across form names
- **One-Click Copy**: Copy embed codes with single click
- **Preview Buttons**: Test live surveys in new tab
- **Bulk Operations**: Copy all codes, generate deployment reports

### 📝 Forms Tab - Form Management
- **Form Overview**: Display all forms with question counts and categories
- **Question Logic Visualization**: Color-coded safe/flag/disqualify options
- **Survey Preview**: Modal iframe preview of live surveys
- **Recent Submissions**: Track form completion data
- **Form Details**: View comprehensive form information

### 🎛️ Control Panel Tab - Automation
- **Safe Automation Controls**: Separated from main workflow
- **Automatic Form Discovery**: Scans surveys directory for new JSON files
- **Real-time Status Checking**: Automatically detects HTML file existence
- **HTML File Status**: Track which forms have generated HTML files
- **Embed Code Status**: Monitor embed code generation progress
- **Batch Operations**: Generate all HTML, all embed codes
- **System Status**: Comprehensive status reporting

## Technical Architecture

### Data Sources
- **Automatic Directory Scanning**: Scans `surveys/weightloss/`, `surveys/hormone/`, `surveys/antiaging/` for JSON files
- **Real-time Status Checking**: Automatically detects HTML file existence
- **Generated HTML**: Live survey files for preview and embedding
- **Form Metadata**: Question counts, categories, and status information

### Data Storage
- **Local Storage**: Forms data cached for performance
- **Dynamic Loading**: Data loaded on-demand for efficiency
- **State Management**: Preserves data across tab switches

### Navigation System
- **Tab-based Interface**: Dashboard, Forms, Analytics, Control Panel tabs
- **Dynamic Content**: Content loads based on active tab
- **Modal System**: Overlay dialogs for detailed views

## File Structure

```
forms-dashboard.html
├── Dashboard Tab (Embed Code Library)
│   ├── Compact Table Layout
│   ├── Category Toggle System
│   ├── Search Functionality
│   ├── One-Click Copy System
│   └── Bulk Operations
├── Forms Tab (Form Management)
│   ├── Form Overview Table
│   ├── Question Logic Visualization
│   ├── Survey Preview Modal
│   └── Recent Submissions
├── Control Panel Tab (Automation)
│   ├── Status Tracking
│   ├── HTML File Management
│   ├── Embed Code Generation
│   └── Batch Operations
└── JavaScript Functions
    ├── Navigation Functions
    ├── Data Loading Functions
    ├── Embed Code Functions
    ├── Modal Functions
    └── UI Rendering Functions
```

## Usage Instructions

### 1. Accessing the Forms Dashboard
- Open `forms-dashboard.html` in a web browser
- Ensure you're running a local server (e.g., `python3 -m http.server 8000`)
- Navigate to `http://localhost:8000/forms-dashboard.html`

### 2. Using the Embed Code Library (Dashboard Tab)
1. **Search/Filter**: Use search bar and category toggles to find forms
2. **Copy Embed Code**: Click "📋 Copy" button for desired form
3. **Preview Survey**: Click "👁️" to test live survey
4. **Bulk Operations**: Use "Copy All Codes" or "Deployment Report" buttons

### 3. Managing Forms (Forms Tab)
1. **View Form Details**: Click "View Questions" to see question logic
2. **Preview Survey**: Click "View Survey" to test live form
3. **Track Submissions**: Monitor recent form completions
4. **Analyze Logic**: Review safe/flag/disqualify answer patterns

### 4. Automation Controls (Control Panel Tab)
1. **Check Status**: View HTML file and embed code status
2. **Generate HTML**: Click "Create HTML" for missing files
3. **Generate Embeds**: Create embed codes for ready forms
4. **Bulk Operations**: Use batch operations for efficiency

## Data Flow

### Forms Data Flow
1. **User Action**: Click "Refresh All Forms"
2. **Webhook Call**: Fetch from `notion-forms` endpoint
3. **Data Processing**: Parse and structure form data
4. **Storage**: Save to localStorage and global variables
5. **Display**: Render in forms table
6. **Persistence**: Data available on page reload

### Questions Data Flow
1. **User Action**: Click individual form button
2. **Form ID**: Send specific form ID to webhook
3. **Webhook Call**: Fetch questions for that form
4. **Data Processing**: Parse and structure questions data
5. **Storage**: Save to localStorage and global variables
6. **Display**: Render in questions view

## Configuration

### Webhook URLs
```javascript
const CONFIG = {
    formsWebhookUrl: 'https://locumtele.app.n8n.cloud/webhook/notion-forms',
    questionsWebhookUrl: 'https://locumtele.app.n8n.cloud/webhook/notion-questions',
    headers: {
        'Content-Type': 'application/json'
    }
};
```

### Data Structure
- **Forms**: Array of form objects with properties like `id`, `name`, `category`, etc.
- **Questions**: Structured data based on form ID (format depends on N8n webhook response)

## Development Notes

### TODO Items
- [ ] Implement form ID parameter in questions webhook
- [ ] Customize questions data display format
- [ ] Add error handling for individual form buttons
- [ ] Implement data validation and sanitization

### Dependencies
- **No External Libraries**: Pure HTML, CSS, JavaScript
- **Local Server Required**: For CORS compliance
- **Modern Browser**: ES6+ features used

### Browser Compatibility
- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## Troubleshooting

### Common Issues
1. **CORS Errors**: Ensure running local server
2. **Data Not Loading**: Check webhook endpoints and network
3. **Buttons Not Working**: Verify JavaScript console for errors
4. **Data Not Persisting**: Check localStorage availability

### Debug Information
- **Console Logs**: Detailed logging for webhook calls
- **Raw Data Display**: JSON data shown for debugging
- **Error Messages**: User-friendly error displays

## Security Considerations

- **No Authentication**: Currently open access
- **Webhook Security**: Ensure N8n webhooks are properly secured
- **Data Privacy**: Forms data may contain sensitive information
- **Local Storage**: Data stored in browser's localStorage

## Future Enhancements

- **User Authentication**: Add login system
- **Role-based Access**: Different permissions for different users
- **Data Export**: Export forms and questions data
- **Advanced Filtering**: Filter forms by category, status, etc.
- **Bulk Operations**: Select multiple forms for batch operations
- **Real-time Updates**: WebSocket integration for live data
- **Mobile Responsiveness**: Optimize for mobile devices

## Support

For technical support or questions about the Internal Dashboard:
- Check browser console for error messages
- Verify webhook endpoints are accessible
- Ensure local server is running
- Review this documentation for usage instructions

---

**Last Updated**: January 2025  
**Version**: 1.0  
**Maintainer**: LocumTele Development Team
