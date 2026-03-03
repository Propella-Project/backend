# Propella Admin - Jazzmin with Bootstrap Styling

This project uses **Jazzmin** with **Bootstrap 5** for a modern, responsive, and elegant Django admin interface.

## 📦 Components

### 1. **Jazzmin Configuration** (`config/settings/base.py`)

#### JAZZMIN_SETTINGS
Complete Django admin customization including:
- Site branding and logos
- Dashboard statistics
- Custom navigation icons
- Related modal styling
- Admin site permissions

#### JAZZMIN_UI_TWEAKS
Bootstrap-specific UI configurations:
- Modern navbar with gradient
- Responsive sidebar navigation
- Bootstrap button styling
- Advanced layout options
- Color scheme customization

### 2. **Custom CSS** (`static/css/jazzmin-custom.css`)

Comprehensive Bootstrap-enhanced styling:
- **Navbar**: Gradient blue background with smooth transitions
- **Sidebar**: Modern navigation with hover effects and active states
- **Cards**: Box shadows and hover animations
- **Buttons**: Gradient backgrounds with smooth interactions
- **Tables**: Enhanced readability with stripe patterns
- **Forms**: Better focus states and validation feedback
- **Modals**: Professional appearance with backdrop
- **Alerts**: Color-coded with left border accent
- **Badges**: Clean, modern styling
- **Pagination**: Smooth transitions and proper spacing
- **Responsive**: Full mobile optimization

### 3. **Bootstrap JavaScript** (`static/js/jazzmin-bootstrap.js`)

Enhanced Bootstrap component initialization:
- Tooltip and Popover support
- Smooth scrolling
- Form validation with Bootstrap styles
- Table row hover effects
- Auto-dismissing alerts
- Button loading states
- Breadcrumb styling
- Responsive sidebar toggle
- Modal enhancements
- Custom utility functions (showToast, showAlert, showConfirm)

## 🎨 Color Scheme

| Color | Value | Usage |
|-------|-------|-------|
| Primary | #1e90ff (Dodger Blue) | Main UI elements |
| Secondary | #6c757d (Gray) | Secondary elements |
| Success | #20c997 (Teal) | Success messages |
| Danger | #ff6b6b (Red) | Alerts/errors |
| Warning | #ffc107 (Amber) | Warnings |
| Info | #17a2b8 (Cyan) | Information |

## 🚀 Features

### Navigation & Structure
- **Expandable Sidebar**: Collapsible navigation with icons
- **Breadcrumbs**: Full path navigation
- **Custom Links**: Quick access to important admin pages
- **Icon System**: FontAwesome icons for all modules

### Admin Interface
- **Carousel Form Layout**: Better form navigation
- **Statistics Dashboard**: Quick insights
- **Related Modal Support**: Tabbed interface for relations
- **Search**: Prepared for global search implementation

### User Experience
- **Smooth Animations**: All transitions and interactions
- **Hover Effects**: Visual feedback on interactive elements
- **Responsive Design**: Mobile-first approach
- **Accessibility**: Semantic HTML and ARIA labels

### Development Features
- **Hot Reload**: CSS changes apply immediately
- **Customizable**: Easy to extend and modify
- **Print Friendly**: Prints without admin UI
- **Admin Actions**: Sticky action bar on mobile

## 🔧 Customization

### Modify Colors
Edit `/static/css/jazzmin-custom.css` root variables:
```css
:root {
    --primary-color: #1e90ff;
    --secondary-color: #6c757d;
    /* ... */
}
```

### Add Custom Icons
Update `JAZZMIN_SETTINGS["icons"]` in settings:
```python
"icons": {
    "auth": "fas fa-users-cog",
    "accounts.user": "fas fa-user-circle",
    # Add more icons here
}
```

### Configure Dashboard
Modify `JAZZMIN_SETTINGS["dashboard_namespace"]` and related settings to customize what displays.

### Bootstrap Utility Functions

Use the provided JavaScript utilities for consistent notifications:

```javascript
// Show toast notification
showToast('Operation successful', 'success', 5000);

// Show alert
showAlert('Warning', 'This action cannot be undone', 'warning');

// Show confirmation dialog
showConfirm(
    'Confirm Action',
    'Are you sure you want to proceed?',
    () => { console.log('Confirmed'); },
    () => { console.log('Cancelled'); }
);
```

## 📱 Responsive Breakpoints

- **Mobile**: < 768px - Sidebar collapses, full-width content
- **Tablet**: 768px - 1024px - Sidebar visible, adjusted spacing
- **Desktop**: > 1024px - Full layout with sidebar

## 🛠️ File Structure

```
static/
├── css/
│   └── jazzmin-custom.css      # Main Bootstrap styling
└── js/
    └── jazzmin-bootstrap.js    # Bootstrap enhancements

config/settings/
└── base.py                     # Jazzmin configuration
```

## 📖 Documentation

- [Jazzmin Documentation](https://django-jazzmin.readthedocs.io/)
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.0/)
- [FontAwesome Icons](https://fontawesome.com/icons)

## ⚙️ Installation

Bootstrap styling is already configured. To use:

1. **Ensure static files are collected**:
   ```bash
   python manage.py collectstatic --noinput
   ```

2. **Run development server**:
   ```bash
   python manage.py runserver
   ```

3. **Access admin**:
   Navigate to `http://localhost:8000/admin/`

## 🎯 Key Settings Summary

| Setting | Value | Description |
|---------|-------|-------------|
| navbar | navbar-light navbar-gradient | Modern light navbar |
| brand_colour | navbar-primary | Primary blue branding |
| sidebar_nav_bold | True | Bold sidebar text |
| actions_sticky_top | True | Sticky action bar |
| changeform_format | carousel | Carousel form layout |
| show_statistics | True | Show dashboard stats |

## 📝 Notes

- All styling is responsive and mobile-optimized
- CSS custom properties enable easy theming
- JavaScript enhancements are optional but recommended
- No external dependencies beyond Django, Jazzmin, and Bootstrap 5

## 🐛 Troubleshooting

### Styles not appearing?
```bash
python manage.py collectstatic --noinput --clear
```

### JavaScript not working?
- Ensure `jazzmin-bootstrap.js` is loaded in admin base template
- Check browser console for errors
- Verify Bootstrap 5 is available (included with Jazzmin)

### Icons not showing?
- Ensure FontAwesome is loaded (included with Jazzmin)
- Check icon names in `JAZZMIN_SETTINGS["icons"]`

## 📄 License

This styling is part of the Propella project and follows the same license.
