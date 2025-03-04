document.addEventListener('DOMContentLoaded', function () {

    // Elementos generales
    const changePasswordLink = document.getElementById('changePasswordLink');
    const changePasswordModal = document.getElementById('changePasswordModal');
    const closeChangePasswordModalButton = document.getElementById('closeChangePasswordModal');
    const changePasswordForm = document.getElementById('changePasswordForm');

    if (changePasswordLink) {
        changePasswordLink.addEventListener('click', function () {
            changePasswordModal.classList.remove('hidden');
        });
    }

    if (closeChangePasswordModalButton) {
        closeChangePasswordModalButton.addEventListener('click', function () {
            changePasswordModal.classList.add('hidden');
        });
    }

    if (changePasswordForm) {
        changePasswordForm.addEventListener('submit', function (event) {
            event.preventDefault();

            const currentPassword = document.getElementById('current_password').value;
            const newPassword = document.getElementById('new_password').value;
            const confirmPassword = document.getElementById('confirm_password').value;

            fetch('/change_password', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').getAttribute('content')
                },
                body: JSON.stringify({
                    current_password: currentPassword,
                    new_password: newPassword,
                    confirm_password: confirmPassword
                })
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert('Contraseña actualizada con éxito');
                        changePasswordModal.classList.add('hidden');
                    } else {
                        alert(data.message);
                    }
                })
                .catch(error => console.error('Error:', error));
        });
    }

    // 🔹 Validamos si existen elementos de C13 antes de ejecutarlo
    const c13Checkbox = document.getElementById("c13-checkbox");
    const modal = document.getElementById("modal-c13");
    const gramsInput = document.getElementById("c13-grams");
    const hiddenC13Grams = document.getElementById("hidden-c13-grams");
    const confirmBtn = document.getElementById("confirm-btn");
    const cancelBtn = document.getElementById("cancel-btn");

    if (!c13Checkbox || !modal || !gramsInput || !hiddenC13Grams || !confirmBtn || !cancelBtn) {
        console.warn("La funcionalidad de C13 no se ejecutará porque uno o más elementos no existen en esta vista.");
        return;
    }


    if (c13Checkbox) {
        c13Checkbox.addEventListener("change", () => {
            if (c13Checkbox.checked) {
                modal.classList.remove("hidden");
            }
        });
    }

    // Botón Aceptar
    confirmBtn.addEventListener("click", () => {
        if (!hiddenC13Grams) {
            console.error("No se puede asignar el valor porque 'hidden-c13-grams' no existe.");
            return;
        }

        const gramsValue = parseFloat(gramsInput.value);
        if (!isNaN(gramsValue) && gramsValue > 0) {
            hiddenC13Grams.value = gramsValue;
            modal.classList.add("hidden");
        } else {
            alert("Ingrese un valor válido para los gramos.");
        }
    });

    // Botón Cancelar
    cancelBtn.addEventListener("click", () => {
        modal.classList.add("hidden");
        if (c13Checkbox) c13Checkbox.checked = false;
    });

});
