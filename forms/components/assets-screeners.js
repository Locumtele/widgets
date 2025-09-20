// Forms data and functionality for assets-screeners.html

// Global data storage
let formsData = [];

// Load forms data when page loads
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOMContentLoaded fired for assets-screeners');
    initializePage();
});

// Also try to load immediately if DOM is already ready
if (document.readyState === 'loading') {
    console.log('Document still loading, waiting for DOMContentLoaded');
} else {
    console.log('Document already ready, initializing page immediately');
    initializePage();
}

// Initialize the page
function initializePage() {
    // Check if content is already generated
    const contentEl = document.getElementById('forms-content');
    if (contentEl && contentEl.innerHTML.trim() !== '') {
        console.log('Content already generated, showing existing content');
        showGeneratedContent();
        return;
    }
    
    // Show the generate button
    showGenerateButton();
}

// Show the generate button
function showGenerateButton() {
    const contentEl = document.getElementById('forms-content');
    if (!contentEl) return;
    
    contentEl.innerHTML = `
        <div style="text-align: center; padding: 3rem;">
            <div style="font-size: 2rem; margin-bottom: 1rem;">🎯</div>
            <h3 style="margin-bottom: 1rem; color: #333;">Generate Embed Codes</h3>
            <p style="color: #666; margin-bottom: 2rem;">Click the button below to generate embed codes for all screener forms.</p>
            <button onclick="generateEmbedCodes()" style="background: #007bff; color: white; border: none; padding: 1rem 2rem; border-radius: 8px; cursor: pointer; font-size: 1rem; font-weight: 600; box-shadow: 0 2px 4px rgba(0,123,255,0.3);">
                🚀 Generate Embed Codes
            </button>
            <p style="color: #999; font-size: 0.9rem; margin-top: 1rem;">This will load all forms and create embed codes for your website.</p>
        </div>
    `;
}

// Show already generated content
function showGeneratedContent() {
    const loadingEl = document.getElementById('forms-loading');
    const contentEl = document.getElementById('forms-content');
    const errorEl = document.getElementById('forms-error');
    
    if (loadingEl) loadingEl.style.display = 'none';
    if (errorEl) errorEl.style.display = 'none';
    if (contentEl) contentEl.style.display = 'block';
}

// Generate embed codes (called by button)
async function generateEmbedCodes() {
    console.log('Generate embed codes button clicked');
    
    // Show loading state
    const loadingEl = document.getElementById('forms-loading');
    const contentEl = document.getElementById('forms-content');
    const errorEl = document.getElementById('forms-error');
    
    if (loadingEl) loadingEl.style.display = 'block';
    if (contentEl) contentEl.style.display = 'none';
    if (errorEl) errorEl.style.display = 'none';
    
    try {
        // Load actual form data from JSON files
        formsData = await loadActualFormsData();
        console.log('Forms data loaded:', formsData.length, 'forms');
        
        // Render the forms list
        renderFormsList();
        
        // Hide loading and show content
        if (loadingEl) loadingEl.style.display = 'none';
        if (contentEl) contentEl.style.display = 'block';
        
        // Show success message
        showSuccessMessage();
        
    } catch (error) {
        console.error('Error generating embed codes:', error);
        if (loadingEl) loadingEl.style.display = 'none';
        if (errorEl) {
            errorEl.style.display = 'block';
            errorEl.innerHTML = `Error generating embed codes: ${error.message}`;
        }
    }
}

// Show success message
function showSuccessMessage() {
    const successEl = document.getElementById('forms-success');
    if (successEl) {
        successEl.style.display = 'block';
        successEl.innerHTML = `
            <div style="text-align: center; padding: 1rem;">
                <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">✅</div>
                <div>Embed codes generated successfully! All ${formsData.length} forms are ready to use.</div>
            </div>
        `;
        
        setTimeout(() => {
            successEl.style.display = 'none';
        }, 3000);
    }
}

// Load forms data
async function loadFormsData() {
    try {
        console.log('loadFormsData called');
        
        // Check if required elements exist
        const loadingEl = document.getElementById('forms-loading');
        const contentEl = document.getElementById('forms-content');
        const errorEl = document.getElementById('forms-error');
        
        console.log('Elements found:', {
            loading: !!loadingEl,
            content: !!contentEl,
            error: !!errorEl
        });
        
        if (!loadingEl || !contentEl || !errorEl) {
            console.error('Required DOM elements not found');
            return;
        }
        
        // Show loading state
        loadingEl.style.display = 'block';
        contentEl.style.display = 'none';
        errorEl.style.display = 'none';

        console.log('Loading actual form data...');
        // Load actual form data from JSON files
        formsData = await loadActualFormsData();
        console.log('Forms data loaded:', formsData.length, 'forms');
        
        renderFormsList();

        loadingEl.style.display = 'none';
        contentEl.style.display = 'block';

    } catch (error) {
        console.error('Error loading forms data:', error);
        const loadingEl = document.getElementById('forms-loading');
        const errorEl = document.getElementById('forms-error');
        if (loadingEl) loadingEl.style.display = 'none';
        if (errorEl) {
            errorEl.style.display = 'block';
            errorEl.innerHTML = `Error: ${error.message}`;
        }
    }
}

