// static/js/modals.js
// MODAL PARA NUEVO HABITO
document.addEventListener('DOMContentLoaded', () => {
    // Elementos del DOM
    const modal = document.getElementById('modalNuevoHabito');
    const btnAbrir = document.querySelector('.btn-add-habit');
    const btnCerrar = document.getElementById('cerrarModal');
    const btnCancelar = document.getElementById('cancelarModal');

    // Verificamos que el modal exista en esta página antes de agregar la lógica
    if (modal) {
        // Funciones para abrir y cerrar
        const abrirModal = () => modal.classList.add('active');
        const cerrarModal = () => modal.classList.remove('active');

        // Asignar los eventos a los botones
        if(btnAbrir) btnAbrir.addEventListener('click', abrirModal);
        if(btnCerrar) btnCerrar.addEventListener('click', cerrarModal);
        if(btnCancelar) btnCancelar.addEventListener('click', cerrarModal);

        // Cerrar el modal si el usuario hace clic afuera de la caja blanca
        window.addEventListener('click', (e) => {
            if (e.target === modal) {
                cerrarModal();
            }
        });
    }
});