# LocumTele Brand CSS System

A consolidated and modular CSS system for LocumTele dashboards and documentation pages.

## Overview

This CSS system is designed to provide:
- **Consistent branding** across all LocumTele interfaces
- **Reusable components** for easy dashboard creation
- **Modular architecture** for maintainability
- **Mobile-responsive** design patterns
- **Easy duplication** of dashboard layouts

## File Structure

```
docs/brand/
├── brand.css                    # Core brand styles and variables
├── dashboard-framework.css      # Reusable dashboard layout system
├── sites-consolidated.css      # Site-specific styles (consolidated)
├── sites.css                   # Legacy site styles (for backward compatibility)
├── dashboard-template.html      # HTML template for new dashboards
├── dashboard-config.js         # JavaScript configuration for dashboards
├── create-dashboard.js         # Script to generate new dashboards
└── README.md                   # This file
```

## CSS Architecture

### 1. brand.css
- **Purpose**: Core brand identity and design tokens
- **Contains**: Colors, typography, spacing, shadows, basic components
- **Usage**: Include in all pages for consistent branding

### 2. dashboard-framework.css
- **Purpose**: Reusable dashboard layout system
- **Contains**: Layout components, navigation, cards, buttons, utilities
- **Usage**: Include when creating dashboard-style interfaces

### 3. sites-consolidated.css
- **Purpose**: Site-specific styles and API documentation
- **Contains**: Documentation styles, form layouts, specialized components
- **Usage**: Include for documentation and complex content pages

## Quick Start

### Creating a New Dashboard

1. **Use the template** (recommended):
   ```bash
   node docs/brand/create-dashboard.js my-dashboard integrations
   ```

2. **Manual setup**:
   ```html
   <!DOCTYPE html>
   <html lang="en">
   <head>
       <link rel="stylesheet" href="docs/brand/brand.css">
       <link rel="stylesheet" href="docs/brand/dashboard-framework.css">
       <link rel="stylesheet" href="docs/brand/sites-consolidated.css">
   </head>
   <body class="lt-branded">
       <div class="dashboard-layout">
           <!-- Your dashboard content -->
       </div>
   </body>
   </html>
   ```

### CSS Class Naming Convention

- **Brand classes**: `lt-*` (e.g., `lt-card`, `lt-btn-primary`)
- **Dashboard classes**: `dashboard-*` (e.g., `dashboard-layout`, `dashboard-card`)
- **Site classes**: `site-*` (e.g., `site-api-section`, `site-nav-link`)

## Dashboard Framework Components

### Layout System
```html
<div class="dashboard-layout">
    <nav class="dashboard-sidebar">...</nav>
    <div class="dashboard-header">...</div>
    <div class="dashboard-content">...</div>
</div>
```

### Cards
```html
<div class="dashboard-card">
    <div class="dashboard-card-header">
        <h3 class="dashboard-card-title">Title</h3>
        <p class="dashboard-card-subtitle">Subtitle</p>
    </div>
    <!-- Card content -->
</div>
```

### Buttons
```html
<a href="#" class="dashboard-btn dashboard-btn-primary">Primary</a>
<a href="#" class="dashboard-btn dashboard-btn-secondary">Secondary</a>
<a href="#" class="dashboard-btn dashboard-btn-outline">Outline</a>
```

### Grids
```html
<div class="dashboard-grid dashboard-grid-2">
    <!-- 2-column grid -->
</div>
<div class="dashboard-grid dashboard-grid-3">
    <!-- 3-column grid -->
</div>
```

### Stats
```html
<div class="dashboard-stats">
    <div class="dashboard-stat">
        <div class="dashboard-stat-value">1,247</div>
        <div class="dashboard-stat-label">Total Items</div>
    </div>
</div>
```

## Configuration System

### Dashboard Configuration
Edit `dashboard-config.js` to customize navigation and page metadata:

