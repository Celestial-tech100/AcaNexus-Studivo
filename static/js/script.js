document.addEventListener("DOMContentLoaded", function () {

    const btn = document.getElementById("themeToggle");

    if (!btn) {
        console.log("Theme button not found");
        return;
    }

    btn.addEventListener("click", function () {

        document.body.classList.toggle("dark-mode");

        if (document.body.classList.contains("dark-mode")) {
            localStorage.setItem("theme", "dark");
        } else {
            localStorage.setItem("theme", "light");
        }
    });

    // load saved theme
    if (localStorage.getItem("theme") === "dark") {
        document.body.classList.add("dark-mode");
    }
});