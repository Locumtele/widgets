/**
 * FormLoader.js - Dynamic Form Generator
 * 
 * This script loads medication JSON files and dynamically generates HTML forms
 * based on the qTemplate.html template structure.
 * 
 * Usage:
 * 1. Include this script in your HTML page
 * 2. Call FormLoader.loadForm('meds/glp1.json') to generate a form
 * 3. The form will be injected into a container with id 'form-container'
 */

class FormLoader {
    constructor() {
        this.template = null;
        this.currentFormData = null;
        this.questionIdCounter = 0;
    }

    /**
     * Load the template HTML file
     */
    async loadTemplate() {
        if (this.template) return this.template;
        
        try {
            const response = await fetch('screeners/qTemplate.html');
            this.template = await response.text();
            return this.template;
        } catch (error) {
            console.error('Error loading template:', error);
            throw error;
        }
    }

    /**
     * Load form data from JSON file
     */
    async loadFormData(jsonPath) {
        try {
            const response = await fetch(jsonPath);
            const formData = await response.json();
            this.currentFormData = formData;
            return formData;
        } catch (error) {
            console.error('Error loading form data:', error);
            throw error;
        }
    }

    /**
     * Generate form HTML from JSON data
     */
    async generateForm(jsonPath, containerId = 'form-container') {
        try {
            // Load template and form data
            await this.loadTemplate();
            const formData = await this.loadFormData(jsonPath);
            
            // Generate the form HTML
            const formHTML = this.buildFormHTML(formData);
            
            // Inject into container
            const container = document.getElementById(containerId);
            if (container) {
                container.innerHTML = formHTML;
                
                // Initialize form functionality
                this.initializeForm();
                
                return formHTML;
            } else {
                throw new Error(`Container with id '${containerId}' not found`);
            }
        } catch (error) {
            console.error('Error generating form:', error);
            throw error;
        }
    }

    /**
     * Build the complete form HTML from JSON data
     */
    buildFormHTML(formData) {
        let html = this.template;
        
        // Replace template placeholders
        html = html.replace(/\{\{FORM_TITLE\}\}/g, formData.screener);
        html = html.replace(/\{\{FORM_CATEGORY\}\}/g, formData.category);
        html = html.replace(/\{\{FORM_SUBTITLE\}\}/g, this.getFormSubtitle(formData));
        html = html.replace(/\{\{ASSESSMENT_TITLE\}\}/g, this.getAssessmentTitle(formData));
        html = html.replace(/\{\{TREATMENT_NAME\}\}/g, formData.screener);
        html = html.replace(/\{\{ASSESSMENT_QUESTIONS\}\}/g, this.generateAssessmentQuestions(formData));
        html = html.replace(/\{\{PREGNANCY_DISQUALIFICATION_MESSAGE\}\}/g, this.getPregnancyDisqualificationMessage(formData));
        html = html.replace(/\{\{CANCER_DISQUALIFICATION_MESSAGE\}\}/g, this.getCancerDisqualificationMessage(formData));
        html = html.replace(/\{\{REDIRECT_PATH\}\}/g, this.getRedirectPath(formData));
        
        return html;
    }

    /**
     * Generate assessment questions section
     */
    generateAssessmentQuestions(formData) {
        const assessmentQuestions = formData.questions.filter(q => q.section === 'Assessment');
        
        if (assessmentQuestions.length === 0) {
            return '<p>No assessment questions available.</p>';
        }

        let html = '';
        assessmentQuestions.forEach(question => {
            html += this.generateQuestionHTML(question);
        });

        return html;
    }

    /**
     * Generate HTML for a single question
     */
    generateQuestionHTML(question) {
        const questionId = `question_${question.id}`;
        const fieldName = this.getFieldName(question);
        const fieldId = `${fieldName}_${question.id}`;
        
        let html = `
            <div class="question" id="${questionId}" data-show-condition="${question.showCondition}">
                <label class="question-label" for="${fieldId}">${question.text} *</label>
        `;

        // Add disqualification message if applicable
        if (question.disqualify && question.disqualify.length > 0) {
            html += `
                <div class="disqualification-message" id="${fieldId}Disqualify" style="display: none;">
                    <strong>💡 You are not eligible for this treatment</strong><br>
                    ${question.disqualifyMessage}
                </div>
            `;
        }

        // Generate input field based on type
        html += this.generateInputField(question, fieldId, fieldName);
        
        // Add error message
        html += `
            <div class="error-message" id="${fieldId}Error">Please answer this question</div>
        </div>
        `;

        return html;
    }

