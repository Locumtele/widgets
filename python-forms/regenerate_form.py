"""
Regenerate the GLP1 form with all fixes applied
"""

from enhanced_form_generator import EnhancedFormGenerator

# Your actual GLP1 JSON data with complete structure
GLP1_FORM_DATA = {
    "id": "27382abf-7eae-8085-816d-df3c924f3a92",
    "name": "GLP1",
    "property_category": "Weightloss",
    "property_consult_type": "async",
    "sections": {
        "Patient Profile": [
            {
                "questionId": "SQ42",
                "questionText": "Full Name",
                "questionType": "text",
                "required": True,
                "showCondition": "always",
                "safeAnswers": ["any_text"],
                "flagAnswers": [],
                "disqualifyAnswers": [],
                "disqualifyMessage": ""
            },
            {
                "questionId": "SQ43",
                "questionText": "Email Address",
                "questionType": "email",
                "required": True,
                "showCondition": "always",
                "safeAnswers": ["any_email"],
                "flagAnswers": [],
                "disqualifyAnswers": [],
                "disqualifyMessage": ""
            },
            {
                "questionId": "SQ44",
                "questionText": "Phone Number",
                "questionType": "phone",
                "required": True,
                "showCondition": "always",
                "safeAnswers": ["any_phone"],
                "flagAnswers": [],
                "disqualifyAnswers": [],
                "disqualifyMessage": ""
            },
            {
                "questionId": "SQ45",
                "questionText": "Date of Birth",
                "questionType": "date",
                "required": True,
                "showCondition": "always",
                "safeAnswers": ["18+_years_old"],
                "flagAnswers": [],
                "disqualifyAnswers": ["under_18"],
                "disqualifyMessage": "You must be 18 years or older to use this service."
            },
            {
                "questionId": "SQ46",
                "questionText": "Gender",
                "questionType": "radio",
                "required": True,
                "showCondition": "always",
                "safeAnswers": ["male", "female"],
                "flagAnswers": [],
                "disqualifyAnswers": [],
                "disqualifyMessage": ""
            },
            {
                "questionId": "SQ47",
                "questionText": "Are you currently pregnant or breastfeeding?",
                "questionType": "radio",
                "required": True,
                "showCondition": "if_gender_female",
                "safeAnswers": ["no"],
                "flagAnswers": [],
                "disqualifyAnswers": ["yes"],
                "disqualifyMessage": "For your safety and your baby's wellbeing, this treatment is not recommended during pregnancy or breastfeeding."
            },
            {
                "questionId": "SQ48",
                "questionText": "Height (feet)",
                "questionType": "height_feet",
                "required": True,
                "showCondition": "always",
                "safeAnswers": ["up_to_7feet"],
                "flagAnswers": [],
                "disqualifyAnswers": [],
                "disqualifyMessage": ""
            },
            {
                "questionId": "SQ49",
                "questionText": "Height (inches)",
                "questionType": "height_inches",
                "required": True,
                "showCondition": "always",
                "safeAnswers": ["up_to_11inches"],
                "flagAnswers": [],
                "disqualifyAnswers": [],
                "disqualifyMessage": ""
            },
            {
                "questionId": "SQ2",
                "questionText": "Weight (pounds)",
                "questionType": "weight_pounds",
                "required": True,
                "showCondition": "always",
                "safeAnswers": ["any_number"],
                "flagAnswers": [],
                "disqualifyAnswers": [],
                "disqualifyMessage": ""
            }
        ],
        "Assessment": [
            {
                "questionId": "SQ50",
                "questionText": "BMI (auto-calculated by height and weight)",
                "questionType": "formula",
                "required": True,
                "showCondition": "always",
                "safeAnswers": ["bmi_25_or_higher"],
                "flagAnswers": [],
                "disqualifyAnswers": ["bmi_under_25"],
                "disqualifyMessage": "A BMI of 25 or higher is required for this program."
            },
            {
                "questionId": "SQ51",
                "questionText": "Have you ever had an adverse or allergic reaction to any GLP-1 receptor agonist?",
                "questionType": "checkbox",
                "required": True,
                "showCondition": "always",
                "safeAnswers": ["no"],
                "flagAnswers": [],
                "disqualifyAnswers": ["semaglutide", "tirzepatide", "dulaglutide", "exenatide", "liraglutide"],
                "disqualifyMessage": "For your safety, we cannot prescribe GLP-1 medications if you have had an allergic reaction to this type of medication before."
            },
            {
                "questionId": "SQ52",
                "questionText": "Are you taking any of the following medications?",
                "questionType": "checkbox",
                "required": True,
                "showCondition": "always",
                "safeAnswers": ["none_of_the_above"],
                "flagAnswers": ["insulin_secretagogues", "other_glp1", "insulin"],
                "disqualifyAnswers": ["abiraterone", "somatrogon", "chloroquine"],
                "disqualifyMessage": "Your current medications may interact with GLP-1 therapy. Please work with your prescribing doctor to explore safe weight management options that won't interfere with your current treatment."
            },
            {
                "questionId": "SQ53",
                "questionText": "What is your HbA1c level? (if known)",
                "questionType": "radio",
                "required": False,
                "showCondition": "always",
                "safeAnswers": ["under_7", "7_to_8", "8_to_9", "over_9", "unknown"],
                "flagAnswers": ["over_9"],
                "disqualifyAnswers": [],
                "disqualifyMessage": ""
            },
            {
                "questionId": "SQ54",
                "questionText": "Do you have a family history of diabetes?",
                "questionType": "radio",
                "required": True,
                "showCondition": "always",
                "safeAnswers": ["yes", "no", "unknown"],
                "flagAnswers": [],
                "disqualifyAnswers": [],
                "disqualifyMessage": ""
            },
            {
                "questionId": "SQ56",
                "questionText": "Upload full-body photos",
                "questionType": "file",
                "required": True,
                "showCondition": "always",
                "safeAnswers": [],
                "flagAnswers": [],
                "disqualifyAnswers": [],
                "disqualifyMessage": ""
            }
        ],
        "Medical History": [
            {
                "questionId": "SQ72",
                "questionText": "What is your exercise level?",
                "questionType": "radio",
                "required": True,
                "showCondition": "always",
                "safeAnswers": ["low", "moderate", "high"],
                "flagAnswers": [],
                "disqualifyAnswers": [],
                "disqualifyMessage": ""
            },
            {
                "questionId": "SQ73",
                "questionText": "Do you have any allergies?",
                "questionType": "radio",
                "required": True,
                "showCondition": "always",
                "safeAnswers": ["yes", "no"],
                "flagAnswers": [],
                "disqualifyAnswers": [],
                "disqualifyMessage": ""
            },
            {
                "questionId": "SQ74",
                "questionText": "If yes, please list your allergies",
                "questionType": "text",
                "required": True,
                "showCondition": "if_allergies_yes",
                "safeAnswers": ["any_text"],
                "flagAnswers": [],
                "disqualifyAnswers": [],
                "disqualifyMessage": ""
            },
            {
                "questionId": "SQ77",
                "questionText": "Are you currently experiencing depression with history of suicidal attempts, thoughts, or ideation?",
                "questionType": "radio",
                "required": True,
                "showCondition": "always",
                "safeAnswers": ["no"],
                "flagAnswers": [],
                "disqualifyAnswers": ["yes"],
                "disqualifyMessage": "We care about your safety.\n\nBecause you indicated that you are feeling depressed or having thoughts of suicide, you are not eligible to continue at this time.\n\nYou are not alone, and help is available:\n• Call or text 988 to connect with the Suicide & Crisis Lifeline.\n• If you are in immediate danger of harming yourself, call 911 or go to the nearest Emergency Department.\n\nYour wellbeing is our top priority."
            }
        ],
        "Verification": [
            {
                "questionId": "SQ78",
                "questionText": "Upload government ID (driver's license) for identity verification",
                "questionType": "file",
                "required": True,
                "showCondition": "always",
                "safeAnswers": [],
                "flagAnswers": [],
                "disqualifyAnswers": [],
                "disqualifyMessage": ""
            }
        ]
    }
}

