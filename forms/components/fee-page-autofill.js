/**
 * Fee Page Autofill Script
 * 
 * This script automatically fills contact information on fee pages
 * using URL parameters passed from the state selector.
 * 
 * Usage: Include this script on your fee pages
 * <script src="forms/components/fee-page-autofill.js"></script>
 */

(function() {
    'use strict';
    
    // Function to get URL parameter value
    function getUrlParameter(name) {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get(name) || '';
    }
    
    // Function to set field value
    function setFieldValue(selector, value) {
        const field = document.querySelector(selector);
        if (field && value) {
            field.value = value;
            // Trigger change event for any listeners
            field.dispatchEvent(new Event('change', { bubbles: true }));
        }
    }
    
    // Function to set field value by name attribute
    function setFieldValueByName(name, value) {
        const field = document.querySelector(`input[name="${name}"], select[name="${name}"], textarea[name="${name}"]`);
        if (field && value) {
            field.value = value;
            field.dispatchEvent(new Event('change', { bubbles: true }));
        }
    }
    
    // Function to set field value by ID
    function setFieldValueById(id, value) {
        const field = document.getElementById(id);
        if (field && value) {
            field.value = value;
            field.dispatchEvent(new Event('change', { bubbles: true }));
        }
    }
    
    // Function to set field value by placeholder text
    function setFieldValueByPlaceholder(placeholder, value) {
        const field = document.querySelector(`input[placeholder*="${placeholder}"], textarea[placeholder*="${placeholder}"]`);
        if (field && value) {
            field.value = value;
            field.dispatchEvent(new Event('change', { bubbles: true }));
        }
    }
    
    // Function to set field value by label text
    function setFieldValueByLabel(labelText, value) {
        const labels = document.querySelectorAll('label');
        for (let label of labels) {
            if (label.textContent.toLowerCase().includes(labelText.toLowerCase())) {
                const field = label.querySelector('input, select, textarea') || 
                             document.getElementById(label.getAttribute('for'));
                if (field && value) {
                    field.value = value;
                    field.dispatchEvent(new Event('change', { bubbles: true }));
                }
                break;
            }
        }
    }
    
    // Main autofill function
    function autofillContactInfo() {
        // Get URL parameters
        const name = getUrlParameter('name');
        const email = getUrlParameter('email');
        const phone = getUrlParameter('phone');
        const state = getUrlParameter('state');
        const stateName = getUrlParameter('state_name');
        const category = getUrlParameter('category');
        const consultType = getUrlParameter('consult_type');
        
        console.log('Autofilling contact info:', { name, email, phone, state, category, consultType });
        
        // Try multiple methods to find and fill fields
        
        // Name field
        if (name) {
            setFieldValue('input[name="name"], input[name="fullName"], input[name="full_name"], input[name="patientName"]', name);
            setFieldValueById('name, fullName, full_name, patientName', name);
            setFieldValueByPlaceholder('name, full name, patient name', name);
            setFieldValueByLabel('name, full name, patient name', name);
        }
        
        // Email field
        if (email) {
            setFieldValue('input[type="email"], input[name="email"], input[name="emailAddress"]', email);
            setFieldValueById('email, emailAddress', email);
            setFieldValueByPlaceholder('email, email address', email);
            setFieldValueByLabel('email, email address', email);
        }
        
        // Phone field
        if (phone) {
            setFieldValue('input[type="tel"], input[name="phone"], input[name="phoneNumber"]', phone);
            setFieldValueById('phone, phoneNumber', phone);
            setFieldValueByPlaceholder('phone, phone number', phone);
            setFieldValueByLabel('phone, phone number', phone);
        }
        
        // State field
        if (state) {
            setFieldValue('select[name="state"], input[name="state"]', state);
            setFieldValueById('state', state);
            setFieldValueByPlaceholder('state', state);
            setFieldValueByLabel('state', state);
        }
        
        // Set hidden fields for tracking
        setFieldValue('input[name="form_category"], input[name="category"]', category);
        setFieldValue('input[name="consult_type"], input[name="consultType"]', consultType);
        setFieldValue('input[name="source_state"], input[name="selectedState"]', state);
        
        // Log success
        if (name || email || phone) {
            console.log('Contact information autofilled successfully');
        }
    }
    
    // Auto-run when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', autofillContactInfo);
    } else {
        autofillContactInfo();
    }
    
    // Also run after a short delay to catch dynamically loaded forms
    setTimeout(autofillContactInfo, 1000);
    
    // Make function available globally for manual triggering
    window.autofillContactInfo = autofillContactInfo;
    
})();
