"""
Universal Form Generator - Python Version

A flexible, unified system that can generate forms from any JSON data structure.
Automatically detects form structure and generates appropriate HTML with logic and validation.

Usage:
    generator = UniversalFormGenerator()
    html = generator.generate_form(form_data, 'container-id')
"""

import json
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass


@dataclass
class FormConfig:
    type: str  # 'single', 'multi-step', 'survey'
    sections: List[Dict]
    questions: List[Dict]
    metadata: Dict


class UniversalFormGenerator:
    def __init__(self):
        self.current_form_data = None
        self.form_config = None
        self.question_id_counter = 0
        self.disqualification_triggered = False
        
        # Supported question types
        self.question_types = [
            'text', 'email', 'phone', 'number', 'date', 'radio', 
            'checkbox', 'select', 'textarea', 'file', 'height', 'weight'
        ]
        
        # Answer types for logic
        self.answer_types = ['safe', 'flag', 'disqualify']

    def generate_form(self, form_data: Dict, container_id: str = 'form-container', options: Dict = None) -> str:
        """
        Generate form from any JSON data structure
        
        Args:
            form_data: The form data (any structure)
            container_id: Container element ID
            options: Additional options
            
        Returns:
            Complete HTML form string
        """
        if options is None:
            options = {}
            
        try:
            self.current_form_data = form_data
            self.form_config = self.analyze_form_structure(form_data)
            
            # Generate the form HTML
            form_html = self.build_form_html(container_id, options)
            
            return form_html
            
        except Exception as error:
            print(f'Error generating form: {error}')
            raise error

    def analyze_form_structure(self, form_data: Dict) -> FormConfig:
        """Analyze form structure to determine the best rendering approach"""
        config = FormConfig(
            type='single',
            sections=[],
            questions=[],
            metadata={}
        )

        if isinstance(form_data, list):
            # Simple array of questions
            config.type = 'single'
            config.questions = form_data
        elif isinstance(form_data, dict):
            # Object structure - analyze properties
            keys = list(form_data.keys())
            
            # Check for common form metadata
            config.metadata = {
                'title': form_data.get('title') or form_data.get('formName') or form_data.get('screener') or 'Form',
                'subtitle': form_data.get('subtitle') or form_data.get('description') or '',
                'category': form_data.get('category') or form_data.get('type') or 'general'
            }

            # Check if it's a multi-section form
            section_keys = [key for key in keys 
                          if isinstance(form_data[key], list) and 
                          key not in ['questions', 'metadata', 'config']]

            if len(section_keys) > 1:
                # Multi-section form
                config.type = 'multi-step'
                config.sections = [{'title': key, 'questions': form_data[key], 'id': self.sanitize_value(key)} 
                                 for key in section_keys]
            elif len(section_keys) == 1:
                # Single section with questions
                config.type = 'single'
                config.questions = form_data[section_keys[0]]
            elif 'questions' in form_data:
                # Questions property
                config.type = 'single'
                config.questions = form_data['questions']
            else:
                # Try to find any array property
                array_props = [key for key in keys if isinstance(form_data[key], list)]
                if array_props:
                    config.questions = form_data[array_props[0]]

        return config

    def build_form_html(self, container_id: str, options: Dict) -> str:
        """Build the complete form HTML"""
        show_progress = options.get('showProgress', True)
        allow_back_navigation = options.get('allowBackNavigation', True)
        submit_text = options.get('submitText', 'Submit Form')
        theme = options.get('theme', 'default')

        metadata = self.form_config.metadata
        form_type = self.form_config.type
        sections = self.form_config.sections
        questions = self.form_config.questions

        html = f'''
        <div id="{container_id}" class="universal-form-container" data-form-type="{form_type}">
            <!-- Form Header -->
            <div class="form-header">
                <h1 class="form-title">{metadata['title']}</h1>
                {f'<p class="form-subtitle">{metadata["subtitle"]}</p>' if metadata['subtitle'] else ''}
            </div>
        '''

        if form_type == 'multi-step' and show_progress:
            html += self.generate_progress_bar(len(sections))

        html += f'''
            <form id="universalForm" class="universal-form" data-category="{metadata['category']}">
        '''

        if form_type == 'multi-step':
            html += self.generate_multi_step_form(sections)
        else:
            html += self.generate_single_form(questions)

        html += f'''
                <!-- Navigation -->
                {self.generate_navigation(form_type, len(sections) if sections else 0, submit_text)}
                
                <!-- Loading indicator -->
                <div class="loading" id="loadingIndicator" style="display: none;">
                    <div class="spinner"></div>
                    <p>Submitting your form...</p>
                </div>

                <!-- Success message -->
                <div id="successMessage" class="success-message" style="display: none;">
                    <h3>✅ Form submitted successfully!</h3>
                    <p>Redirecting you to the next step...</p>
                </div>

                <!-- Disqualification message -->
                <div id="disqualificationMessage" class="disqualification-container" style="display: none;">
                    <h2 class="disqualification-title">Not Eligible for Treatment</h2>
                    <p id="disqualificationText">Based on your answers, you are not eligible for this treatment at this time.</p>
                    <div class="crisis-resources">
                        <p><strong>Need Help?</strong></p>
                        <p>If you're experiencing a mental health crisis, please contact:</p>
                        <ul>
                            <li><strong>National Suicide Prevention Lifeline:</strong> 988</li>
                            <li><strong>Crisis Text Line:</strong> Text HOME to 741741</li>
                            <li><strong>Emergency:</strong> 911</li>
                        </ul>
                    </div>
                </div>
            </form>
        </div>
        '''

        return html

    def generate_progress_bar(self, total_steps: int) -> str:
        """Generate progress bar for multi-step forms"""
        return f'''
            <div class="progress-container">
                <div class="progress-bar">
                    <div class="progress-fill" id="progressFill"></div>
                </div>
                <div class="progress-text">
                    <span id="currentStep">1</span> of <span id="totalSteps">{total_steps}</span>
                </div>
            </div>
        '''

    def generate_multi_step_form(self, sections: List[Dict]) -> str:
        """Generate multi-step form"""
        return ''.join([f'''
            <div class="form-step {'active' if index == 0 else ''}" id="step-{index}" data-step="{index}">
                <div class="step-content">
                    <h2 class="step-title">{section['title']}</h2>
                    <div class="questions-container">
                        {''.join([self.generate_question_html(question) for question in section['questions']])}
                    </div>
                </div>
            </div>
        ''' for index, section in enumerate(sections)])

    def generate_single_form(self, questions: List[Dict]) -> str:
        """Generate single form"""
        return f'''
            <div class="questions-container">
                {''.join([self.generate_question_html(question) for question in questions])}
            </div>
        '''

    def generate_navigation(self, form_type: str, total_steps: int, submit_text: str) -> str:
        """Generate navigation buttons"""
        if form_type == 'multi-step':
            return f'''
                <div class="navigation-buttons">
                    <button type="button" class="nav-button nav-button-secondary" id="prevButton" style="display: none;">
                        ← Previous
                    </button>
                    <button type="button" class="nav-button nav-button-primary" id="nextButton">
                        Next →
                    </button>
                    <button type="submit" class="nav-button nav-button-primary" id="submitButton" style="display: none;">
                        {submit_text}
                    </button>
                </div>
            '''
        else:
            return f'''
                <div class="submit-container">
                    <button type="submit" class="nav-button nav-button-primary" id="submitButton">
                        {submit_text}
                    </button>
                </div>
            '''

    def generate_question_html(self, question: Dict) -> str:
        """Generate HTML for a single question"""
        question_id = self.generate_question_id(question)
        field_name = self.get_field_name(question)
        is_required = self.is_question_required(question)
        question_type = self.detect_question_type(question)

        html = f'''
            <div class="question" id="{question_id}_container" data-question-type="{question_type}">
                <label class="question-label" for="{question_id}">
                    {question.get('text') or question.get('questionText') or question.get('name')}{' *' if is_required else ''}
                </label>
        '''

        # Generate input field based on type
        html += self.generate_input_field(question, question_id, field_name, question_type)

        # Add error message
        html += f'''
            <div class="error-message" id="{question_id}_error" style="display: none;">Please answer this question</div>
        </div>
        '''

        return html

    def generate_input_field(self, question: Dict, question_id: str, field_name: str, question_type: str) -> str:
        """Generate input field based on question type"""
        field_generators = {
            'text': self.generate_text_input,
            'email': self.generate_email_input,
            'phone': self.generate_phone_input,
            'number': self.generate_number_input,
            'date': self.generate_date_input,
            'radio': self.generate_radio_input,
            'checkbox': self.generate_checkbox_input,
            'select': self.generate_select_input,
            'textarea': self.generate_textarea_input,
            'file': self.generate_file_input,
            'height': self.generate_height_input,
            'weight': self.generate_weight_input
        }

        generator = field_generators.get(question_type, self.generate_text_input)
        return generator(question, question_id, field_name)

    def generate_text_input(self, question: Dict, question_id: str, field_name: str) -> str:
        """Generate text input"""
        placeholder = question.get('placeholder', '')
        required = 'required' if self.is_question_required(question) else ''
        return f'''
            <input type="text" id="{question_id}" name="{field_name}" class="text-input" 
                   placeholder="{placeholder}" {required}>
        '''

    def generate_email_input(self, question: Dict, question_id: str, field_name: str) -> str:
        """Generate email input"""
        required = 'required' if self.is_question_required(question) else ''
        return f'''
            <input type="email" id="{question_id}" name="{field_name}" class="text-input" 
                   placeholder="Enter your email address" {required}>
        '''

    def generate_phone_input(self, question: Dict, question_id: str, field_name: str) -> str:
        """Generate phone input"""
        required = 'required' if self.is_question_required(question) else ''
        return f'''
            <input type="tel" id="{question_id}" name="{field_name}" class="text-input" 
                   placeholder="Enter your phone number" maxlength="10" {required}>
        '''

    def generate_number_input(self, question: Dict, question_id: str, field_name: str) -> str:
        """Generate number input"""
        min_val = question.get('min', '')
        max_val = question.get('max', '')
        placeholder = question.get('placeholder', '')
        required = 'required' if self.is_question_required(question) else ''
        
        min_attr = f'min="{min_val}"' if min_val else ''
        max_attr = f'max="{max_val}"' if max_val else ''
        
        return f'''
            <input type="number" id="{question_id}" name="{field_name}" class="text-input" 
                   placeholder="{placeholder}" {min_attr} {max_attr} {required}>
        '''

    def generate_date_input(self, question: Dict, question_id: str, field_name: str) -> str:
        """Generate date input"""
        required = 'required' if self.is_question_required(question) else ''
        return f'''
            <input type="text" id="{question_id}" name="{field_name}" class="text-input" 
                   placeholder="MM/DD/YYYY" maxlength="10" {required}>
        '''

    def generate_radio_input(self, question: Dict, question_id: str, field_name: str) -> str:
        """Generate radio input"""
        options = self.get_question_options(question)
        html = '<div class="option-group">'

        for index, option in enumerate(options):
            option_id = f"{question_id}_{index}"
            option_value = self.sanitize_value(option)
            option_label = self.format_label(option)
            answer_type = self.get_answer_type(option, question)

            html += f'''
                <div class="option-item">
                    <input type="radio" id="{option_id}" name="{field_name}" value="{option_value}" 
                           data-answer-type="{answer_type}" data-question-id="{question_id}">
                    <label for="{option_id}">{option_label}</label>
                </div>
            '''

        html += '</div>'
        return html

    def generate_checkbox_input(self, question: Dict, question_id: str, field_name: str) -> str:
        """Generate checkbox input"""
        options = self.get_question_options(question)
        html = '<div class="option-group">'

        for index, option in enumerate(options):
            option_id = f"{question_id}_{index}"
            option_value = self.sanitize_value(option)
            option_label = self.format_label(option)

            html += f'''
                <div class="option-item">
                    <input type="checkbox" id="{option_id}" name="{field_name}" value="{option_value}">
                    <label for="{option_id}">{option_label}</label>
                </div>
            '''

        html += '</div>'
        return html

    def generate_select_input(self, question: Dict, question_id: str, field_name: str) -> str:
        """Generate select input"""
        options = self.get_question_options(question)
        required = 'required' if self.is_question_required(question) else ''
        
        html = f'<select id="{question_id}" name="{field_name}" class="text-input" {required}>'
        html += '<option value="">Select an option</option>'

        for option in options:
            option_value = self.sanitize_value(option)
            option_label = self.format_label(option)
            answer_type = self.get_answer_type(option, question)
            html += f'<option value="{option_value}" data-answer-type="{answer_type}">{option_label}</option>'

        html += '</select>'
        return html

    def generate_textarea_input(self, question: Dict, question_id: str, field_name: str) -> str:
        """Generate textarea input"""
        rows = question.get('rows', 4)
        placeholder = question.get('placeholder', '')
        required = 'required' if self.is_question_required(question) else ''
        
        return f'''
            <textarea id="{question_id}" name="{field_name}" class="textarea-input" 
                      rows="{rows}" placeholder="{placeholder}" {required}></textarea>
        '''

    def generate_file_input(self, question: Dict, question_id: str, field_name: str) -> str:
        """Generate file input"""
        accept = question.get('accept', 'image/*,.pdf')
        required = 'required' if self.is_question_required(question) else ''
        
        return f'''
            <div class="file-input">
                <input type="file" id="{question_id}" name="{field_name}" 
                       accept="{accept}" {required}>
                Choose File
            </div>
        '''

    def generate_height_input(self, question: Dict, question_id: str, field_name: str) -> str:
        """Generate height input (feet and inches)"""
        return f'''
            <div class="height-inputs">
                <div class="height-input-wrapper">
                    <input type="number" id="{question_id}_feet" name="{field_name}_feet" 
                           class="text-input" min="3" max="8" placeholder="Feet" required>
                    <span class="height-unit">ft</span>
                </div>
                <div class="height-input-wrapper">
                    <input type="number" id="{question_id}_inches" name="{field_name}_inches" 
                           class="text-input" min="0" max="11" placeholder="Inches" required>
                    <span class="height-unit">in</span>
                </div>
            </div>
        '''

    def generate_weight_input(self, question: Dict, question_id: str, field_name: str) -> str:
        """Generate weight input"""
        required = 'required' if self.is_question_required(question) else ''
        
        return f'''
            <input type="number" id="{question_id}" name="{field_name}" class="text-input" 
                   min="50" max="500" placeholder="Enter your weight in pounds" {required}>
        '''

    def detect_question_type(self, question: Dict) -> str:
        """Detect question type from question data"""
        # Check explicit type first
        if question.get('type') or question.get('questionType'):
            return (question.get('type') or question.get('questionType')).lower()

        # Detect from text content
        text = (question.get('text') or question.get('questionText') or question.get('name') or '').lower()
        
        if 'email' in text:
            return 'email'
        elif 'phone' in text or 'number' in text:
            return 'phone'
        elif 'date' in text or 'birth' in text:
            return 'date'
        elif 'height' in text:
            return 'height'
        elif 'weight' in text:
            return 'weight'
        elif 'gender' in text or 'sex' in text:
            return 'radio'
        elif 'pregnant' in text or 'cancer' in text:
            return 'radio'
        elif 'allergies' in text or 'describe' in text:
            return 'textarea'
        elif 'upload' in text or 'file' in text or 'id' in text:
            return 'file'
        
        # Check for options to determine input type
        if any(key in question for key in ['options', 'safeAnswers', 'safe']):
            if question.get('multiple') or question.get('allowMultiple'):
                return 'checkbox'
            else:
                return 'radio'

        # Default to text
        return 'text'

    def get_question_options(self, question: Dict) -> List[str]:
        """Get question options from various possible structures"""
        return (question.get('options') or 
                question.get('safeAnswers') or 
                question.get('safe') or 
                question.get('choices') or 
                question.get('values') or 
                [])

    def is_question_required(self, question: Dict) -> bool:
        """Check if question is required"""
        return (question.get('required') is True or 
                question.get('required') == 'true' or 
                question.get('required') == 1 or
                (question.get('text') and '*' in question.get('text')))

    def get_field_name(self, question: Dict) -> str:
        """Get field name from question"""
        if question.get('name'):
            return question['name']
        if question.get('field'):
            return question['field']
        
        text = question.get('text') or question.get('questionText') or ''
        return self.sanitize_value(text)

    def generate_question_id(self, question: Dict) -> str:
        """Generate unique question ID"""
        if question.get('id'):
            return question['id']
        
        text = question.get('text') or question.get('questionText') or question.get('name') or 'question'
        self.question_id_counter += 1
        return f"q_{self.sanitize_value(text)}_{self.question_id_counter}"

    def get_answer_type(self, answer: str, question: Dict) -> str:
        """Get answer type (safe, disqualify, flag)"""
        if question.get('safeAnswers') and answer in question['safeAnswers']:
            return 'safe'
        if question.get('disqualifyAnswers') and answer in question['disqualifyAnswers']:
            return 'disqualify'
        if question.get('flagAnswers') and answer in question['flagAnswers']:
            return 'flag'
        if question.get('safe') and answer in question['safe']:
            return 'safe'
        if question.get('disqualify') and answer in question['disqualify']:
            return 'disqualify'
        return 'safe'

    def sanitize_value(self, value: str) -> str:
        """Sanitize value for use as HTML attribute"""
        return re.sub(r'[^a-z0-9]', '_', str(value).lower()).replace('_+', '_').strip('_')

    def format_label(self, value: str) -> str:
        """Format label for display"""
        if value in ['any_text', 'any_email', 'any_phone', 'any_valid']:
            return 'Yes'
        if value == 'none':
            return 'No'
        return str(value).replace('_', ' ').title()


# Example usage
if __name__ == "__main__":
    # Example form data
    form_data = {
        "title": "Medical Screening",
        "category": "weightloss",
        "questions": [
            {
                "text": "Full Name",
                "type": "text",
                "required": True
            },
            {
                "text": "Email Address",
                "type": "email",
                "required": True
            },
            {
                "text": "Do you have diabetes?",
                "type": "radio",
                "options": ["No", "Type 1", "Type 2"],
                "safeAnswers": ["No"],
                "disqualifyAnswers": ["Type 1", "Type 2"],
                "disqualifyMessage": "This treatment is not suitable for diabetics"
            }
        ]
    }
    
    generator = UniversalFormGenerator()
    html = generator.generate_form(form_data, 'form-container')
    print(html)
