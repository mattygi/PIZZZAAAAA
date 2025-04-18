document.addEventListener("DOMContentLoaded", () => {
    const buttons = document.querySelectorAll("button");
  
    buttons.forEach(button => {
      button.addEventListener("click", event => {
        console.log(`Button clicked: ${event.target.textContent}`);
      });
    });
  });
  