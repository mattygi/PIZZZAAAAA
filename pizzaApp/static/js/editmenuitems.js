document.addEventListener("DOMContentLoaded", () => {
  document.querySelector(".container").addEventListener("click", (event) => {
    const button = event.target.closest(".delete-btn");
    
    if (button) {
      if (!confirm("Are you sure you want to delete this item?")) {
        event.preventDefault(); // Prevent form submission
      }
    }
  });
});
