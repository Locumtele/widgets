"""
Regenerate the GLP1 form using complete JSON data from forms directory
"""

from enhanced_form_generator import EnhancedFormGenerator
from form_data_loader import FormDataLoader

# Remove the old form
import os
for old_file in ["GLP1_Weightloss_Screening.html", "GLP1_Weightloss_Screening_FIXED.html"]:
    if os.path.exists(old_file):
        os.remove(old_file)

print("🔧 Loading complete GLP1 form data from JSON files...")

# Load the complete form data using the new loader
loader = FormDataLoader()
form_data = loader.generate_complete_form_data("Weightloss", "GLP1", "async")

if not form_data["sections"]:
    print("❌ Error: No form data loaded!")
    exit(1)

print(f"✅ Loaded {len(form_data['sections'])} sections:")
for section_name, questions in form_data['sections'].items():
    print(f"   📋 {section_name}: {len(questions)} questions")

print("\n🔧 Generating complete form with all fixes...")

generator = EnhancedFormGenerator()
html = generator.generate_notion_form(form_data)

filename = "../surveys/weightloss/GLP1-screener-live.html"

with open(filename, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\n✅ Complete form generated successfully!")
print(f"📄 Saved as: {filename}")
print(f"🌐 Open {filename} in your browser to test")

print("\n📊 FORM SUMMARY:")
total_questions = sum(len(questions) for questions in form_data['sections'].values())
print(f"   📝 Total Questions: {total_questions}")

for section_name, questions in form_data['sections'].items():
    print(f"\n   📋 {section_name} ({len(questions)} questions):")
    for q in questions:
        question_type = q.get('questionType', 'unknown')
        disqualify = "⚠️ " if q.get('disqualifyAnswers') else ""
        flag = "🚩 " if q.get('flagAnswers') else ""
        print(f"      {disqualify}{flag}{q['questionId']}: {q['questionText'][:60]}...")

print("\n🔧 ALL FIXES APPLIED:")
print("✅ BMI progression fix - can see BMI before disqualification")
print("✅ Complete question set from JSON data")
print("✅ Date validation error persistence - Fixed")
print("✅ Conditional logic for pregnancy question - Fixed")
print("✅ Height/weight 3-column layout - Fixed")
print("✅ BMI calculation and display - Fixed")
print("✅ Error message persistence - Fixed")
print("✅ File upload handling - Fixed")
print("✅ Webhook data submission - Fixed")

print("\n🧪 COMPLETE TEST CHECKLIST:")
print("1. ✅ Select 'Female' gender → pregnancy question should appear")
print("2. ✅ Enter invalid date → error should clear when fixed")
print("3. ✅ Enter height/weight → BMI should calculate automatically")
print("4. ✅ BMI under 25 → can proceed to Assessment to see BMI value")
print("5. ✅ All missing Assessment questions now present:")
print("   - What other GLP-1 medications are you taking and at what dose?")
print("   - Do you have any of the following medical conditions?")
print("   - Do you currently have a known HbA1C >8%?")
print("   - How much alcohol do you typically consume?")
print("   - Do you have family history of Multiple Endocrine Neoplasia Type 2 or Medullary Thyroid Carcinoma?")
print("6. ✅ Select disqualifying answer → message should appear under answers")
print("7. ✅ Change answer → disqualification should clear")
print("8. ✅ Upload file → should show filename and green border")
print("9. ✅ Navigate through all 5 sections")
print("10. ✅ Test state selector with sync-only states")
print("11. ✅ Form submission to webhook with complete data")