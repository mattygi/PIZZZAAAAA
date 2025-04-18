document.addEventListener("DOMContentLoaded", function () {
    document.querySelector('form').addEventListener('submit', async (event) => {
        event.preventDefault(); // Prevent default form submission

        const formData = new FormData(event.target);
        const data = {};
        formData.forEach((value, key) => {
            data[key] = value;
        });

        try {
            const response = await fetch("/checkout", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(data),
            });

            if (!response.ok) {
                const errorResponse = await response.json();
                throw new Error(errorResponse.error || "Unknown error occurred.");
            }

            const result = await response.json();
            alert(result.message); // Success message

            // Optionally, redirect users upon successful payment
            window.location.href = "/orderPlaced";
        } catch (error) {
            console.error("Checkout error:", error);
            alert("Error: " + error.message);
        }
    });
});
