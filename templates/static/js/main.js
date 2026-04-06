// Main JavaScript for Education Management System

document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap components
    try {
        initializeBootstrap();
    } catch (err) {
        console.warn('Bootstrap init failed:', err);
    }
    
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize form validations
    initializeFormValidations();

    // Initialize submit loading states
    initializeSubmitLoading();
    
    // Initialize data tables
    initializeDataTables();
    
    // Initialize date pickers
    initializeDatePickers();
    
    // Initialize notifications
    initializeNotifications();

    // Initialize theme toggle
    initializeThemeToggle();

    // Keyboard shortcut for top search
    initializeSearchShortcut();

    // Initialize newsletter submission
    initializeNewsletterForm();

    // Initialize chatbot links
    initializeChatbotLinks();

    // Initialize cookie consent banner
    initializeCookieBanner();

    // Ensure fetch includes CSRF token for all POST/PUT/DELETE requests
    enableFetchCsrf();

    // Smooth scrolling for anchor links
    initializeSmoothScroll();

    // Mobile nav behavior
    initializeMobileNav();
    
    // Auto-dismiss alerts
    autoDismissAlerts();
    
    // Handle sidebar collapse
    handleSidebar();
    
    // Handle file upload previews
    handleFileUploads();
    
    // Handle responsive tables
    handleResponsiveTables();

    // Scroll reveal animations
    initializeScrollReveal();

    // Animated counters
    initializeCounters();
});

// Utility function to get cookie value by name
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function readStoredJson(key, fallback) {
    try {
        const raw = window.localStorage.getItem(key);
        return raw ? JSON.parse(raw) : fallback;
    } catch (err) {
        console.warn(`Could not read localStorage key "${key}"`, err);
        return fallback;
    }
}

function writeStoredValue(key, value) {
    try {
        const normalizedValue = typeof value === 'string' ? value : JSON.stringify(value);
        window.localStorage.setItem(key, normalizedValue);
    } catch (err) {
        console.warn(`Could not write localStorage key "${key}"`, err);
    }
}

function setThemeColorMeta(mode) {
    const meta = document.querySelector('meta[name="theme-color"]');
    if (!meta) return;
    meta.setAttribute('content', mode === 'dark' ? '#081221' : '#0b1120');
}

function prefersReducedMotion() {
    return !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
}

function openSharedChatbot(trigger) {
    if (window.AaditechChatbot && typeof window.AaditechChatbot.open === 'function') {
        window.AaditechChatbot.open(trigger || null);
        return;
    }

    const panel = document.querySelector('.aaditech-chatbot__panel');
    const toggle = document.querySelector('.aaditech-chatbot__toggle');
    const input = document.querySelector('.aaditech-chatbot__input');
    if (!panel) return;

    panel.classList.add('is-open');
    if (toggle) {
        toggle.setAttribute('aria-expanded', 'true');
    }
    if (input) {
        input.focus();
    }
}

function focusGlobalSearch(triggerOpen) {
    const searchInput = document.querySelector('.top-search input[type="search"], .top-search .form-control[type="search"]');
    if (!searchInput) return;

    const collapseEl = searchInput.closest('.navbar-collapse');
    if (triggerOpen && collapseEl && !collapseEl.classList.contains('show') && window.matchMedia('(max-width: 1199.98px)').matches) {
        if (typeof bootstrap !== 'undefined' && bootstrap.Collapse) {
            const instance = bootstrap.Collapse.getInstance(collapseEl) || new bootstrap.Collapse(collapseEl, { toggle: false });
            instance.show();
        } else {
            collapseEl.classList.add('show');
        }
    }

    searchInput.focus();
    searchInput.select();
}

// Enhance fetch to automatically include CSRF token for same-origin unsafe requests
function enableFetchCsrf() {
    if (!window.fetch) return;

    const originalFetch = window.fetch.bind(window);
    window.fetch = function(input, init) {
        try {
            init = init || {};
            const requestMethod =
                init.method ||
                (typeof input !== 'string' && input && input.method) ||
                'GET';
            const method = String(requestMethod).toUpperCase();
            const isUnsafe = ['POST','PUT','PATCH','DELETE'].includes(method);
            const url = (typeof input === 'string') ? input : (input && input.url) || window.location.href;

            // Only add CSRF for same-origin requests
            const resolvedUrl = new URL(url, window.location.origin);
            const isSameOrigin = resolvedUrl.origin === window.location.origin;
            if (isUnsafe && isSameOrigin) {
                const headers = new Headers(init.headers || (typeof input !== 'string' && input && input.headers) || {});
                // Respect existing header if explicitly provided
                if (!headers.has('X-CSRFToken') && !headers.has('x-csrftoken')) {
                    const token = document.querySelector('input[name="csrfmiddlewaretoken"]')?.value || getCookie('csrftoken') || document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') || '';
                    if (token) {
                        headers.set('X-CSRFToken', token);
                    }
                }
                init.headers = headers;
            }
        } catch (err) {
            console.warn('enableFetchCsrf error', err);
        }
        return originalFetch(input, init);
    };
}

