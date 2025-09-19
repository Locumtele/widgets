#!/usr/bin/env node

/**
 * LocumTele Dashboard Generator
 * 
 * This script creates new dashboard HTML files from the template
 * Usage: node create-dashboard.js <dashboard-name> [dashboard-type]
 * 
 * Example: node create-dashboard.js my-dashboard integrations
 */

const fs = require('fs');
const path = require('path');

// Load the dashboard configuration
const { DASHBOARD_CONFIGS, generateNavigationHTML } = require('./dashboard-config.js');

function createDashboard(dashboardName, dashboardType = 'custom') {
    const config = DASHBOARD_CONFIGS[dashboardType] || DASHBOARD_CONFIGS.custom;
    
    // Read the template
    const templatePath = path.join(__dirname, 'dashboard-template.html');
    const template = fs.readFileSync(templatePath, 'utf8');
    
    // Generate navigation HTML
    const navigationHTML = generateNavigationHTML(config);
    
    // Replace template placeholders
    const dashboardHTML = template
        .replace(/\{\{DASHBOARD_TITLE\}\}/g, config.title)
        .replace(/\{\{HEADER_TITLE\}\}/g, config.headerTitle)
        .replace(/\{\{HEADER_DESCRIPTION\}\}/g, config.headerDescription)
        .replace(/\{\{PAGE_DIRECTORY\}\}/g, config.pageDirectory)
        .replace(/\{\{DEFAULT_PAGE\}\}/g, config.defaultPage)
        .replace(/\{\{NAVIGATION_ITEMS\}\}/g, navigationHTML);
    
    // Create the output file
    const outputPath = path.join(__dirname, '..', '..', '..', `${dashboardName}.html`);
    fs.writeFileSync(outputPath, dashboardHTML);
    
    console.log(`✅ Dashboard created: ${outputPath}`);
    console.log(`📁 Page directory: pages/${config.pageDirectory}/`);
    console.log(`🏠 Default page: ${config.defaultPage}`);
    
    // Create the pages directory if it doesn't exist
    const pagesDir = path.join(__dirname, '..', '..', '..', 'pages', config.pageDirectory);
    if (!fs.existsSync(pagesDir)) {
        fs.mkdirSync(pagesDir, { recursive: true });
        console.log(`📁 Created pages directory: ${pagesDir}`);
    }
    
    // Create a basic dashboard page if it doesn't exist
    const dashboardPagePath = path.join(pagesDir, 'dashboard.html');
    if (!fs.existsSync(dashboardPagePath)) {
        const basicDashboardPage = `<!-- Page Header -->
<header class="site-page-header">
    <h1>${config.headerTitle}</h1>
    <p>${config.headerDescription}</p>
</header>

<!-- Elle's Introduction Section -->
<div class="lt-section-intro dashboard-animate">
    <div class="lt-section-robot"></div>
    <div class="lt-section-content">
        <h2>Hi! I'm Elle, your LocumTele assistant</h2>
        <p>I'm here to help you get started with your dashboard! Below you'll find all the resources you need to manage your system effectively.</p>
    </div>
</div>

<!-- Dashboard Content -->
<div class="dashboard-grid dashboard-grid-2 dashboard-animate delay-1">
    <div class="dashboard-card">
        <div class="dashboard-card-header">
            <h3 class="dashboard-card-title">📊 Overview</h3>
            <p class="dashboard-card-subtitle">Get a quick overview of your system status and key metrics.</p>
        </div>
        <div style="display: flex; gap: 0.5rem; flex-wrap: wrap; margin-top: 1rem;">
            <a href="#" class="dashboard-btn dashboard-btn-primary" onclick="loadPage('dashboard')">View Details</a>
        </div>
    </div>
    
    <div class="dashboard-card">
        <div class="dashboard-card-header">
            <h3 class="dashboard-card-title">⚙️ Settings</h3>
            <p class="dashboard-card-subtitle">Configure your system settings and preferences.</p>
        </div>
        <div style="display: flex; gap: 0.5rem; flex-wrap: wrap; margin-top: 1rem;">
            <a href="#" class="dashboard-btn dashboard-btn-primary" onclick="loadPage('settings')">Configure</a>
        </div>
    </div>
</div>

<!-- Quick Stats -->
<div class="dashboard-stats dashboard-animate delay-2">
    <div class="dashboard-stat">
        <div class="dashboard-stat-value">0</div>
        <div class="dashboard-stat-label">Total Items</div>
    </div>
    
    <div class="dashboard-stat">
        <div class="dashboard-stat-value">0</div>
        <div class="dashboard-stat-label">Active Items</div>
    </div>
    
    <div class="dashboard-stat">
        <div class="dashboard-stat-value">0</div>
        <div class="dashboard-stat-label">Success Rate</div>
    </div>
</div>`;
        
        fs.writeFileSync(dashboardPagePath, basicDashboardPage);
        console.log(`📄 Created basic dashboard page: ${dashboardPagePath}`);
    }
    
    console.log(`\n🎉 Dashboard setup complete!`);
    console.log(`\nNext steps:`);
    console.log(`1. Open ${dashboardName}.html in your browser`);
    console.log(`2. Add your page content to pages/${config.pageDirectory}/`);
    console.log(`3. Customize the navigation in dashboard-config.js if needed`);
}

// Command line interface
if (require.main === module) {
    const args = process.argv.slice(2);
    
    if (args.length === 0) {
        console.log('Usage: node create-dashboard.js <dashboard-name> [dashboard-type]');
        console.log('\nAvailable dashboard types:');
        Object.keys(DASHBOARD_CONFIGS).forEach(type => {
            console.log(`  - ${type}`);
        });
        process.exit(1);
    }
    
    const dashboardName = args[0];
    const dashboardType = args[1] || 'custom';
    
    if (!DASHBOARD_CONFIGS[dashboardType]) {
        console.error(`❌ Unknown dashboard type: ${dashboardType}`);
        console.log('Available types:', Object.keys(DASHBOARD_CONFIGS).join(', '));
        process.exit(1);
    }
    
    createDashboard(dashboardName, dashboardType);
}

module.exports = { createDashboard };
