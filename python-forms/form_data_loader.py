"""
Form Data Loader - Loads form data from JSON files in the forms directory
"""
import json
import os
from typing import Dict, List, Any

class FormDataLoader:
    def __init__(self, base_path: str = "."):
        self.base_path = base_path

    def load_general_sections(self) -> Dict[str, List[Dict]]:
        """Load general sections (Patient Profile, Medical History, Verification)"""
        general_path = os.path.join(self.base_path, "..", "surveys", "all-forms")
        sections = {}

        section_files = {
            "Patient Profile": "patient-profile.json",
            "Medical History": "medical-history.json",
            "Verification": "verification.json"
        }

        for section_name, filename in section_files.items():
            file_path = os.path.join(general_path, filename)
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Parse the JSON data (skip the form metadata at top)
                    lines = content.strip().split('\n')
                    json_start = None
                    for i, line in enumerate(lines):
                        if line.strip() == '{' or line.strip().startswith('{"id"'):
                            # Check if this is the main data object (has "questions" key)
                            try:
                                test_json = '\n'.join(lines[i:])
                                test_data = json.loads(test_json)
                                if 'questions' in test_data:
                                    json_start = i
                                    break
                            except:
                                continue

                    if json_start:
                        json_content = '\n'.join(lines[json_start:])
                        try:
                            data = json.loads(json_content)
                            questions = data.get('questions', [])
                            sections[section_name] = self._convert_questions(questions)
                        except json.JSONDecodeError as e:
                            print(f"JSON parse error in {section_name}: {e}")

        return sections

    def load_form_assessment(self, category: str, form_name: str) -> List[Dict]:
        """Load assessment questions for a specific form"""
        surveys_path = os.path.join(self.base_path, "..", "surveys", category.lower())
        filename = f"{form_name}-screener.json"
        file_path = os.path.join(surveys_path, filename)

        if not os.path.exists(file_path):
            print(f"Warning: Assessment file not found: {file_path}")
            return []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                questions = data.get('questions', [])
                return self._convert_questions(questions)
        except json.JSONDecodeError as e:
            print(f"JSON parse error in assessment: {e}")
            return []

    def _convert_questions(self, questions: List[Dict]) -> List[Dict]:
        """Convert Notion JSON format to our form generator format"""
        converted = []

        for q in questions:
            # Create question ID from the last part of the Notion ID
            question_id = q['id'].split('-')[-1][:4].upper()  # Take last 4 chars and uppercase
            if not question_id.startswith('SQ'):
                question_id = f"SQ{question_id}"

            converted_q = {
                "questionId": question_id,
                "questionText": q.get('property_question_text', q.get('name', '')),
                "questionType": q.get('property_question_type', 'text'),
                "required": q.get('property_required', True),
                "showCondition": q.get('property_show_condition', 'always'),
                "safeAnswers": q.get('property_safe_answers', []),
                "flagAnswers": q.get('property_flag_answers', []),
                "disqualifyAnswers": q.get('property_disqualify_answers', []),
                "disqualifyMessage": q.get('property_disqualify_message', '')
            }

            converted.append(converted_q)

        # Sort by order if available
        for i, converted_q in enumerate(converted):
            original_q = questions[i] if i < len(questions) else {}
            converted_q['_original_order'] = original_q.get('property_order', 999)

        converted.sort(key=lambda x: x.get('_original_order', 999))

        # Remove the temporary sort key
        for q in converted:
            q.pop('_original_order', None)

        return converted

    def generate_complete_form_data(self, category: str, form_name: str, consult_type: str = "async") -> Dict:
        """Generate complete form data structure combining general sections and form-specific assessment"""

        # Load general sections
        general_sections = self.load_general_sections()

        # Load form-specific assessment
        assessment_questions = self.load_form_assessment(category, form_name)

        # Create complete form structure
        form_data = {
            "id": f"auto-generated-{category}-{form_name}",
            "name": form_name,
            "property_category": category,
            "property_consult_type": consult_type,
            "sections": {}
        }

        # Add general sections
        for section_name, questions in general_sections.items():
            form_data["sections"][section_name] = questions

        # Add assessment section
        if assessment_questions:
            form_data["sections"]["Assessment"] = assessment_questions

        # Ensure State Selection section exists (this is handled by the form generator)

        return form_data

    def list_available_forms(self) -> List[Dict[str, str]]:
        """List all available forms in the surveys directory"""
        surveys_path = os.path.join(self.base_path, "..", "surveys")
        forms = []

        if os.path.exists(surveys_path):
            for category_dir in os.listdir(surveys_path):
                category_path = os.path.join(surveys_path, category_dir)
                if os.path.isdir(category_path):
                    for filename in os.listdir(category_path):
                        if filename.endswith('-screener.json'):
                            form_name = filename.replace('-screener.json', '')
                            forms.append({
                                "category": category_dir.title(),
                                "form_name": form_name,
                                "filename": filename
                            })

        return forms

if __name__ == "__main__":
    # Test the loader
    loader = FormDataLoader()

    print("Available forms:")
    forms = loader.list_available_forms()
    for form in forms:
        print(f"  {form['category']} - {form['form_name']}")

    print("\nLoading GLP1 form data...")
    form_data = loader.generate_complete_form_data("Weightloss", "GLP1")

    print(f"Sections loaded: {list(form_data['sections'].keys())}")
    for section_name, questions in form_data['sections'].items():
        print(f"  {section_name}: {len(questions)} questions")