// Initialize Bootstrap Components
function initializeBootstrap() {
    if (typeof bootstrap === 'undefined') {
        // Lightweight fallback for dropdown menus when Bootstrap JS is unavailable.
        const dropdowns = document.querySelectorAll('.dropdown-toggle');
        dropdowns.forEach(dropdown => {
            dropdown.addEventListener('click', function(e) {
                e.preventDefault();
                const menu = this.nextElementSibling;
                if (menu) {
                    menu.classList.toggle('show');
                }
            });
        });

        document.addEventListener('click', function(e) {
            if (!e.target.closest('.dropdown')) {
                document.querySelectorAll('.dropdown-menu').forEach(dropdown => {
                    dropdown.classList.remove('show');
                });
            }
        });
        return;
    }
    // Tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Modals
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        modal.addEventListener('shown.bs.modal', function() {
            const focusable = modal.querySelector('input, select, textarea, button');
            if (focusable) focusable.focus();
        });
    });
    
}

// Initialize Tooltips
function initializeTooltips() {
    // Mouse + keyboard + touch friendly tooltip behavior.
    const tooltips = document.querySelectorAll('[title]');
    const isTouchDevice = window.matchMedia && window.matchMedia('(hover: none)').matches;
    let activeTooltipTrigger = null;
    let activeTooltipEl = null;

    const removeActiveTooltip = () => {
        if (activeTooltipTrigger) {
            const originalTitle = activeTooltipTrigger.getAttribute('data-original-title');
            if (originalTitle) {
                activeTooltipTrigger.setAttribute('title', originalTitle);
                activeTooltipTrigger.removeAttribute('data-original-title');
            }
        }
        if (activeTooltipEl) {
            activeTooltipEl.remove();
        }
        activeTooltipEl = null;
        activeTooltipTrigger = null;
    };

    const positionTooltip = (trigger, tooltipEl) => {
        const rect = trigger.getBoundingClientRect();
        const horizontalCenter = rect.left + rect.width / 2;
        const minLeft = 12 + tooltipEl.offsetWidth / 2;
        const maxLeft = window.innerWidth - 12 - tooltipEl.offsetWidth / 2;
        const clampedLeft = Math.min(Math.max(horizontalCenter, minLeft), maxLeft);
        const top = Math.max(rect.top - tooltipEl.offsetHeight - 10, 12);

        tooltipEl.style.left = `${clampedLeft}px`;
        tooltipEl.style.top = `${top}px`;
    };

    const showTooltip = function () {
        if (this.hasAttribute('data-bs-toggle')) return;
        const title = this.getAttribute('title');
        if (!title) return;

        removeActiveTooltip();

        const tooltipEl = document.createElement('div');
        tooltipEl.className = 'custom-tooltip';
        tooltipEl.setAttribute('role', 'tooltip');
        tooltipEl.textContent = title;
        document.body.appendChild(tooltipEl);
        positionTooltip(this, tooltipEl);

        this.setAttribute('data-original-title', title);
        this.removeAttribute('title');
        activeTooltipTrigger = this;
        activeTooltipEl = tooltipEl;
    };

    const hideTooltip = function () {
        if (!this || activeTooltipTrigger === this) {
            removeActiveTooltip();
        }
    };

    tooltips.forEach(tooltip => {
        if (!isTouchDevice) {
            tooltip.addEventListener('mouseenter', showTooltip);
            tooltip.addEventListener('mouseleave', hideTooltip);
        }
        tooltip.addEventListener('focus', showTooltip);
        tooltip.addEventListener('blur', hideTooltip);
        tooltip.addEventListener('click', function () {
            const isOpen = !!this.getAttribute('data-original-title');
            if (isOpen) {
                hideTooltip.call(this);
            } else {
                showTooltip.call(this);
            }
        });
    });
}

// Initialize Form Validations
function initializeFormValidations() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!this.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
                
                // Add Bootstrap validation classes
                const inputs = this.querySelectorAll('input, select, textarea');
                inputs.forEach(input => {
                    if (!input.checkValidity()) {
                        input.classList.add('is-invalid');
                        
                        // Show error message
                        let errorDiv = input.nextElementSibling;
                        if (!errorDiv || !errorDiv.classList.contains('invalid-feedback')) {
                            errorDiv = document.createElement('div');
                            errorDiv.className = 'invalid-feedback';
                            input.parentNode.appendChild(errorDiv);
                        }
                        
                        if (input.validity.valueMissing) {
                            errorDiv.textContent = 'This field is required';
                        } else if (input.validity.typeMismatch) {
                            errorDiv.textContent = 'Please enter a valid ' + input.type;
                        } else if (input.validity.patternMismatch) {
                            errorDiv.textContent = 'Please match the requested format';
                        } else if (input.validity.tooShort) {
                            errorDiv.textContent = 'Input is too short';
                        } else if (input.validity.tooLong) {
                            errorDiv.textContent = 'Input is too long';
                        }
                    } else {
                        input.classList.remove('is-invalid');
                        input.classList.add('is-valid');
                    }
                });
                
                this.classList.add('was-validated');
            }
        });
        
        // Real-time validation
        const inputs = form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.addEventListener('input', function() {
                if (this.checkValidity()) {
                    this.classList.remove('is-invalid');
                    this.classList.add('is-valid');
                    
                    const errorDiv = this.nextElementSibling;
                    if (errorDiv && errorDiv.classList.contains('invalid-feedback')) {
                        errorDiv.textContent = '';
                    }
                } else {
                    this.classList.remove('is-valid');
                }
            });
            
            input.addEventListener('blur', function() {
                if (!this.checkValidity()) {
                    this.classList.add('is-invalid');
                }
            });
        });
    });
}