# Remove the old form
import os
if os.path.exists("GLP1_Weightloss_Screening.html"):
    os.remove("GLP1_Weightloss_Screening.html")

print("🔧 Regenerating GLP1 form with all fixes...")

generator = EnhancedFormGenerator()
html = generator.generate_notion_form(GLP1_FORM_DATA)

filename = "GLP1_Weightloss_Screening_FIXED.html"

with open(filename, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"✅ Fixed form generated successfully!")
print(f"📄 Saved as: {filename}")
print(f"🌐 Open {filename} in your browser to test")
print()
print("🔧 FIXES APPLIED:")
print("✅ Date validation error persistence - Fixed")
print("✅ Conditional logic for pregnancy question - Fixed")
print("✅ Height/weight 3-column layout - Fixed")
print("✅ BMI calculation and display - Fixed")
print("✅ Error message persistence - Fixed")
print("✅ File upload handling - Fixed")
print()
print("🧪 TEST CHECKLIST:")
print("1. Select 'Female' gender → pregnancy question should appear")
print("2. Enter invalid date → error should clear when fixed")
print("3. Enter height/weight → BMI should calculate automatically")
print("4. Select disqualifying answer → message should appear under answers")
print("5. Change answer → disqualification should clear")
print("6. Upload file → should show filename and green border")
print("7. Navigate through all 5 sections")
print("8. Test state selector with sync-only states")