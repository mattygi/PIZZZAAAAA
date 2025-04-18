document.addEventListener("DOMContentLoaded", () => {
    const usernameInput = document.getElementById("username");
    const passwordInput = document.getElementById("password");
    const loginBtn = document.getElementById("loginBtn");

    const usernameFeedback = document.getElementById("usernameFeedback");
    const passwordFeedback = document.getElementById("passwordFeedback");

    // ✅ Validate username input
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

    // ✅ Validate password input
    passwordInput.addEventListener("input", () => {
        const password = passwordInput.value;
        if (password.length < 6) {
            passwordFeedback.textContent = "Password must be at least 6 characters.";
            passwordFeedback.style.color = "red";
        } else {
            passwordFeedback.textContent = "✓ Secure password!";
            passwordFeedback.style.color = "green";
        }
        validateForm();
    });

    // ✅ Enable login button when all inputs are valid
    function validateForm() {
        if (
            usernameFeedback.style.color === "green" &&
            passwordFeedback.style.color === "green"
        ) {
            loginBtn.disabled = false;
        } else {
            loginBtn.disabled = true;
        }
    }
});
