"""
Flask Web Application - Python Form System

A Flask web application that provides the Python form system as a web service.
Handles form generation, state selection, and embed types.

Usage:
    python flask_app.py
"""

from flask import Flask, request, jsonify, render_template_string
import json
from universal_form_generator import UniversalFormGenerator
from state_selector import StateSelector
from embed_handler import EmbedHandler

app = Flask(__name__)

# Initialize handlers
form_generator = UniversalFormGenerator()
state_selector = StateSelector()
embed_handler = EmbedHandler()


@app.route('/')
def index():
    """Main page with embed type selection"""
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>LocumTele Python Form System</title>
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
            h1 { text-align: center; color: #333; margin-bottom: 30px; }
            .embed-types { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-bottom: 30px; }
            .embed-card { background: #f8f9fa; padding: 20px; border-radius: 8px; border: 2px solid #e9ecef; }
            .embed-card h3 { margin-top: 0; color: #007cba; }
            .btn { background: #007cba; color: white; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer; text-decoration: none; display: inline-block; }
            .btn:hover { background: #005a87; }
            .demo-section { margin-top: 30px; padding: 20px; background: #f0f8ff; border-radius: 8px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🏥 LocumTele Python Form System</h1>
            
            <div class="embed-types">
                <div class="embed-card">
                    <h3>📝 Embed Type 1: Form Only</h3>
                    <p>Simple screening forms that redirect to state selection</p>
                    <p><strong>Flow:</strong> Form → {{rootdomain}}/{{category}}-state</p>
                    <a href="/embed/type1" class="btn">Try Form Only</a>
                </div>
                
                <div class="embed-card">
                    <h3>🗺️ Embed Type 2: State + API</h3>
                    <p>State selection with API-driven consult type determination</p>
                    <p><strong>Flow:</strong> State → API → {{rootdomain}}/{{category}}-{{consultType}}-fee</p>
                    <a href="/embed/type2" class="btn">Try State + API</a>
                </div>
                
                <div class="embed-card">
                    <h3>📅 Embed Type 3: Sync Calendar</h3>
                    <p>Direct calendar booking for sync consultations</p>
                    <p><strong>Flow:</strong> Calendar → {{rootdomain}}/{{category}}-consult-booked</p>
                    <a href="/embed/type3" class="btn">Try Sync Calendar</a>
                </div>
            </div>
            
            <div class="demo-section">
                <h2>🚀 Quick Demo</h2>
                <p>Test the form system with sample data:</p>
                <a href="/demo/form" class="btn">Generate Sample Form</a>
                <a href="/demo/state" class="btn">Test State Selection</a>
                <a href="/api/info" class="btn">API Information</a>
            </div>
        </div>
    </body>
    </html>
    ''')


@app.route('/embed/type1')
def embed_type_1():
    """Embed Type 1: Form Only"""
    form_data = {
        "title": "Medical Screening Form",
        "category": "weightloss",
        "questions": [
            {"text": "Full Name", "type": "text", "required": True},
            {"text": "Email Address", "type": "email", "required": True},
            {"text": "Phone Number", "type": "phone", "required": True},
            {"text": "Date of Birth", "type": "date", "required": True},
            {"text": "Gender", "type": "radio", "options": ["Male", "Female", "Other"], "required": True},
            {"text": "Do you have diabetes?", "type": "radio", "options": ["No", "Type 1", "Type 2"], 
             "safeAnswers": ["No"], "disqualifyAnswers": ["Type 1", "Type 2"]},
            {"text": "Height", "type": "height", "required": True},
            {"text": "Weight", "type": "weight", "required": True}
        ]
    }
    
    result = embed_handler.embed_type_1_form_only(form_data, "weightloss")
    
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Embed Type 1: Form Only</title>
        <link rel="stylesheet" href="https://locumtele.github.io/widgets/python-forms/components/universalFormStyle.css">
    </head>
    <body>
        <div style="max-width: 800px; margin: 0 auto; padding: 20px;">
            <h1>📝 Embed Type 1: Form Only</h1>
            <p><strong>Description:</strong> {{ description }}</p>
            <p><strong>Redirect URL:</strong> <code>{{ redirect_url }}</code></p>
            
            <div id="form-container">
                {{ form_html|safe }}
            </div>
            
            <script>
                // Form submission handler
                document.getElementById('universalForm').addEventListener('submit', function(e) {
                    e.preventDefault();
                    alert('Form submitted! In a real implementation, this would redirect to: ' + '{{ redirect_url }}');
                });
            </script>
        </div>
    </body>
    </html>
    ''', **result)


@app.route('/embed/type2')
def embed_type_2():
    """Embed Type 2: State Selector with API"""
    # Generate state selector HTML
    state_html = state_selector.generate_state_selector_html("weightloss")
    
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Embed Type 2: State + API</title>
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
            .info { background: #e3f2fd; padding: 15px; border-radius: 8px; margin-bottom: 20px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🗺️ Embed Type 2: State + API</h1>
            <div class="info">
                <p><strong>Description:</strong> State selection with API-driven consult type determination</p>
                <p><strong>Flow:</strong> State Selection → API Call → {{rootdomain}}/{{category}}-{{consultType}}-fee</p>
                <p><strong>API Endpoint:</strong> <code>https://locumtele.app.n8n.cloud/webhook/patient-screener</code></p>
            </div>
            
            {{ state_html|safe }}
            
            <script>
                // State selection handler
                document.querySelectorAll('.state-item').forEach(item => {
                    item.addEventListener('click', function() {
                        const stateCode = this.dataset.code;
                        const stateName = this.querySelector('.state-name').textContent;
                        
                        // Simulate form data
                        const formData = {
                            fullName: "John Doe",
                            email: "john@example.com",
                            phone: "5551234567"
                        };
                        
                        // In a real implementation, this would call the API
                        alert(`State selected: ${stateName} (${stateCode})\\n\\nIn a real implementation, this would:\\n1. Call the API\\n2. Get consult type\\n3. Redirect to appropriate fee page`);
                    });
                });
            </script>
        </div>
    </body>
    </html>
    ''')


@app.route('/embed/type3')
def embed_type_3():
    """Embed Type 3: Sync Calendar"""
    result = embed_handler.embed_type_3_sync_calendar("weightloss")
    
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Embed Type 3: Sync Calendar</title>
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
            .info { background: #e8f5e8; padding: 15px; border-radius: 8px; margin-bottom: 20px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📅 Embed Type 3: Sync Calendar</h1>
            <div class="info">
                <p><strong>Description:</strong> {{ description }}</p>
                <p><strong>Redirect URL:</strong> <code>{{ redirect_url }}</code></p>
            </div>
            
            {{ calendar_html|safe }}
        </div>
    </body>
    </html>
    ''', **result)


@app.route('/demo/form')
def demo_form():
    """Demo form generation"""
    form_data = {
        "title": "Demo Medical Form",
        "category": "weightloss",
        "questions": [
            {"text": "Full Name", "type": "text", "required": True},
            {"text": "Email", "type": "email", "required": True},
            {"text": "Phone", "type": "phone", "required": True},
            {"text": "Do you have diabetes?", "type": "radio", "options": ["No", "Yes"], 
             "safeAnswers": ["No"], "disqualifyAnswers": ["Yes"]}
        ]
    }
    
    html = form_generator.generate_form(form_data, 'form-container')
    
    return f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Demo Form</title>
        <link rel="stylesheet" href="https://locumtele.github.io/widgets/python-forms/components/universalFormStyle.css">
    </head>
    <body>
        <div style="max-width: 800px; margin: 0 auto; padding: 20px;">
            <h1>Demo Form Generation</h1>
            <div id="form-container">
                {html}
            </div>
        </div>
    </body>
    </html>
    '''


@app.route('/demo/state')
def demo_state():
    """Demo state selection"""
    form_data = {
        "fullName": "John Doe",
        "email": "john@example.com",
        "phone": "5551234567"
    }
    
    # Test different states
    states_to_test = ["CA", "NY", "TX", "AR"]  # AR is sync-only
    
    results = []
    for state in states_to_test:
        try:
            result = state_selector.process_state_selection(state, form_data, "weightloss")
            consult_type = state_selector.determine_consult_type(state)
            results.append({
                'state': state,
                'consult_type': consult_type,
                'redirect_url': result
            })
        except Exception as e:
            results.append({
                'state': state,
                'error': str(e)
            })
    
    return jsonify({
        'message': 'State selection demo results',
        'results': results
    })


@app.route('/api/info')
def api_info():
    """Get API information"""
    info = embed_handler.get_embed_info()
    return jsonify(info)


@app.route('/api/generate-form', methods=['POST'])
def api_generate_form():
    """API endpoint for form generation"""
    try:
        data = request.get_json()
        form_data = data.get('form_data')
        container_id = data.get('container_id', 'form-container')
        options = data.get('options', {})
        
        if not form_data:
            return jsonify({'error': 'form_data is required'}), 400
        
        html = form_generator.generate_form(form_data, container_id, options)
        
        return jsonify({
            'success': True,
            'html': html,
            'container_id': container_id
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/process-state', methods=['POST'])
def api_process_state():
    """API endpoint for state processing"""
    try:
        data = request.get_json()
        state_code = data.get('state_code')
        form_data = data.get('form_data')
        category = data.get('category', 'weightloss')
        location_id = data.get('location_id', 'default_location')
        location_name = data.get('location_name', 'Default Clinic')
        root_domain = data.get('root_domain')
        
        if not all([state_code, form_data]):
            return jsonify({'error': 'state_code and form_data are required'}), 400
        
        redirect_url = state_selector.process_state_selection(
            state_code, form_data, category, location_id, location_name, root_domain
        )
        
        consult_type = state_selector.determine_consult_type(state_code)
        
        return jsonify({
            'success': True,
            'redirect_url': redirect_url,
            'consult_type': consult_type,
            'state_code': state_code
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("🏥 Starting LocumTele Python Form System...")
    print("📝 Available endpoints:")
    print("  - / : Main page with embed type selection")
    print("  - /embed/type1 : Form Only demo")
    print("  - /embed/type2 : State + API demo")
    print("  - /embed/type3 : Sync Calendar demo")
    print("  - /demo/form : Form generation demo")
    print("  - /demo/state : State selection demo")
    print("  - /api/info : API information")
    print("  - /api/generate-form : Form generation API")
    print("  - /api/process-state : State processing API")
    print("\n🚀 Server starting on http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