// Initialize submit loading indicators
function initializeSubmitLoading() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            if (form.hasAttribute('data-ajax') || form.hasAttribute('data-no-loading')) {
                return;
            }

            if (!form.checkValidity()) {
                return;
            }

            const submitBtn = form.querySelector('button[type=\"submit\"], input[type=\"submit\"]');
            if (!submitBtn || submitBtn.classList.contains('btn-loading')) {
                return;
            }

            submitBtn.classList.add('btn-loading');
            submitBtn.setAttribute('aria-busy', 'true');
            submitBtn.disabled = true;
        });
    });
}

// Initialize Data Tables
function initializeDataTables() {
    const tables = document.querySelectorAll('table[data-table="true"]');
    tables.forEach(table => {
        if (table.dataset.enhanced === 'true') return;
        table.dataset.enhanced = 'true';

        const tbody = table.querySelector('tbody');
        if (!tbody) return;

        const tableContainer = table.closest('.table-responsive') || table.parentNode;
        const tableHost = tableContainer.parentNode;
        const headerCells = Array.from(table.querySelectorAll('thead th'));
        const rows = Array.from(tbody.querySelectorAll('tr'));
        const emptyRow = rows.find(row => row.children.length === 1 && row.querySelector('td[colspan]'));
        const dataRows = rows.filter(row => row !== emptyRow);
        const pageSize = Math.max(parseInt(table.dataset.pageSize || '8', 10), 1);
        const headers = Array.from(table.querySelectorAll('thead th[data-sortable="true"]'));

        tableContainer.classList.add('table-shell');

        dataRows.forEach(row => {
            Array.from(row.children).forEach((cell, index) => {
                const label = headerCells[index] ? headerCells[index].textContent.trim() : 'Value';
                cell.setAttribute('data-label', label);
            });
        });

        if (!dataRows.length) return;

        const toolbar = document.createElement('div');
        toolbar.className = 'table-toolbar';
        toolbar.innerHTML = `
            <div class="table-toolbar__search">
                <i class="fa-solid fa-magnifying-glass" aria-hidden="true"></i>
                <input type="search" class="form-control" placeholder="Search this table">
            </div>
            <div class="table-toolbar__meta" aria-live="polite"></div>
        `;
        tableHost.insertBefore(toolbar, tableContainer);

        const pagination = document.createElement('div');
        pagination.className = 'table-pagination';
        pagination.innerHTML = `
            <div class="table-pagination__label" aria-live="polite"></div>
            <button type="button" class="btn btn-outline-secondary btn-sm" data-table-prev aria-label="Previous page">
                <i class="fa-solid fa-chevron-left"></i>
            </button>
            <button type="button" class="btn btn-outline-secondary btn-sm" data-table-next aria-label="Next page">
                <i class="fa-solid fa-chevron-right"></i>
            </button>
        `;
        if (tableContainer.nextSibling) {
            tableHost.insertBefore(pagination, tableContainer.nextSibling);
        } else {
            tableHost.appendChild(pagination);
        }

        const searchInput = toolbar.querySelector('input');
        const meta = toolbar.querySelector('.table-toolbar__meta');
        const pageLabel = pagination.querySelector('.table-pagination__label');
        const prevBtn = pagination.querySelector('[data-table-prev]');
        const nextBtn = pagination.querySelector('[data-table-next]');

        let filteredRows = [...dataRows];
        let currentPage = 1;
        let activeSort = null;

        const parseValue = (value) => {
            const trimmed = value.trim();
            const numberText = trimmed.replace(/[^0-9.-]/g, '');
            if (numberText && !Number.isNaN(Number(numberText))) {
                return Number(numberText);
            }

            const dateValue = Date.parse(trimmed);
            if (!Number.isNaN(dateValue) && /\d/.test(trimmed)) {
                return dateValue;
            }

            return trimmed.toLowerCase();
        };

        const sortRows = () => {
            if (!activeSort) return;

            filteredRows.sort((rowA, rowB) => {
                const aValue = parseValue(rowA.children[activeSort.index]?.textContent || '');
                const bValue = parseValue(rowB.children[activeSort.index]?.textContent || '');
                const direction = activeSort.direction === 'desc' ? -1 : 1;

                if (typeof aValue === 'number' && typeof bValue === 'number') {
                    return (aValue - bValue) * direction;
                }

                return String(aValue).localeCompare(String(bValue), undefined, {
                    numeric: true,
                    sensitivity: 'base'
                }) * direction;
            });
        };

        const updatePagination = () => {
            const totalRows = filteredRows.length;
            const totalPages = Math.max(Math.ceil(totalRows / pageSize), 1);
            currentPage = Math.min(currentPage, totalPages);

            const start = (currentPage - 1) * pageSize;
            const visibleRows = filteredRows.slice(start, start + pageSize);
            const visibleSet = new Set(visibleRows);

            dataRows.forEach(row => {
                row.style.display = visibleSet.has(row) ? '' : 'none';
            });

            if (emptyRow) {
                emptyRow.style.display = totalRows ? 'none' : '';
            }

            meta.textContent = totalRows
                ? `${totalRows} result${totalRows === 1 ? '' : 's'}`
                : 'No matching results';

            pageLabel.textContent = totalRows
                ? `Page ${currentPage} of ${totalPages}`
                : 'Nothing to paginate';

            prevBtn.disabled = currentPage <= 1 || !totalRows;
            nextBtn.disabled = currentPage >= totalPages || !totalRows;
        };

        const applyFilters = () => {
            const query = (searchInput.value || '').trim().toLowerCase();
            filteredRows = dataRows.filter(row => row.textContent.toLowerCase().includes(query));
            sortRows();
            currentPage = 1;
            updatePagination();
        };

        searchInput.addEventListener('input', applyFilters);

        headers.forEach(header => {
            header.style.cursor = 'pointer';
            header.addEventListener('click', function() {
                const columnIndex = Array.from(this.parentNode.children).indexOf(this);
                const nextDirection = this.classList.contains('sort-asc') ? 'desc' : 'asc';

                headers.forEach(item => item.classList.remove('sort-asc', 'sort-desc'));
                this.classList.add(nextDirection === 'asc' ? 'sort-asc' : 'sort-desc');

                activeSort = {
                    index: columnIndex,
                    direction: nextDirection
                };
                sortRows();
                updatePagination();
            });
        });

        prevBtn.addEventListener('click', () => {
            if (currentPage > 1) {
                currentPage -= 1;
                updatePagination();
            }
        });

        nextBtn.addEventListener('click', () => {
            const totalPages = Math.max(Math.ceil(filteredRows.length / pageSize), 1);
            if (currentPage < totalPages) {
                currentPage += 1;
                updatePagination();
            }
        });

        updatePagination();
    });
}

