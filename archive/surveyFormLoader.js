/**
 * SurveyFormLoader.js - Multi-Step Survey Form Generator
 *
 * Creates survey-style forms where each section is a "slide" that displays one at a time
 * Based on the original FormLoader but with slide navigation functionality
 */

class SurveyFormLoader {
    constructor() {
        this.template = null;
        this.currentFormData = null;
        this.currentSlide = 0;
        this.totalSlides = 0;
        this.slides = [];
        this.formData = {};
    }

    /**
     * Generate survey form from N8n data structure
     */
    async generateSurveyForm(formData, containerId = 'form-container') {
        try {
            this.currentFormData = formData;
            this.processFormSections(formData);

            // Generate the survey HTML
            const surveyHTML = this.buildSurveyHTML();

            // Inject into container
            const container = document.getElementById(containerId);
            if (container) {
                container.innerHTML = surveyHTML;

                // Initialize survey functionality
                this.initializeSurvey();

                return surveyHTML;
            } else {
                throw new Error(`Container with id '${containerId}' not found`);
            }
        } catch (error) {
            console.error('Error generating survey form:', error);
            throw error;
        }
    }

    /**
     * Process form sections from N8n data structure
     */
    processFormSections(formData) {
        this.slides = [];

        // Extract sections from the form data
        // Assuming structure: { formName: "NAD+", "Patient Profile": [...], "Assessment": [...], etc. }
        Object.keys(formData).forEach(key => {
            if (Array.isArray(formData[key]) && key !== 'formId' && key !== 'formName') {
                const section = {
                    title: key,
                    questions: formData[key],
                    id: this.sanitizeValue(key)
                };
                this.slides.push(section);
            }
        });

        this.totalSlides = this.slides.length;
    }

    /**
     * Build the complete survey HTML
     */
    buildSurveyHTML() {
        const formTitle = this.currentFormData.formName || 'Form';

        return `
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
                <title>${formTitle} Survey</title>
                <link rel="stylesheet" href="components/formStyle.css">
                <style>
                    /* Survey-specific styles */
                    .survey-container {
                        max-width: 800px;
                        margin: 0 auto;
                        padding: 2rem;
                    }

                    .survey-header {
                        text-align: center;
                        margin-bottom: 2rem;
                    }

                    .progress-bar {
                        width: 100%;
                        height: 8px;
                        background: #e1e5e9;
                        border-radius: 4px;
                        margin: 1rem 0;
                        overflow: hidden;
                    }

                    .progress-fill {
                        height: 100%;
                        background: linear-gradient(90deg, #007bff, #0056b3);
                        border-radius: 4px;
                        transition: width 0.3s ease;
                        width: 0%;
                    }

                    .progress-text {
                        font-size: 0.9rem;
                        color: #666;
                        margin-top: 0.5rem;
                    }

                    .slide {
                        display: none;
                        animation: slideIn 0.3s ease-in-out;
                    }

                    .slide.active {
                        display: block;
                    }

                    @keyframes slideIn {
                        from {
                            opacity: 0;
                            transform: translateX(20px);
                        }
                        to {
                            opacity: 1;
                            transform: translateX(0);
                        }
                    }

                    .slide-content {
                        min-height: 400px;
                        padding: 2rem 0;
                    }

                    .navigation-buttons {
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        margin-top: 2rem;
                        padding-top: 2rem;
                        border-top: 1px solid #e1e5e9;
                    }

                    .nav-button {
                        padding: 0.75rem 2rem;
                        border: none;
                        border-radius: 6px;
                        font-size: 1rem;
                        font-weight: 600;
                        cursor: pointer;
                        transition: all 0.2s ease;
                    }

                    .nav-button-primary {
                        background: #007bff;
                        color: white;
                    }

                    .nav-button-primary:hover {
                        background: #0056b3;
                    }

                    .nav-button-secondary {
                        background: #f8f9fa;
                        color: #666;
                        border: 1px solid #e1e5e9;
                    }

                    .nav-button-secondary:hover {
                        background: #e9ecef;
                    }

                    .nav-button:disabled {
                        opacity: 0.5;
                        cursor: not-allowed;
                    }

                    .question-group h2 {
                        color: #333;
                        margin-bottom: 1.5rem;
                        font-size: 1.5rem;
                    }

                    /* Mobile optimizations */
                    @media (max-width: 768px) {
                        .survey-container {
                            padding: 1rem;
                        }

                        .slide-content {
                            min-height: 300px;
                            padding: 1rem 0;
                        }

                        .nav-button {
                            padding: 0.6rem 1.5rem;
                            font-size: 0.9rem;
                        }
                    }
                </style>
            </head>
            <body>
                <div class="survey-container">
                    <!-- Survey Header -->
                    <div class="survey-header">
                        <h1>${formTitle} Assessment</h1>
                        <p>Complete this survey to determine your eligibility</p>

                        <!-- Progress Bar -->
                        <div class="progress-bar">
                            <div class="progress-fill" id="progressFill"></div>
                        </div>
                        <div class="progress-text">
                            <span id="currentStep">1</span> of <span id="totalSteps">${this.totalSlides}</span>
                        </div>
                    </div>

                    <!-- Survey Form -->
                    <form id="surveyForm">
                        ${this.generateSlides()}

                        <!-- Navigation -->
                        <div class="navigation-buttons">
                            <button type="button" class="nav-button nav-button-secondary" id="prevButton" onclick="window.surveyLoader.previousSlide()">
                                ← Previous
                            </button>

                            <button type="button" class="nav-button nav-button-primary" id="nextButton" onclick="window.surveyLoader.nextSlide()">
                                Next →
                            </button>

                            <button type="submit" class="nav-button nav-button-primary" id="submitButton" style="display: none;">
                                Submit Assessment
                            </button>
                        </div>
                    </form>

                    <!-- Loading indicator -->
                    <div class="loading" id="loadingIndicator" style="display: none;">
                        <div class="spinner"></div>
                        <p>Submitting your assessment...</p>
                    </div>

                    <!-- Success message -->
                    <div id="successMessage" class="success-message" style="display: none;">
                        <h3>✅ Assessment submitted successfully!</h3>
                        <p>Redirecting you to the next step...</p>
                    </div>
                </div>

                <script>
                    ${this.generateSurveyScript()}
                </script>
            </body>
            </html>
        `;
    }

