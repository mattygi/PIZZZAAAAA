document.addEventListener("DOMContentLoaded", () => {
    const usernameInput = document.getElementById("username");
    const emailInput = document.getElementById("email");
    const passwordInput = document.getElementById("password");
    const registerBtn = document.getElementById("registerBtn");

    const usernameFeedback = document.getElementById("usernameFeedback");
    const emailFeedback = document.getElementById("emailFeedback");
    const passwordFeedback = document.getElementById("passwordFeedback");

    // ✅ Check username availability
    usernameInput.addEventListener("input", () => {
        const username = usernameInput.value.trim();
        if (username.length < 3) {
            usernameFeedback.textContent = "Username must be at least 3 characters.";
            usernameFeedback.style.color = "red";
        } else {
            usernameFeedback.textContent = "✓ Username looks good!";
            usernameFeedback.style.color = "green";
        }
        validateForm();
    });

    // ✅ Validate email format
    emailInput.addEventListener("input", () => {
        const email = emailInput.value.trim();
        const emailRegex = /^[^@]+@[^@]+\.[^@]+$/;
        if (!emailRegex.test(email)) {
            emailFeedback.textContent = "Invalid email format.";
            emailFeedback.style.color = "red";
        } else {
            emailFeedback.textContent = "✓ Email is valid!";
            emailFeedback.style.color = "green";
        }
        validateForm();
    });

    // ✅ Password strength check
    passwordInput.addEventListener("input", () => {
        const password = passwordInput.value;
        if (password.length < 6) {
            passwordFeedback.textContent = "Password must be at least 6 characters.";
            passwordFeedback.style.color = "red";
        } else {
            passwordFeedback.textContent = "✓ Strong password!";
            passwordFeedback.style.color = "green";
        }
        validateForm();
    });

    // ✅ Enable register button only when all fields are valid
    function validateForm() {
        if (
            usernameFeedback.style.color === "green" &&
            emailFeedback.style.color === "green" &&
            passwordFeedback.style.color === "green"
        ) {
            registerBtn.disabled = false;
        } else {
            registerBtn.disabled = true;
        }
    }
});
