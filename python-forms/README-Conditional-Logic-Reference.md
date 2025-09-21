# Show Condition Patterns for Form Questions

This document explains how to use the `property_show_condition` field in your JSON data to control when questions appear.

## Available Show Conditions

### 1. `"always"`
- **Usage**: Question is always visible
- **Example**: Basic information fields like name, email, phone number

### 2. `"if_gender_female"`
- **Usage**: Question appears only when user selects "Female" for gender
- **Example**: Pregnancy/breastfeeding questions
- **Trigger**: Any radio button with `value="female"` is selected

### 3. `"if_allergies_yes"`
- **Usage**: Question appears when user indicates they have allergies
- **Example**: "Please list your allergies" follow-up question
- **Trigger**: Any radio button with `value="yes"` is selected in a question containing the word "allergies"

### 4. `"if_other_glp1s_yes"`
- **Usage**: Question appears when user indicates they're taking other GLP-1 medications
- **Example**: "What other GLP-1 medications are you taking and at what dose?"
- **Trigger**: Any checkbox with value containing "other_glp1" is checked

## How to Add New Show Conditions

To add new conditional logic patterns:

1. **Identify the trigger**: What user action should show/hide the question?
2. **Choose a condition name**: Use descriptive names like `if_[trigger]_[value]`
3. **Update the JavaScript**: Add the new condition to `checkQuestionVisibility()` function

### Example: Adding tobacco follow-up questions

If you want a follow-up question for tobacco users:

```json
{
  "property_show_condition": "if_tobacco_yes"
}
```

Then add to the JavaScript:
```javascript
} else if (condition === 'if_tobacco_yes') {
    const tobaccoInputs = document.querySelectorAll('input[type="radio"][value="yes"]:checked');
    for (let input of tobaccoInputs) {
        const questionText = input.closest('.question-container').querySelector('label[class*="question-label"]')?.textContent;
        if (questionText && questionText.toLowerCase().includes('tobacco')) {
            shouldShow = true;
            break;
        }
    }
}
```

## Current Implementation Details

The conditional logic system:

1. **Hides questions by default**: Any question with `property_show_condition` other than "always" starts hidden
2. **Dynamic evaluation**: Conditions are re-evaluated whenever form inputs change
3. **Cross-section support**: Questions can be conditional based on answers from any section
4. **Automatic cleanup**: When questions are hidden, their values are cleared

## Best Practices

1. **Use descriptive names**: `if_diabetes_yes` is better than `if_condition_1`
2. **Test thoroughly**: Always test conditional logic with different answer combinations
3. **Consider UX**: Don't hide too many questions behind conditions - it can confuse users
4. **Clear validation**: Hidden questions should not be required or should have their validation cleared

## Common Patterns

- **Follow-up details**: `if_[main_answer]_yes` for detail questions
- **Gender-specific**: `if_gender_[male/female]` for gender-specific questions
- **Condition-based**: `if_[medical_condition]_yes` for condition-specific questions
- **Medication-based**: `if_[medication_name]_yes` for medication-specific questions