// Initialize Date Pickers
function initializeDatePickers() {
    const dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(input => {
        // Set min date to today for future dates
        if (input.hasAttribute('data-future-only')) {
            const today = new Date().toISOString().split('T')[0];
            input.min = today;
        }
        
        // Set max date to today for past dates
        if (input.hasAttribute('data-past-only')) {
            const today = new Date().toISOString().split('T')[0];
            input.max = today;
        }
        
        if (input.hasAttribute('data-no-picker-wrap') || input.closest('.date-picker') || input.closest('.form-floating')) {
            return;
        }

        const wrapper = document.createElement('div');
        wrapper.className = 'input-group date-picker';
        input.parentNode.insertBefore(wrapper, input);
        wrapper.appendChild(input);

        const icon = document.createElement('span');
        icon.className = 'input-group-text';
        icon.innerHTML = '<i class="fas fa-calendar"></i>';
        wrapper.appendChild(icon);
        
        // If browser doesn't support date input, use flatpickr
        if (input.type === 'text') {
            // You can integrate flatpickr or another datepicker library here
            console.log('Consider adding a datepicker library for better UX');
        }
    });
}

// Initialize Notifications
function initializeNotifications() {
    // Check for browser notifications permission
    if ('Notification' in window) {
        if (Notification.permission === 'default') {
            Notification.requestPermission();
        }
    }
    
    // Handle real-time notifications (WebSocket example)
    if (typeof WebSocket !== 'undefined') {
        // Example WebSocket connection for real-time updates
        // const ws = new WebSocket('ws://your-domain/notifications/');
        // ws.onmessage = function(event) {
        //     const notification = JSON.parse(event.data);
        //     showNotification(notification);
        // };
    }

    initializeHeaderNotifications();
}

