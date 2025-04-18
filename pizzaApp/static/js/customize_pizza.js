
document.addEventListener("DOMContentLoaded", () => {
  function clearCheckboxes(groupName) {
    const checkboxes = document.querySelectorAll(`input[name='${groupName}[]']`);
    checkboxes.forEach(cb => cb.checked = false);
  }

  function selectAllCheckboxes(groupName) {
    const checkboxes = document.querySelectorAll(`input[name='${groupName}[]']`);
    checkboxes.forEach(cb => cb.checked = true);
  }

  // Event listeners for select all / clear buttons
  document.querySelectorAll(".select-btn").forEach(button => {
    button.addEventListener("click", () => {
      const groupName = button.getAttribute("data-group");
      selectAllCheckboxes(groupName);
    });
  });

  document.querySelectorAll(".clear-btn").forEach(button => {
    button.addEventListener("click", () => {
      const groupName = button.getAttribute("data-group");
      clearCheckboxes(groupName);
    });
  });
});
