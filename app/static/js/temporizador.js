// Fichero: app/static/js/temporizador.js

document.addEventListener('DOMContentLoaded', () => {
    // 1. OBTENER ELEMENTOS DEL DOM
    const temporizadorDisplay = document.getElementById('temporizador');
    const controlBtn = document.getElementById('control-temporizador');
    const reiniciarBtn = document.getElementById('reiniciar-temporizador');
    const sumarBtn = document.getElementById('sumar-tiempo');
    const restarBtn = document.getElementById('restar-tiempo');

    if (!temporizadorDisplay || !controlBtn || !reiniciarBtn) {
        return; // No ejecutar si el temporizador no está en la página actual.
    }

    // 2. CONFIGURACIÓN Y FUNCIONES AUXILIARES
    const sonidoFinalizacion = new Audio('/static/audio/temporizador.mp3');
    let intervalo;
    let audioDesbloqueado = false;

    function desbloquearAudio() {
        if (audioDesbloqueado) return;
        const promise = sonidoFinalizacion.play();
        if (promise !== undefined) {
            promise.then(() => {
                sonidoFinalizacion.pause();
                sonidoFinalizacion.currentTime = 0;
                audioDesbloqueado = true;
            }).catch(() => {});
        }
    }

    function actualizarDisplay(segundos) {
        const segundosAMostrar = Math.max(0, segundos);
        const minutos = Math.floor(segundosAMostrar / 60);
        const secs = segundosAMostrar % 60;
        temporizadorDisplay.textContent = `${minutos.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }

    // 3. LÓGICA PRINCIPAL DEL TEMPORIZADOR

    function correrTemporizador() {
        const tiempoFinal = parseInt(sessionStorage.getItem('timer_tiempoFinal'));
        if (!tiempoFinal) {
            clearInterval(intervalo);
            return;
        }
        const tiempoRestante = Math.round((tiempoFinal - Date.now()) / 1000);

        if (tiempoRestante <= 0) {
            finalizarTemporizador();
        } else {
            actualizarDisplay(tiempoRestante);
        }
    }

    // 4. MANEJADORES DE ESTADO (ACCIONES DEL USUARIO)

    function toggleTemporizador() {
        desbloquearAudio();
        const tiempoFinalGuardado = sessionStorage.getItem('timer_tiempoFinal');

        if (tiempoFinalGuardado) { // Si existe, el temporizador está corriendo -> PAUSAR
            clearInterval(intervalo);
            const tiempoRestante = Math.round((parseInt(tiempoFinalGuardado) - Date.now()) / 1000);

            sessionStorage.setItem('timer_tiempoRestante', Math.max(0, tiempoRestante));
            sessionStorage.removeItem('timer_tiempoFinal');

            controlBtn.textContent = 'Reanudar';
            if (sumarBtn) sumarBtn.disabled = false;
            if (restarBtn) restarBtn.disabled = false;

        } else { // Si no existe, está pausado o detenido -> INICIAR/REANUDAR
            const tiempoRestanteGuardado = parseInt(sessionStorage.getItem('timer_tiempoRestante'));
            const duracionBase = parseInt(sessionStorage.getItem('timer_duracionBase')) || parseInt(temporizadorDisplay.dataset.minutos) || 25;

            const segundosParaCorrer = (tiempoRestanteGuardado !== null && !isNaN(tiempoRestanteGuardado)) ? tiempoRestanteGuardado : duracionBase * 60;

            const nuevoTiempoFinal = Date.now() + segundosParaCorrer * 1000;
            sessionStorage.setItem('timer_tiempoFinal', nuevoTiempoFinal);
            sessionStorage.removeItem('timer_tiempoRestante');

            controlBtn.textContent = 'Pausar';
            if (sumarBtn) sumarBtn.disabled = true;
            if (restarBtn) restarBtn.disabled = true;

            correrTemporizador(); // Ejecutar inmediatamente
            intervalo = setInterval(correrTemporizador, 1000);
        }
    }

    function ajustarTiempo(minutos) {
        desbloquearAudio();
        if (sessionStorage.getItem('timer_tiempoFinal')) return; // No ajustar si está corriendo

        let duracionBase = parseInt(sessionStorage.getItem('timer_duracionBase')) || parseInt(temporizadorDisplay.dataset.minutos) || 25;
        duracionBase += minutos;
        if (duracionBase < 5) duracionBase = 5;

        sessionStorage.setItem('timer_duracionBase', duracionBase);
        sessionStorage.removeItem('timer_tiempoRestante'); // Forzar que use la nueva duración base
        actualizarDisplay(duracionBase * 60);
    }

    function finalizarTemporizador() {
        clearInterval(intervalo);
        limpiarEstado();
        actualizarDisplay(0);

        controlBtn.textContent = '¡Completado!';
        controlBtn.disabled = true;
        if (sumarBtn) sumarBtn.disabled = true;
        if (restarBtn) restarBtn.disabled = true;

        sonidoFinalizacion.play().catch(err => console.error("Error al reproducir sonido:", err));
        alert('¡Tiempo completado!');
    }

    function reiniciarTemporizador() {
        desbloquearAudio();
        clearInterval(intervalo);

        const duracionBase = parseInt(sessionStorage.getItem('timer_duracionBase')) || parseInt(temporizadorDisplay.dataset.minutos) || 25;
        limpiarEstado();

        actualizarDisplay(duracionBase * 60);
        controlBtn.textContent = 'Iniciar';
        controlBtn.disabled = false;
        if (sumarBtn) sumarBtn.disabled = false;
        if (restarBtn) restarBtn.disabled = false;
    }

    function limpiarEstado() {
        sessionStorage.removeItem('timer_tiempoFinal');
        sessionStorage.removeItem('timer_tiempoRestante');
    }

    // 5. INICIALIZACIÓN AL CARGAR LA PÁGINA

    function inicializar() {
        const tiempoFinalGuardado = sessionStorage.getItem('timer_tiempoFinal');
        const tiempoRestanteGuardado = sessionStorage.getItem('timer_tiempoRestante');
        const duracionBase = parseInt(sessionStorage.getItem('timer_duracionBase')) || parseInt(temporizadorDisplay.dataset.minutos) || 25;

        if (tiempoFinalGuardado) { // Estaba corriendo
            controlBtn.textContent = 'Pausar';
            if (sumarBtn) sumarBtn.disabled = true;
            if (restarBtn) restarBtn.disabled = true;
            correrTemporizador();
            intervalo = setInterval(correrTemporizador, 1000);
        } else if (tiempoRestanteGuardado !== null) { // Estaba pausado
            controlBtn.textContent = 'Reanudar';
            actualizarDisplay(parseInt(tiempoRestanteGuardado));
        } else { // Nunca se inició
            controlBtn.textContent = 'Iniciar';
            actualizarDisplay(duracionBase * 60);
        }
    }

    // 6. ASIGNAR EVENTOS
    controlBtn.addEventListener('click', toggleTemporizador);
    reiniciarBtn.addEventListener('click', reiniciarTemporizador);
    if (sumarBtn) sumarBtn.addEventListener('click', () => ajustarTiempo(5));
    if (restarBtn) restarBtn.addEventListener('click', () => ajustarTiempo(-5));

    // ¡Empezar!
    inicializar();
});