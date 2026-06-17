// static/js/alertas.js
document.addEventListener('DOMContentLoaded', () => {
    const alertas = document.querySelectorAll('.alerta');

    if (alertas.length > 0) {
        setTimeout(() => {
            alertas.forEach(alerta => {
                alerta.style.transition = "opacity 0.5s ease, margin 0.5s ease, padding 0.5s ease";
                alerta.style.opacity = "0";
                alerta.style.margin = "0";
                alerta.style.padding = "0";
                alerta.style.height = "0";
                alerta.style.overflow = "hidden";

                setTimeout(() => alerta.remove(), 500);
            });
        }, 5000);
    }
});