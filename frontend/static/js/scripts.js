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
function toggleVisibilityId() {
    var clientIdDisplay = document.getElementById("client_id_display");
    var currentText = clientIdDisplay.innerHTML;
    console.log("Current text:", currentText);
    console.log("clientid:", clientIdDisplay);
    if (currentText === '****') {
        fetchCredentials().then(data => {
            clientIdDisplay.innerHTML = data.client_id;
        });
    } else {
        clientIdDisplay.innerHTML = '****';
    }
    console.log("ID:", '{{ client_id }}');
}
function toggleVisibilitySecret() {
    var clientSecretDisplay = document.getElementById("client_secret_display");
    var currentText = clientSecretDisplay.innerHTML;
    console.log("Current text:", currentText);
    console.log("clientscret:", clientSecretDisplay);
    if (currentText === '****') {
        fetchCredentials().then(data => {
            clientSecretDisplay.innerHTML = data.client_secret;
        });
    } else {
        clientSecretDisplay.innerHTML = '****';
    }
    console.log("Secret:", '{{ client_secret }}');
}

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

// Validate form inputs and show errors if any
function validateForm(event) {
    event.preventDefault();
    var clientIdInput = document.getElementById('client_id');
    var clientSecretInput = document.getElementById('client_secret');
    var clientIdError = document.getElementById('client_id_error');
    var clientSecretError = document.getElementById('client_secret_error');
    var clientIdInvalid = document.getElementById('client_id_invalid');
    var clientSecretInvalid = document.getElementById('client_secret_invalid');
    var valid = true;

    if (clientIdInput.value.trim() === '') {
        clientIdInput.classList.add('error');
        clientIdError.classList.remove('hidden');
        clientIdInvalid.classList.add('hidden');
        valid = false;
    } else {
        clientIdError.classList.add('hidden');
        validateCredentials(clientIdInput, clientIdError, clientIdInvalid);
        if (clientIdInvalid.classList.contains('hidden') === false) {
            valid = false;
        }
    }

    if (clientSecretInput.value.trim() === '') {
        clientSecretInput.classList.add('error');
        clientSecretError.classList.remove('hidden');
        clientSecretInvalid.classList.add('hidden');
        valid = false;
    } else {
        clientSecretError.classList.add('hidden');
        validateCredentials(clientSecretInput, clientSecretError, clientSecretInvalid);
        if (clientSecretInvalid.classList.contains('hidden') === false) {
            valid = false;
        }
    }

    if (valid) {
        document.getElementById('credentialsForm').submit();
    }
}