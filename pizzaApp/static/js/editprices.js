document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("price-form").addEventListener("submit", async (event) => {
    event.preventDefault(); // Prevent default form submission

    const formData = new FormData(event.target);
    const data = {};
    formData.forEach((value, key) => {
        data[key] = parseFloat(value) || 0;
    });

    try {
        const response = await fetch("/update_prices", {
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

        // Optionally reload the page to reflect changes
        location.reload();
    } catch (error) {
        console.error("Error updating prices:", error);
        alert("Error: " + error.message);
    }
  });
});
