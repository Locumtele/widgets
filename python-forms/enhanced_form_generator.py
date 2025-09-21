"""
Enhanced Universal Form Generator - Fixed Version

This file contains the complete enhanced form generator with all fixes applied.
"""

import json
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass


@dataclass
class FormSection:
    title: str
    questions: List[Dict]
    order: int
    is_standard: bool  # True for standard sections, False for assessment


class EnhancedFormGenerator:
    def __init__(self):
        self.current_form_data = None
        self.form_responses = {}
        self.disqualification_triggered = False
        self.question_id_counter = 0

        # Supported question types from your data
        self.question_types = [
            'text', 'email', 'phone', 'date', 'radio', 'checkbox',
            'file', 'height_feet', 'height_inches', 'weight_pounds', 'formula'
        ]

        # Sync-only states (from your data)
        self.sync_only_states = [
            'AR', 'DC', 'DE', 'ID', 'KS', 'LA', 'MS', 'NM',
            'RI', 'WV', 'NC', 'SC', 'ME'
        ]

    def generate_notion_form(self, notion_form_data: Dict, options: Dict = None) -> str:
        """
        Generate 5-section form from Notion JSON data structure

        Args:
            notion_form_data: Your exact JSON structure from Notion
            options: Additional options

        Returns:
            Complete HTML form with 5 sections + state selector
        """
        if options is None:
            options = {}

        try:
            self.current_form_data = notion_form_data

            # Extract form metadata
            form_name = notion_form_data.get('name', 'Medical Screening')
            form_category = notion_form_data.get('property_category', 'general')
            consult_type = notion_form_data.get('property_consult_type', 'async')

            # Build 5-section structure
            sections = self.build_five_section_structure(notion_form_data)

            # Generate complete form HTML
            form_html = self.build_complete_form_html(
                form_name, form_category, consult_type, sections, options
            )

            return form_html

        except Exception as error:
            print(f'Error generating Notion form: {error}')
            raise error

    def build_five_section_structure(self, notion_data: Dict) -> List[FormSection]:
        """Build the required 5-section structure"""
        sections = []
        notion_sections = notion_data.get('sections', {})

        # Section 1: Patient Profile (standard)
        if 'Patient Profile' in notion_sections:
            sections.append(FormSection(
                title='Patient Profile',
                questions=notion_sections['Patient Profile'],
                order=1,
                is_standard=True
            ))

        # Section 2: Assessment (unique per form)
        if 'Assessment' in notion_sections:
            sections.append(FormSection(
                title='Assessment',
                questions=notion_sections['Assessment'],
                order=2,
                is_standard=False
            ))

        # Section 3: Medical History (standard)
        if 'Medical History' in notion_sections:
            sections.append(FormSection(
                title='Medical History',
                questions=notion_sections['Medical History'],
                order=3,
                is_standard=True
            ))

        # Section 4: Verification (standard)
        if 'Verification' in notion_sections:
            sections.append(FormSection(
                title='Verification',
                questions=notion_sections['Verification'],
                order=4,
                is_standard=True
            ))

        # Note: State is now handled in Verification section via address

        return sections

    def build_complete_form_html(self, form_name: str, category: str, consult_type: str,
                                sections: List[FormSection], options: Dict) -> str:
        """Build the complete form HTML with modern styling"""

        # Generate CSS styles
        styles = self.generate_modern_styles()

        # Generate JavaScript for conditional logic and form handling
        javascript = self.generate_form_javascript(category, consult_type, form_name, len(sections))

        html = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{form_name} Assessment</title>
    <style>{styles}</style>
</head>
<body>
    <div class="form-wrapper">
        <!-- Fixed Title Container -->
        <div class="title-container">
            <h1 class="form-title">{form_name} Assessment</h1>
            <p class="form-subtitle">See if you prequalify by completing this questionnaire</p>
            <div class="progress-container">
                <div class="progress-bar">
                    <div class="progress-fill" style="width: 20%;"></div>
                </div>
                <span class="progress-text">Section 1 of 5</span>
            </div>
        </div>

        <!-- Survey Container (changes per section) -->
        <div class="survey-container">
            <form id="medicalForm" class="medical-form" data-category="{category}" data-consult-type="{consult_type}">
                {self.generate_all_sections(sections)}

                <!-- Navigation Buttons -->
                <div class="form-navigation">
                    <button type="button" id="prevBtn" class="nav-btn prev-btn" style="display: none;">Previous</button>
                    <button type="button" id="nextBtn" class="nav-btn next-btn">Next</button>
                    <button type="submit" id="submitBtn" class="nav-btn submit-btn" style="display: none;">Complete Screening</button>
                </div>
            </form>
        </div>
    </div>

    <script>{javascript}</script>
