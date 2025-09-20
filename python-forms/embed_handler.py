"""
Embed Handler - Python Version

Handles the three different embed types for the LocumTele widget system.

Usage:
    handler = EmbedHandler()
    result = handler.handle_embed_type_1(form_data, category)
"""

from typing import Dict, Optional
from universal_form_generator import UniversalFormGenerator
from state_selector import StateSelector


class EmbedHandler:
    def __init__(self):
        self.form_generator = UniversalFormGenerator()
        self.state_selector = StateSelector()

    def embed_type_1_form_only(self, form_data: Dict, category: str, 
                              root_domain: str = None) -> Dict:
        """
        Embed Type 1: Form Only
        Form submits → Redirects to {{rootdomain}}/{{category}}-state
        
        Args:
            form_data: Form configuration data
            category: Form category (weightloss, antiaging, etc.)
            root_domain: Root domain for redirects
            
        Returns:
            Dict with form HTML and redirect URL
        """
        # Generate form HTML
        form_html = self.form_generator.generate_form(form_data, 'form-container')
        
        # Generate redirect URL
        if not root_domain:
            root_domain = self.detect_root_domain()
        
        redirect_url = f"{root_domain}/{category}-state"
        
        return {
            'type': 'form_only',
            'form_html': form_html,
            'redirect_url': redirect_url,
            'description': 'Form submits and redirects to state selection'
        }

    def embed_type_2_state_api(self, state_code: str, form_data: Dict, category: str,
                              location_id: str = 'default_location',
                              location_name: str = 'Default Clinic',
                              root_domain: str = None) -> Dict:
        """
        Embed Type 2: State Selector with API
        State Selection → API Call → {{rootdomain}}/{{category}}-{{consultType}}-fee
        
        Args:
            state_code: Two-letter state code
            form_data: Form data from session storage
            category: Form category
            location_id: Clinic location ID
            location_name: Clinic location name
            root_domain: Root domain for redirects
            
        Returns:
            Dict with redirect URL and consult type
        """
        # Process state selection with API call
        redirect_url = self.state_selector.process_state_selection(
            state_code=state_code,
            form_data=form_data,
            category=category,
            location_id=location_id,
            location_name=location_name,
            root_domain=root_domain
        )
        
        # Determine consult type
        consult_type = self.state_selector.determine_consult_type(state_code)
        
        return {
            'type': 'state_api',
            'redirect_url': redirect_url,
            'consult_type': consult_type,
            'state_code': state_code,
            'description': 'State selection with API-driven consult type determination'
        }

    def embed_type_3_sync_calendar(self, category: str, 
                                  root_domain: str = None) -> Dict:
        """
        Embed Type 3: Sync Calendar
        Calendar Booking → {{rootdomain}}/{{category}}-consult-booked
        
        Args:
            category: Form category
            root_domain: Root domain for redirects
            
        Returns:
            Dict with calendar HTML and redirect URL
        """
        # Generate redirect URL
        if not root_domain:
            root_domain = self.detect_root_domain()
        
        redirect_url = f"{root_domain}/{category}-consult-booked"
        
        # Generate calendar HTML (simplified)
        calendar_html = self.generate_calendar_html(category)
        
        return {
            'type': 'sync_calendar',
            'calendar_html': calendar_html,
            'redirect_url': redirect_url,
            'description': 'Direct calendar booking for sync consultations'
        }

    def generate_calendar_html(self, category: str) -> str:
        """Generate HTML for calendar widget"""
        return f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Book Your {category.title()} Consultation</title>
            <style>
                .calendar-container {{
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                }}
                .calendar-header {{
                    text-align: center;
                    margin-bottom: 30px;
                }}
                .calendar-grid {{
                    display: grid;
                    grid-template-columns: repeat(7, 1fr);
                    gap: 1px;
                    background: #e0e0e0;
                    border: 1px solid #e0e0e0;
                }}
                .calendar-day {{
                    background: white;
                    padding: 10px;
                    text-align: center;
                    cursor: pointer;
                    transition: background-color 0.2s;
                }}
                .calendar-day:hover {{
                    background: #e3f2fd;
                }}
                .calendar-day.available {{
                    background: #4caf50;
                    color: white;
                }}
                .calendar-day.selected {{
                    background: #2196f3;
                    color: white;
                }}
            </style>
        </head>
        <body>
            <div class="calendar-container">
                <div class="calendar-header">
                    <h1>Book Your {category.title()} Consultation</h1>
                    <p>Select an available time slot for your consultation</p>
                </div>
                <div class="calendar-grid" id="calendarGrid">
                    <!-- Calendar days would be generated here -->
                </div>
                <div class="booking-controls" style="text-align: center; margin-top: 20px;">
                    <button id="bookAppointment" class="btn btn-primary" disabled>
                        Book Appointment
                    </button>
                </div>
            </div>
            
            <script>
                // Calendar booking JavaScript would go here
                // This would handle appointment booking and redirect
            </script>
        </body>
        </html>
        '''

    def detect_root_domain(self) -> str:
        """Detect root domain from environment or use default"""
        # In a real implementation, this would detect from the embedding site
        # For now, return a default
        return "https://example.com"

    def get_embed_info(self) -> Dict:
        """Get information about all embed types"""
        return {
            'embed_types': {
                'type_1': {
                    'name': 'Form Only',
                    'description': 'Simple screening forms that redirect to state selection',
                    'flow': 'Form → {{rootdomain}}/{{category}}-state',
                    'use_case': 'Basic patient screening with state selection'
                },
                'type_2': {
                    'name': 'State Selector with API',
                    'description': 'State selection with API-driven consult type determination',
                    'flow': 'State Selection → API Call → {{rootdomain}}/{{category}}-{{consultType}}-fee',
                    'use_case': 'When consult type needs to be determined by API'
                },
                'type_3': {
                    'name': 'Sync Calendar',
                    'description': 'Direct calendar booking for sync consultations',
                    'flow': 'Calendar Booking → {{rootdomain}}/{{category}}-consult-booked',
                    'use_case': 'Direct appointment scheduling'
                }
            },
            'sync_only_states': self.state_selector.sync_only_states,
            'api_endpoint': self.state_selector.webhook_url
        }


# Example usage
if __name__ == "__main__":
    handler = EmbedHandler()
    
    # Example form data
    form_data = {
        "title": "Medical Screening",
        "category": "weightloss",
        "questions": [
            {"text": "Full Name", "type": "text", "required": True},
            {"text": "Email", "type": "email", "required": True},
            {"text": "Phone", "type": "phone", "required": True}
        ]
    }
    
    # Embed Type 1: Form Only
    result1 = handler.embed_type_1_form_only(form_data, "weightloss")
    print("Embed Type 1:", result1['description'])
    
    # Embed Type 2: State Selector with API
    session_data = {
        "fullName": "John Doe",
        "email": "john@example.com",
        "phone": "5551234567"
    }
    result2 = handler.embed_type_2_state_api("CA", session_data, "weightloss")
    print("Embed Type 2:", result2['description'])
    print("Redirect URL:", result2['redirect_url'])
    
    # Embed Type 3: Sync Calendar
    result3 = handler.embed_type_3_sync_calendar("weightloss")
    print("Embed Type 3:", result3['description'])
    
    # Get embed info
    info = handler.get_embed_info()
    print("\nEmbed Types Info:")
    for type_key, type_info in info['embed_types'].items():
        print(f"- {type_info['name']}: {type_info['description']}")