function initializeThemeToggle() {
    const toggle = document.getElementById('darkModeToggle');
    const mediaQuery = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;

    const applyTheme = (mode) => {
        document.body.classList.toggle('dark-mode', mode === 'dark');
        setThemeColorMeta(mode);
        if (toggle) {
            toggle.setAttribute('aria-pressed', mode === 'dark' ? 'true' : 'false');
            const icon = toggle.querySelector('i');
            if (icon) {
                icon.className = mode === 'dark' ? 'fa-solid fa-sun' : 'fa-solid fa-moon';
            }
        }
    };

    const saved = (() => {
        try {
            return localStorage.getItem('themeMode');
        } catch (err) {
            return null;
        }
    })();
    const prefersDark = mediaQuery ? mediaQuery.matches : false;
    applyTheme(saved || (prefersDark ? 'dark' : 'light'));

    if (toggle) {
        toggle.addEventListener('click', function () {
            const isDark = document.body.classList.contains('dark-mode');
            const next = isDark ? 'light' : 'dark';
            writeStoredValue('themeMode', next);
            applyTheme(next);
        });
    }

    if (mediaQuery && typeof mediaQuery.addEventListener === 'function') {
        mediaQuery.addEventListener('change', function (event) {
            const storedMode = (() => {
                try {
                    return localStorage.getItem('themeMode');
                } catch (err) {
                    return null;
                }
            })();
            if (!storedMode) {
                applyTheme(event.matches ? 'dark' : 'light');
            }
        });
    }
}

function initializeHeaderNotifications() {
    const bellIcon = document.querySelector('.nav-link .fa-bell');
    const dot = document.querySelector('.notification-dot');
    const bellLink = bellIcon ? bellIcon.closest('.nav-link') : null;
    const dropdown = bellLink ? bellLink.parentElement.querySelector('.dropdown-menu') : null;

    if (!bellIcon || !dot || !dropdown || !bellLink) return;

    const defaultNotifs = [
        { id: 1, title: 'New notice published', url: '/dashboard/notices/' },
        { id: 2, title: 'Weekly report ready', url: '/dashboard/reports/' },
        { id: 3, title: 'Fee reminders updated', url: '/dashboard/fees/' }
    ];

    const stored = (() => {
        const items = readStoredJson('emsNotifications', defaultNotifs);
        return Array.isArray(items) && items.length ? items : defaultNotifs;
    })();
    const read = new Set((() => {
        const items = readStoredJson('emsNotificationsRead', []);
        return Array.isArray(items) ? items : [];
    })());

    const persistRead = () => {
        writeStoredValue('emsNotificationsRead', Array.from(read));
    };

    const render = () => {
        dropdown.innerHTML = '';
        const header = document.createElement('li');
        header.innerHTML = '<span class="dropdown-item-text small text-muted">Notifications</span>';
        dropdown.appendChild(header);

        stored.forEach(item => {
            const li = document.createElement('li');
            const a = document.createElement('a');
            a.className = 'dropdown-item';
            a.href = item.url;
            a.textContent = item.title;
            if (!read.has(item.id)) {
                a.style.fontWeight = '600';
            }
            a.addEventListener('click', function () {
                if (!read.has(item.id)) {
                    read.add(item.id);
                    persistRead();
                }
            });
            li.appendChild(a);
            dropdown.appendChild(li);
        });

        const divider = document.createElement('li');
        divider.innerHTML = '<hr class="dropdown-divider">';
        dropdown.appendChild(divider);

        const clear = document.createElement('li');
        const clearBtn = document.createElement('button');
        clearBtn.className = 'dropdown-item';
        clearBtn.type = 'button';
        clearBtn.textContent = 'Mark all as read';
        clearBtn.addEventListener('click', function () {
            stored.forEach(item => read.add(item.id));
            persistRead();
            updateDot();
            render();
        });
        clear.appendChild(clearBtn);
        dropdown.appendChild(clear);
    };

    const updateDot = () => {
        const unreadCount = stored.filter(item => !read.has(item.id)).length;
        dot.style.display = unreadCount > 0 ? 'inline-block' : 'none';
    };

    updateDot();
    render();
}

function initializeNewsletterForm() {
    const forms = document.querySelectorAll('.footer-newsletter, .js-newsletter-form');
    if (!forms.length) return;

    forms.forEach(form => {
        const feedback = form.querySelector('.newsletter-feedback');
        const submitBtn = form.querySelector('button[type="submit"], input[type="submit"]');
        form.addEventListener('submit', async function (event) {
            event.preventDefault();
            if (!form.checkValidity()) return;

            const formData = new FormData(form);
            const csrf = form.querySelector('input[name="csrfmiddlewaretoken"]')?.value || '';

            try {
                if (submitBtn) {
                    submitBtn.classList.add('btn-loading');
                    submitBtn.setAttribute('aria-busy', 'true');
                    submitBtn.disabled = true;
                }
                const response = await fetch(form.action, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrf
                    },
                    body: formData
                });

                const data = await response.json();
                if (!response.ok) {
                    throw new Error(data.error || 'Subscription failed');
                }
                if (feedback) {
                    feedback.classList.remove('text-danger');
                    feedback.classList.add('text-success');
                    feedback.textContent = data.message || 'Subscribed successfully.';
                }
                form.reset();
            } catch (err) {
                if (feedback) {
                    feedback.classList.remove('text-success');
                    feedback.classList.add('text-danger');
                    feedback.textContent = 'Could not subscribe. Try again later.';
                }
            } finally {
                if (submitBtn) {
                    submitBtn.classList.remove('btn-loading');
                    submitBtn.removeAttribute('aria-busy');
                    submitBtn.disabled = false;
                }
            }
        });
    });
}

