// frontend/static/js/script.js

// Add input event listeners for real-time validation and submission
document.getElementById('client_id').addEventListener('input', handleInput);
document.getElementById('client_secret').addEventListener('input', handleInput);
document.getElementById('credentialsForm').addEventListener('submit', validateForm);

// Fetch credentials when the page loads
document.addEventListener('DOMContentLoaded', () => {
    fetchCredentials().then(data => {
        document.getElementById('client_id_display').innerText = '****';
        document.getElementById('client_secret_display').innerText = '****';
    });
});

// Function to fetch the credentials from the server
function fetchCredentials() {
    return fetch('/get_credentials')
        .then(response => response.json())
        .then(data => {
            return data;
        })
        .catch(error => console.error('Error fetching credentials:', error));
}

// Functions to toggle the visibility of the credentials
function toggleVisibility(elementId) {
    const display = document.getElementById(elementId);
    if (display.innerHTML === '****') {
        fetchCredentials().then(data => {
            display.innerHTML = data[elementId.replace('_display', '')];
        });
    } else {
        display.innerHTML = '****';
    }
}

// Add click event listeners to the toggle buttons
document.getElementById('toggle_id_btn').onclick = () => toggleVisibility('client_id_display');
document.getElementById('toggle_secret_btn').onclick = () => toggleVisibility('client_secret_display');

// Function to validate credentials
function validateCredentials(input, errorField, invalidField) {
    const value = input.value.trim();
    const valid = /^[a-zA-Z0-9]{30}$/.test(value);

    if (!valid) {
        input.classList.add('error');
        errorField.classList.add('hidden');
        invalidField.classList.remove('hidden');
    } else {
        input.classList.remove('error');
        invalidField.classList.add('hidden');
    }
}

// Function to handle input event
function handleInput(event) {
    const input = event.target;
    const errorField = document.getElementById(input.id + '_error');
    const invalidField = document.getElementById(input.id + '_invalid');
    validateCredentials(input, errorField, invalidField);
}

function validateForm(event) {
    event.preventDefault();
    const fields = ['client_id', 'client_secret'];
    const valid = fields.every(field => {
        const input = document.getElementById(field);
        const error = document.getElementById(`${field}_error`);
        const invalid = document.getElementById(`${field}_invalid`);

        if (input.value.trim() === '') {
            showError(input, error, invalid);
            return false;
        }

        error.classList.add('hidden');
        return validateCredentials(input, error, invalid);
    });

    if (valid) {
        document.getElementById('credentialsForm').submit();
    }
}

function showError(input, error, invalid) {
    input.classList.add('error');
    error.classList.remove('hidden');
    invalid.classList.add('hidden');
}