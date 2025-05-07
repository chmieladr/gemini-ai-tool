document.addEventListener('DOMContentLoaded', function () {
    const container = document.getElementById('conversation');
    const promptInput = document.getElementById('prompt-input');
    const submitButton = document.getElementById('submit-prompt');

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
});