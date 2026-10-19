const formulario = document.querySelector('form');

formulario.addEventListener('submit', function(event) {
    const campos = formulario.querySelectorAll('[required]');
    let formularioValido = true;

    campos.forEach(campo => {
        const mensagem = campo.parentElement.querySelector(
            '.msg-erro-campos'
        );

        if (!campo.value.trim()) {
            formularioValido = false;

            if (mensagem) {
                mensagem.textContent =
                    `Preencha o campo "${campo.placeholder}"`;
            }
        } else {
            if (mensagem) {
                mensagem.textContent = '';
            }
        }
    });

    if (!formularioValido) {
        event.preventDefault();

        formulario.querySelector(':invalid')?.focus();
    }
});


const campos = document.querySelectorAll('input[required]');

campos.forEach(campo => {
    campo.addEventListener('input', function() {
        const mensagem = campo.parentElement.querySelector(
            '.msg-erro-campos'
        );

        if (mensagem && campo.value.trim() !== '') {
            mensagem.textContent = '';
        }
    });
});