// Load actual forms data from JSON files
async function loadActualFormsData() {
    const formFiles = [
        'acne.json', 'ala.json', 'cbd.json', 'ed.json', 'glp1.json',
        'herpes.json', 'hydroxychloroquine.json', 'ivermectin.json',
        'mcas.json', 'mebendazole.json', 'metabolicpeptide.json',
        'metformin.json', 'nad.json', 'oxytocin.json', 'sermorelin.json',
        'vitamina.json', 'weightloss.json'
    ];
    
    const forms = [];
    
    for (const fileName of formFiles) {
        try {
                const response = await fetch(`../../archive/screeners/${fileName}`);
            if (response.ok) {
                const formData = await response.json();
                
                // Transform the data to match our expected format
                const transformedData = {
                    id: formData.screener ? formData.screener.toLowerCase().replace(/\s+/g, '-') : fileName.replace('.json', ''),
                    title: formData.screener || fileName.replace('.json', ''),
                    category: formData.category ? formData.category.toLowerCase() : 'uncategorized',
                    formType: 'screener',
                    status: 'published',
                    totalQuestions: formData.totalQuestions || (formData.questions ? formData.questions.length : 0),
                    color: getCategoryColor(formData.category),
                    description: `${formData.screener || fileName.replace('.json', '')} screening form`,
                    lastUpdated: formData.lastUpdated || 'Unknown',
                    questions: formData.questions || []
                };
                
                forms.push(transformedData);
            }
        } catch (error) {
            console.warn(`Failed to load ${fileName}:`, error);
        }
    }
    
    return forms;
}

// Get color for category
function getCategoryColor(category) {
    const colors = {
        'weightloss': '#2196f3',
        'hormones': '#9c27b0',
        'antiaging': '#4caf50',
        'metabolic': '#ff9800',
        'infection': '#e91e63',
        'specialty': '#8bc34a'
    };
    return colors[category?.toLowerCase()] || '#007bff';
}


// Render forms list
function renderFormsList() {
    const container = document.getElementById('forms-list');
    if (!container) return;

    // Filter for screener forms only
    const screenerForms = formsData.filter(form => form.formType === 'screener');

    if (screenerForms.length === 0) {
        container.innerHTML = '<p>No screener forms available.</p>';
        return;
    }

    // Add regenerate button at the top
    let formsHTML = `
        <div style="text-align: right; margin-bottom: 1.5rem; padding-bottom: 1rem; border-bottom: 1px solid #e9ecef;">
            <button onclick="regenerateEmbedCodes()" style="background: #6c757d; color: white; border: none; padding: 0.5rem 1rem; border-radius: 6px; cursor: pointer; font-size: 0.9rem;">
                🔄 Regenerate Codes
            </button>
        </div>
    `;

    // Group forms by category for better organization
    const groupedForms = screenerForms.reduce((groups, form) => {
        const category = form.category;
        if (!groups[category]) {
            groups[category] = [];
        }
        groups[category].push(form);
        return groups;
    }, {});

    Object.keys(groupedForms).forEach(category => {
        const categoryForms = groupedForms[category];
        const categoryColor = categoryForms[0].color || '#007bff';

        formsHTML += '<div style="margin-bottom: 2rem;">';
        formsHTML += '<h4 style="color: ' + categoryColor + '; margin-bottom: 1rem; text-transform: capitalize; border-bottom: 2px solid ' + categoryColor + '; padding-bottom: 0.5rem;">';
        formsHTML += category + ' Forms (' + categoryForms.length + ')';
        formsHTML += '</h4>';
        formsHTML += '<div style="display: grid; gap: 1rem;">';

        categoryForms.forEach(form => {
            formsHTML += '<div class="form-item" style="border-left: 4px solid ' + form.color + ';">';
            formsHTML += '<div class="form-header">';
            formsHTML += '<h4 class="form-title">' + form.title + '</h4>';
            formsHTML += '<div class="form-meta">';
            formsHTML += '<span class="form-badge category" style="background-color: ' + form.color + '20; color: ' + form.color + ';">' + form.category + '</span>';
            formsHTML += '<span class="form-badge type">' + form.formType + '</span>';
            formsHTML += '<span class="form-badge status">' + form.status + '</span>';
            formsHTML += '<span class="form-badge">' + form.totalQuestions + ' questions</span>';
            formsHTML += '</div>';
            formsHTML += '</div>';

            formsHTML += '<div style="margin: 0.5rem 0; color: #666; font-size: 0.9rem;">';
            formsHTML += 'Webhook: <code>https://hook.us1.make.com/webhook/' + form.id + '</code>';
            formsHTML += '</div>';

            formsHTML += '<div class="embed-code-box">';
            formsHTML += '<div class="embed-code-header">';
            formsHTML += '<span class="loading-text">📋 ' + form.title + ' Embed Code</span>';
            formsHTML += '<span class="loading-subtext">Copy and paste this code into your website</span>';
            formsHTML += '</div>';
            formsHTML += '<div class="code-container">';
            formsHTML += '<textarea class="embed-code-text" readonly>' + generateEmbedCode(form) + '</textarea>';
            formsHTML += '<button class="copy-button" onclick="copyEmbedCode(\'' + form.id + '\')">📋 Copy Code</button>';
            formsHTML += '</div>';
            formsHTML += '</div>';
            formsHTML += '</div>';
        });

        formsHTML += '</div>';
        formsHTML += '</div>';
    });

    container.innerHTML = formsHTML;
}

