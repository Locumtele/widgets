// Test form data
var testFormData = {
    id: "test123",
    title: "Test Form",
    questions: [
        {
            id: "q1",
            text: "What is your name?",
            type: "text"
        },
        {
            id: "q2", 
            text: "Select your state:",
            type: "select",
            options: [
                {value: "CA", text: "California"},
                {value: "NY", text: "New York"},
                {value: "TX", text: "Texas"}
            ]
        }
    ]
};

// Simple form loader function
function loadForm(formId) {
    var container = document.getElementById('locumtele-form-' + formId);
    if (container) {
        container.innerHTML = '<h3>Test Form Loaded!</h3><p>Form ID: ' + formId + '</p><button onclick="alert(\'Form submitted!\')">Submit</button>';
    }
}