```javascript
const DASHBOARD_CONFIGS = {
    integrations: {
        title: "Integration Dashboard",
        headerTitle: "🏥 Integration Dashboard",
        headerDescription: "API Documentation & Integration Resources",
        pageDirectory: "integrations",
        navigation: [
            {
                id: "dashboard",
                title: "Dashboard",
                icon: "🏠",
                onClick: "loadPage('dashboard', this)"
            }
            // ... more navigation items
        ]
    }
};
```

### Creating Custom Dashboard Types

1. Add your configuration to `dashboard-config.js`:
   ```javascript
   const DASHBOARD_CONFIGS = {
       myCustomType: {
           title: "My Custom Dashboard",
           headerTitle: "🏥 My Custom Dashboard",
           headerDescription: "Custom dashboard description",
           pageDirectory: "my-custom",
           navigation: [
               // Your navigation items
           ],
           pages: {
               // Your page metadata
           }
       }
   };
   ```

2. Generate the dashboard:
   ```bash
   node create-dashboard.js my-dashboard myCustomType
   ```

## Migration Guide

### From Old System to New System

1. **Update CSS includes**:
   ```html
   <!-- Old -->
   <link rel="stylesheet" href="docs/brand/brand.css">
   <link rel="stylesheet" href="docs/brand/sites.css">
   
   <!-- New -->
   <link rel="stylesheet" href="docs/brand/brand.css">
   <link rel="stylesheet" href="docs/brand/dashboard-framework.css">
   <link rel="stylesheet" href="docs/brand/sites-consolidated.css">
   ```

2. **Update class names** (optional, old classes still work):
   ```html
   <!-- Old -->
   <div class="site-layout">
       <nav class="site-sidebar">
   
   <!-- New -->
   <div class="dashboard-layout">
       <nav class="dashboard-sidebar">
   ```

3. **Use new components**:
   ```html
   <!-- Old -->
   <div class="lt-card">
   
   <!-- New (more features) -->
   <div class="dashboard-card">
   ```

## Best Practices

### 1. Use Semantic Class Names
```html
<!-- Good -->
<div class="dashboard-card">
    <h3 class="dashboard-card-title">User Statistics</h3>
</div>

<!-- Avoid -->
<div class="blue-box">
    <h3 class="big-text">User Statistics</h3>
</div>
```

### 2. Leverage the Grid System
```html
<!-- Responsive grid that adapts to screen size -->
<div class="dashboard-grid dashboard-grid-3">
    <div class="dashboard-card">Item 1</div>
    <div class="dashboard-card">Item 2</div>
    <div class="dashboard-card">Item 3</div>
</div>
```

### 3. Use Utility Classes
```html
<div class="dashboard-card dashboard-text-center dashboard-mb-3">
    <h3 class="dashboard-card-title">Centered Card</h3>
</div>
```

### 4. Maintain Consistent Spacing
```html
<!-- Use the spacing scale -->
<div class="dashboard-mb-1">Small margin</div>
<div class="dashboard-mb-3">Medium margin</div>
<div class="dashboard-mb-5">Large margin</div>
```

## Browser Support

- Chrome 60+
- Firefox 60+
- Safari 12+
- Edge 79+

## Contributing

When adding new styles:

1. **Follow the naming convention**
2. **Add to the appropriate file** (brand.css for core styles, dashboard-framework.css for layout components)
3. **Include responsive design**
4. **Document new classes** in this README
5. **Test across different screen sizes**

## Troubleshooting

### Common Issues

1. **Styles not applying**: Check CSS file order and class names
2. **Layout broken**: Ensure you're using the correct layout classes
3. **Mobile issues**: Test responsive breakpoints and mobile-specific classes

### Debug Mode

Add this to your HTML for visual debugging:
```html
<style>
* { outline: 1px solid red; }
</style>
```

## Examples

See the following files for complete examples:
- `dashboard-integrations.html` - Integration dashboard
- `docs/api/api-htmls/dashboard.html` - Dashboard page content
- `docs/pages/widgets/dashboard.html` - Widget dashboard page

## Support

For questions or issues with the CSS system, please refer to the LocumTele development team.
