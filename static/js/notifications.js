

/* 
#SMARTBIZ MVP 
#SYSTEM DEVELOPER: CALMEY CROWN @rown.calmey 
#START DATE: 3.12.2025
#UPDATE: 15.04.2026

*/

setTimeout(() => {
    document.querySelectorAll('.flash').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(-10px)';

        setTimeout(() => el.remove(), 400);
    });
}, 3000);