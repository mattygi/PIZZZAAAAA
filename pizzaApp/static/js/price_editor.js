const form = document.getElementById('price-form');

form.addEventListener('submit', (e) => {
  e.preventDefault();
  const formData = new FormData(form);
  const prices = {};

  for (const [key, value] of formData.entries()) {
    prices[key] = parseFloat(value);
  }

  localStorage.setItem('pizzaPrices', JSON.stringify(prices));
  alert("Prices saved!");
});

window.onload = () => {
  const saved = JSON.parse(localStorage.getItem('pizzaPrices'));
  if (saved) {
    for (const key in saved) {
      if (form.elements[key]) {
        form.elements[key].value = saved[key];
      }
    }
  }
};