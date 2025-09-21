# 🔗 Python Form System Integration Guide

This guide shows how to integrate the Python Form System with your existing LocumTele workflow.

## 🚀 Quick Integration

### 1. Deploy Python System

```bash
# Copy Python system to your server
scp -r python-forms/ user@your-server:/path/to/locumtele/

# Install dependencies
cd /path/to/locumtele/python-forms/
pip3 install -r requirements.txt

# Run the system
python3 flask_app.py
```

### 2. Update Your Embed Codes

**Option A: Use Forms Dashboard (Recommended)**
1. Open `forms-dashboard.html`
2. Navigate to Dashboard tab (Embed Code Library)
3. Copy embed codes for your forms
4. Replace existing embeds with new codes

**Option B: Use Python API Directly**

Replace your existing JavaScript embeds with Python API calls:

#### Before (JavaScript):
```html
<script src="https://locumtele.github.io/widgets/python-forms/components/universalFormLoader.js"></script>
<script>
    const formData = { /* your form data */ };
    await window.generateForm(formData, 'form-container');
</script>
```

#### After (Python API):
```html
<div id="form-container"></div>
<script>
fetch('https://your-server.com/api/generate-form', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        form_data: { /* your form data */ },
        container_id: 'form-container'
    })
})
.then(response => response.json())
.then(data => {
    document.getElementById('form-container').innerHTML = data.html;
});
</script>
```

## 📋 API Endpoints

### Form Generation
```bash
POST /api/generate-form
Content-Type: application/json

{
    "form_data": {
        "title": "Medical Screening",
        "category": "weightloss",
        "questions": [...]
    },
    "container_id": "form-container",
    "options": {}
}
```

### State Processing
```bash
POST /api/process-state
Content-Type: application/json

{
    "state_code": "CA",
    "form_data": {...},
    "category": "weightloss",
    "location_id": "clinic_123",
    "location_name": "Downtown Clinic",
    "root_domain": "https://locumtele.com"
}
```

## 🔄 Migration Strategy

### Phase 1: Parallel Deployment
- Deploy Python system alongside JavaScript
- Test with a subset of forms
- Monitor performance and errors

### Phase 2: Gradual Migration
- Update embed codes one by one
- A/B test Python vs JavaScript
- Collect user feedback

### Phase 3: Full Migration
- Replace all JavaScript embeds
- Remove old JavaScript system
- Optimize Python system

## 🎯 Benefits of Python System

1. **Better Performance**: Server-side processing
2. **Easier Maintenance**: Cleaner, more readable code
3. **Better Testing**: Comprehensive test suite
4. **API Integration**: Built-in REST API
5. **Scalability**: Better for high traffic
6. **Error Handling**: More robust error management

## 🔧 Configuration

### Environment Variables
```bash
export FLASK_ENV=production
export WEBHOOK_URL=https://locumtele.app.n8n.cloud/webhook/patient-screener
export DEFAULT_ROOT_DOMAIN=https://locumtele.com
```

### Nginx Configuration
```nginx
location /api/ {
    proxy_pass http://localhost:5000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

## 📊 Monitoring

### Health Check
```bash
curl https://your-server.com/api/info
```

### Logs
```bash
tail -f /var/log/locumtele-python.log
```

## 🧪 Testing

### Run Tests
```bash
cd python-forms/
python3 test_system.py
```

### Integration Test
```bash
python3 integration_demo.py
```

## 🚨 Troubleshooting

### Common Issues

1. **Port 5000 in use**: Use different port
   ```bash
   python3 flask_app.py --port 5001
   ```

2. **Module not found**: Install dependencies
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Webhook errors**: Check API endpoint
   ```bash
   curl -X POST https://locumtele.app.n8n.cloud/webhook/patient-screener
   ```

## 📞 Support

- Check logs for error details
- Run integration demo for testing
- Review API documentation
- Test with sample data first

## ✅ Success Checklist

- [ ] Python system deployed
- [ ] Dependencies installed
- [ ] Tests passing
- [ ] API endpoints working
- [ ] Webhook integration tested
- [ ] Embed codes updated
- [ ] Monitoring configured
- [ ] Performance optimized
