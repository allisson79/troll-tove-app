// Troll-Tove Spåkone - Interactive Features

// Theme Toggle Functionality
(function() {
    // Get stored theme or check system preference
    function getInitialTheme() {
        const storedTheme = localStorage.getItem('theme');
        if (storedTheme) {
            return storedTheme;
        }
        // Check system preference
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            return 'dark';
        }
        return 'light';
    }
    
    // Apply theme to document
    function applyTheme(theme) {
        if (theme === 'dark') {
            document.body.setAttribute('data-theme', 'dark');
        } else {
            document.body.removeAttribute('data-theme');
        }
        localStorage.setItem('theme', theme);
        
        // Update toggle button if it exists
        const toggleButton = document.getElementById('themeToggle');
        if (toggleButton) {
            const icon = toggleButton.querySelector('.theme-toggle-icon');
            const text = toggleButton.querySelector('.theme-toggle-text');
            if (theme === 'dark') {
                if (icon) icon.textContent = '☀️';
                if (text) text.textContent = 'Lys';
            } else {
                if (icon) icon.textContent = '🌙';
                if (text) text.textContent = 'Mørk';
            }
        }
    }
    
    // Toggle between themes
    function toggleTheme() {
        const currentTheme = document.body.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        applyTheme(newTheme);
    }
    
    // Initialize theme on page load
    document.addEventListener('DOMContentLoaded', function() {
        // Apply initial theme
        const initialTheme = getInitialTheme();
        applyTheme(initialTheme);
        
        // Set up theme toggle button if it exists
        const toggleButton = document.getElementById('themeToggle');
        if (toggleButton) {
            toggleButton.addEventListener('click', toggleTheme);
        }
        
        // Listen for system theme changes
        if (window.matchMedia) {
            window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e) {
                // Only apply system preference if user hasn't manually set a theme
                if (!localStorage.getItem('theme')) {
                    applyTheme(e.matches ? 'dark' : 'light');
                }
            });
        }
    });
})();

// Show loading animation when form is submitted
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    
    if (form) {
        form.addEventListener('submit', function(event) {
            const submitButton = form.querySelector('button[type="submit"]');
            if (submitButton) {
                // Create spinner element using DOM methods
                const spinner = document.createElement('div');
                spinner.className = 'spinner';
                submitButton.textContent = '';
                submitButton.appendChild(spinner);
                submitButton.disabled = true;
            }
        });
    }
    
    // Share button functionality
    const shareButton = document.getElementById('shareButton');
    if (shareButton) {
        shareButton.addEventListener('click', function() {
            const predictionTextElement = document.querySelector('.prediction-text');
            if (predictionTextElement) {
                const predictionText = predictionTextElement.textContent.trim();
                
                // Try to use Web Share API if available
                if (navigator.share) {
                    navigator.share({
                        title: 'Troll-Tove Spådom',
                        text: predictionText,
                        url: window.location.href
                    }).catch(() => {
                        // Fallback to clipboard
                        copyToClipboard(predictionText);
                    });
                } else {
                    // Fallback to clipboard
                    copyToClipboard(predictionText);
                }
            }
        });
    }
});

// Copy text to clipboard - prioritize modern API
function copyToClipboard(text) {
    // Modern Clipboard API (preferred method)
    if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(() => {
            showToast('Spådommen er kopiert til utklippstavla!');
        }).catch(() => {
            // Fallback to deprecated method only if modern API fails
            fallbackCopyToClipboard(text);
        });
    } else {
        // Use deprecated method only for very old browsers
        fallbackCopyToClipboard(text);
    }
}

// Fallback copy method for older browsers (deprecated)
function fallbackCopyToClipboard(text) {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.opacity = '0';
    document.body.appendChild(textarea);
    textarea.select();
    
    try {
        // Note: document.execCommand is deprecated but kept as fallback for old browsers
        document.execCommand('copy');
        showToast('Spådommen er kopiert til utklippstavla!');
    } catch (error) {
        showToast('Kunne ikke kopiere teksten. Prøv igjen!');
    }
    
    document.body.removeChild(textarea);
}

// Show toast notification
function showToast(message) {
    const existingToast = document.querySelector('.toast');
    if (existingToast) {
        existingToast.remove();
    }
    
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = message;
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.classList.add('show');
    }, 10);
    
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => {
            toast.remove();
        }, 300);
    }, 3000);
}