function initializeChatbotLinks() {
    const links = document.querySelectorAll('.open-chatbot-link');
    const panel = document.querySelector('.aaditech-chatbot__panel');
    if (!links.length || !panel) return;

    links.forEach(link => {
        link.addEventListener('click', function (event) {
            event.preventDefault();
            openSharedChatbot(link);
        });

        link.addEventListener('keydown', function (event) {
            if (event.key === 'Enter' || event.key === ' ') {
                event.preventDefault();
                openSharedChatbot(link);
            }
        });
    });

    window.addEventListener('scroll', removeActiveTooltip, { passive: true });
    window.addEventListener('resize', removeActiveTooltip);
}

function initializeSearchShortcut() {
    const searchInput = document.querySelector('.top-search input[type="search"], .top-search .form-control[type="search"]');
    if (!searchInput) return;

    document.addEventListener('keydown', function (event) {
        const key = (event.key || '').toLowerCase();
        const isMetaCombo = event.ctrlKey || event.metaKey;
        const activeTag = document.activeElement ? document.activeElement.tagName : '';
        const isTypingContext = ['INPUT', 'TEXTAREA', 'SELECT'].includes(activeTag) || document.activeElement?.isContentEditable;

        if (isMetaCombo && key === 'k') {
            event.preventDefault();
            focusGlobalSearch(true);
            return;
        }

        if (event.key === 'Escape' && document.activeElement === searchInput) {
            searchInput.blur();
        }

        if (!isTypingContext && key === '/' && !event.altKey && !event.shiftKey) {
            event.preventDefault();
            focusGlobalSearch(true);
        }
    });
}

function initializeCookieBanner() {
    const banner = document.querySelector('.cookie-banner');
    if (!banner) return;

    const accepted = localStorage.getItem('ems_cookie_consent');
    if (!accepted) {
        banner.classList.add('is-visible');
    }

    const acceptBtn = banner.querySelector('[data-cookie-accept]');
    const dismissBtn = banner.querySelector('[data-cookie-dismiss]');

    if (acceptBtn) {
        acceptBtn.addEventListener('click', () => {
            localStorage.setItem('ems_cookie_consent', 'accepted');
            banner.classList.remove('is-visible');
        });
    }

    if (dismissBtn) {
        dismissBtn.addEventListener('click', () => {
            localStorage.setItem('ems_cookie_consent', 'dismissed');
            banner.classList.remove('is-visible');
        });
    }
}

// Smooth scrolling with header offset
function initializeSmoothScroll() {
    const links = document.querySelectorAll('a[href^="#"]');
    if (!links.length) return;

    const header = document.querySelector('header.navbar, .topbar');

    links.forEach(link => {
        link.addEventListener('click', function (event) {
            const href = link.getAttribute('href');
            if (!href || href === '#' || href.length < 2 || link.hasAttribute('data-bs-toggle')) return;

            let targetUrl;
            try {
                targetUrl = new URL(link.href, window.location.origin);
            } catch (err) {
                return;
            }

            if (targetUrl.origin !== window.location.origin || targetUrl.pathname !== window.location.pathname || !targetUrl.hash) {
                return;
            }

            const target = document.querySelector(targetUrl.hash);
            if (!target) return;

            event.preventDefault();
            const offset = header ? header.offsetHeight + 12 : 0;
            const top = target.getBoundingClientRect().top + window.pageYOffset - offset;
            window.scrollTo({ top, behavior: prefersReducedMotion() ? 'auto' : 'smooth' });
        });
    });
}

// Close mobile nav after clicking a link
function initializeMobileNav() {
    const collapseEl = document.querySelector('.navbar-collapse');
    if (!collapseEl) return;

    const links = collapseEl.querySelectorAll('.nav-link, .dropdown-item');
    if (!links.length) return;

    const hideCollapse = () => {
        if (typeof bootstrap !== 'undefined' && bootstrap.Collapse) {
            const instance = bootstrap.Collapse.getInstance(collapseEl) || new bootstrap.Collapse(collapseEl, { toggle: false });
            instance.hide();
        } else {
            collapseEl.classList.remove('show');
        }
    };

    links.forEach(link => {
        link.addEventListener('click', () => {
            if (window.matchMedia('(max-width: 991.98px)').matches) {
                hideCollapse();
            }
        });
    });
}

// Auto Dismiss Alerts
function autoDismissAlerts() {
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            if (typeof bootstrap !== 'undefined' && bootstrap.Alert) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            } else {
                alert.remove();
            }
        }, 5000); // Auto dismiss after 5 seconds
    });
}