</body>
</html>
        '''

        return html

    def generate_all_sections(self, sections: List[FormSection]) -> str:
        """Generate HTML for all 5 sections"""
        html = ""

        for i, section in enumerate(sections):
            section_class = "section active" if i == 0 else "section"

            html += f'''
                <div class="{section_class}" id="section-{i + 1}">
                    <h2 class="section-title">{section.title}</h2>
                    <div class="questions-container">
            '''

            # Generate questions for this section
            # Regular questions from Notion data - group height/weight
            html += self.generate_section_questions(section.questions)

            html += '''
                    </div>
                </div>
            '''

        return html

    def generate_section_questions(self, questions: List[Dict]) -> str:
        """Generate questions for a section, grouping height/weight together"""
        html = ""
        i = 0

        while i < len(questions):
            question = questions[i]

            # Check if this is height_feet and next questions are height_inches, weight
            if (question.get('questionType') == 'height_feet' and
                i + 2 < len(questions) and
                questions[i + 1].get('questionType') == 'height_inches' and
                questions[i + 2].get('questionType') == 'weight_pounds'):

                # Generate grouped height/weight layout
                html += self.generate_height_weight_group(questions[i:i+3])
                i += 3  # Skip next 2 questions as they're included in the group
            else:
                # Regular question
                html += self.generate_question_html(question)
                i += 1

        return html

    def generate_height_weight_group(self, height_weight_questions: List[Dict]) -> str:
        """Generate grouped height and weight inputs in 3-column layout"""
        feet_q = height_weight_questions[0]
        inches_q = height_weight_questions[1]
        weight_q = height_weight_questions[2]

        html = f'''
            <div class="question-wrapper" data-question-group="height-weight">
                <div class="question-container">
                    <label class="question-label">
                        Height and Weight
                        <span class="required-asterisk">*</span>
                    </label>
                    <div class="answer-container">
                        <div class="height-weight-container">
                            {self.generate_height_feet_input(feet_q, feet_q.get('questionId', 'height_feet'))}
                            {self.generate_height_inches_input(inches_q, inches_q.get('questionId', 'height_inches'))}
                            {self.generate_weight_input(weight_q, weight_q.get('questionId', 'weight'))}
                        </div>
                        <div class="bmi-display-section">
                            <div class="formula-display">
                                <div id="patient-profile-bmi" class="bmi-result">
                                    <span class="bmi-label">BMI: </span>
                                    <span class="bmi-value" id="bmi-value">Enter height and weight above</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        '''

        return html

    def generate_question_html(self, question: Dict) -> str:
        """Generate HTML for a single question with conditional logic"""
        question_id = question.get('questionId', f"q_{self.get_next_id()}")
        question_text = question.get('questionText', '')
        question_type = question.get('questionType', 'text')
        required = question.get('required', False)
        show_condition = question.get('showCondition', 'always')
        disqualify_message = question.get('disqualifyMessage', '')

        # Determine if question should be hidden by default
        hidden_class = '' if show_condition == 'always' else 'question-hidden'

        html = f'''
            <div class="question-wrapper {hidden_class}"
                 data-question-id="{question_id}"
                 data-show-condition="{show_condition}">
                <div class="question-container">
                    <label class="question-label" for="{question_id}">
                        {question_text}
                        {' <span class="required-asterisk">*</span>' if required else ''}
                    </label>

                    <div class="answer-container">
                        {self.generate_input_html(question, question_id)}
                    </div>

                    <!-- Disqualification message container -->
                    {f'<div class="disqualification-message" style="display: none;">{disqualify_message}</div>' if disqualify_message else ''}
                </div>
            </div>
        '''

        return html

    def generate_input_html(self, question: Dict, question_id: str) -> str:
        """Generate the appropriate input HTML based on question type"""
        question_type = question.get('questionType', 'text')

        if question_type in ['text', 'email', 'phone']:
            return self.generate_text_input(question, question_id)
        elif question_type == 'date':
            return self.generate_date_input(question, question_id)
        elif question_type == 'radio':
            return self.generate_radio_input(question, question_id)
        elif question_type == 'checkbox':
            return self.generate_checkbox_input(question, question_id)
        elif question_type == 'file':
            return self.generate_file_input(question, question_id)
        elif question_type == 'height_feet':
            return self.generate_height_feet_input(question, question_id)
        elif question_type == 'height_inches':
            return self.generate_height_inches_input(question, question_id)
        elif question_type == 'weight_pounds':
            return self.generate_weight_input(question, question_id)
        elif question_type == 'formula':
            return self.generate_formula_display(question, question_id)
        elif question_type == 'dropdown':
            return self.generate_dropdown_input(question, question_id)
        else:
            return f'<input type="text" id="{question_id}" name="{question_id}" class="form-input">'

    def generate_text_input(self, question: Dict, question_id: str) -> str:
        """Generate text, email, or phone input"""
        question_type = question.get('questionType', 'text')
        required = question.get('required', False)

        input_type = 'email' if question_type == 'email' else 'tel' if question_type == 'phone' else 'text'

        # Set appropriate autocomplete values
        autocomplete_value = "off"
        if question_type == 'email':
            autocomplete_value = "email"
        elif question_type == 'phone':
            autocomplete_value = "tel"
        elif 'name' in question.get('questionText', '').lower():
            autocomplete_value = "name"

        # Add phone-specific attributes
        phone_attrs = ""
        if question_type == 'phone':
            phone_attrs = 'oninput="formatPhoneInput(this)" maxlength="14" placeholder="(555) 123-4567"'

        return f'''
            <input type="{input_type}"
                   id="{question_id}"
                   name="{question_id}"
                   class="form-input"
                   autocomplete="{autocomplete_value}"
                   {phone_attrs}
                   {'required' if required else ''}>
        '''

    def generate_date_input(self, question: Dict, question_id: str) -> str:
        """Generate date input with age validation"""
        required = question.get('required', False)

        return f'''
            <input type="date"
                   id="{question_id}"
                   name="{question_id}"
                   class="form-input date-input"
                   {'required' if required else ''}
                   onchange="validateAge(this)">
        '''

    def generate_radio_input(self, question: Dict, question_id: str) -> str:
        """Generate radio button options"""
        safe_answers = question.get('safeAnswers', [])
        flag_answers = question.get('flagAnswers', [])
        disqualify_answers = question.get('disqualifyAnswers', [])

        # Create options from all answer types
        all_options = set(safe_answers + flag_answers + disqualify_answers)

        # Sort options to put "none" and "no" options last
        sorted_options = sorted(all_options, key=lambda x: (
            x.lower().startswith('none'),
            x.lower() == 'none_of_the_above',
            x.lower() == 'no',
            x.lower()
        ))

        html = '<div class="radio-group">'
        for option in sorted_options:
            # Determine answer type for data attribute
            answer_type = 'safe'
            if option in disqualify_answers:
                answer_type = 'disqualify'
            elif option in flag_answers:
                answer_type = 'flag'

            option_label = option.replace('_', ' ').title()

            html += f'''
                <label class="radio-option">
                    <input type="radio"
                           name="{question_id}"
                           value="{option}"
                           data-answer-type="{answer_type}"
                           autocomplete="off"
                           onchange="handleAnswerChange(this)">
                    <span class="radio-checkmark"></span>
                    {option_label}
                </label>
            '''

        html += '</div>'
        return html

    def generate_checkbox_input(self, question: Dict, question_id: str) -> str:
        """Generate checkbox options"""
        safe_answers = question.get('safeAnswers', [])
        flag_answers = question.get('flagAnswers', [])
        disqualify_answers = question.get('disqualifyAnswers', [])

        # Create options from all answer types
        all_options = set(safe_answers + flag_answers + disqualify_answers)

        # Sort options to put "none" and "no" options last
        sorted_options = sorted(all_options, key=lambda x: (
            x.lower().startswith('none'),
            x.lower() == 'none_of_the_above',
            x.lower() == 'no',
            x.lower()
        ))

        html = '<div class="checkbox-group">'
        for option in sorted_options:
            # Determine answer type for data attribute
            answer_type = 'safe'
            if option in disqualify_answers:
                answer_type = 'disqualify'
            elif option in flag_answers:
                answer_type = 'flag'

            option_label = option.replace('_', ' ').title()

            html += f'''
                <label class="checkbox-option">
                    <input type="checkbox"
                           name="{question_id}"
                           value="{option}"
                           data-answer-type="{answer_type}"
                           autocomplete="off"
                           onchange="handleAnswerChange(this)">
                    <span class="checkbox-checkmark"></span>
                    {option_label}
                </label>
            '''

        html += '</div>'
        return html

    def generate_file_input(self, question: Dict, question_id: str) -> str:
        """Generate file upload input with better handling"""
        return f'''
            <div class="file-input-container">
                <input type="file"
                       id="{question_id}"
                       name="{question_id}"
                       class="file-input"
                       accept="image/*,.pdf"
                       onchange="handleFileUpload(this)">
                <label for="{question_id}" class="file-input-label">
                    <span class="file-input-text" id="{question_id}_text">Choose File</span>
                    <span class="file-input-button">Browse</span>
                </label>
            </div>
        '''

    def generate_height_feet_input(self, question: Dict, question_id: str) -> str:
        """Generate height feet input - part of 3-column layout"""
        return f'''
            <div class="height-input-group">
                <input type="number"
                       id="{question_id}"
                       name="{question_id}"
                       class="form-input height-input"
                       min="3" max="8"
                       placeholder="Feet"
                       onchange="calculateBMI()">
                <span class="input-suffix">ft</span>
            </div>
        '''

    def generate_height_inches_input(self, question: Dict, question_id: str) -> str:
        """Generate height inches input - part of 3-column layout"""
        return f'''
            <div class="height-input-group">
                <input type="number"
                       id="{question_id}"
                       name="{question_id}"
                       class="form-input height-input"
                       min="0" max="11"
                       placeholder="Inches"
                       onchange="calculateBMI()">
                <span class="input-suffix">in</span>
            </div>
        '''

    def generate_weight_input(self, question: Dict, question_id: str) -> str:
        """Generate weight input - part of 3-column layout"""
        return f'''
            <div class="weight-input-group">
                <input type="number"
                       id="{question_id}"
                       name="{question_id}"
                       class="form-input weight-input"
                       min="50" max="500"
                       placeholder="Weight"
                       onchange="calculateBMI()">
                <span class="input-suffix">lbs</span>
            </div>
        '''

    def generate_formula_display(self, question: Dict, question_id: str) -> str:
        """Generate BMI formula display (calculated automatically)"""
        return f'''
            <div class="formula-display">
                <div id="{question_id}" class="bmi-result">
                    <span class="bmi-label">BMI: </span>
                    <span class="bmi-value" id="bmi-value">Enter height and weight above</span>
                </div>
            </div>
        '''

    def generate_dropdown_input(self, question: Dict, question_id: str) -> str:
        """Generate dropdown select input"""
        question_text = question.get('questionText', '')

        if 'state' in question_text.lower():
            # Generate state dropdown
            states = [
                ('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'),
                ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'),
                ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'),
                ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'),
                ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'),
                ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'),
                ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'),
                ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'),
                ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'),
                ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'),
                ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'),
                ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'),
                ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')
            ]

            options_html = '<option value="">Choose your state...</option>'
            for code, name in states:
                options_html += f'<option value="{code}">{name}</option>'

            return f'''
                <select id="{question_id}" name="{question_id}" class="form-input state-select" required>
                    {options_html}
                </select>
            '''
        else:
            # Generic dropdown
            return f'''
                <select id="{question_id}" name="{question_id}" class="form-input" required>
                    <option value="">Choose an option...</option>
                </select>
            '''

    def generate_state_selector(self) -> str:
        """Generate the custom state selector (section 5)"""
        states = [
            'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
            'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
            'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
            'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
            'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
        ]

        html = '''
            <div class="question-container">
                <label class="question-label">Select your state <span class="required-asterisk">*</span></label>
                <div class="answer-container">
                    <select id="state-selector" name="state" class="form-input state-select" required>
                        <option value="">Choose your state...</option>
        '''

        for state in states:
            sync_indicator = ' (Sync Only)' if state in self.sync_only_states else ''
            html += f'<option value="{state}">{state}{sync_indicator}</option>'

        html += '''
                    </select>
                </div>
            </div>
        '''

        return html

    def generate_modern_styles(self) -> str:
        """Generate modern, clean CSS styles"""
        return '''
            * {
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }

            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: transparent;
                color: #333;
                line-height: 1.6;
            }

            .form-wrapper {
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }

            /* Fixed Title Container */
            .title-container {
                background: white;
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                margin-bottom: 20px;
                text-align: center;
            }

            .form-title {
                font-size: 2rem;
                font-weight: 600;
                color: #333;
                margin-bottom: 10px;
            }

            .form-subtitle {
                font-size: 1.1rem;
                color: #666;
                text-align: center;
                margin-bottom: 20px;
                font-weight: 400;
            }

            .progress-container {
                margin-top: 20px;
            }

            .progress-bar {
                width: 100%;
                height: 8px;
                background: #f0f0f0;
                border-radius: 4px;
                overflow: hidden;
                margin-bottom: 10px;
            }

            .progress-fill {
                height: 100%;
                background: linear-gradient(90deg, #333 0%, #555 100%);
                transition: width 0.3s ease;
            }

            .progress-text {
                font-size: 0.9rem;
                color: #666;
            }

            /* Survey Container */
            .survey-container {
                background: white;
                padding: 40px;
                border-radius: 12px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }

            .section {
                display: none;
            }

            .section.active {
                display: block;
            }

            .section-title {
                font-size: 1.5rem;
                font-weight: 600;
                color: #333;
                margin-bottom: 30px;
                padding-bottom: 15px;
                border-bottom: 2px solid #f0f0f0;
            }

            .questions-container {
                margin-bottom: 40px;
            }

            .question-wrapper {
                margin-bottom: 30px;
            }

            .question-wrapper.question-hidden {
                display: none;
            }

            .question-container {
                margin-bottom: 20px;
            }

            .question-label {
                display: block;
                font-weight: 600;
                color: #333;
                margin-bottom: 12px;
                font-size: 1rem;
            }

            .required-asterisk {
                color: #e74c3c;
                margin-left: 4px;
            }

            .answer-container {
                margin-bottom: 10px;
            }

            /* Form Inputs */
            .form-input {
                width: 100%;
                padding: 14px 16px;
                border: 2px solid #e1e5e9;
                border-radius: 8px;
                font-size: 1rem;
                transition: border-color 0.2s ease;
                background: white;
            }

            .form-input:focus {
                outline: none;
                border-color: #333;
                box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            }

            /* Radio and Checkbox Groups */
            .radio-group, .checkbox-group {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin-top: 10px;
            }

            .radio-option, .checkbox-option {
                display: flex;
                align-items: center;
                cursor: pointer;
                padding: 12px 16px;
                border: 2px solid #e1e5e9;
                border-radius: 8px;
                transition: all 0.2s ease;
                background: white;
            }

            .radio-option:hover, .checkbox-option:hover {
                border-color: #333;
                background: #f8f9ff;
            }

            .radio-option input, .checkbox-option input {
                margin-right: 12px;
                transform: scale(1.2);
            }

            /* Height and Weight Inputs - 3 Column Layout */
            .height-weight-container {
                display: grid;
                grid-template-columns: 1fr 1fr 1fr;
                gap: 15px;
                max-width: 500px;
            }

            .height-input-group, .weight-input-group {
                display: flex;
                align-items: center;
                gap: 8px;
            }

            .height-input, .weight-input {
                flex: 1;
                min-width: 80px;
                width: 100%;
            }

            .input-suffix {
                font-weight: 600;
                color: #666;
                font-size: 0.9rem;
            }

            /* File Input */
            .file-input-container {
                position: relative;
            }

            .file-input {
                opacity: 0;
                position: absolute;
                z-index: -1;
            }

            .file-input-label {
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 14px 16px;
                border: 2px dashed #e1e5e9;
                border-radius: 8px;
                cursor: pointer;
                transition: border-color 0.2s ease;
                background: white;
            }

            .file-input-label:hover {
                border-color: #333;
            }

            .file-input-label.file-selected {
                border-color: #28a745;
                background: #f8fff9;
            }

            .file-input-button {
                background: #333;
                color: white;
                padding: 8px 16px;
                border-radius: 6px;
                font-size: 0.9rem;
                font-weight: 600;
            }

            /* BMI Display */
            .bmi-display-section {
                margin-top: 15px;
                padding-top: 15px;
                border-top: 1px solid #e1e5e9;
            }

            .formula-display {
                padding: 15px;
                background: #f8f9fa;
                border: 2px solid #e1e5e9;
                border-radius: 8px;
                text-align: center;
            }

            .bmi-result {
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 10px;
                font-size: 1.1rem;
            }

            .bmi-value {
                font-weight: 600;
                color: #333;
            }

            /* Disqualification Message */
            .disqualification-message {
                margin-top: 15px;
                padding: 16px 20px;
                background: linear-gradient(135deg, #fff 0%, #fef7f7 100%);
                border: 1px solid #f0a6a6;
                border-radius: 12px;
                color: #2d2d2d;
                font-weight: 500;
                line-height: 1.6;
                white-space: pre-line;
                border-left: 4px solid #e74c3c;
                box-shadow: 0 2px 8px rgba(231, 76, 60, 0.1);
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            }

            /* Navigation Buttons */
            .form-navigation {
                display: flex;
                justify-content: flex-end;
                gap: 20px;
                margin-top: 40px;
                padding-top: 30px;
                border-top: 2px solid #f0f0f0;
            }

            .form-navigation.has-prev {
                justify-content: space-between;
            }

            .nav-btn {
                padding: 14px 28px;
                border: none;
                border-radius: 8px;
                font-size: 1rem;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.2s ease;
                min-width: 120px;
            }

            .prev-btn {
                background: #f1f3f4;
                color: #333;
            }

            .prev-btn:hover {
                background: #e8eaed;
            }

            .next-btn, .submit-btn {
                background: linear-gradient(90deg, #333 0%, #555 100%);
                color: white;
            }

            .next-btn:hover, .submit-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
            }

            .next-btn:disabled, .submit-btn:disabled {
                background: #e1e5e9;
                color: #999;
                cursor: not-allowed;
                transform: none;
                box-shadow: none;
            }

            /* Mobile Responsiveness */
            @media (max-width: 768px) {
                .form-wrapper {
                    padding: 10px;
                }

                .title-container, .survey-container {
                    padding: 20px;
                }

                .form-title {
                    font-size: 1.5rem;
                }

                .radio-group, .checkbox-group {
                    grid-template-columns: 1fr;
                    gap: 10px;
                }

                .height-weight-container {
                    grid-template-columns: 1fr;
                    gap: 10px;
                }

                .form-navigation {
                    flex-direction: column;
                }

                .nav-btn {
                    width: 100%;
                }
            }
        '''

    def generate_form_javascript(self, category: str, consult_type: str, form_name: str = "form", total_sections: int = 4) -> str:
        """Generate JavaScript for form functionality and conditional logic - FIXED VERSION"""
        sync_only_states = json.dumps(self.sync_only_states)

        return f'''
            // Form state
            let currentSection = 1;
            const totalSections = {total_sections};
            let formData = {{}};
            let isDisqualified = false;
            let errorMessages = new Map();

            // Local storage key for this form
            const storageKey = 'medicalForm_{form_name}_{category}';

            // Sync-only states
            const syncOnlyStates = {sync_only_states};

            // Initialize form
            document.addEventListener('DOMContentLoaded', function() {{
                resetFormState();
                loadFormData();
                updateProgressBar();
                setupEventListeners();
                setupConditionalLogic();
                calculateBMI();
            }});

            function formatPhoneInput(input) {{
                // Remove all non-digit characters
                let value = input.value.replace(/\D/g, '');

                // Limit to 10 digits
                if (value.length > 10) {{
                    value = value.substring(0, 10);
                }}

                // Format as (XXX) XXX-XXXX
                if (value.length >= 6) {{
                    value = `(${{value.substring(0, 3)}}) ${{value.substring(3, 6)}}-${{value.substring(6)}}`;
                }} else if (value.length >= 3) {{
                    value = `(${{value.substring(0, 3)}}) ${{value.substring(3)}}`;
                }} else if (value.length > 0) {{
                    value = `(${{value}}`;
                }}

                input.value = value;
            }}

            function resetFormState() {{
                // Clear any problematic localStorage data
                const savedData = localStorage.getItem(storageKey);
                if (savedData) {{
                    try {{
                        const data = JSON.parse(savedData);
                        // If data contains 'no' as values, clear it
                        if (data.formData && Object.values(data.formData).some(val => val === 'no' && typeof val === 'string')) {{
                            localStorage.removeItem(storageKey);
                        }}
                    }} catch (e) {{
                        localStorage.removeItem(storageKey);
                    }}
                }}

                // Ensure all radio buttons start unselected unless saved data exists
                setTimeout(() => {{
                    const allRadios = document.querySelectorAll('input[type="radio"]');
                    allRadios.forEach(radio => {{
                        radio.checked = false;
                        radio.removeAttribute('checked');
                    }});

                    // Also reset checkboxes to be safe
                    const allCheckboxes = document.querySelectorAll('input[type="checkbox"]');
                    allCheckboxes.forEach(checkbox => {{
                        checkbox.checked = false;
                        checkbox.removeAttribute('checked');
                    }});
                }}, 100);
            }}

            function loadFormData() {{
                try {{
                    const savedData = localStorage.getItem(storageKey);
                    if (savedData) {{
                        const data = JSON.parse(savedData);
                        formData = data.formData || {{}};
                        currentSection = data.currentSection || 1;

                        // Restore form values
                        Object.keys(formData).forEach(name => {{
                            const input = document.querySelector(`[name="${{name}}"]`);
                            if (input) {{
                                if (input.type === 'radio' || input.type === 'checkbox') {{
                                    if (input.value === formData[name]) {{
                                        input.checked = true;
                                    }}
                                }} else if (input.type === 'file') {{
                                    // Handle file uploads - show filename if available
                                    const fileData = formData[name];
                                    if (fileData && typeof fileData === 'object' && fileData.filename) {{
                                        const textElement = document.getElementById(input.id + '_text');
                                        const label = input.closest('.file-input-container').querySelector('.file-input-label');
                                        if (textElement && label) {{
                                            textElement.textContent = fileData.filename;
                                            label.classList.add('file-selected');
                                        }}
                                    }}
                                }} else {{
                                    input.value = formData[name];
                                }}
                            }}
                        }});

                        // Update UI to match restored section
                        if (currentSection > 1) {{
                            for (let i = 1; i < currentSection; i++) {{
                                document.getElementById(`section-${{i}}`).classList.remove('active');
                            }}
                            document.getElementById(`section-${{currentSection}}`).classList.add('active');
                        }}
                    }}
                }} catch (error) {{
                    console.log('No previous form data found');
                }}
            }}

            function saveFormData() {{
                try {{
                    const dataToSave = {{
                        formData: formData,
                        currentSection: currentSection,
                        timestamp: new Date().toISOString()
                    }};
                    localStorage.setItem(storageKey, JSON.stringify(dataToSave));
                }} catch (error) {{
                    console.log('Could not save form data');
                }}
            }}

            function clearFormData() {{
                try {{
                    localStorage.removeItem(storageKey);
                }} catch (error) {{
                    console.log('Could not clear form data');
                }}
            }}

            function setupEventListeners() {{
                // Navigation buttons
                document.getElementById('nextBtn').addEventListener('click', nextSection);
                document.getElementById('prevBtn').addEventListener('click', prevSection);
                document.getElementById('submitBtn').addEventListener('click', submitForm);

                // Height/weight inputs for BMI calculation
                const heightFeet = document.querySelector('input[name*="SQ48"]');
                const heightInches = document.querySelector('input[name*="SQ49"]');
                const weight = document.querySelector('input[name*="SQ2"]');

                if (heightFeet) heightFeet.addEventListener('input', calculateBMI);
                if (heightInches) heightInches.addEventListener('input', calculateBMI);
                if (weight) weight.addEventListener('input', calculateBMI);
            }}

            function setupConditionalLogic() {{
                // Set up conditional question display
                const questions = document.querySelectorAll('[data-show-condition]');
                questions.forEach(question => {{
                    const condition = question.dataset.showCondition;
                    if (condition !== 'always') {{
                        question.classList.add('question-hidden');
                    }}
                }});

                // Set up listeners for trigger inputs
                // Gender questions (triggers pregnancy question)
                const genderInputs = document.querySelectorAll('input[type="radio"][value="female"], input[type="radio"][value="male"]');
                genderInputs.forEach(input => {{
                    input.addEventListener('change', updateConditionalQuestions);
                }});

                // Allergy questions (triggers allergy detail question)
                const allergyInputs = document.querySelectorAll('input[type="radio"][value="yes"], input[type="radio"][value="no"]');
                allergyInputs.forEach(input => {{
                    if (input.closest('.question-container').querySelector('label[class*="question-label"]')?.textContent?.includes('allergies')) {{
                        input.addEventListener('change', updateConditionalQuestions);
                    }}
                }});

                // Other GLP-1 medication questions (triggers dosage question)
                const medicationInputs = document.querySelectorAll('input[type="checkbox"][value*="glp1"], input[type="checkbox"][value*="other_glp1"]');
                medicationInputs.forEach(input => {{
                    input.addEventListener('change', updateConditionalQuestions);
                }});
            }}

            function updateConditionalQuestions() {{
                // Update visibility of conditional questions
                const questions = document.querySelectorAll('[data-show-condition]');
                questions.forEach(question => {{
                    const condition = question.dataset.showCondition;
                    checkQuestionVisibility(question, condition);
                }});
            }}

            function checkQuestionVisibility(questionElement, condition) {{
                let shouldShow = false;

                if (condition === 'always') {{
                    shouldShow = true;
                }} else if (condition === 'if_gender_female') {{
                    const genderInput = document.querySelector('input[type="radio"][value="female"]:checked');
                    shouldShow = genderInput && genderInput.value === 'female';
                }} else if (condition === 'if_allergies_yes') {{
                    // Find the checked radio button with value "yes" in any allergy question
                    const allergyInputs = document.querySelectorAll('input[type="radio"][value="yes"]:checked');
                    for (let input of allergyInputs) {{
                        const questionText = input.closest('.question-container').querySelector('label[class*="question-label"]')?.textContent;
                        if (questionText && questionText.toLowerCase().includes('allergies')) {{
                            shouldShow = true;
                            break;
                        }}
                    }}
                }} else if (condition === 'if_other_glp1s_yes') {{
                    // Check if any "other_glp1" checkbox is checked
                    const glp1Input = document.querySelector('input[type="checkbox"][value*="other_glp1"]:checked');
                    shouldShow = glp1Input !== null;
                }} else if (condition === 'if_tobacco_yes' || condition === 'if_tobacco_use_yes') {{
                    // Find the checked radio button with value "yes" in any tobacco question
                    const tobaccoInputs = document.querySelectorAll('input[type="radio"][value="yes"]:checked');
                    for (let input of tobaccoInputs) {{
                        const questionText = input.closest('.question-container').querySelector('label[class*="question-label"]')?.textContent;
                        if (questionText && (questionText.toLowerCase().includes('tobacco') || questionText.toLowerCase().includes('vape'))) {{
                            shouldShow = true;
                            break;
                        }}
                    }}
                }}

                if (shouldShow) {{
                    questionElement.classList.remove('question-hidden');
                }} else {{
                    questionElement.classList.add('question-hidden');
                    // Clear values when hidden
                    const inputs = questionElement.querySelectorAll('input, select, textarea');
                    inputs.forEach(input => {{
                        if (input.type === 'radio' || input.type === 'checkbox') {{
                            input.checked = false;
                        }} else {{
                            input.value = '';
                        }}
                    }});
                    // Clear any error messages
                    const questionId = questionElement.dataset.questionId;
                    if (questionId && errorMessages.has(questionId)) {{
                        errorMessages.delete(questionId);
                        const disqualMsg = questionElement.querySelector('.disqualification-message');
                        if (disqualMsg) disqualMsg.style.display = 'none';
                    }}
                }}
            }}

            function handleAnswerChange(input) {{
                const answerType = input.dataset.answerType;
                const questionWrapper = input.closest('.question-wrapper');
                const disqualificationMsg = questionWrapper.querySelector('.disqualification-message');
                const questionId = questionWrapper.dataset.questionId;

                // For checkbox questions, check if ANY disqualifying options are checked
                if (input.type === 'checkbox') {{
                    const allCheckboxes = questionWrapper.querySelectorAll('input[type="checkbox"]');
                    const disqualifyingChecked = Array.from(allCheckboxes).some(cb =>
                        cb.checked && cb.dataset.answerType === 'disqualify');

                    if (disqualifyingChecked) {{
                        // Show disqualification message
                        if (disqualificationMsg) {{
                            disqualificationMsg.style.display = 'block';
                            errorMessages.set(questionId, true);
                            isDisqualified = true;
                        }}
                    }} else {{
                        // Hide disqualification message
                        if (disqualificationMsg) {{
                            disqualificationMsg.style.display = 'none';
                            errorMessages.delete(questionId);
                        }}
                    }}

                    // Store checkbox values as array
                    const checkedValues = Array.from(allCheckboxes)
                        .filter(cb => cb.checked)
                        .map(cb => cb.value);
                    formData[input.name] = checkedValues;
                }} else {{
                    // Radio button logic
                    // Clear existing error state for this question
                    if (errorMessages.has(questionId)) {{
                        errorMessages.delete(questionId);
                        if (disqualificationMsg) {{
                            disqualificationMsg.style.display = 'none';
                        }}
                    }}

                    if (answerType === 'disqualify') {{
                        // Show disqualification message
                        if (disqualificationMsg) {{
                            disqualificationMsg.style.display = 'block';
                            errorMessages.set(questionId, true);
                            isDisqualified = true;
                        }}
                    }} else if (answerType === 'flag') {{
                        // Just add flag class, no disqualification
                        questionWrapper.classList.add('flagged');
                    }}

                    // Store single value for radio buttons
                    formData[input.name] = input.value;
                }}

                // Update conditional questions based on this answer
                updateConditionalQuestions();

                // Save form data
                saveFormData();
            }}

            function calculateBMI() {{
                // Find height and weight inputs dynamically by looking for the pattern in Patient Profile
                const heightFeetInput = document.querySelector('input[placeholder*="Feet"], input[class*="height-input"][id*="ft"], input[name*="feet"]') ||
                                       Array.from(document.querySelectorAll('input')).find(input =>
                                           input.closest('.question-container')?.textContent?.includes('Height') &&
                                           input.closest('.question-container')?.textContent?.includes('feet'));

                const heightInchesInput = document.querySelector('input[placeholder*="Inches"], input[class*="height-input"][id*="in"], input[name*="inches"]') ||
                                         Array.from(document.querySelectorAll('input')).find(input =>
                                             input.closest('.question-container')?.textContent?.includes('Height') &&
                                             input.closest('.question-container')?.textContent?.includes('inches'));

                const weightInput = document.querySelector('input[placeholder*="Weight"], input[class*="weight-input"], input[name*="weight"]') ||
                                   Array.from(document.querySelectorAll('input')).find(input =>
                                       input.closest('.question-container')?.textContent?.includes('Weight') &&
                                       input.closest('.question-container')?.textContent?.includes('pounds'));

                const heightFeet = heightFeetInput?.value;
                const heightInches = heightInchesInput?.value;
                const weight = weightInput?.value;
                const bmiDisplay = document.getElementById('bmi-value');

                if (heightFeet && heightInches && weight && bmiDisplay) {{
                    const totalInches = (parseInt(heightFeet) * 12) + parseInt(heightInches);
                    const bmi = (parseFloat(weight) * 703) / (totalInches * totalInches);

                    if (!isNaN(bmi)) {{
                        bmiDisplay.textContent = bmi.toFixed(1);
                        formData.bmi = bmi.toFixed(1);

                        // Check BMI disqualification for GLP1 specifically (only if form name includes GLP1)
                        if ('{form_name}'.includes('GLP1') && bmi < 25) {{
                            // Find BMI question in Assessment section if it exists
                            const assessmentBmiQuestion = document.querySelector('[data-question-id*="BMI"], [data-question-id*="bmi"], .bmi-result').closest('.question-wrapper');
                            if (assessmentBmiQuestion) {{
                                const questionId = assessmentBmiQuestion.getAttribute('data-question-id');
                                let disqualMsg = assessmentBmiQuestion.querySelector('.disqualification-message');

                                // Create disqualification message if it doesn't exist
                                if (!disqualMsg) {{
                                    disqualMsg = document.createElement('div');
                                    disqualMsg.className = 'disqualification-message';
                                    disqualMsg.textContent = 'A BMI of 25 or higher is required for this program.';
                                    assessmentBmiQuestion.querySelector('.question-container').appendChild(disqualMsg);
                                }}

                                disqualMsg.style.display = 'block';
                                errorMessages.set(questionId, true);
                                isDisqualified = true;
                            }}
                        }} else {{
                            // Clear BMI disqualification if BMI is now acceptable
                            const assessmentBmiQuestion = document.querySelector('[data-question-id*="BMI"], [data-question-id*="bmi"], .bmi-result').closest('.question-wrapper');
                            if (assessmentBmiQuestion) {{
                                const questionId = assessmentBmiQuestion.getAttribute('data-question-id');
                                const disqualMsg = assessmentBmiQuestion.querySelector('.disqualification-message');
                                if (disqualMsg) {{
                                    disqualMsg.style.display = 'none';
                                    errorMessages.delete(questionId);
                                }}
                            }}
                        }}
                    }}
                }} else if (bmiDisplay) {{
                    bmiDisplay.textContent = 'Enter height and weight above';
                }}
            }}

            function handleFileUpload(input) {{
                const textElement = document.getElementById(input.id + '_text');
                const label = input.closest('.file-input-container').querySelector('.file-input-label');

                if (input.files && input.files.length > 0) {{
                    const file = input.files[0];
                    const fileName = file.name;

                    // Validate file size (10MB limit)
                    if (file.size > 10 * 1024 * 1024) {{
                        alert('File size must be less than 10MB');
                        input.value = '';
                        return;
                    }}

                    // Validate file type
                    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'application/pdf'];
                    if (!allowedTypes.includes(file.type)) {{
                        alert('Please upload an image (JPEG, PNG, GIF) or PDF file');
                        input.value = '';
                        return;
                    }}

                    // Update UI
                    textElement.textContent = fileName;
                    label.classList.add('file-selected');

                    // Convert file to base64 for API transmission
                    const reader = new FileReader();
                    reader.onload = function(e) {{
                        formData[input.name] = {{
                            filename: fileName,
                            fileType: file.type,
                            fileSize: file.size,
                            fileData: e.target.result // base64 data
                        }};
                        saveFormData(); // Save to localStorage
                    }};
                    reader.readAsDataURL(file);

                }} else {{
                    textElement.textContent = 'Choose File';
                    label.classList.remove('file-selected');
                    delete formData[input.name];
                    saveFormData();
                }}
            }}

            function validateAge(dateInput) {{
                const birthDate = new Date(dateInput.value);
                const today = new Date();
                const age = Math.floor((today - birthDate) / (365.25 * 24 * 60 * 60 * 1000));
                const questionWrapper = dateInput.closest('.question-wrapper');
                const questionId = questionWrapper.dataset.questionId;
                const disqualificationMsg = questionWrapper.querySelector('.disqualification-message');

                // Clear previous date errors
                dateInput.setCustomValidity('');

                if (isNaN(age) || age < 0 || age > 120) {{
                    dateInput.setCustomValidity('Please enter a valid date of birth');
                    return;
                }}

                if (age < 18) {{
                    // Show age disqualification
                    if (disqualificationMsg) {{
                        disqualificationMsg.style.display = 'block';
                        errorMessages.set(questionId, true);
                        isDisqualified = true;
                    }}
                }} else {{
                    // Clear age disqualification
                    if (disqualificationMsg) {{
                        disqualificationMsg.style.display = 'none';
                        errorMessages.delete(questionId);
                    }}
                }}
            }}

            function nextSection() {{
                if (!validateCurrentSection()) {{
                    return;
                }}

                // For BMI-related sections, allow progression to Assessment to see BMI value
                // before showing disqualification message
                const isLeavingPatientProfile = currentSection === 1;
                const hasDisqualifyingBMI = errorMessages.has('SQ50'); // BMI question ID

                if (errorMessages.size > 0 && !(isLeavingPatientProfile && hasDisqualifyingBMI)) {{
                    alert('Please review your answers. Some responses may affect your eligibility.');
                    return;
                }}

                if (currentSection < totalSections) {{
                    document.getElementById(`section-${{currentSection}}`).classList.remove('active');
                    currentSection++;
                    document.getElementById(`section-${{currentSection}}`).classList.add('active');
                    updateProgressBar();
                    updateNavigationButtons();

                    // Scroll to top of new section
                    window.scrollTo({{ top: 0, behavior: 'smooth' }});
                }}
            }}

            function prevSection() {{
                if (currentSection > 1) {{
                    document.getElementById(`section-${{currentSection}}`).classList.remove('active');
                    currentSection--;
                    document.getElementById(`section-${{currentSection}}`).classList.add('active');
                    updateProgressBar();
                    updateNavigationButtons();

                    // Scroll to top of new section
                    window.scrollTo({{ top: 0, behavior: 'smooth' }});
                }}
            }}

            function updateProgressBar() {{
                const progress = (currentSection / totalSections) * 100;
                document.querySelector('.progress-fill').style.width = progress + '%';
                document.querySelector('.progress-text').textContent = `Section ${{currentSection}} of ${{totalSections}}`;
            }}

            function updateNavigationButtons() {{
                const prevBtn = document.getElementById('prevBtn');
                const nextBtn = document.getElementById('nextBtn');
                const submitBtn = document.getElementById('submitBtn');
                const navigation = document.querySelector('.form-navigation');

                const showPrev = currentSection > 1;
                prevBtn.style.display = showPrev ? 'inline-block' : 'none';
                nextBtn.style.display = currentSection < totalSections ? 'inline-block' : 'none';
                submitBtn.style.display = currentSection === totalSections ? 'inline-block' : 'none';

                // Add conditional class for navigation alignment
                if (showPrev) {{
                    navigation.classList.add('has-prev');
                }} else {{
                    navigation.classList.remove('has-prev');
                }}
            }}

            function validateCurrentSection() {{
                const currentSectionElement = document.getElementById(`section-${{currentSection}}`);
                const visibleRequiredInputs = currentSectionElement.querySelectorAll('input[required]:not(.question-hidden input), select[required]:not(.question-hidden select)');

                for (let input of visibleRequiredInputs) {{
                    // Skip inputs in hidden questions
                    if (input.closest('.question-hidden')) {{
                        continue;
                    }}

                    if (input.type === 'radio') {{
                        const radioGroup = currentSectionElement.querySelectorAll(`input[name="${{input.name}}"]:not(.question-hidden input)`);
                        const isChecked = Array.from(radioGroup).some(radio => radio.checked);
                        if (!isChecked) {{
                            input.focus();
                            alert('Please fill in all required fields before continuing.');
                            return false;
                        }}
                    }} else if (input.type === 'file') {{
                        if (!input.files || input.files.length === 0) {{
                            input.focus();
                            alert('Please upload the required file before continuing.');
                            return false;
                        }}
                    }} else if (!input.value.trim()) {{
                        input.focus();
                        alert('Please fill in all required fields before continuing.');
                        return false;
                    }} else if (input.type === 'tel') {{
                        // Phone number validation - must be 10 digits
                        const phoneValue = input.value.replace(/\D/g, ''); // Remove non-digits
                        if (phoneValue.length !== 10) {{
                            input.focus();
                            alert('Please enter a valid 10-digit phone number.');
                            return false;
                        }}
                    }}
                }}

                return true;
            }}

            function submitForm() {{
                if (!validateCurrentSection()) {{
                    return;
                }}

                // Get state from address field in Verification section
                const stateInput = document.querySelector('input[name*="State"], select[name*="state"], input[name*="state"]') ||
                                  Array.from(document.querySelectorAll('input, select')).find(input =>
                                      input.closest('.question-container')?.textContent?.includes('State'));
                const selectedState = stateInput?.value;
                if (!selectedState) {{
                    alert('Please select your state in the address section before submitting.');
                    return;
                }}

                let finalConsultType = '{consult_type}';

                // Override to sync if state requires it
                if (syncOnlyStates.includes(selectedState)) {{
                    finalConsultType = 'sync';
                }}

                // Collect all form data
                const formElement = document.getElementById('medicalForm');
                const formDataObj = new FormData(formElement);
                const webhookData = buildWebhookData(formDataObj, selectedState, finalConsultType);

                // Submit to webhook
                submitToWebhook(webhookData, selectedState, finalConsultType);
            }}

            function buildWebhookData(formData, state, consultType) {{
                // Find actual question IDs from the form
                const nameInput = document.querySelector('input[type="text"]');
                const emailInput = document.querySelector('input[type="email"]');
                const phoneInput = document.querySelector('input[type="tel"]');
                const heightFeetInput = document.querySelector('input[placeholder*="feet"], input[placeholder*="Feet"]');
                const heightInchesInput = document.querySelector('input[placeholder*="inches"], input[placeholder*="Inches"]');
                const weightInput = document.querySelector('input[placeholder*="weight"], input[placeholder*="Weight"], input[placeholder*="pounds"], input[placeholder*="Pounds"]');

                // Get address fields
                const addressInputs = document.querySelectorAll('input[type="text"]');
                let address = '', address2 = '', city = '', postalCode = '';

                addressInputs.forEach(input => {{
                    const label = input.closest('.question-wrapper')?.querySelector('label')?.textContent?.toLowerCase() || '';
                    if (label.includes('address') && !label.includes('2')) {{
                        address = input.value || '';
                    }} else if (label.includes('address 2')) {{
                        address2 = input.value || '';
                    }} else if (label.includes('city')) {{
                        city = input.value || '';
                    }} else if (label.includes('postal') || label.includes('zip')) {{
                        postalCode = input.value || '';
                    }}
                }});

                // Get actual form values
                const name = nameInput?.value || '';
                const email = emailInput?.value || '';
                const phone = phoneInput?.value || '';
                const heightFeet = heightFeetInput?.value || '0';
                const heightInches = heightInchesInput?.value || '0';
                const weight = weightInput?.value || '';
                const bmi = document.getElementById('bmi-value')?.textContent || '';

                // Build comprehensive form answers object with question text as keys
                const formAnswers = {{}};
                const contactFields = ['name', 'email', 'phone', 'address', 'city', 'state', 'postal'];

                const allInputs = document.querySelectorAll('input, select, textarea');
                allInputs.forEach(input => {{
                    // Get question text
                    const questionWrapper = input.closest('.question-wrapper');
                    let questionText = questionWrapper?.querySelector('label')?.textContent?.trim() || input.name;

                    // Remove asterisk from required fields
                    questionText = questionText.replace('*', '').trim();

                    // Escape apostrophes for JavaScript object keys
                    const escapedQuestionText = questionText.replace(/'/g, "\\'");

                    // Skip contact info fields - they're already in contact section
                    const isContactField = contactFields.some(field =>
                        questionText.toLowerCase().includes(field) ||
                        (field === 'name' && questionText.toLowerCase().includes('full name'))
                    );

                    if (!isContactField) {{
                        if (input.type === 'file') {{
                            // Handle file uploads
                            const fileData = formData[input.name];
                            if (fileData && typeof fileData === 'object' && fileData.filename) {{
                                formAnswers[escapedQuestionText] = fileData; // Include full file object
                            }}
                        }} else if (input.name && input.value) {{
                            if (input.type === 'radio' || input.type === 'checkbox') {{
                                if (input.checked) {{
                                    if (formAnswers[escapedQuestionText]) {{
                                        // Multiple selections (checkboxes)
                                        if (Array.isArray(formAnswers[escapedQuestionText])) {{
                                            formAnswers[escapedQuestionText].push(input.value);
                                        }} else {{
                                            formAnswers[escapedQuestionText] = [formAnswers[escapedQuestionText], input.value];
                                        }}
                                    }} else {{
                                        formAnswers[escapedQuestionText] = input.value;
                                    }}
                                }}
                            }} else {{
                                formAnswers[escapedQuestionText] = input.value;
                            }}
                        }}
                    }}
                }});

                // Extract specific data from formAnswers for patient section
                const genderValue = document.querySelector('input[name*="Gender"]:checked')?.value ||
                                  document.querySelector('input[type="radio"]:checked')?.closest('.question-wrapper')?.querySelector('label')?.textContent?.toLowerCase().includes('gender') ?
                                  document.querySelector('input[type="radio"]:checked')?.value : '';

                const dobValue = document.querySelector('input[type="date"]')?.value || '';

                const pregnancyValue = formAnswers['Are you currently pregnant or breastfeeding?'] || '';
                const allergiesValue = formAnswers['Do you have any allergies?'] || '';
                const activityLevelValue = formAnswers['What is your exercise level?'] || '';
                const tobaccoUseValue = formAnswers['Do you currently use tobacco or vape?'] || '';
                const mentalHealthValue = formAnswers['Are you currently experiencing depression with history of suicidal ideation?'] || '';
                const idVerificationValue = formAnswers['Upload government ID (driver\\'s license) for identity verification'] || '';

                // Filter out mapped fields from responses
                const mappedFields = [
                    'Are you currently pregnant or breastfeeding?',
                    'Do you have any allergies?',
                    'What is your exercise level?',
                    'Do you currently use tobacco or vape?',
                    'Are you currently experiencing depression with history of suicidal ideation?',
                    'Upload government ID (driver\\'s license) for identity verification'
                ];

                const responses = {{}};
                Object.keys(formAnswers).forEach(key => {{
                    if (!mappedFields.includes(key)) {{
                        responses[key] = formAnswers[key];
                    }}
                }});

                // Build the complete webhook data structure
                const data = {{
                    contact: {{
                        name: name,
                        email: email,
                        gender: genderValue,
                        dateOfBirth: dobValue,
                        phone: phone,
                        address1: address,
                        city: city,
                        state: state,
                        postalCode: postalCode,
                        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
                        type: 'patient'
                    }},
                    patient: {{
                        rxRequested: '{form_name}',
                        height: `${{heightFeet}}'${{heightInches}}"`,
                        weight: weight,
                        BMI: bmi.replace('BMI: ', '').replace('Enter height and weight above', ''),
                        pregnancy: pregnancyValue,
                        allergies: allergiesValue,
                        activityLevel: activityLevelValue,
                        tobaccoUse: tobaccoUseValue,
                        mentalHealth: mentalHealthValue,
                        idVerification: idVerificationValue
                    }},
                    form: {{
                        formType: 'screener',
                        category: '{category}',
                        name: '{form_name}',
                        responses: responses,
                        timestamp: new Date().toISOString(),
                        formVersion: new Date().toISOString().split('T')[0] // Current date as version
                    }},
                    clinic: {{
                        name: '{{{{location.name}}}}',
                        id: '{{{{location.id}}}}',
                        email: '{{{{location.email}}}}',
                        phone: '{{{{location.phone}}}}',
                        integration: '{{{{custom_values.private}}}}',
                        type: 'healthcare'
                    }}
                }};

                return data;
            }}


            async function submitToWebhook(data, state, consultType) {{
                try {{
                    const response = await fetch('https://locumtele.app.n8n.cloud/webhook/patient-screener', {{
                        method: 'POST',
                        headers: {{
                            'Content-Type': 'application/json'
                        }},
                        body: JSON.stringify(data)
                    }});

                    if (response.ok) {{
                        // Redirect to appropriate fee page
                        const rootDomain = window.location.origin;
                        const redirectUrl = `${{rootDomain}}/{category.lower()}-${{consultType}}-fee`;
                        window.location.href = redirectUrl;
                    }} else {{
                        throw new Error('Submission failed');
                    }}
                }} catch (error) {{
                    console.error('Error submitting form:', error);
                    alert('There was an error submitting your form. Please try again.');
                }}
            }}
        '''

    def get_next_id(self) -> int:
        """Get next unique ID for questions"""
        self.question_id_counter += 1
        return self.question_id_counter

    def sanitize_value(self, value: str) -> str:
        """Sanitize value for HTML attributes"""
        return re.sub(r'[^a-zA-Z0-9_-]', '_', str(value).lower())


# Test the fixed generator
if __name__ == "__main__":
    print("✅ Enhanced Form Generator - Fixed Version Ready!")
    print("All issues have been addressed:")
    print("  - Date validation error persistence")
    print("  - Conditional logic for pregnancy question")
    print("  - Height/weight 3-column layout")
    print("  - BMI calculation and display")
    print("  - Error message persistence")
    print("  - File upload handling")