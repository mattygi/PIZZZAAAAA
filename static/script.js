function showApology() {
    var inputField = document.getElementById("inputField");
    var apologyMessage = document.getElementById("apologyMessage");

    var inputValue = inputField.value.trim();

    if (inputValue === "") {
        apologyMessage.innerHTML = "Apology: Please enter something.";
        apologyMessage.style.display = "block";
    } else {
        apologyMessage.style.display = "none";
    }
}