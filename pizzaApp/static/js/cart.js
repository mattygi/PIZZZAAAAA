document.addEventListener("DOMContentLoaded", () => {
    const checkoutButton = document.getElementById("checkoutBtn");

    // ✅ Ensure checkout button is ALWAYS visible
    if (checkoutButton) {
        checkoutButton.style.display = "block";
    }

    // ✅ Flash message fade-out effect
    const flashMessages = document.querySelectorAll(".flash-msg");
    flashMessages.forEach(msg => {
        setTimeout(() => {
            msg.style.opacity = "0";
            msg.style.transition = "opacity 0.5s ease-out";
        }, 3000);
    });

    // ✅ Dynamically show checkout button when items are added
    document.querySelectorAll(".add-to-cart").forEach(button => {
        button.addEventListener("click", (event) => {
            event.preventDefault();
            checkoutButton.style.display = "block"; // ✅ Ensures visibility
        });
    });
});
