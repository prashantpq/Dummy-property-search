// Show spinner during form submission
document.querySelector("form").addEventListener("submit", function() {
    const spinner = document.createElement('div');
    spinner.className = "spinner-border text-primary";
    spinner.role = "status";
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '';
    resultsDiv.appendChild(spinner);
});
