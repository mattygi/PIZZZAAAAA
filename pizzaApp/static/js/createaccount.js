document.getElementById("registerForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent default form submission

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    fetch("http://127.0.0.1:5000/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ username: username, password: password })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message); // Show the response message
    })
    .catch(error => {
        console.error("Error:", error);
    });
});