    /**
     * Generate input field based on question type
     */
    generateInputField(question, fieldId, fieldName) {
        switch (question.type) {
            case 'text':
                return this.generateTextInput(question, fieldId, fieldName);
            case 'email':
                return this.generateEmailInput(question, fieldId, fieldName);
            case 'phone':
                return this.generatePhoneInput(question, fieldId, fieldName);
            case 'date':
                return this.generateDateInput(question, fieldId, fieldName);
            case 'number':
                return this.generateNumberInput(question, fieldId, fieldName);
            case 'checkbox':
                return this.generateCheckboxInput(question, fieldId, fieldName);
            case 'select':
                return this.generateSelectInput(question, fieldId, fieldName);
            case 'file':
                return this.generateFileInput(question, fieldId, fieldName);
            case 'height_feet':
                return this.generateHeightInput(question, fieldId, fieldName);
            case 'weight_pounds':
                return this.generateWeightInput(question, fieldId, fieldName);
            default:
                return this.generateTextInput(question, fieldId, fieldName);
        }
    }

    /**
     * Generate text input
     */
    generateTextInput(question, fieldId, fieldName) {
        return `
            <input type="text" id="${fieldId}" name="${fieldName}" class="text-input" placeholder="Enter your ${question.text.toLowerCase()}" required>
        `;
    }

    /**
     * Generate email input
     */
    generateEmailInput(question, fieldId, fieldName) {
        return `
            <input type="email" id="${fieldId}" name="${fieldName}" class="text-input" placeholder="Enter your email address" required>
        `;
    }

    /**
     * Generate phone input
     */
    generatePhoneInput(question, fieldId, fieldName) {
        return `
            <input type="tel" id="${fieldId}" name="${fieldName}" class="text-input" placeholder="Enter your phone number" maxlength="10" required>
        `;
    }

    /**
     * Generate date input
     */
    generateDateInput(question, fieldId, fieldName) {
        return `
            <input type="text" id="${fieldId}" name="${fieldName}" class="text-input" placeholder="MM/DD/YYYY" maxlength="10" required>
        `;
    }

    /**
     * Generate number input
     */
    generateNumberInput(question, fieldId, fieldName) {
        const min = question.safe.includes('any_valid') ? '' : 'min="1"';
        return `
            <input type="number" id="${fieldId}" name="${fieldName}" class="text-input" placeholder="Enter ${question.text.toLowerCase()}" ${min} required>
        `;
    }

    /**
     * Generate checkbox input
     */
    generateCheckboxInput(question, fieldId, fieldName) {
        let html = '<div class="option-group">';
        
        // Handle special cases for gender
        if (question.text.toLowerCase().includes('gender')) {
            html += `
                <div class="option-item">
                    <input type="radio" id="${fieldId}_male" name="${fieldName}" value="male">
                    <label for="${fieldId}_male">Male</label>
                </div>
                <div class="option-item">
                    <input type="radio" id="${fieldId}_female" name="${fieldName}" value="female">
                    <label for="${fieldId}_female">Female</label>
                </div>
            `;
        } else {
            // Generate options from safe values
            question.safe.forEach((option, index) => {
                const optionId = `${fieldId}_${index}`;
                const optionValue = this.sanitizeValue(option);
                const optionLabel = this.formatLabel(option);
                
                html += `
                    <div class="option-item">
                        <input type="checkbox" id="${optionId}" name="${fieldName}" value="${optionValue}">
                        <label for="${optionId}">${optionLabel}</label>
                    </div>
                `;
            });
        }
        
        html += '</div>';
        return html;
    }

