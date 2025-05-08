document.addEventListener('DOMContentLoaded', function () {
    const container = document.getElementById('conversation');
    const promptInput = document.getElementById('prompt-input');
    const submitButton = document.getElementById('submit-prompt');
    const submitFormButton = document.getElementById('submit-form');

    function updateFormState() {
        fetch('/get_form_state')
            .then(response => response.json())
            .then(data => {
                for (const [key, value] of Object.entries(data)) {
                    const element = document.getElementById(key);
                    if (element) {
                        element.textContent = value.toString();
                    }
                }
            })
            .catch(error => console.error('Error fetching form state:', error));
    }

    updateFormState();

    submitButton.addEventListener('click', function() {
        const userPrompt = promptInput.value.trim();
        if (!userPrompt) {
            return;
        }

        const userDiv = document.createElement('div');
        userDiv.className = 'user-msg';
        userDiv.innerHTML = `<b>You:</b> ${userPrompt}`;
        container.appendChild(userDiv);

        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'ai-msg loading';
        loadingDiv.innerHTML = `<b>Gemini:</b> Loading...`;
        container.appendChild(loadingDiv);

        promptInput.value = '';

        fetch(`/get_response?prompt=${encodeURIComponent(userPrompt)}`)
            .then(response => response.text())
            .then(data => {
                loadingDiv.innerHTML = `<b>Gemini:</b> ${data}`;
                loadingDiv.classList.remove('loading');
                updateFormState();
            })
            .catch(error => {
                loadingDiv.innerHTML = `<b>Gemini:</b> Error: ${error}`;
                loadingDiv.classList.add('error');
            });
    });

    submitFormButton.addEventListener('click', function() {
        fetch('/get_form_state')
            .then(response => response.json())
            .then(data => {
                if (data.firstname === "Unknown" || data.lastname === "Unknown" ||
                    data.email === "example@gmail.com" || data.reason_of_contact === "Unknown") {
                    alert("The form still contains unknown values. Please fill in all fields before submitting.");
                    return;
                }

                fetch('/submit_form', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                })
                .then(response => response.json())
                .then(result => {
                    if (result.success) {
                        alert("Form submitted successfully!");
                    } else {
                        alert("Error submitting form: " + result.error);
                    }
                })
                .catch(error => {
                    console.error('Error submitting form:', error);
                    alert("Failed to submit form. Please try again.");
                });
            });
    });
});