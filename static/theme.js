/* 
#SMARTBIZ MVP 
#SYSTEM DEVELOPER: CALMEY CROWN @rown.calmey 
#START DATE: 3.12.2025
#UPDATE: 21.01.2026

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



// ACTIONS (delete/confirm/undo/)
/*
document.addEventListener('DOMContentLoaded', ()=>{
    let deleteForm = null;
    // EVENT DELETION KEY
document.body.addEventListener('click', function(e){
    // OPEN MODAL
    if (e.target.classList.contains('pin-required')){
        return;
    }

    if (e.target.classList.contains('pin-required')){
        e.preventDefault();
        deleteUrl = e.target.dataset.url;

document.getElementById('confirm-modal').classList.remove('hidden')
    }
    // CANCEL
    if (e.target.id=== 'confirm-no'){
        deleteForm = null;

document.getElementById('confirm-modal').classList.add('hidden');
    }
    //CONFIRM
    if(e.target.id=== 'confirm-yes'){
        if(deleteForm){
            deleteForm.submit();
        }
    }
});
});


//function confirmDelete(){
 //   return confirm("Are you sure you want to delete this record?");
//}

//document.addEventListener("submit", function(e){
//    if (e.target.classList.contains('delete-form')){
//        if (!confirm("Delete this item?")){
 //           e.preventDefault();
 //       }
 //   }
//});
// TIMERS
*/

setTimeout(()=>{
    const flashes = document.querySelectorAll('.flash');
    flashes.forEach(flash=>{
        flash.style.opacity = '0';
        setTimeout(()=> flash.remove(), 500);
    });
}, 3000);