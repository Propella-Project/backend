/**
 * Propella Admin - Bootstrap Enhancement Script
 * Adds Bootstrap 5 components and interactive features to Jazzmin admin interface
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize Bootstrap popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    const popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Add smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add Bootstrap form validation styles
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Add dynamic table row hover effects
    const tables = document.querySelectorAll('.table');
    tables.forEach(function(table) {
        const rows = table.querySelectorAll('tbody tr');
        rows.forEach(function(row) {
            row.style.cursor = 'pointer';
            row.addEventListener('mouseenter', function() {
                this.style.backgroundColor = '#f0f7ff';
            });
            row.addEventListener('mouseleave', function() {
                this.style.backgroundColor = '';
            });
        });
    });

    // Add Bootstrap alerts with auto-dismiss
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        if (alert.classList.contains('alert-dismissible')) {
            setTimeout(function() {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }, 5000); // Auto-dismiss after 5 seconds
        }
    });

    // Add button loading state
    const buttons = document.querySelectorAll('button[type="submit"]');
    buttons.forEach(function(button) {
        button.addEventListener('click', function() {
            if (this.form && this.form.checkValidity()) {
                this.disabled = true;
                this.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Loading...';
            }
        });
    });

    // Add Bootstrap breadcrumb styling
    const breadcrumbs = document.querySelectorAll('.breadcrumb');
    breadcrumbs.forEach(function(breadcrumb) {
        breadcrumb.classList.add('mb-3');
    });

    // Add responsive table wrapper
    const responsiveTables = document.querySelectorAll('.table');
    responsiveTables.forEach(function(table) {
        if (!table.parentElement.classList.contains('table-responsive')) {
            table.parentElement.classList.add('table-responsive');
        }
    });

    // Custom sidebar toggle for mobile
    const sidebarToggle = document.querySelector('[data-bs-toggle="sidebar"]');
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function() {
            const sidebar = document.querySelector('.sidebar');
            if (sidebar) {
                sidebar.classList.toggle('show');
            }
        });
    }

    // Add Bootstrap pagination styling
    const paginationItems = document.querySelectorAll('.pagination');
    paginationItems.forEach(function(pagination) {
        pagination.classList.add('gap-2');
    });

    // Enhanced form field styling
    const formControls = document.querySelectorAll('.form-control, .form-select');
    formControls.forEach(function(control) {
        // Add Bootstrap classes if not already present
        if (!control.classList.contains('form-control')) {
            control.classList.add('form-control');
        }
        
        // Add focus styling
        control.addEventListener('focus', function() {
            this.parentElement.classList.add('has-focus');
        });
        
        control.addEventListener('blur', function() {
            this.parentElement.classList.remove('has-focus');
        });
    });

    // Add Bootstrap modal enhancements
    const modals = document.querySelectorAll('.modal');
    modals.forEach(function(modal) {
        modal.addEventListener('show.bs.modal', function(e) {
            // Fade animation
            e.relatedTarget.classList.add('animate-fade');
        });
    });

    // Add collapsible sidebar on mobile
    if (window.innerWidth < 768) {
        const sidebar = document.querySelector('.sidebar');
        if (sidebar) {
            sidebar.style.display = 'none';
        }
    }

    // Responsive sidebar toggle on window resize
    window.addEventListener('resize', function() {
        const sidebar = document.querySelector('.sidebar');
        if (window.innerWidth < 768) {
            if (sidebar && !sidebar.classList.contains('collapsed')) {
                sidebar.style.display = 'none';
            }
        } else {
            if (sidebar) {
                sidebar.style.display = 'block';
            }
        }
    });

    // Add Bootstrap badge styling to status indicators
    const badges = document.querySelectorAll('[data-status]');
    badges.forEach(function(badge) {
        const status = badge.getAttribute('data-status').toLowerCase();
        const badgeClass = 'badge badge-' + status;
        badge.className = badgeClass;
    });

    // Enhance form groups with Bootstrap classes
    const formGroups = document.querySelectorAll('.form-group');
    formGroups.forEach(function(group) {
        group.classList.add('mb-3');
    });

    // Add Bootstrap card styling to fieldsets
    const fieldsets = document.querySelectorAll('fieldset');
    fieldsets.forEach(function(fieldset) {
        if (!fieldset.classList.contains('card')) {
            fieldset.classList.add('card', 'border', 'mt-3');
        }
    });

    console.log('✓ Bootstrap Jazzmin enhancements loaded');
});

/**
 * Utility functions for Bootstrap components
 */

// Show toast notification with Bootstrap
function showToast(message, type = 'info', duration = 5000) {
    const toastHTML = `
        <div class="toast" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="toast-header bg-${type} text-white">
                <strong class="me-auto">Notification</strong>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        </div>
    `;
    
    const toastContainer = document.createElement('div');
    toastContainer.className = 'position-fixed bottom-0 end-0 p-3';
    toastContainer.innerHTML = toastHTML;
    document.body.appendChild(toastContainer);
    
    const toast = new bootstrap.Toast(toastContainer.querySelector('.toast'));
    toast.show();
    
    setTimeout(() => {
        toastContainer.remove();
    }, duration);
}

// Show alert dialog with Bootstrap
function showAlert(title, message, type = 'info') {
    const alertHTML = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            <strong>${title}</strong> ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
    
    const alertContainer = document.createElement('div');
    alertContainer.className = 'mt-3';
    alertContainer.innerHTML = alertHTML;
    
    const mainContent = document.querySelector('.content-wrapper') || document.querySelector('main');
    if (mainContent) {
        mainContent.insertBefore(alertContainer, mainContent.firstChild);
    }
}

// Confirm dialog with Bootstrap Modal
function showConfirm(title, message, onConfirm, onCancel) {
    const confirmModal = document.createElement('div');
    confirmModal.className = 'modal fade';
    confirmModal.innerHTML = `
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">${title}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    ${message}
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="button" class="btn btn-primary" id="confirmBtn">Confirm</button>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(confirmModal);
    const modal = new bootstrap.Modal(confirmModal);
    
    confirmModal.querySelector('#confirmBtn').addEventListener('click', () => {
        if (onConfirm) onConfirm();
        modal.hide();
    });
    
    confirmModal.addEventListener('hidden.bs.modal', () => {
        if (onCancel) onCancel();
        confirmModal.remove();
    });
    
    modal.show();
}
