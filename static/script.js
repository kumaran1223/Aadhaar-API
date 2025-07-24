// DOM Elements
const uploadForm = document.getElementById('uploadForm');
const searchForm = document.getElementById('searchForm');
const uploadStatus = document.getElementById('uploadStatus');
const searchStatus = document.getElementById('searchStatus');
const resultsSection = document.getElementById('resultsSection');
const resultsContent = document.getElementById('resultsContent');
const loadingOverlay = document.getElementById('loadingOverlay');
const aadhaarNumberInput = document.getElementById('aadhaarNumber');

// Utility Functions
function showLoading() {
    loadingOverlay.classList.add('show');
}

function hideLoading() {
    loadingOverlay.classList.remove('show');
}

function showStatus(element, message, type) {
    element.innerHTML = message;
    element.className = `status-message ${type}`;
    element.style.display = 'block';
    
    // Auto-hide after 5 seconds for success messages
    if (type === 'success') {
        setTimeout(() => {
            element.style.display = 'none';
        }, 5000);
    }
}

function hideStatus(element) {
    element.style.display = 'none';
}

function formatAadhaarNumber(value) {
    // Remove all non-digits
    const digits = value.replace(/\D/g, '');
    
    // Add spaces every 4 digits
    if (digits.length <= 4) {
        return digits;
    } else if (digits.length <= 8) {
        return digits.slice(0, 4) + ' ' + digits.slice(4);
    } else {
        return digits.slice(0, 4) + ' ' + digits.slice(4, 8) + ' ' + digits.slice(8, 12);
    }
}

function createDataTable(data) {
    const table = document.createElement('table');
    table.className = 'data-table';
    
    const fields = [
        { key: 'aadhaar_number', label: 'Aadhaar Number' },
        { key: 'vid', label: 'VID' },
        { key: 'name', label: 'Name' },
        { key: 'name_tamil', label: 'Name (Tamil)' },
        { key: 'guardian_name', label: 'Guardian Name' },
        { key: 'dob', label: 'Date of Birth' },
        { key: 'gender', label: 'Gender' },
        { key: 'address', label: 'Address' },
        { key: 'vtc', label: 'VTC' },
        { key: 'po', label: 'Post Office' },
        { key: 'sub_district', label: 'Sub District' },
        { key: 'district', label: 'District' },
        { key: 'state', label: 'State' },
        { key: 'pincode', label: 'PIN Code' },
        { key: 'phone', label: 'Phone' }
    ];
    
    fields.forEach(field => {
        if (data[field.key]) {
            const row = table.insertRow();
            const labelCell = row.insertCell(0);
            const valueCell = row.insertCell(1);
            
            labelCell.innerHTML = `<strong>${field.label}:</strong>`;
            valueCell.textContent = data[field.key];
        }
    });
    
    return table;
}

// Event Listeners
aadhaarNumberInput.addEventListener('input', function(e) {
    e.target.value = formatAadhaarNumber(e.target.value);
});

// Upload Form Handler
uploadForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const fileInput = document.getElementById('file');
    const passwordInput = document.getElementById('password');
    
    if (!fileInput.files[0]) {
        showStatus(uploadStatus, '<i class="fas fa-exclamation-triangle"></i> Please select a file to upload.', 'error');
        return;
    }
    
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    
    if (passwordInput.value.trim()) {
        formData.append('password', passwordInput.value.trim());
    }
    
    showLoading();
    hideStatus(uploadStatus);
    
    try {
        const response = await fetch('/api/form/submit', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (response.ok && result.success) {
            showStatus(uploadStatus, 
                `<i class="fas fa-check-circle"></i> ${result.message}<br>
                <strong>Aadhaar Number:</strong> ${result.aadhaar_number}`, 
                'success'
            );
            
            // Display extracted data
            if (result.data) {
                resultsContent.innerHTML = '';
                resultsContent.appendChild(createDataTable(result.data));
                resultsSection.style.display = 'block';
                resultsSection.scrollIntoView({ behavior: 'smooth' });
            }
            
            // Reset form
            uploadForm.reset();
            
        } else {
            showStatus(uploadStatus, 
                `<i class="fas fa-exclamation-circle"></i> ${result.message || 'Upload failed'}`, 
                'error'
            );
        }
        
    } catch (error) {
        console.error('Upload error:', error);
        showStatus(uploadStatus, 
            '<i class="fas fa-exclamation-circle"></i> Network error occurred. Please try again.', 
            'error'
        );
    } finally {
        hideLoading();
    }
});

// Search Form Handler
searchForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const aadhaarNumber = aadhaarNumberInput.value.trim();
    
    if (!aadhaarNumber) {
        showStatus(searchStatus, '<i class="fas fa-exclamation-triangle"></i> Please enter an Aadhaar number.', 'error');
        return;
    }
    
    showLoading();
    hideStatus(searchStatus);
    
    try {
        const response = await fetch(`/api/form/${encodeURIComponent(aadhaarNumber)}`);
        const result = await response.json();
        
        if (response.ok && result.success && result.data) {
            showStatus(searchStatus, 
                `<i class="fas fa-check-circle"></i> ${result.message}`, 
                'success'
            );
            
            // Display found data
            resultsContent.innerHTML = '';
            resultsContent.appendChild(createDataTable(result.data));
            resultsSection.style.display = 'block';
            resultsSection.scrollIntoView({ behavior: 'smooth' });
            
        } else {
            showStatus(searchStatus, 
                `<i class="fas fa-info-circle"></i> ${result.message || 'No data found'}`, 
                'info'
            );
            resultsSection.style.display = 'none';
        }
        
    } catch (error) {
        console.error('Search error:', error);
        showStatus(searchStatus, 
            '<i class="fas fa-exclamation-circle"></i> Network error occurred. Please try again.', 
            'error'
        );
    } finally {
        hideLoading();
    }
});

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    console.log('Aadhaar OCR API Frontend Loaded');
    
    // Check API health on page load
    fetch('/health')
        .then(response => response.json())
        .then(data => {
            console.log('API Health:', data);
        })
        .catch(error => {
            console.warn('API health check failed:', error);
        });
});