    /**
     * Generate slides HTML
     */
    generateSlides() {
        return this.slides.map((slide, index) => `
            <div class="slide ${index === 0 ? 'active' : ''}" id="slide-${index}">
                <div class="slide-content">
                    <div class="question-group">
                        <h2 class="question-title">${slide.title}</h2>
                        ${this.generateSlideQuestions(slide.questions)}
                    </div>
                </div>
            </div>
        `).join('');
    }

    /**
     * Generate questions for a slide
     */
    generateSlideQuestions(questions) {
        return questions.map(question => this.generateQuestionHTML(question)).join('');
    }

    /**
     * Generate HTML for a single question
     */
    generateQuestionHTML(question) {
        const questionId = `q_${this.sanitizeValue(question.name || question.questionText)}`;
        const isRequired = question.required === true || question.required === 'true';

        let html = `
            <div class="question" id="${questionId}_container" data-question-type="${question.questionType}">
                <label class="question-label" for="${questionId}">
                    ${question.questionText || question.name}${isRequired ? ' *' : ''}
                </label>
        `;

        // Add disqualification message if applicable
        if (question.disqualifyAnswers && question.disqualifyAnswers.length > 0) {
            html += `
                <div class="disqualification-message" id="${questionId}_disqualify" style="display: none;">
                    <strong>💡 You are not eligible for this treatment</strong><br>
                    ${question.disqualifyMessage || 'This answer disqualifies you from treatment.'}
                </div>
            `;
        }

        // Generate input field based on type
        html += this.generateInputField(question, questionId);

        // Add error message
        html += `
            <div class="error-message" id="${questionId}_error">Please answer this question</div>
        </div>
        `;

        return html;
    }

