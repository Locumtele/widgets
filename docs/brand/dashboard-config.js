/**
 * LocumTele Dashboard Configuration
 * 
 * This file provides a simple way to configure new dashboards
 * by defining the navigation structure and page metadata.
 */

// Dashboard Configuration Template
const DASHBOARD_CONFIG_TEMPLATE = {
    // Basic dashboard information
    title: "Dashboard Title",
    headerTitle: "🏥 Dashboard Header",
    headerDescription: "Dashboard description goes here",
    defaultPage: "dashboard",
    pageDirectory: "integrations", // or "widgets", etc.
    
    // Navigation structure
    navigation: [
        {
            id: "dashboard",
            title: "Dashboard",
            icon: "🏠",
            onClick: "loadPage('dashboard', this)"
        },
        {
            id: "api-docs",
            title: "API Docs",
            icon: "📚",
            hasSubmenu: true,
            onClick: "loadPageAndToggleSubmenu('api-docs', event)",
            submenu: [
                {
                    id: "screeners",
                    title: "Screeners",
                    icon: "📝",
                    onClick: "loadPage('screeners', this)"
                },
                {
                    id: "reassessments",
                    title: "Reassessments",
                    icon: "🔄",
                    onClick: "loadPage('reassessments', this)"
                }
            ]
        },
        {
            id: "calendar",
            title: "Calendars",
            icon: "📅",
            onClick: "loadPage('calendar', this)"
        },
        {
            id: "support",
            title: "Support",
            icon: "🆘",
            onClick: "loadPage('support', this)"
        }
    ],
    
    // Page metadata
    pages: {
        dashboard: {
            title: "🏥 Dashboard",
            description: "Main dashboard overview"
        },
        "api-docs": {
            title: "🏥 Dashboard / 📚 API Documentation",
            description: "Complete API reference with examples and integration guides"
        },
        screeners: {
            title: "🏥 Dashboard / 📝 Screeners",
            description: "Submit patient screening data from your custom forms"
        },
        reassessments: {
            title: "🏥 Dashboard / 🔄 Reassessments",
            description: "Patient follow-up and reassessment tools"
        },
        calendar: {
            title: "🏥 Dashboard / 📅 Calendars",
            description: "Ready-to-use calendar booking widgets"
        },
        support: {
            title: "🏥 Dashboard / 🆘 Support",
            description: "Get help with integrations and technical support"
        }
    }
};

// Example configurations for different dashboard types
const DASHBOARD_CONFIGS = {
    // Integration Dashboard
    integrations: {
        ...DASHBOARD_CONFIG_TEMPLATE,
        title: "Integration Dashboard",
        headerTitle: "🏥 Integration Dashboard",
        headerDescription: "API Documentation & Integration Resources for Healthcare Providers",
        pageDirectory: "integrations"
    },
    
    // Widget Dashboard
    widgets: {
        ...DASHBOARD_CONFIG_TEMPLATE,
        title: "Widget Dashboard",
        headerTitle: "🏥 Widget Dashboard",
        headerDescription: "Welcome to the LocumTele Widget Management System",
        pageDirectory: "widgets",
        navigation: [
            {
                id: "dashboard",
                title: "Dashboard",
                icon: "🏠",
                onClick: "loadPage('dashboard', this)"
            },
            {
                id: "forms",
                title: "Forms",
                icon: "📋",
                hasSubmenu: true,
                onClick: "loadPageAndToggleSubmenu('forms', event)",
                submenu: [
                    {
                        id: "screeners",
                        title: "Screeners",
                        icon: "📝",
                        onClick: "loadPage('screeners', this)"
                    },
                    {
                        id: "reassessments",
                        title: "Reassessments",
                        icon: "🔄",
                        onClick: "loadPage('reassessments', this)"
                    }
                ]
            },
            {
                id: "admin",
                title: "Admin",
                icon: "⚙️",
                onClick: "loadPage('admin', this)"
            },
            {
                id: "support",
                title: "Support",
                icon: "🆘",
                onClick: "loadPage('support', this)"
            }
        ],
        pages: {
            dashboard: {
                title: "🏥 Widget Dashboard",
                description: "Welcome to the LocumTele Widget Management System"
            },
            forms: {
                title: "🏥 Widget Dashboard / 📋 Forms Management",
                description: "Manage patient screening and reassessment forms"
            },
            screeners: {
                title: "🏥 Widget Dashboard / 📝 Screeners",
                description: "View and manage screening form data"
            },
            reassessments: {
                title: "🏥 Widget Dashboard / 🔄 Reassessments",
                description: "View and manage reassessment form data"
            },
            admin: {
                title: "🏥 Widget Dashboard / ⚙️ Admin Controls",
                description: "System administration and data management"
            },
            support: {
                title: "🏥 Widget Dashboard / 🆘 Support",
                description: "Get help with widget management"
            }
        }
    },
    
    // Custom Dashboard Template
    custom: {
        ...DASHBOARD_CONFIG_TEMPLATE,
        title: "Custom Dashboard",
        headerTitle: "🏥 Custom Dashboard",
        headerDescription: "Your custom dashboard description",
        pageDirectory: "custom"
    }
};

// Function to generate navigation HTML from config
function generateNavigationHTML(config) {
    return config.navigation.map(item => {
        let html = `<li class="dashboard-nav-item">`;
        
        if (item.hasSubmenu) {
            html += `<a href="#" class="dashboard-nav-link has-submenu" onclick="${item.onClick}">
                ${item.icon} ${item.title}
                <span class="dashboard-nav-arrow">▶</span>
            </a>`;
            
            if (item.submenu) {
                html += `<ul class="dashboard-nav-submenu">`;
                item.submenu.forEach(subItem => {
                    html += `<li class="dashboard-nav-item">
                        <a href="#" class="dashboard-nav-link" onclick="${subItem.onClick}">
                            ${subItem.icon} ${subItem.title}
                        </a>
                    </li>`;
                });
                html += `</ul>`;
            }
        } else {
            html += `<a href="#" class="dashboard-nav-link" onclick="${item.onClick}">
                ${item.icon} ${item.title}
            </a>`;
        }
        
        html += `</li>`;
        return html;
    }).join('\n');
}

// Function to create a new dashboard configuration
function createDashboardConfig(options = {}) {
    const defaultConfig = {
        title: "New Dashboard",
        headerTitle: "🏥 New Dashboard",
        headerDescription: "Dashboard description",
        defaultPage: "dashboard",
        pageDirectory: "pages",
        navigation: [],
        pages: {}
    };
    
    return { ...defaultConfig, ...options };
}

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        DASHBOARD_CONFIG_TEMPLATE,
        DASHBOARD_CONFIGS,
        generateNavigationHTML,
        createDashboardConfig
    };
}
