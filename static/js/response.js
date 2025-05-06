document.addEventListener('DOMContentLoaded', function () {
    const container = document.getElementById('response-container');
    const promptInput = document.getElementById('prompt-input');
    const submitButton = document.getElementById('submit-prompt');

    submitButton.addEventListener('click', function() {
        const userPrompt = promptInput.value.trim();
        if (!userPrompt) {
            container.innerText = "Please enter a prompt";
            container.style.color = "red";
            return;
        }

        container.innerText = "Loading...";
        container.style.color = "";

        fetch(`/get_response?prompt=${encodeURIComponent(userPrompt)}`)
            .then(response => response.text())
            .then(data => {
                container.innerText = data;
            })
            .catch(error => {
                container.innerText = "Error loading response: " + error;
                container.style.color = "red";
            });
    });
});