    /**
     * Generate input field based on question type
     */
    generateInputField(question, questionId) {
        const questionType = question.questionType || 'text';

        switch (questionType) {
            case 'text':
                return `<input type="text" id="${questionId}" name="${questionId}" class="text-input" placeholder="${question.placeholder || ''}" ${question.required ? 'required' : ''}>`;

            case 'email':
                return `<input type="email" id="${questionId}" name="${questionId}" class="text-input" placeholder="Enter your email address" ${question.required ? 'required' : ''}>`;

            case 'phone':
                return `<input type="tel" id="${questionId}" name="${questionId}" class="text-input" placeholder="Enter your phone number" ${question.required ? 'required' : ''}>`;

            case 'number':
                return `<input type="number" id="${questionId}" name="${questionId}" class="text-input" placeholder="${question.placeholder || ''}" ${question.required ? 'required' : ''}>`;

            case 'radio':
                return this.generateRadioOptions(question, questionId);

            case 'checkbox':
                return this.generateCheckboxOptions(question, questionId);

            case 'select':
                return this.generateSelectOptions(question, questionId);

            case 'textarea':
                return `<textarea id="${questionId}" name="${questionId}" class="textarea-input" rows="4" placeholder="${question.placeholder || ''}" ${question.required ? 'required' : ''}></textarea>`;

            case 'file':
                return `
                    <div class="file-input">
                        <input type="file" id="${questionId}" name="${questionId}" accept="image/*,.pdf" ${question.required ? 'required' : ''}>
                        Choose File
                    </div>
                `;

            default:
                return `<input type="text" id="${questionId}" name="${questionId}" class="text-input" placeholder="${question.placeholder || ''}" ${question.required ? 'required' : ''}>`;
        }
    }

    /**
     * Generate radio button options
     */
    generateRadioOptions(question, questionId) {
        const safeAnswers = question.safeAnswers || [];
        const disqualifyAnswers = question.disqualifyAnswers || [];
        const flagAnswers = question.flagAnswers || [];

        // Combine all possible answers
        const allAnswers = [...new Set([...safeAnswers, ...disqualifyAnswers, ...flagAnswers])];

        let html = '<div class="option-group">';

        allAnswers.forEach((answer, index) => {
            const optionId = `${questionId}_${index}`;
            const optionValue = this.sanitizeValue(answer);
            const optionLabel = this.formatLabel(answer);

            html += `
                <div class="option-item">
                    <input type="radio" id="${optionId}" name="${questionId}" value="${optionValue}" data-answer-type="${this.getAnswerType(answer, question)}">
                    <label for="${optionId}">${optionLabel}</label>
                </div>
            `;
        });

        html += '</div>';
        return html;
    }

    /**
     * Generate checkbox options
     */
    generateCheckboxOptions(question, questionId) {
        const safeAnswers = question.safeAnswers || [];

        let html = '<div class="option-group">';

        safeAnswers.forEach((answer, index) => {
            const optionId = `${questionId}_${index}`;
            const optionValue = this.sanitizeValue(answer);
            const optionLabel = this.formatLabel(answer);

            html += `
                <div class="option-item">
                    <input type="checkbox" id="${optionId}" name="${questionId}" value="${optionValue}">
                    <label for="${optionId}">${optionLabel}</label>
                </div>
            `;
        });

        html += '</div>';
        return html;
    }

    /**
     * Generate select options
     */
    generateSelectOptions(question, questionId) {
        const safeAnswers = question.safeAnswers || [];

        let html = `<select id="${questionId}" name="${questionId}" class="text-input" ${question.required ? 'required' : ''}>`;
        html += '<option value="">Select an option</option>';

        safeAnswers.forEach(answer => {
            const optionValue = this.sanitizeValue(answer);
            const optionLabel = this.formatLabel(answer);
            html += `<option value="${optionValue}">${optionLabel}</option>`;
        });

        html += '</select>';
        return html;
    }

    /**
     * Get answer type (safe, disqualify, flag)
     */
    getAnswerType(answer, question) {
        if (question.safeAnswers && question.safeAnswers.includes(answer)) return 'safe';
        if (question.disqualifyAnswers && question.disqualifyAnswers.includes(answer)) return 'disqualify';
        if (question.flagAnswers && question.flagAnswers.includes(answer)) return 'flag';
        return 'safe';
    }

