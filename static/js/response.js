window.onload = function () {
    const container = document.getElementById('response-container');
    fetch('/get_response')
        .then(response => response.text())
        .then(data => {
            container.innerText = data;
        })
        .catch(error => {
            container.innerText = "Error loading response: " + error;
            container.style.color = "red";
        });
};