// Handle Sidebar
function handleSidebar() {
    const sidebar = document.getElementById('sidebarMenu');
    const toggles = document.querySelectorAll('.sidebar-toggle');
    const backdrop = document.querySelector('[data-sidebar-backdrop]');

    if (!sidebar || toggles.length === 0) return;

    const isDesktop = () => window.matchMedia('(min-width: 992px)').matches;
    const navLinks = Array.from(sidebar.querySelectorAll('.nav-link'));

    const applyState = () => {
        const open = document.body.classList.contains('sidebar-open');
        sidebar.classList.toggle('show', open);
        sidebar.setAttribute('aria-hidden', open ? 'false' : 'true');
        if (backdrop) {
            backdrop.setAttribute('aria-hidden', open ? 'false' : 'true');
        }
        toggles.forEach(toggle => {
            toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
            toggle.setAttribute('aria-controls', sidebar.id);
        });
    };

    const markActiveLink = () => {
        if (!navLinks.length) return;
        const normalizePath = (path) => {
            if (!path) return '/';
            const trimmed = path.replace(/\/+$/, '');
            return trimmed.length ? trimmed : '/';
        };
        const currentPath = normalizePath(window.location.pathname);
        let bestMatch = null;

        navLinks.forEach(link => {
            let linkPath = '/';
            try {
                linkPath = normalizePath(new URL(link.href, window.location.origin).pathname);
            } catch (err) {
                return;
            }

            const isMatch = currentPath === linkPath || (linkPath !== '/' && currentPath.startsWith(`${linkPath}/`));
            if (isMatch && (!bestMatch || linkPath.length > bestMatch.path.length)) {
                bestMatch = { link, path: linkPath };
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            link.removeAttribute('aria-current');
        });

        if (bestMatch) {
            bestMatch.link.classList.add('active');
            bestMatch.link.setAttribute('aria-current', 'page');
        }
    };

    const setOpen = (open) => {
        document.body.classList.toggle('sidebar-open', open);
        applyState();
    };

    setOpen(false);
    markActiveLink();

    const handleToggleClick = () => {
        const next = !document.body.classList.contains('sidebar-open');
        setOpen(next);
    };

    toggles.forEach(toggle => {
        toggle.addEventListener('click', handleToggleClick);
    });

    if (backdrop) {
        backdrop.addEventListener('click', () => setOpen(false));
    }

    sidebar.addEventListener('click', (event) => {
        const link = event.target.closest('.nav-link');
        if (link && !isDesktop()) {
            setOpen(false);
        }
    });

    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape' && document.body.classList.contains('sidebar-open')) {
            setOpen(false);
        }
    });

    window.addEventListener('resize', applyState);
}

// Handle File Uploads
function handleFileUploads() {
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        input.addEventListener('change', function() {
            const files = this.files;
            const previewContainer = this.nextElementSibling || this.parentNode.nextElementSibling;
            
            if (previewContainer && previewContainer.classList.contains('file-preview')) {
                previewContainer.innerHTML = '';
                
                Array.from(files).forEach(file => {
                    const preview = document.createElement('div');
                    preview.className = 'file-preview-item';
                    
                    if (file.type.startsWith('image/')) {
                        const img = document.createElement('img');
                        img.src = URL.createObjectURL(file);
                        img.className = 'img-thumbnail';
                        preview.appendChild(img);
                    } else {
                        const icon = document.createElement('i');
                        icon.className = 'fas fa-file';
                        preview.appendChild(icon);
                    }
                    
                    const name = document.createElement('span');
                    name.textContent = file.name;
                    preview.appendChild(name);
                    
                    const size = document.createElement('small');
                    size.textContent = formatFileSize(file.size);
                    preview.appendChild(size);
                    
                    previewContainer.appendChild(preview);
                });
            }
        });
    });
}

// Handle Responsive Tables
function handleResponsiveTables() {
    const tables = document.querySelectorAll('.table-responsive table');
    tables.forEach(table => {
        if (!table.parentNode.classList.contains('table-responsive')) {
            const wrapper = document.createElement('div');
            wrapper.className = 'table-responsive';
            table.parentNode.insertBefore(wrapper, table);
            wrapper.appendChild(table);
        }

        const wrapper = table.parentNode;
        wrapper.classList.add('table-shell');

        const syncScrollState = () => {
            const maxScrollLeft = Math.max(wrapper.scrollWidth - wrapper.clientWidth, 0);
            const isScrollable = maxScrollLeft > 8;
            const scrollLeft = wrapper.scrollLeft;
            wrapper.classList.toggle('is-scrollable', isScrollable);
            wrapper.classList.toggle('is-scrolled', scrollLeft > 6);
            wrapper.classList.toggle('is-scroll-end', scrollLeft >= maxScrollLeft - 6);
        };

        syncScrollState();
        wrapper.addEventListener('scroll', syncScrollState, { passive: true });
        window.addEventListener('resize', syncScrollState);
    });
}

