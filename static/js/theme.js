/* 
#SMARTBIZ MVP 
#SYSTEM DEVELOPER: CALMEY CROWN @rown.calmey 
#START DATE: 3.12.2025
#UPDATE: 15.04.2026

*/

// LIGHT/DARK MODE
document.addEventListener("DOMContentLoaded", () => {
    const card = document.querySelector(".card");
    const toggleBtn = document.getElementById("theme-toggle");

    if (!card || !toggleBtn) return;

    // Load saved theme (card-level)
    const savedTheme = localStorage.getItem("card-theme") || "light";
    card.setAttribute("data-theme", savedTheme);
    toggleBtn.textContent =
        savedTheme === "dark" ? "☀ Day" : "🌙 Night";

    toggleBtn.addEventListener("click", () => {
        const currentTheme = card.getAttribute("data-theme");
        const newTheme = currentTheme === "dark" ? "light" : "dark";

        card.setAttribute("data-theme", newTheme);
        localStorage.setItem("card-theme", newTheme);

        toggleBtn.textContent =
            newTheme === "dark" ? "☀ Day" : "🌙 Night";
    });
});
