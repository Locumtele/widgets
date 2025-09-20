"""
Test Suite for Python Form System

Comprehensive tests for all components of the Python form system.

Usage:
    python test_system.py
"""

import unittest
import json
from universal_form_generator import UniversalFormGenerator
from state_selector import StateSelector
from embed_handler import EmbedHandler


class TestUniversalFormGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = UniversalFormGenerator()

    def test_simple_form_generation(self):
        """Test basic form generation"""
        form_data = {
            "title": "Test Form",
            "questions": [
                {"text": "Name", "type": "text", "required": True},
                {"text": "Email", "type": "email", "required": True}
            ]
        }
        
        html = self.generator.generate_form(form_data, 'test-container')
        
        self.assertIn('Test Form', html)
        self.assertIn('Name', html)
        self.assertIn('Email', html)
        self.assertIn('test-container', html)

    def test_question_type_detection(self):
        """Test automatic question type detection"""
        questions = [
            {"text": "What is your email address?"},
            {"text": "What is your phone number?"},
            {"text": "What is your date of birth?"},
            {"text": "What is your height?"},
            {"text": "What is your weight?"},
            {"text": "Are you pregnant?"},
            {"text": "Describe your allergies"}
        ]
        
        form_data = {"questions": questions}
        html = self.generator.generate_form(form_data, 'test-container')
        
        # Check that appropriate input types are generated
        self.assertIn('type="email"', html)
        self.assertIn('type="tel"', html)
        self.assertIn('type="text"', html)  # For date, height, weight
        self.assertIn('type="radio"', html)  # For pregnancy
        self.assertIn('textarea', html)  # For allergies

    def test_answer_logic(self):
        """Test answer logic (safe, flag, disqualify)"""
        form_data = {
            "questions": [
                {
                    "text": "Do you have diabetes?",
                    "type": "radio",
                    "options": ["No", "Type 1", "Type 2"],
                    "safeAnswers": ["No"],
                    "disqualifyAnswers": ["Type 1", "Type 2"]
                }
            ]
        }
        
        html = self.generator.generate_form(form_data, 'test-container')
        
        # Check that answer types are set
        self.assertIn('data-answer-type="safe"', html)
        self.assertIn('data-answer-type="disqualify"', html)

    def test_multi_step_form(self):
        """Test multi-step form generation"""
        form_data = {
            "title": "Multi-step Form",
            "personal_info": [
                {"text": "Name", "type": "text", "required": True},
                {"text": "Email", "type": "email", "required": True}
            ],
            "medical_info": [
                {"text": "Height", "type": "height", "required": True},
                {"text": "Weight", "type": "weight", "required": True}
            ]
        }
        
        html = self.generator.generate_form(form_data, 'test-container')
        
        self.assertIn('Multi-step Form', html)
        self.assertIn('personal_info', html)
        self.assertIn('medical_info', html)

    def test_form_validation(self):
        """Test form validation"""
        form_data = {
            "questions": [
                {"text": "Required Field", "required": True},
                {"text": "Optional Field", "required": False}
            ]
        }
        
        html = self.generator.generate_form(form_data, 'test-container')
        
        # Check that required fields have required attribute
        self.assertIn('required', html)


class TestStateSelector(unittest.TestCase):
    def setUp(self):
        self.selector = StateSelector()

    def test_state_validation(self):
        """Test state code validation"""
        # Valid states
        self.assertIsNotNone(self.selector.get_state_info("CA"))
        self.assertIsNotNone(self.selector.get_state_info("NY"))
        self.assertIsNotNone(self.selector.get_state_info("TX"))
        
        # Invalid states
        self.assertIsNone(self.selector.get_state_info("XX"))
        self.assertIsNone(self.selector.get_state_info(""))

    def test_consult_type_determination(self):
        """Test consult type determination"""
        # Sync-only states
        self.assertEqual(self.selector.determine_consult_type("AR"), "sync")
        self.assertEqual(self.selector.determine_consult_type("DC"), "sync")
        self.assertEqual(self.selector.determine_consult_type("DE"), "sync")
        
        # Async-allowed states
        self.assertEqual(self.selector.determine_consult_type("CA"), "async")
        self.assertEqual(self.selector.determine_consult_type("NY"), "async")
        self.assertEqual(self.selector.determine_consult_type("TX"), "async")

    def test_form_data_mapping(self):
        """Test form data mapping"""
        form_data = {
            "fullName": "John Doe",
            "email": "john@example.com",
            "phone": "5551234567",
            "heightFeet": "6",
            "heightInches": "0",
            "weight": "200"
        }
        
        mapped = self.selector.map_form_data(form_data)
        
        self.assertEqual(mapped["fullName"], "John Doe")
        self.assertEqual(mapped["email"], "john@example.com")
        self.assertEqual(mapped["phone"], "5551234567")

    def test_bmi_calculation(self):
        """Test BMI calculation"""
        # Test valid BMI calculation
        bmi = self.selector.calculate_bmi("6", "0", "200")
        self.assertIsNotNone(bmi)
        self.assertNotEqual(bmi, "")
        
        # Test invalid inputs
        bmi = self.selector.calculate_bmi("", "", "")
        self.assertEqual(bmi, "")
        
        bmi = self.selector.calculate_bmi("invalid", "invalid", "invalid")
        self.assertEqual(bmi, "")

    def test_webhook_data_formatting(self):
        """Test webhook data formatting"""
        form_data = {
            "fullName": "John Doe",
            "email": "john@example.com",
            "phone": "5551234567"
        }
        
        state_info = self.selector.get_state_info("CA")
        webhook_data = self.selector.format_webhook_data(
            form_data, state_info, "weightloss", "async", "123", "Test Clinic"
        )
        
        self.assertEqual(webhook_data["contact"]["name"], "John Doe")
        self.assertEqual(webhook_data["contact"]["email"], "john@example.com")
        self.assertEqual(webhook_data["contact"]["state"], "CA")
        self.assertEqual(webhook_data["patient"]["rxRequested"], "weightloss")
        self.assertEqual(webhook_data["clinic"]["id"], "123")