    /**
     * Generate survey JavaScript
     */
    generateSurveyScript() {
        return `
            // Survey loader instance
            window.surveyLoader = {
                currentSlide: 0,
                totalSlides: ${this.totalSlides},
                formData: {},

                // Navigate to next slide
                nextSlide: function() {
                    if (this.validateCurrentSlide()) {
                        this.saveCurrentSlideData();

                        if (this.currentSlide < this.totalSlides - 1) {
                            this.currentSlide++;
                            this.updateSlideDisplay();
                        }
                    }
                },

                // Navigate to previous slide
                previousSlide: function() {
                    if (this.currentSlide > 0) {
                        this.currentSlide--;
                        this.updateSlideDisplay();
                    }
                },

                // Update slide display
                updateSlideDisplay: function() {
                    // Hide all slides
                    document.querySelectorAll('.slide').forEach(slide => {
                        slide.classList.remove('active');
                    });

                    // Show current slide
                    const currentSlideElement = document.getElementById('slide-' + this.currentSlide);
                    if (currentSlideElement) {
                        currentSlideElement.classList.add('active');
                    }

                    // Update progress bar
                    const progress = ((this.currentSlide + 1) / this.totalSlides) * 100;
                    const progressFill = document.getElementById('progressFill');
                    if (progressFill) {
                        progressFill.style.width = progress + '%';
                    }

                    // Update step counter
                    const currentStep = document.getElementById('currentStep');
                    if (currentStep) {
                        currentStep.textContent = this.currentSlide + 1;
                    }

                    // Update navigation buttons
                    this.updateNavigationButtons();

                    // Check for disqualifications
                    this.checkDisqualifications();
                },

                // Update navigation button states
                updateNavigationButtons: function() {
                    const prevButton = document.getElementById('prevButton');
                    const nextButton = document.getElementById('nextButton');
                    const submitButton = document.getElementById('submitButton');

                    if (prevButton) {
                        prevButton.style.display = this.currentSlide === 0 ? 'none' : 'block';
                    }

                    if (this.currentSlide === this.totalSlides - 1) {
                        if (nextButton) nextButton.style.display = 'none';
                        if (submitButton) submitButton.style.display = 'block';
                    } else {
                        if (nextButton) nextButton.style.display = 'block';
                        if (submitButton) submitButton.style.display = 'none';
                    }
                },

                // Validate current slide
                validateCurrentSlide: function() {
                    const currentSlideElement = document.getElementById('slide-' + this.currentSlide);
                    if (!currentSlideElement) return true;

                    const requiredFields = currentSlideElement.querySelectorAll('[required]');
                    let isValid = true;

                    requiredFields.forEach(field => {
                        if (!this.validateField(field)) {
                            isValid = false;
                        }
                    });

                    // Validate radio groups
                    const radioGroups = this.getRadioGroups(currentSlideElement);
                    radioGroups.forEach(groupName => {
                        if (!this.validateRadioGroup(groupName)) {
                            isValid = false;
                        }
                    });

                    return isValid;
                },

                // Validate individual field
                validateField: function(field) {
                    const errorElement = document.getElementById(field.id + '_error');
                    let isValid = true;
                    let errorMessage = '';

                    if (field.hasAttribute('required') && !field.value.trim()) {
                        isValid = false;
                        errorMessage = 'This field is required';
                    }

                    // Email validation
                    if (isValid && field.type === 'email' && field.value && !this.isValidEmail(field.value)) {
                        isValid = false;
                        errorMessage = 'Please enter a valid email address';
                    }

                    // Phone validation
                    if (isValid && field.type === 'tel' && field.value && !this.isValidPhone(field.value)) {
                        isValid = false;
                        errorMessage = 'Please enter a valid phone number';
                    }

                    this.showFieldValidation(field, errorElement, isValid, errorMessage);
                    return isValid;
                },

                // Validate radio group
                validateRadioGroup: function(groupName) {
                    const radios = document.querySelectorAll('input[name="' + groupName + '"]');
                    const isSelected = Array.from(radios).some(radio => radio.checked);

                    if (!isSelected && radios.length > 0) {
                        const errorElement = document.getElementById(groupName + '_error');
                        if (errorElement) {
                            errorElement.style.display = 'block';
                            errorElement.textContent = 'Please select an option';
                        }
                        return false;
                    } else {
                        const errorElement = document.getElementById(groupName + '_error');
                        if (errorElement) {
                            errorElement.style.display = 'none';
                        }
                        return true;
                    }
                },

                // Get radio groups in current slide
                getRadioGroups: function(slideElement) {
                    const radioInputs = slideElement.querySelectorAll('input[type="radio"]');
                    const groups = new Set();
                    radioInputs.forEach(radio => {
                        groups.add(radio.name);
                    });
                    return Array.from(groups);
                },

                // Show field validation
                showFieldValidation: function(field, errorElement, isValid, errorMessage) {
                    if (isValid) {
                        field.classList.remove('error');
                        if (errorElement) errorElement.style.display = 'none';
                    } else {
                        field.classList.add('error');
                        if (errorElement) {
                            errorElement.textContent = errorMessage;
                            errorElement.style.display = 'block';
                        }
                    }
                },

                // Save current slide data
                saveCurrentSlideData: function() {
                    const currentSlideElement = document.getElementById('slide-' + this.currentSlide);
                    if (!currentSlideElement) return;

                    const inputs = currentSlideElement.querySelectorAll('input, select, textarea');
                    inputs.forEach(input => {
                        if (input.type === 'radio' || input.type === 'checkbox') {
                            if (input.checked) {
                                if (input.type === 'checkbox') {
                                    if (!this.formData[input.name]) this.formData[input.name] = [];
                                    if (!this.formData[input.name].includes(input.value)) {
                                        this.formData[input.name].push(input.value);
                                    }
                                } else {
                                    this.formData[input.name] = input.value;
                                }
                            }
                        } else {
                            this.formData[input.name] = input.value;
                        }
                    });
                },

                // Check for disqualifications
                checkDisqualifications: function() {
                    const currentSlideElement = document.getElementById('slide-' + this.currentSlide);
                    if (!currentSlideElement) return;

                    const radioInputs = currentSlideElement.querySelectorAll('input[type="radio"]:checked');

                    radioInputs.forEach(radio => {
                        if (radio.dataset.answerType === 'disqualify') {
                            const questionContainer = radio.closest('.question');
                            const disqualifyElement = questionContainer.querySelector('.disqualification-message');
                            if (disqualifyElement) {
                                disqualifyElement.style.display = 'block';
                            }
                        }
                    });
                },

                // Email validation
                isValidEmail: function(email) {
                    const emailRegex = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;
                    return emailRegex.test(email);
                },

                // Phone validation
                isValidPhone: function(phone) {
                    const phoneRegex = /^\\d{10}$/;
                    return phoneRegex.test(phone.replace(/\\D/g, ''));
                },

                // Submit form
                submitForm: async function() {
                    this.saveCurrentSlideData();

                    // Show loading
                    const loadingIndicator = document.getElementById('loadingIndicator');
                    const submitButton = document.getElementById('submitButton');

                    if (loadingIndicator) loadingIndicator.style.display = 'block';
                    if (submitButton) submitButton.disabled = true;

                    try {
                        // Add metadata
                        this.formData.formType = '${this.currentFormData.formName || 'Survey'}';
                        this.formData.timestamp = new Date().toISOString();
                        this.formData.userAgent = navigator.userAgent;
                        this.formData.url = window.location.href;

                        console.log('Submitting survey data:', this.formData);

                        // Submit to API
                        const response = await fetch('https://locumtele.app.n8n.cloud/webhook/patient-screener', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify(this.formData)
                        });

                        if (response.ok) {
                            const successMessage = document.getElementById('successMessage');
                            if (successMessage) successMessage.style.display = 'block';

                            // Redirect logic would go here
                            console.log('Survey submitted successfully');
                        } else {
                            throw new Error('Submission failed');
                        }

                    } catch (error) {
                        console.error('Survey submission error:', error);
                        alert('There was an error submitting your survey. Please try again.');
                    } finally {
                        if (loadingIndicator) loadingIndicator.style.display = 'none';
                        if (submitButton) submitButton.disabled = false;
                    }
                }
            };

            // Initialize survey on load
            document.addEventListener('DOMContentLoaded', function() {
                window.surveyLoader.updateSlideDisplay();

                // Form submission handler
                document.getElementById('surveyForm').addEventListener('submit', function(e) {
                    e.preventDefault();
                    window.surveyLoader.submitForm();
                });

                // Real-time validation
                document.addEventListener('change', function(e) {
                    if (e.target.matches('input, select, textarea')) {
                        window.surveyLoader.checkDisqualifications();
                    }
                });
            });
        `;
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
}

// Create global instance
window.SurveyFormLoader = new SurveyFormLoader();

// Helper function to generate survey from N8n data
window.generateSurveyFromN8nData = function(formData, containerId) {
    return window.SurveyFormLoader.generateSurveyForm(formData, containerId);
};