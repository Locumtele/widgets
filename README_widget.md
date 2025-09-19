# Internal Dashboard Widget Documentation

## Overview
The Internal Dashboard is a comprehensive management system for LocumTele's Notion forms and questions data. It provides a centralized interface for viewing, managing, and refreshing form data through N8n webhook integrations.

## Features

### 📋 Forms Management
- **Forms Tab**: Displays all forms from Notion database
- **Real-time Data**: Fetches latest form information via N8n webhook
- **Data Persistence**: Forms data cached in localStorage
- **Table View**: Clean, organized display of form information

#### Forms Table Columns
- **Name**: Form title/name
- **Form Type**: Type of form (e.g., screener)
- **Category**: Form category (e.g., Weightloss, Hormone, AntiAging)
- **Consult Type**: Consultation type (e.g., async)
- **Status**: Form status (e.g., published)
- **Questions**: Number of questions in the form

### ❓ Questions Management
- **Questions Tab**: Individual form question management
- **Per-Form Buttons**: Each form has its own "Refresh Questions" button
- **Form ID Integration**: Buttons send specific form IDs to N8n webhook
- **Data Display**: Shows questions data in organized format

### ⚙️ Admin Controls
- **Refresh All Forms**: Updates all forms data from Notion
- **Refresh All Questions**: Updates all questions data from Notion
- **System Status**: Real-time counts and sync information
- **Webhook Configuration**: Displays current webhook endpoints

## Technical Architecture

### Webhook Endpoints
- **Forms Webhook**: `https://locumtele.app.n8n.cloud/webhook/notion-forms`
- **Questions Webhook**: `https://locumtele.app.n8n.cloud/webhook/notion-questions`

### Data Storage
- **Local Storage**: Forms and questions data persisted locally
- **Cache Management**: Automatic data restoration on page reload
- **Sync Tracking**: Last sync timestamps stored and displayed

### Navigation System
- **Tab-based Interface**: Forms, Questions, Admin tabs
- **Dynamic Content**: Content loads based on active tab
- **State Management**: Preserves data across tab switches

## File Structure

```
internal-dashboard.html
├── Forms Section
│   ├── Forms Table Display
│   ├── Data Loading Logic
│   └── Webhook Integration
├── Questions Section
│   ├── Individual Form Buttons
│   ├── Questions Data Display
│   └── Form ID Management
├── Admin Section
│   ├── Refresh Controls
│   ├── System Status
│   └── Webhook Configuration
└── JavaScript Functions
    ├── Navigation Functions
    ├── Data Loading Functions
    ├── Webhook Functions
    └── UI Rendering Functions
```

## Usage Instructions

### 1. Accessing the Dashboard
- Open `internal-dashboard.html` in a web browser
- Ensure you're running a local server (e.g., `python3 -m http.server 8000`)
- Navigate to `http://localhost:8000/internal-dashboard.html`

### 2. Loading Forms Data
1. Go to **Forms** tab
2. Click **"Refresh All Forms"** in Admin tab
3. Forms will load and display in organized table
4. Data persists across page reloads

### 3. Managing Questions
1. Go to **Questions** tab
2. Individual form buttons will appear for each loaded form
3. Click **"❓ Refresh Questions"** for specific forms
4. Questions data will load and display

### 4. Admin Functions
1. Go to **Admin** tab
2. Use **"Refresh All Forms"** to update all forms
3. Use **"Refresh All Questions"** to update all questions
4. Monitor system status and sync information

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
