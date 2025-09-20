/**
 * Universal Form Loader
 * 
 * A flexible, unified system that can generate forms from any JSON data structure.
 * Automatically detects form structure and generates appropriate HTML with logic and validation.
 * 
 * Usage:
 * const formLoader = new UniversalFormLoader();
 * await formLoader.generateForm(formData, 'container-id');
 */

class UniversalFormLoader {
    constructor() {
        this.currentFormData = null;
        this.formConfig = null;
        this.questionIdCounter = 0;
        this.conditionalLogic = new Map();
        this.disqualificationTriggered = false;
    }

    /**
     * Generate form from any JSON data structure
     * @param {Object} formData - The form data (any structure)
     * @param {string} containerId - Container element ID
     * @param {Object} options - Additional options
     */
    async generateForm(formData, containerId = 'form-container', options = {}) {
        try {
            this.currentFormData = formData;
            this.formConfig = this.analyzeFormStructure(formData);
            
            // Generate the form HTML
            const formHTML = this.buildFormHTML(options);
            
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
     * Analyze form structure to determine the best rendering approach
     */
    analyzeFormStructure(formData) {
        const config = {
            type: 'single', // 'single', 'multi-step', 'survey'
            sections: [],
            questions: [],
            metadata: {}
        };

        // Detect form type and structure
        if (Array.isArray(formData)) {
            // Simple array of questions
            config.type = 'single';
            config.questions = formData;
        } else if (typeof formData === 'object') {
            // Object structure - analyze properties
            const keys = Object.keys(formData);
            
            // Check for common form metadata
            config.metadata = {
                title: formData.title || formData.formName || formData.screener || 'Form',
                subtitle: formData.subtitle || formData.description || '',
                category: formData.category || formData.type || 'general'
            };

            // Check if it's a multi-section form
            const sectionKeys = keys.filter(key => 
                Array.isArray(formData[key]) && 
                !['questions', 'metadata', 'config'].includes(key)
            );

            if (sectionKeys.length > 1) {
                // Multi-section form
                config.type = 'multi-step';
                config.sections = sectionKeys.map(key => ({
                    title: key,
                    questions: formData[key],
                    id: this.sanitizeValue(key)
                }));
            } else if (sectionKeys.length === 1) {
                // Single section with questions
                config.type = 'single';
                config.questions = formData[sectionKeys[0]];
            } else if (formData.questions) {
                // Questions property
                config.type = 'single';
                config.questions = formData.questions;
            } else {
                // Try to find any array property
                const arrayProps = keys.filter(key => Array.isArray(formData[key]));
                if (arrayProps.length > 0) {
                    config.questions = formData[arrayProps[0]];
                }
            }
        }

        return config;
    }

    /**
     * Build the complete form HTML
     */
    buildFormHTML(options = {}) {
        const { 
            showProgress = true, 
            allowBackNavigation = true,
            submitText = 'Submit Form',
            theme = 'default'
        } = options;

        const { metadata, type, sections, questions } = this.formConfig;

        let html = `
            <div class="universal-form-container" data-form-type="${type}">
                <!-- Form Header -->
                <div class="form-header">
                    <h1 class="form-title">${metadata.title}</h1>
                    ${metadata.subtitle ? `<p class="form-subtitle">${metadata.subtitle}</p>` : ''}
                </div>
        `;

        if (type === 'multi-step' && showProgress) {
            html += this.generateProgressBar(sections.length);
        }

        html += `
            <form id="universalForm" class="universal-form" data-category="${metadata.category}">
        `;

        if (type === 'multi-step') {
            html += this.generateMultiStepForm(sections);
        } else {
            html += this.generateSingleForm(questions);
        }

        html += `
                <!-- Navigation -->
                ${this.generateNavigation(type, sections?.length || 0, submitText)}
                
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
        `;

        return html;
    }

    /**
     * Generate progress bar for multi-step forms
     */
    generateProgressBar(totalSteps) {
        return `
            <div class="progress-container">
                <div class="progress-bar">
                    <div class="progress-fill" id="progressFill"></div>
                </div>
                <div class="progress-text">
                    <span id="currentStep">1</span> of <span id="totalSteps">${totalSteps}</span>
                </div>
            </div>
        `;
    }

    /**
     * Generate multi-step form
     */
    generateMultiStepForm(sections) {
        return sections.map((section, index) => `
            <div class="form-step ${index === 0 ? 'active' : ''}" id="step-${index}" data-step="${index}">
                <div class="step-content">
                    <h2 class="step-title">${section.title}</h2>
                    <div class="questions-container">
                        ${section.questions.map(question => this.generateQuestionHTML(question)).join('')}
                    </div>
                </div>
            </div>
        `).join('');
    }

    /**
     * Generate single form
     */
    generateSingleForm(questions) {
        return `
            <div class="questions-container">
                ${questions.map(question => this.generateQuestionHTML(question)).join('')}
            </div>
        `;
    }

    /**
     * Generate navigation buttons
     */
    generateNavigation(type, totalSteps, submitText) {
        if (type === 'multi-step') {
            return `
                <div class="navigation-buttons">
                    <button type="button" class="nav-button nav-button-secondary" id="prevButton" style="display: none;">
                        ← Previous
                    </button>
                    <button type="button" class="nav-button nav-button-primary" id="nextButton">
                        Next →
                    </button>
                    <button type="submit" class="nav-button nav-button-primary" id="submitButton" style="display: none;">
                        ${submitText}
                    </button>
                </div>
            `;
        } else {
            return `
                <div class="submit-container">
                    <button type="submit" class="nav-button nav-button-primary" id="submitButton">
                        ${submitText}
                    </button>
                </div>
            `;
        }
    }

    /**
     * Generate HTML for a single question
     */
    generateQuestionHTML(question) {
        const questionId = this.generateQuestionId(question);
        const fieldName = this.getFieldName(question);
        const isRequired = this.isQuestionRequired(question);
        const questionType = this.detectQuestionType(question);

        let html = `
            <div class="question" id="${questionId}_container" data-question-type="${questionType}">
                <label class="question-label" for="${questionId}">
                    ${question.text || question.questionText || question.name}${isRequired ? ' *' : ''}
                </label>
        `;

        // Generate input field based on type
        html += this.generateInputField(question, questionId, fieldName, questionType);

        // Add error message
        html += `
            <div class="error-message" id="${questionId}_error" style="display: none;">Please answer this question</div>
        </div>
        `;

        return html;
    }

    /**
     * Generate input field based on question type
     */
    generateInputField(question, questionId, fieldName, questionType) {
        switch (questionType) {
            case 'text':
                return this.generateTextInput(question, questionId, fieldName);
            case 'email':
                return this.generateEmailInput(question, questionId, fieldName);
            case 'phone':
                return this.generatePhoneInput(question, questionId, fieldName);
            case 'number':
                return this.generateNumberInput(question, questionId, fieldName);
            case 'date':
                return this.generateDateInput(question, questionId, fieldName);
            case 'radio':
                return this.generateRadioInput(question, questionId, fieldName);
            case 'checkbox':
                return this.generateCheckboxInput(question, questionId, fieldName);
            case 'select':
                return this.generateSelectInput(question, questionId, fieldName);
            case 'textarea':
                return this.generateTextareaInput(question, questionId, fieldName);
            case 'file':
                return this.generateFileInput(question, questionId, fieldName);
            case 'height':
                return this.generateHeightInput(question, questionId, fieldName);
            case 'weight':
                return this.generateWeightInput(question, questionId, fieldName);
            default:
                return this.generateTextInput(question, questionId, fieldName);
        }
    }

    /**
     * Generate text input
     */
    generateTextInput(question, questionId, fieldName) {
        return `
            <input type="text" id="${questionId}" name="${fieldName}" class="text-input" 
                   placeholder="${question.placeholder || ''}" 
                   ${this.isQuestionRequired(question) ? 'required' : ''}>
        `;
    }

    /**
     * Generate email input
     */
    generateEmailInput(question, questionId, fieldName) {
        return `
            <input type="email" id="${questionId}" name="${fieldName}" class="text-input" 
                   placeholder="Enter your email address" 
                   ${this.isQuestionRequired(question) ? 'required' : ''}>
        `;
    }

    /**
     * Generate phone input
     */
    generatePhoneInput(question, questionId, fieldName) {
        return `
            <input type="tel" id="${questionId}" name="${fieldName}" class="text-input" 
                   placeholder="Enter your phone number" maxlength="10" 
                   ${this.isQuestionRequired(question) ? 'required' : ''}>
        `;
    }

    /**
     * Generate number input
     */
    generateNumberInput(question, questionId, fieldName) {
        const min = question.min || '';
        const max = question.max || '';
        return `
            <input type="number" id="${questionId}" name="${fieldName}" class="text-input" 
                   placeholder="${question.placeholder || ''}" 
                   ${min ? `min="${min}"` : ''} ${max ? `max="${max}"` : ''} 
                   ${this.isQuestionRequired(question) ? 'required' : ''}>
        `;
    }

    /**
     * Generate date input
     */
    generateDateInput(question, questionId, fieldName) {
        return `
            <input type="text" id="${questionId}" name="${fieldName}" class="text-input" 
                   placeholder="MM/DD/YYYY" maxlength="10" 
                   ${this.isQuestionRequired(question) ? 'required' : ''}>
        `;
    }

    /**
     * Generate radio input
     */
    generateRadioInput(question, questionId, fieldName) {
        const options = this.getQuestionOptions(question);
        let html = '<div class="option-group">';

        options.forEach((option, index) => {
            const optionId = `${questionId}_${index}`;
            const optionValue = this.sanitizeValue(option);
            const optionLabel = this.formatLabel(option);
            const answerType = this.getAnswerType(option, question);

            html += `
                <div class="option-item">
                    <input type="radio" id="${optionId}" name="${fieldName}" value="${optionValue}" 
                           data-answer-type="${answerType}" data-question-id="${questionId}">
                    <label for="${optionId}">${optionLabel}</label>
                </div>
            `;
        });

        html += '</div>';
        return html;
    }

    /**
     * Generate checkbox input
     */
    generateCheckboxInput(question, questionId, fieldName) {
        const options = this.getQuestionOptions(question);
        let html = '<div class="option-group">';

        options.forEach((option, index) => {
            const optionId = `${questionId}_${index}`;
            const optionValue = this.sanitizeValue(option);
            const optionLabel = this.formatLabel(option);

            html += `
                <div class="option-item">
                    <input type="checkbox" id="${optionId}" name="${fieldName}" value="${optionValue}">
                    <label for="${optionId}">${optionLabel}</label>
                </div>
            `;
        });

        html += '</div>';
        return html;
    }

    /**
     * Generate select input
     */
    generateSelectInput(question, questionId, fieldName) {
        const options = this.getQuestionOptions(question);
        let html = `<select id="${questionId}" name="${fieldName}" class="text-input" ${this.isQuestionRequired(question) ? 'required' : ''}>`;
        html += '<option value="">Select an option</option>';

        options.forEach(option => {
            const optionValue = this.sanitizeValue(option);
            const optionLabel = this.formatLabel(option);
            const answerType = this.getAnswerType(option, question);
            html += `<option value="${optionValue}" data-answer-type="${answerType}">${optionLabel}</option>`;
        });

        html += '</select>';
        return html;
    }

    /**
     * Generate textarea input
     */
    generateTextareaInput(question, questionId, fieldName) {
        return `
            <textarea id="${questionId}" name="${fieldName}" class="textarea-input" 
                      rows="${question.rows || 4}" 
                      placeholder="${question.placeholder || ''}" 
                      ${this.isQuestionRequired(question) ? 'required' : ''}></textarea>
        `;
    }

    /**
     * Generate file input
     */
    generateFileInput(question, questionId, fieldName) {
        return `
            <div class="file-input">
                <input type="file" id="${questionId}" name="${fieldName}" 
                       accept="${question.accept || 'image/*,.pdf'}" 
                       ${this.isQuestionRequired(question) ? 'required' : ''}>
                Choose File
            </div>
        `;
    }

    /**
     * Generate height input (feet and inches)
     */
    generateHeightInput(question, questionId, fieldName) {
        return `
            <div class="height-inputs">
                <div class="height-input-wrapper">
                    <input type="number" id="${questionId}_feet" name="${fieldName}_feet" 
                           class="text-input" min="3" max="8" placeholder="Feet" required>
                    <span class="height-unit">ft</span>
                </div>
                <div class="height-input-wrapper">
                    <input type="number" id="${questionId}_inches" name="${fieldName}_inches" 
                           class="text-input" min="0" max="11" placeholder="Inches" required>
                    <span class="height-unit">in</span>
                </div>
            </div>
        `;
    }

    /**
     * Generate weight input
     */
    generateWeightInput(question, questionId, fieldName) {
        return `
            <input type="number" id="${questionId}" name="${fieldName}" class="text-input" 
                   min="50" max="500" placeholder="Enter your weight in pounds" 
                   ${this.isQuestionRequired(question) ? 'required' : ''}>
        `;
    }

    /**
     * Detect question type from question data
     */
    detectQuestionType(question) {
        // Check explicit type first
        if (question.type || question.questionType) {
            return (question.type || question.questionType).toLowerCase();
        }

        // Detect from text content
        const text = (question.text || question.questionText || question.name || '').toLowerCase();
        
        if (text.includes('email')) return 'email';
        if (text.includes('phone') || text.includes('number')) return 'phone';
        if (text.includes('date') || text.includes('birth')) return 'date';
        if (text.includes('height')) return 'height';
        if (text.includes('weight')) return 'weight';
        if (text.includes('gender') || text.includes('sex')) return 'radio';
        if (text.includes('pregnant') || text.includes('cancer')) return 'radio';
        if (text.includes('allergies') || text.includes('describe')) return 'textarea';
        if (text.includes('upload') || text.includes('file') || text.includes('id')) return 'file';
        
        // Check for options to determine input type
        if (question.options || question.safeAnswers || question.safe) {
            if (question.multiple || question.allowMultiple) {
                return 'checkbox';
            } else {
                return 'radio';
            }
        }

        // Default to text
        return 'text';
    }

    /**
     * Get question options from various possible structures
     */
    getQuestionOptions(question) {
        return question.options || 
               question.safeAnswers || 
               question.safe || 
               question.choices || 
               question.values || 
               [];
    }

    /**
     * Check if question is required
     */
    isQuestionRequired(question) {
        return question.required === true || 
               question.required === 'true' || 
               question.required === 1 ||
               (question.text && question.text.includes('*'));
    }

    /**
     * Get field name from question
     */
    getFieldName(question) {
        if (question.name) return question.name;
        if (question.field) return question.field;
        
        const text = question.text || question.questionText || '';
        return this.sanitizeValue(text);
    }

    /**
     * Generate unique question ID
     */
    generateQuestionId(question) {
        if (question.id) return question.id;
        
        const text = question.text || question.questionText || question.name || 'question';
        return `q_${this.sanitizeValue(text)}_${++this.questionIdCounter}`;
    }

    /**
     * Get answer type (safe, disqualify, flag)
     */
    getAnswerType(answer, question) {
        if (question.safeAnswers && question.safeAnswers.includes(answer)) return 'safe';
        if (question.disqualifyAnswers && question.disqualifyAnswers.includes(answer)) return 'disqualify';
        if (question.flagAnswers && question.flagAnswers.includes(answer)) return 'flag';
        if (question.safe && question.safe.includes(answer)) return 'safe';
        if (question.disqualify && question.disqualify.includes(answer)) return 'disqualify';
        return 'safe';
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
     * Initialize form functionality
     */
    initializeForm() {
        this.setupEventListeners();
        this.setupConditionalLogic();
        this.setupValidation();
        this.setupMobileOptimizations();
    }

    /**
     * Setup event listeners
     */
    setupEventListeners() {
        const form = document.getElementById('universalForm');
        if (!form) return;

        // Form submission
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleFormSubmission();
        });

        // Real-time validation
        form.addEventListener('input', (e) => {
            this.validateField(e.target);
        });

        // Navigation for multi-step forms
        const nextButton = document.getElementById('nextButton');
        const prevButton = document.getElementById('prevButton');
        
        if (nextButton) {
            nextButton.addEventListener('click', () => this.nextStep());
        }
        
        if (prevButton) {
            prevButton.addEventListener('click', () => this.previousStep());
        }
    }

    /**
     * Setup conditional logic
     */
    setupConditionalLogic() {
        // Listen for all radio button and select changes
        const form = document.getElementById('universalForm');
        if (!form) return;

        form.addEventListener('change', (e) => {
            if (e.target.type === 'radio' || e.target.tagName === 'SELECT') {
                this.checkAnswerLogic(e.target);
            }
        });
    }

    /**
     * Check answer logic for safe/flag/disqualify
     */
    checkAnswerLogic(input) {
        const answerType = input.dataset.answerType;
        const questionId = input.dataset.questionId || input.name;
        
        console.log(`Answer selected: ${input.value}, Type: ${answerType}, Question: ${questionId}`);

        if (answerType === 'disqualify') {
            this.handleDisqualification(input);
        } else if (answerType === 'flag') {
            this.handleFlaggedAnswer(input);
        } else if (answerType === 'safe') {
            this.handleSafeAnswer(input);
        }
    }

    /**
     * Handle disqualification
     */
    handleDisqualification(input) {
        console.log('Disqualification triggered');
        this.disqualificationTriggered = true;
        
        // Show disqualification message
        const disqualifyMessage = document.getElementById('disqualificationMessage');
        if (disqualifyMessage) {
            disqualifyMessage.style.display = 'block';
        }

        // Hide form and show disqualification
        const form = document.getElementById('universalForm');
        if (form) {
            form.style.display = 'none';
        }

        // Scroll to disqualification message
        disqualifyMessage.scrollIntoView({ behavior: 'smooth' });
    }

    /**
     * Handle flagged answer
     */
    handleFlaggedAnswer(input) {
        console.log('Flagged answer selected');
        // You can add specific logic for flagged answers here
        // For example, show a warning or note
    }

    /**
     * Handle safe answer
     */
    handleSafeAnswer(input) {
        console.log('Safe answer selected');
        // You can add specific logic for safe answers here
    }

    /**
     * Setup validation
     */
    setupValidation() {
        // Basic validation setup - can be expanded
        console.log('Validation system initialized');
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

    /**
     * Handle form submission
     */
    async handleFormSubmission() {
        try {
            // Check if disqualified
            if (this.disqualificationTriggered) {
                console.log('Form submission blocked - user disqualified');
                return;
            }

            const formData = this.collectFormData();
            console.log('Form data collected:', formData);
            
            // Show loading
            this.showLoading(true);
            
            // Store form data in sessionStorage for state selector to use
            sessionStorage.setItem('formData', JSON.stringify(formData));
            
            // Show success message
            this.showSuccess();
            
            // Redirect to state selection (no webhook submission yet)
            const category = this.formConfig.metadata.category || 'weightloss';
            
            // Get root domain from embedding site
            let rootDomain = window.location.origin;
            try {
                if (window.parent && window.parent !== window) {
                    rootDomain = window.parent.location.origin;
                } else if (window.top && window.top !== window) {
                    rootDomain = window.top.location.origin;
                } else if (document.referrer) {
                    const referrerUrl = new URL(document.referrer);
                    rootDomain = referrerUrl.origin;
                }
            } catch (error) {
                console.log('Using current domain for redirect:', rootDomain);
            }
            
            const stateSelectionUrl = `${rootDomain}/${category}-state`;
            
            setTimeout(() => {
                window.location.href = stateSelectionUrl;
            }, 2000);
            
        } catch (error) {
            console.error('Form submission error:', error);
            alert('There was an error submitting your form. Please try again.');
        } finally {
            this.showLoading(false);
        }
    }

    /**
     * Collect form data
     */
    collectFormData() {
        const form = document.getElementById('universalForm');
        const formData = new FormData(form);
        const data = {};

        for (let [key, value] of formData.entries()) {
            if (data[key]) {
                if (Array.isArray(data[key])) {
                    data[key].push(value);
                } else {
                    data[key] = [data[key], value];
                }
            } else {
                data[key] = value;
            }
        }

        // Add metadata
        data.formType = this.formConfig.metadata.title;
        data.category = this.formConfig.metadata.category;
        data.timestamp = new Date().toISOString();
        data.userAgent = navigator.userAgent;
        data.url = window.location.href;

        return data;
    }

    /**
     * Show/hide loading indicator
     */
    showLoading(show) {
        const loading = document.getElementById('loadingIndicator');
        if (loading) {
            loading.style.display = show ? 'block' : 'none';
        }
    }

    /**
     * Show success message
     */
    showSuccess() {
        const success = document.getElementById('successMessage');
        if (success) {
            success.style.display = 'block';
        }
    }

    /**
     * Validate individual field
     */
    validateField(field) {
        // Basic validation - can be expanded
        const errorElement = document.getElementById(field.id + '_error');
        if (field.hasAttribute('required') && !field.value.trim()) {
            if (errorElement) {
                errorElement.style.display = 'block';
                errorElement.textContent = 'This field is required';
            }
            field.classList.add('error');
            return false;
        } else {
            if (errorElement) {
                errorElement.style.display = 'none';
            }
            field.classList.remove('error');
            return true;
        }
    }

    /**
     * Check conditional logic for a question
     */
    checkConditionalLogic(question) {
        // This would be expanded based on your specific needs
        const inputs = question.querySelectorAll('input[type="radio"]:checked');
        inputs.forEach(input => {
            if (input.dataset.answerType === 'disqualify') {
                const disqualifyElement = question.querySelector('.disqualification-message');
                if (disqualifyElement) {
                    disqualifyElement.style.display = 'block';
                }
            }
        });
    }

    /**
     * Navigate to next step (multi-step forms)
     */
    nextStep() {
        // Implementation for multi-step navigation
        console.log('Next step');
    }

    /**
     * Navigate to previous step (multi-step forms)
     */
    previousStep() {
        // Implementation for multi-step navigation
        console.log('Previous step');
    }
}

// Create global instance
window.UniversalFormLoader = new UniversalFormLoader();

// Helper function for easy usage
window.generateForm = function(formData, containerId, options) {
    return window.UniversalFormLoader.generateForm(formData, containerId, options);
};