    /**
     * Generate select input
     */
    generateSelectInput(question, fieldId, fieldName) {
        let html = `<select id="${fieldId}" name="${fieldName}" class="text-input" required>`;
        html += '<option value="">Select an option</option>';
        
        question.safe.forEach(option => {
            const optionValue = this.sanitizeValue(option);
            const optionLabel = this.formatLabel(option);
            html += `<option value="${optionValue}">${optionLabel}</option>`;
        });
        
        html += '</select>';
        return html;
    }

    /**
     * Generate file input
     */
    generateFileInput(question, fieldId, fieldName) {
        return `
            <div class="file-input">
                <input type="file" id="${fieldId}" name="${fieldName}" accept="image/*,.pdf" required>
                Choose File
            </div>
        `;
    }

    /**
     * Generate height input (feet and inches)
     */
    generateHeightInput(question, fieldId, fieldName) {
        return `
            <div class="height-inputs">
                <div class="height-input-wrapper">
                    <input type="number" id="${fieldId}_feet" name="${fieldName}_feet" class="text-input" min="3" max="8" placeholder="Feet" required>
                    <span class="height-unit">ft</span>
                </div>
                <div class="height-input-wrapper">
                    <input type="number" id="${fieldId}_inches" name="${fieldName}_inches" class="text-input" min="0" max="11" placeholder="Inches" required>
                    <span class="height-unit">in</span>
                </div>
            </div>
        `;
    }

    /**
     * Generate weight input
     */
    generateWeightInput(question, fieldId, fieldName) {
        return `
            <input type="number" id="${fieldId}" name="${fieldName}" class="text-input" min="50" max="500" placeholder="Enter your weight in pounds" required>
        `;
    }

    /**
     * Get field name from question
     */
    getFieldName(question) {
        const text = question.text.toLowerCase();
        if (text.includes('full name')) return 'fullName';
        if (text.includes('email')) return 'email';
        if (text.includes('phone')) return 'phone';
        if (text.includes('date of birth')) return 'dateOfBirth';
        if (text.includes('gender')) return 'gender';
        if (text.includes('height')) return 'height';
        if (text.includes('weight')) return 'weight';
        if (text.includes('pregnant')) return 'pregnancy';
        if (text.includes('cancer')) return 'cancer';
        if (text.includes('allergies')) return 'allergies';
        if (text.includes('state')) return 'state';
        
        // Default to sanitized question text
        return this.sanitizeValue(question.text);
    }

    /**
     * Sanitize value for use as HTML attribute
     */
    sanitizeValue(value) {
        return value.toString()
            .toLowerCase()
            .replace(/[^a-z0-9]/g, '_')
            .replace(/_+/g, '_')
            .replace(/^_|_$/g, '');
    }

    /**
     * Format label for display
     */
    formatLabel(value) {
        if (value === 'any_text' || value === 'any_email' || value === 'any_phone' || value === 'any_valid') {
            return 'Yes';
        }
        if (value === 'none') {
            return 'No';
        }
        return value.toString().replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    }

    /**
     * Get form subtitle
     */
    getFormSubtitle(formData) {
        const subtitles = {
            'GLP1': 'Complete this screening to determine if GLP-1 therapy is right for you.',
            'nad': 'Complete this screening to determine if NAD therapy is right for you.',
            'sermorelin': 'Complete this screening to determine if Sermorelin therapy is right for you.'
        };
        return subtitles[formData.screener] || 'Complete this screening to determine if this treatment is right for you.';
    }

    /**
     * Get assessment title
     */
    getAssessmentTitle(formData) {
        return `${formData.screener} Assessment`;
    }

    /**
     * Get pregnancy disqualification message
     */
    getPregnancyDisqualificationMessage(formData) {
        const messages = {
            'GLP1': 'For the safety of you and your baby, GLP-1 medications are not recommended during pregnancy, while trying to conceive, or while breastfeeding.',
            'sermorelin': 'For your safety and your baby\'s wellbeing, Sermorelin is not recommended during pregnancy or breastfeeding.'
        };
        return messages[formData.screener] || 'This treatment is not recommended during pregnancy or breastfeeding.';
    }

