"""
Simple Flask API for Dashboard Form Generation
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from enhanced_form_generator import EnhancedFormGenerator
from form_data_loader import FormDataLoader
import os
import traceback

app = Flask(__name__)
CORS(app)  # Enable CORS for dashboard communication

@app.route('/generate-form', methods=['POST'])
def generate_form():
    try:
        data = request.get_json()

        # Extract form parameters
        form_name = data.get('formName', 'GLP1')
        category = data.get('category', 'Weightloss')
        consult_type = data.get('consultType', 'async')

        print(f"🔧 Generating form: {form_name} ({category})")

        # Load form data using the universal system
        loader = FormDataLoader()
        form_data = loader.generate_complete_form_data(category, form_name, consult_type)

        if not form_data["sections"]:
            return jsonify({
                'success': False,
                'error': 'No form data loaded'
            }), 400

        # Generate HTML
        generator = EnhancedFormGenerator()
        html = generator.generate_notion_form(form_data)

        # Save to appropriate location
        output_dir = f"../surveys/{category.lower()}"
        os.makedirs(output_dir, exist_ok=True)

        filename = f"{output_dir}/{form_name}-screener-live.html"

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"✅ Form generated: {filename}")

        return jsonify({
            'success': True,
            'message': f'{form_name} form generated successfully',
            'outputPath': filename,
            'formName': form_name,
            'category': category
        })

    except Exception as e:
        print(f"❌ Error generating form: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'LocumTele Form Generator API is running'
    })

if __name__ == '__main__':
    print("🚀 Starting LocumTele Form Generator API...")
    print("📍 Available at: http://localhost:5000")
    print("🔧 Endpoint: POST /generate-form")
    print("💡 Install flask-cors: pip install flask-cors")
    app.run(debug=True, port=5000, host='localhost')