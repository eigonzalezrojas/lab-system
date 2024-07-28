document.addEventListener('DOMContentLoaded', function () {
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
});