// Scroll Reveal Animations
function initializeScrollReveal() {
    const items = document.querySelectorAll('.reveal-on-scroll');
    if (!items.length) return;

    if (!('IntersectionObserver' in window) || prefersReducedMotion()) {
        items.forEach(item => item.classList.add('is-visible'));
        return;
    }

    const observer = new IntersectionObserver((entries, obs) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                obs.unobserve(entry.target);
            }
        });
    }, { threshold: 0.18 });

    items.forEach(item => observer.observe(item));
}

// Animated Counters
function initializeCounters() {
    const counters = document.querySelectorAll('[data-counter]');
    if (!counters.length) return;

    if (!('IntersectionObserver' in window) || prefersReducedMotion()) {
        counters.forEach(counter => {
            const target = Number(counter.getAttribute('data-counter')) || 0;
            counter.textContent = target.toLocaleString();
        });
        return;
    }

    const animateCounter = (el) => {
        const target = Number(el.getAttribute('data-counter')) || 0;
        const duration = 1400;
        const startTime = performance.now();

        const update = (now) => {
            const progress = Math.min((now - startTime) / duration, 1);
            const value = Math.floor(progress * target);
            el.textContent = value.toLocaleString();
            if (progress < 1) requestAnimationFrame(update);
        };

        requestAnimationFrame(update);
    };

    const observer = new IntersectionObserver((entries, obs) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounter(entry.target);
                obs.unobserve(entry.target);
            }
        });
    }, { threshold: 0.3 });

    counters.forEach(counter => observer.observe(counter));
}

// Utility Functions
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function showNotification(notification) {
    // Create notification element
    const notificationEl = document.createElement('div');
    notificationEl.className = `alert alert-${notification.type} alert-dismissible fade show`;
    notificationEl.role = 'alert';
    const messageText = document.createTextNode(notification.message || 'Action completed.');
    const closeBtn = document.createElement('button');
    closeBtn.type = 'button';
    closeBtn.className = 'btn-close';
    closeBtn.setAttribute('data-bs-dismiss', 'alert');
    closeBtn.setAttribute('aria-label', 'Close');
    notificationEl.appendChild(messageText);
    notificationEl.appendChild(closeBtn);
    
    // Add to notifications container
    const container = document.querySelector('.messages-container') || document.querySelector('main');
    if (container) {
        container.prepend(notificationEl);
    }
    
    // Auto dismiss
    setTimeout(() => {
        if (typeof bootstrap !== 'undefined' && bootstrap.Alert) {
            const bsAlert = new bootstrap.Alert(notificationEl);
            bsAlert.close();
        } else {
            notificationEl.remove();
        }
    }, 5000);
    
    // Browser notification
    if ('Notification' in window && Notification.permission === 'granted') {
        new Notification(notification.title || 'EMS Notification', {
            body: notification.message,
            icon: '/static/images/aaditech_logo.jpeg'
        });
    }
}

// Export functions for use in other scripts
window.EMS = {
    showNotification,
    formatFileSize,
    initializeFormValidations,
    openChatbot: openSharedChatbot,
    focusSearch: focusGlobalSearch
};

// Add global error handler
window.addEventListener('error', function(e) {
    console.error('Global error:', e.error);
    
    // Show user-friendly error message
    if (e.error && e.error.message) {
        showNotification({
            type: 'danger',
            message: 'An error occurred. Please try again.'
        });
    }
});

// Handle AJAX forms
document.addEventListener('submit', function(e) {
    const form = e.target;
    if (form.hasAttribute('data-ajax')) {
        e.preventDefault();
        
        const formData = new FormData(form);
        const submitBtn = form.querySelector('button[type="submit"]');
        const originalText = submitBtn ? submitBtn.innerHTML : '';
        
        // Show loading state
        if (submitBtn) {
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
            submitBtn.disabled = true;
        }
        
        // Get CSRF token from form or cookie
        const csrfToken = form.querySelector('input[name="csrfmiddlewaretoken"]')?.value || 
                         document.querySelector('input[name="csrfmiddlewaretoken"]')?.value || 
                         getCookie('csrftoken') || '';
        
        fetch(form.action, {
            method: form.method,
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrfToken
            }
        })
        .then(async response => {
            let data = {};
            try {
                data = await response.json();
            } catch (err) {
                data = { success: response.ok, message: response.ok ? 'Operation successful' : 'Operation failed' };
            }
            return { response, data };
        })
        .then(({ response, data }) => {
            if (!response.ok && data.success === undefined) {
                data.success = false;
            }
            if (data.success) {
                showNotification({
                    type: 'success',
                    message: data.message || 'Operation successful'
                });
                
                if (data.redirect) {
                    setTimeout(() => {
                        window.location.href = data.redirect;
                    }, 1500);
                }
            } else {
                showNotification({
                    type: 'danger',
                    message: data.message || 'Operation failed'
                });
            }
        })
        .catch(error => {
            showNotification({
                type: 'danger',
                message: 'An error occurred. Please try again.'
            });
        })
        .finally(() => {
            // Reset button state
            if (submitBtn) {
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            }
        });
    }
});
