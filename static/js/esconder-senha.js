function mostrarSenha(idInput, idBtn) {
    const inputPass = document.getElementById(idInput);
    const btnMostrarSenha = document.getElementById(idBtn);

    inputPass.type =
        inputPass.type === 'password' ? 'text' : 'password';

    if (inputPass.type === 'text') {
        btnMostrarSenha.classList.replace('fa-eye', 'fa-eye-slash');
    } else {
        btnMostrarSenha.classList.replace('fa-eye-slash', 'fa-eye');
    }
}