// Regenerate embed codes
function regenerateEmbedCodes() {
    console.log('Regenerating embed codes...');
    // Clear the content and show the generate button again
    const contentEl = document.getElementById('forms-content');
    if (contentEl) {
        contentEl.innerHTML = '';
    }
    showGenerateButton();
}

// Generate embed code for a form
function generateEmbedCode(form) {
    const formConfig = {
        id: form.id,
        title: form.title,
        category: form.category,
        formType: form.formType,
        questions: form.questions,
        webhookUrl: "https://hook.us1.make.com/webhook/" + form.id,
        redirectConfig: {
            enabled: true,
            baseUrl: "https://locumtele.github.io/widgets/redirect/",
            params: {
                formId: form.id,
                category: form.category
            }
        },
        styling: {
            primaryColor: form.color || "#007bff",
            borderRadius: "8px",
            fontFamily: "Arial, sans-serif"
        },
        validation: {
            enabled: true,
            showErrors: true
        }
    };

    const formIdClean = form.id.replace(/-/g, '_');
    const configJson = JSON.stringify(formConfig, null, 4);

    let embedCode = '<!-- ' + form.title + ' - Universal Form System -->\n';
    embedCode += '<link rel="stylesheet" href="https://locumtele.github.io/widgets/forms/components/universalFormStyle.css">\n';
    embedCode += '<script src="https://locumtele.github.io/widgets/forms/components/universalFormLoader.js"></script>\n\n';
    embedCode += '<div id="form-container-' + form.id + '" class="lt-form-container"></div>\n\n';
    embedCode += '<script>\n';
    embedCode += '    const formConfig_' + formIdClean + ' = ' + configJson + ';\n\n';
    embedCode += '    document.addEventListener(\'DOMContentLoaded\', function() {\n';
    embedCode += '        if (typeof window.generateForm === \'function\') {\n';
    embedCode += '            window.generateForm(formConfig_' + formIdClean + ', \'form-container-' + form.id + '\');\n';
    embedCode += '        } else {\n';
    embedCode += '            console.error(\'Universal Form Loader not found.\');\n';
    embedCode += '        }\n';
    embedCode += '    });\n\n';
    embedCode += '    window.addEventListener(\'formSubmitted_' + form.id + '\', function(event) {\n';
    embedCode += '        fetch(\'' + formConfig.webhookUrl + '\', {\n';
    embedCode += '            method: \'POST\',\n';
    embedCode += '            headers: { \'Content-Type\': \'application/json\' },\n';
    embedCode += '            body: JSON.stringify(event.detail)\n';
    embedCode += '        }).then(response => {\n';
    embedCode += '            if (response.ok) {\n';
    embedCode += '                window.dispatchEvent(new CustomEvent(\'triggerRedirect_' + form.id + '\', {\n';
    embedCode += '                    detail: event.detail\n';
    embedCode += '                }));\n';
    embedCode += '            }\n';
    embedCode += '        });\n';
    embedCode += '    });\n';
    embedCode += '</script>\n\n';
    embedCode += '<script src="https://locumtele.github.io/widgets/forms/components/ghl-redirect.js"></script>';

    return embedCode;
}

// Copy embed code to clipboard
async function copyEmbedCode(formId) {
    const button = document.querySelector('[onclick="copyEmbedCode(\'' + formId + '\')"]');
    const formItem = button.closest('.form-item');
    const embedCode = formItem.querySelector('.embed-code-text');

    if (!embedCode) {
        console.error('Embed code textarea not found for form:', formId);
        return;
    }

    try {
        await navigator.clipboard.writeText(embedCode.value);
        button.textContent = 'Copied!';
        button.classList.add('copied');

        setTimeout(() => {
            button.textContent = '📋 Copy Code';
            button.classList.remove('copied');
        }, 2000);
    } catch (err) {
        console.error('Failed to copy: ', err);
        // Fallback for older browsers
        embedCode.select();
        document.execCommand('copy');

        button.textContent = 'Copied!';
        button.classList.add('copied');

        setTimeout(() => {
            button.textContent = '📋 Copy Code';
            button.classList.remove('copied');
        }, 2000);
    }
}