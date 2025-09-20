"""
State Selector with API Integration - Python Version

Handles state selection with API-driven consult type determination.
Calls the screener API to determine sync vs async consultations.

Usage:
    selector = StateSelector()
    redirect_url = selector.process_state_selection(state, form_data, category)
"""

import json
import requests
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class StateInfo:
    code: str
    name: str


class StateSelector:
    def __init__(self):
        # States that require sync consultations (no async allowed)
        self.sync_only_states = [
            'AR', 'DC', 'DE', 'ID', 'KS', 'LA', 'MS', 'NM', 
            'RI', 'WV', 'NC', 'SC', 'ME'
        ]
        
        # API endpoint
        self.webhook_url = 'https://locumtele.app.n8n.cloud/webhook/patient-screener'
        
        # All US states
        self.states = [
            StateInfo('AL', 'Alabama'), StateInfo('AK', 'Alaska'), StateInfo('AZ', 'Arizona'),
            StateInfo('AR', 'Arkansas'), StateInfo('CA', 'California'), StateInfo('CO', 'Colorado'),
            StateInfo('CT', 'Connecticut'), StateInfo('DE', 'Delaware'), StateInfo('FL', 'Florida'),
            StateInfo('GA', 'Georgia'), StateInfo('HI', 'Hawaii'), StateInfo('ID', 'Idaho'),
            StateInfo('IL', 'Illinois'), StateInfo('IN', 'Indiana'), StateInfo('IA', 'Iowa'),
            StateInfo('KS', 'Kansas'), StateInfo('KY', 'Kentucky'), StateInfo('LA', 'Louisiana'),
            StateInfo('ME', 'Maine'), StateInfo('MD', 'Maryland'), StateInfo('MA', 'Massachusetts'),
            StateInfo('MI', 'Michigan'), StateInfo('MN', 'Minnesota'), StateInfo('MS', 'Mississippi'),
            StateInfo('MO', 'Missouri'), StateInfo('MT', 'Montana'), StateInfo('NE', 'Nebraska'),
            StateInfo('NV', 'Nevada'), StateInfo('NH', 'New Hampshire'), StateInfo('NJ', 'New Jersey'),
            StateInfo('NM', 'New Mexico'), StateInfo('NY', 'New York'), StateInfo('NC', 'North Carolina'),
            StateInfo('ND', 'North Dakota'), StateInfo('OH', 'Ohio'), StateInfo('OK', 'Oklahoma'),
            StateInfo('OR', 'Oregon'), StateInfo('PA', 'Pennsylvania'), StateInfo('RI', 'Rhode Island'),
            StateInfo('SC', 'South Carolina'), StateInfo('SD', 'South Dakota'), StateInfo('TN', 'Tennessee'),
            StateInfo('TX', 'Texas'), StateInfo('UT', 'Utah'), StateInfo('VT', 'Vermont'),
            StateInfo('VA', 'Virginia'), StateInfo('WA', 'Washington'), StateInfo('WV', 'West Virginia'),
            StateInfo('WI', 'Wisconsin'), StateInfo('WY', 'Wyoming'), StateInfo('DC', 'Washington DC')
        ]

    def process_state_selection(self, state_code: str, form_data: Dict, category: str, 
                              location_id: str = 'default_location', 
                              location_name: str = 'Default Clinic',
                              root_domain: str = None) -> str:
        """
        Process state selection and return redirect URL
        
        Args:
            state_code: Two-letter state code
            form_data: Form data from session storage
            category: Form category (weightloss, antiaging, etc.)
            location_id: Clinic location ID
            location_name: Clinic location name
            root_domain: Root domain for redirects
            
        Returns:
            Redirect URL for appropriate fee page
        """
        # Validate state
        state_info = self.get_state_info(state_code)
        if not state_info:
            raise ValueError(f"Invalid state code: {state_code}")
        
        # Determine consult type
        consult_type = self.determine_consult_type(state_code)
        
        # Format webhook data
        webhook_data = self.format_webhook_data(form_data, state_info, category, consult_type, 
                                               location_id, location_name)
        
        # Call API to get consult type (if API returns different type, use it)
        try:
            api_consult_type = self.call_screener_api(webhook_data)
            if api_consult_type:
                consult_type = api_consult_type
                print(f"API returned consult type: {consult_type}")
        except Exception as e:
            print(f"API call failed, using state-based logic: {e}")
        
        # Generate redirect URL
        if not root_domain:
            root_domain = self.detect_root_domain()
        
        redirect_url = self.generate_redirect_url(root_domain, category, consult_type, 
                                                state_info, form_data, location_id, location_name)
        
        return redirect_url

    def get_state_info(self, state_code: str) -> Optional[StateInfo]:
        """Get state information by code"""
        return next((state for state in self.states if state.code == state_code), None)

    def determine_consult_type(self, state_code: str) -> str:
        """Determine consult type based on state"""
        return 'sync' if state_code in self.sync_only_states else 'async'

    def call_screener_api(self, webhook_data: Dict) -> Optional[str]:
        """Call the screener API to get consult type"""
        try:
            response = requests.post(
                self.webhook_url,
                headers={'Content-Type': 'application/json'},
                json=webhook_data,
                timeout=30
            )
            
            if response.ok:
                print('Webhook submission successful')
                
                # Try to get consult type from response
                try:
                    response_data = response.json()
                    if 'consultType' in response_data:
                        return response_data['consultType']
                except json.JSONDecodeError:
                    print('No JSON response, using state-based logic')
            else:
                print(f'Webhook submission failed: {response.status_code}')
                
        except Exception as error:
            print(f'Webhook submission error: {error}')
        
        return None

    def format_webhook_data(self, form_data: Dict, state_info: StateInfo, category: str, 
                          consult_type: str, location_id: str, location_name: str) -> Dict:
        """Format form data for webhook submission"""
        # Map form data to expected field names
        mapped_data = self.map_form_data(form_data)
        
        # Calculate BMI if height and weight are available
        bmi = self.calculate_bmi(mapped_data.get('heightFeet'), 
                               mapped_data.get('heightInches'), 
                               mapped_data.get('weight'))
        
        return {
            "contact": {
                "name": mapped_data.get('fullName', ''),
                "email": mapped_data.get('email', ''),
                "gender": mapped_data.get('gender', ''),
                "dateOfBirth": mapped_data.get('dateOfBirth', ''),
                "phone": mapped_data.get('phone', ''),
                "address1": form_data.get('address1', form_data.get('address', '')),
                "city": form_data.get('city', ''),
                "state": state_info.code,
                "postalCode": form_data.get('postalCode', form_data.get('zip', form_data.get('zipCode', ''))),
                "timezone": "America/New_York",  # Default timezone
                "type": "patient"
            },
            "patient": {
                "patientId": "",
                "contactId": "",
                "rxRequested": category,
                "height": f"{mapped_data.get('heightFeet', '')}'{mapped_data.get('heightInches', '')}\"" 
                         if mapped_data.get('heightFeet') and mapped_data.get('heightInches') else '',
                "weight": mapped_data.get('weight', ''),
                "BMI": bmi,
                "pregnancy": mapped_data.get('pregnancy', ''),
                "conditions": mapped_data.get('conditions', []) if isinstance(mapped_data.get('conditions'), list) else [],
                "medications": mapped_data.get('medications', []) if isinstance(mapped_data.get('medications'), list) else [],
                "allergies": mapped_data.get('allergies', ''),
                "activityLevel": mapped_data.get('activityLevel', ''),
                "tobaccoUse": mapped_data.get('tobaccoUse', ''),
                "alcoholUse": mapped_data.get('alcoholUse', ''),
                "otcConsumption": mapped_data.get('otcConsumption', []) if isinstance(mapped_data.get('otcConsumption'), list) else [],
                "mentalHealth": mapped_data.get('mentalHealth', '')
            },
            "form": {
                "formType": form_data.get('formType', category),
                "category": category,
                "screener": form_data.get('formType', category),
                "screenerData": json.dumps(form_data),
                "timestamp": self.get_current_timestamp(),
                "formVersion": "2.0.0"
            },
            "clinic": {
                "name": location_name,
                "id": location_id,
                "email": "contact@clinic.com",  # Default email
                "phone": "555-123-4567",  # Default phone
                "type": "healthcare"
            }
        }

    def map_form_data(self, form_data: Dict) -> Dict:
        """Map form data to expected field names (handle variations)"""
        return {
            'fullName': (form_data.get('fullName') or form_data.get('name') or 
                        form_data.get('full_name') or ''),
            'email': (form_data.get('email') or form_data.get('email_address') or ''),
            'phone': (form_data.get('phone') or form_data.get('phone_number') or 
                     form_data.get('phoneNumber') or ''),
            'gender': form_data.get('gender') or form_data.get('sex') or '',
            'dateOfBirth': (form_data.get('dateOfBirth') or form_data.get('dob') or 
                           form_data.get('birth_date') or ''),
            'heightFeet': (form_data.get('heightFeet') or form_data.get('height_feet') or 
                          form_data.get('height_ft') or ''),
            'heightInches': (form_data.get('heightInches') or form_data.get('height_inches') or 
                            form_data.get('height_in') or ''),
            'weight': (form_data.get('weight') or form_data.get('weight_pounds') or 
                      form_data.get('weight_lbs') or ''),
            'pregnancy': form_data.get('pregnancy') or form_data.get('pregnant') or '',
            'conditions': (form_data.get('conditions') or form_data.get('medical_conditions') or 
                          form_data.get('medicalConditions') or []),
            'medications': (form_data.get('medications') or form_data.get('current_medications') or 
                           form_data.get('currentMedications') or []),
            'allergies': (form_data.get('allergies') or form_data.get('allergy') or 
                         form_data.get('allergic_to') or ''),
            'activityLevel': (form_data.get('activityLevel') or form_data.get('activity_level') or 
                             form_data.get('exercise_level') or ''),
            'tobaccoUse': (form_data.get('tobaccoUse') or form_data.get('tobacco_use') or 
                          form_data.get('smoking') or ''),
            'alcoholUse': (form_data.get('alcoholUse') or form_data.get('alcohol_use') or 
                          form_data.get('alcohol_consumption') or ''),
            'otcConsumption': (form_data.get('otcConsumption') or form_data.get('otc_consumption') or 
                              form_data.get('otc_medications') or []),
            'mentalHealth': (form_data.get('mentalHealth') or form_data.get('mental_health') or 
                            form_data.get('depression') or '')
        }

    def calculate_bmi(self, height_feet: str, height_inches: str, weight: str) -> str:
        """Calculate BMI from height and weight"""
        try:
            if height_feet and height_inches and weight:
                total_inches = (int(height_feet) * 12) + int(height_inches)
                height_meters = total_inches * 0.0254
                weight_kg = int(weight) * 0.453592
                bmi = (weight_kg / (height_meters * height_meters))
                return f"{bmi:.1f}"
        except (ValueError, ZeroDivisionError):
            pass
        return ''

    def detect_root_domain(self) -> str:
        """Detect root domain from environment or use default"""
        # In a real implementation, this would detect from the embedding site
        # For now, return a default
        return "https://example.com"

    def generate_redirect_url(self, root_domain: str, category: str, consult_type: str,
                            state_info: StateInfo, form_data: Dict, 
                            location_id: str, location_name: str) -> str:
        """Generate redirect URL for fee page"""
        from urllib.parse import urlencode
        
        # Build contact parameters
        contact_params = {
            'location_id': location_id,
            'location_name': location_name,
            'state': state_info.code,
            'state_name': state_info.name,
            'name': form_data.get('fullName', form_data.get('name', '')),
            'email': form_data.get('email', ''),
            'phone': form_data.get('phone', ''),
            'category': category,
            'consult_type': consult_type
        }
        
        # Generate fee page URL
        fee_url = f"{root_domain}/{category}-{consult_type}-fee?{urlencode(contact_params)}"
        print(f"Redirecting to: {fee_url}")
        
        return fee_url

    def get_current_timestamp(self) -> str:
        """Get current timestamp in ISO format"""
        from datetime import datetime
        return datetime.now().isoformat()

    def generate_state_selector_html(self, category: str = 'weightloss') -> str:
        """Generate HTML for state selector interface"""
        states_html = ''.join([
            f'''
            <div class="state-item" data-code="{state.code}">
                <div class="state-code">{state.code}</div>
                <div class="state-name">{state.name}</div>
            </div>
            ''' for state in self.states
        ])
        
        return f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Select Your State</title>
            <style>
                /* State selector styles would go here */
                .state-grid {{ display: grid; grid-template-columns: repeat(8, 1fr); gap: 6px; }}
                .state-item {{ aspect-ratio: 1; display: flex; flex-direction: column; align-items: center; 
                             justify-content: center; background: #f8f9fa; border: 2px solid #e9ecef; 
                             border-radius: 8px; cursor: pointer; transition: all 0.2s ease; }}
                .state-item:hover {{ border-color: #007cba; background: #e3f2fd; }}
                .state-item.selected {{ background: #007cba; color: white; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Select Your State</h1>
                <div class="state-grid" id="stateGrid">
                    {states_html}
                </div>
                <div class="selection-row" id="selectionRow" style="display: none;">
                    <div class="selected-display" id="selectedDisplay">
                        <div id="selectedText">Please select your state</div>
                    </div>
                    <button class="btn" id="continueBtn">Continue</button>
                </div>
            </div>
            
            <script>
                // State selection JavaScript would go here
                // This would handle the form submission and redirect
            </script>
        </body>
        </html>
        '''


# Example usage
if __name__ == "__main__":
    # Example form data
    form_data = {
        "fullName": "John Doe",
        "email": "john@example.com",
        "phone": "5551234567",
        "heightFeet": "6",
        "heightInches": "0",
        "weight": "200"
    }
    
    selector = StateSelector()
    
    # Process state selection
    redirect_url = selector.process_state_selection(
        state_code="CA",
        form_data=form_data,
        category="weightloss",
        location_id="123",
        location_name="Downtown Clinic",
        root_domain="https://example.com"
    )
    
    print(f"Redirect URL: {redirect_url}")
    
    # Generate state selector HTML
    html = selector.generate_state_selector_html("weightloss")
    print("State selector HTML generated")