    /**
     * Get cancer disqualification message
     */
    getCancerDisqualificationMessage(formData) {
        const messages = {
            'sermorelin': 'For your safety, Sermorelin therapy is not appropriate for individuals with current or previous cancer. Please discuss alternative wellness approaches with your oncologist.'
        };
        return messages[formData.screener] || 'This treatment may not be appropriate for individuals with current or previous cancer.';
    }

    /**
     * Get redirect path
     */
    getRedirectPath(formData) {
        const paths = {
            'Weightloss': 'weightloss-sync-fee',
            'Antiaging': 'antiaging-sync-fee',
            'Hormone': 'hormone-sync-fee'
        };
        return paths[formData.category] || 'consultation-fee';
    }

    /**
     * Initialize form functionality after injection
     */
    initializeForm() {
        // Add event listeners for conditional logic
        this.setupConditionalLogic();
        
        // Add validation
        this.setupValidation();
        
        // Add mobile optimizations
        this.setupMobileOptimizations();
    }

    /**
     * Setup conditional logic for questions
     */
    setupConditionalLogic() {
        // Handle gender-based pregnancy question
        const genderInputs = document.querySelectorAll('input[name="gender"]');
        genderInputs.forEach(input => {
            input.addEventListener('change', () => {
                this.togglePregnancyQuestion();
            });
        });

        // Handle other conditional questions
        const conditionalQuestions = document.querySelectorAll('[data-show-condition]');
        conditionalQuestions.forEach(question => {
            const condition = question.getAttribute('data-show-condition');
            this.setupConditionalQuestion(question, condition);
        });
    }

    /**
     * Toggle pregnancy question based on gender
     */
    togglePregnancyQuestion() {
        const genderFemale = document.querySelector('input[name="gender"][value="female"]');
        const pregnancyQuestions = document.querySelectorAll('[data-show-condition="if_gender_female"]');
        
        if (genderFemale && pregnancyQuestions.length > 0) {
            pregnancyQuestions.forEach(question => {
                question.style.display = genderFemale.checked ? 'block' : 'none';
            });
        }
    }

    /**
     * Setup conditional question display
     */
    setupConditionalQuestion(question, condition) {
        // This is a simplified implementation
        // In a full implementation, you'd parse the condition and set up appropriate listeners
        if (condition === 'if_gender_female') {
            question.style.display = 'none';
        }
    }

    /**
     * Setup form validation
     */
    setupValidation() {
        const form = document.querySelector('form');
        if (form) {
            form.addEventListener('submit', (e) => {
                e.preventDefault();
                this.validateForm();
            });
        }
    }

    /**
     * Validate the form
     */
    validateForm() {
        const requiredFields = document.querySelectorAll('input[required], select[required]');
        let isValid = true;

        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                this.showFieldError(field, 'This field is required');
                isValid = false;
            } else {
                this.hideFieldError(field);
            }
        });

        if (isValid) {
            this.submitForm();
        }
    }

    /**
     * Show field error
     */
    showFieldError(field, message) {
        const errorElement = document.getElementById(field.id + 'Error');
        if (errorElement) {
            errorElement.textContent = message;
            errorElement.style.display = 'block';
        }
        field.classList.add('error');
    }

    /**
     * Hide field error
     */
    hideFieldError(field) {
        const errorElement = document.getElementById(field.id + 'Error');
        if (errorElement) {
            errorElement.style.display = 'none';
        }
        field.classList.remove('error');
    }

    /**
     * Submit the form
     */
    submitForm() {
        console.log('Form submitted successfully');
        // Add your form submission logic here
    }

    /**
     * Setup mobile optimizations
     */
    setupMobileOptimizations() {
        // Prevent zoom on input focus for iOS
        const inputs = document.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.addEventListener('focus', function() {
                if (window.innerWidth <= 768 && this.style.fontSize !== '16px') {
                    this.style.fontSize = '16px';
                }
            });
        });
    }
}

// Create global instance
window.FormLoader = new FormLoader();

// Auto-initialize if data attributes are present
document.addEventListener('DOMContentLoaded', () => {
    const formContainer = document.querySelector('[data-form-loader]');
    if (formContainer) {
        const jsonPath = formContainer.getAttribute('data-json-path');
        if (jsonPath) {
            window.FormLoader.generateForm(jsonPath, formContainer.id);
        }
    }
});