class TestEmbedHandler(unittest.TestCase):
    def setUp(self):
        self.handler = EmbedHandler()

    def test_embed_type_1(self):
        """Test Embed Type 1: Form Only"""
        form_data = {
            "title": "Test Form",
            "category": "weightloss",
            "questions": [
                {"text": "Name", "type": "text", "required": True}
            ]
        }
        
        result = self.handler.embed_type_1_form_only(form_data, "weightloss")
        
        self.assertEqual(result["type"], "form_only")
        self.assertIn("form_html", result)
        self.assertIn("redirect_url", result)
        self.assertIn("weightloss-state", result["redirect_url"])

    def test_embed_type_2(self):
        """Test Embed Type 2: State + API"""
        form_data = {
            "fullName": "John Doe",
            "email": "john@example.com"
        }
        
        result = self.handler.embed_type_2_state_api("CA", form_data, "weightloss")
        
        self.assertEqual(result["type"], "state_api")
        self.assertEqual(result["state_code"], "CA")
        self.assertIn("redirect_url", result)
        self.assertIn("consult_type", result)

    def test_embed_type_3(self):
        """Test Embed Type 3: Sync Calendar"""
        result = self.handler.embed_type_3_sync_calendar("weightloss")
        
        self.assertEqual(result["type"], "sync_calendar")
        self.assertIn("calendar_html", result)
        self.assertIn("redirect_url", result)
        self.assertIn("weightloss-consult-booked", result["redirect_url"])

    def test_embed_info(self):
        """Test embed information retrieval"""
        info = self.handler.get_embed_info()
        
        self.assertIn("embed_types", info)
        self.assertIn("sync_only_states", info)
        self.assertIn("api_endpoint", info)
        
        # Check embed types
        self.assertIn("type_1", info["embed_types"])
        self.assertIn("type_2", info["embed_types"])
        self.assertIn("type_3", info["embed_types"])


class TestIntegration(unittest.TestCase):
    def test_end_to_end_flow(self):
        """Test complete end-to-end flow"""
        # Step 1: Generate form
        generator = UniversalFormGenerator()
        form_data = {
            "title": "Medical Screening",
            "category": "weightloss",
            "questions": [
                {"text": "Full Name", "type": "text", "required": True},
                {"text": "Email", "type": "email", "required": True},
                {"text": "Phone", "type": "phone", "required": True}
            ]
        }
        
        form_html = generator.generate_form(form_data, 'test-container')
        self.assertIsNotNone(form_html)
        
        # Step 2: Process state selection
        selector = StateSelector()
        session_data = {
            "fullName": "John Doe",
            "email": "john@example.com",
            "phone": "5551234567"
        }
        
        redirect_url = selector.process_state_selection("CA", session_data, "weightloss")
        self.assertIsNotNone(redirect_url)
        self.assertIn("weightloss", redirect_url)
        
        # Step 3: Test embed handler
        handler = EmbedHandler()
        result = handler.embed_type_2_state_api("CA", session_data, "weightloss")
        self.assertEqual(result["state_code"], "CA")


def run_tests():
    """Run all tests"""
    print("🧪 Running Python Form System Tests...\n")
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_suite.addTest(unittest.makeSuite(TestUniversalFormGenerator))
    test_suite.addTest(unittest.makeSuite(TestStateSelector))
    test_suite.addTest(unittest.makeSuite(TestEmbedHandler))
    test_suite.addTest(unittest.makeSuite(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\n📊 Test Summary:")
    print(f"  Tests run: {result.testsRun}")
    print(f"  Failures: {len(result.failures)}")
    print(f"  Errors: {len(result.errors)}")
    
    if result.failures:
        print(f"\n❌ Failures:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")
    
    if result.errors:
        print(f"\n💥 Errors:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")
    
    if result.wasSuccessful():
        print(f"\n✅ All tests passed!")
    else:
        print(f"\n❌ Some tests failed!")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
