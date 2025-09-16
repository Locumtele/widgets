/**
 * Global Form Loader
 * 
 * Universal loader for easy form integration.
 * This script loads the formLoader and provides a simplified API.
 * 
 * Usage:
 * <script src="https://locumtele.github.io/ltGlobalWidgets/forms/components/globalForm.js"></script>
 * 
 * Then use: window.GlobalWidgets.loadForm('forms/screeners/glp1.json', 'container-id')
 */

(function() {
    'use strict';
    
    // Global Widgets API
    window.GlobalWidgets = {
        // Track if formLoader is loaded
        formLoaderLoaded: false,
        
        // Queue for API calls made before formLoader loads
        callQueue: [],
        
        /**
         * Load a form into a container
         * @param {string} jsonPath - Path to the JSON form configuration
         * @param {string} containerId - ID of the container element
         * @returns {Promise} - Promise that resolves when form is loaded
         */
        loadForm: function(jsonPath, containerId) {
            if (this.formLoaderLoaded && window.FormLoader) {
                return window.FormLoader.generateForm(jsonPath, containerId);
            } else {
                // Queue the call if formLoader isn't ready yet
                return new Promise((resolve, reject) => {
                    this.callQueue.push({
                        method: 'loadForm',
                        args: [jsonPath, containerId],
                        resolve: resolve,
                        reject: reject
                    });
                });
            }
        },
        
        /**
         * Load form data without rendering
         * @param {string} jsonPath - Path to the JSON form configuration
         * @returns {Promise} - Promise that resolves with form data
         */
        loadFormData: function(jsonPath) {
            if (this.formLoaderLoaded && window.FormLoader) {
                return window.FormLoader.loadFormData(jsonPath);
            } else {
                return new Promise((resolve, reject) => {
                    this.callQueue.push({
                        method: 'loadFormData',
                        args: [jsonPath],
                        resolve: resolve,
                        reject: reject
                    });
                });
            }
        },
        
        /**
         * Get available forms list
         * @returns {Array} - Array of available form configurations
         */
        getAvailableForms: function() {
            return [
                { name: 'GLP-1 Weight Loss', path: 'forms/screeners/glp1.json', category: 'Weight Loss' },
                { name: 'NAD Anti-Aging', path: 'forms/screeners/nad.json', category: 'Anti-Aging' },
                { name: 'Sermorelin Hormone', path: 'forms/screeners/sermorelin.json', category: 'Hormones' },
                { name: 'Metformin', path: 'forms/screeners/metformin.json', category: 'Diabetes' },
                { name: 'Vitamin A', path: 'forms/screeners/vitamina.json', category: 'Vitamins' },
                { name: 'Weight Loss', path: 'forms/screeners/weightloss.json', category: 'Weight Loss' },
                { name: 'Acne', path: 'forms/screeners/acne.json', category: 'Skin Care' },
                { name: 'ED', path: 'forms/screeners/ed.json', category: 'Men\'s Health' },
                { name: 'Herpes', path: 'forms/screeners/herpes.json', category: 'Sexual Health' },
                { name: 'MCAS', path: 'forms/screeners/mcas.json', category: 'Allergies' }
            ];
        },
        
        /**
         * Initialize the global widgets system
         */
        init: function() {
            console.log('Global Widgets initialized');
        }
    };
    
    /**
     * Load the formLoader script
     */
    function loadFormLoader() {
        return new Promise((resolve, reject) => {
            // Check if formLoader is already loaded
            if (window.FormLoader) {
                window.GlobalWidgets.formLoaderLoaded = true;
                resolve();
                return;
            }
            
            // Create script element
            const script = document.createElement('script');
            script.src = 'forms/components/formLoader.js';
            script.onload = function() {
                window.GlobalWidgets.formLoaderLoaded = true;
                console.log('FormLoader loaded successfully');
                
                // Process queued calls
                processCallQueue();
                resolve();
            };
            script.onerror = function() {
                console.error('Failed to load FormLoader');
                reject(new Error('Failed to load FormLoader'));
            };
            
            // Append to document head
            document.head.appendChild(script);
        });
    }
    
    /**
     * Process queued API calls
     */
    function processCallQueue() {
        while (window.GlobalWidgets.callQueue.length > 0) {
            const call = window.GlobalWidgets.callQueue.shift();
            try {
                const result = window.FormLoader[call.method].apply(window.FormLoader, call.args);
                call.resolve(result);
            } catch (error) {
                call.reject(error);
            }
        }
    }
    
    /**
     * Auto-initialize when DOM is ready
     */
    function autoInit() {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', function() {
                loadFormLoader().then(() => {
                    window.GlobalWidgets.init();
                }).catch(console.error);
            });
        } else {
            loadFormLoader().then(() => {
                window.GlobalWidgets.init();
            }).catch(console.error);
        }
    }
    
    // Start auto-initialization
    autoInit();
    
})();
