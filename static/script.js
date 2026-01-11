// Troll-Tove Spåkone - Interactive Features

// Show loading animation when form is submitted
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    
    if (form) {
        form.addEventListener('submit', function(e) {
            const button = form.querySelector('button[type="submit"]');
            if (button) {
                // Create spinner element using DOM methods
                const spinner = document.createElement('div');
                spinner.className = 'spinner';
                button.textContent = '';
                button.appendChild(spinner);
                button.disabled = true;
            }
        });
    }
    
    // Share button functionality
    const shareButton = document.getElementById('shareButton');
    if (shareButton) {
        shareButton.addEventListener('click', function() {
            const predictionText = document.querySelector('.prediction-text');
            if (predictionText) {
                const text = predictionText.textContent.trim();
                
                // Try to use Web Share API if available
                if (navigator.share) {
                    navigator.share({
                        title: 'Troll-Tove Spådom',
                        text: text,
                        url: window.location.href
                    }).catch(() => {
                        // Fallback to clipboard
                        copyToClipboard(text);
                    });
                } else {
                    // Fallback to clipboard
                    copyToClipboard(text);
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
    } catch (err) {
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
