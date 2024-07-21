document.addEventListener('DOMContentLoaded', function () {
    // Para usuarios
    const openUserModalButton = document.getElementById('openModal');
    const closeUserModalButton = document.getElementById('closeModal');
    const userEditButtons = document.querySelectorAll('.btn-edit');
    const userDeleteButtons = document.querySelectorAll('.btn-delete');

    if (openUserModalButton) {
        openUserModalButton.addEventListener('click', function () {
            document.getElementById('modal').classList.remove('hidden');
        });
    }

    if (closeUserModalButton) {
        closeUserModalButton.addEventListener('click', function () {
            document.getElementById('modal').classList.add('hidden');
        });
    }

    function closeModalOnSubmit() {
        document.getElementById('modal').classList.add('hidden');
        return true;
    }

    let userToEdit = null;
    userEditButtons.forEach(button => {
        button.addEventListener('click', function () {
            userToEdit = {
                rut: this.closest('tr').children[0].textContent.trim(),
                first_name: this.closest('tr').children[1].textContent.trim(),
                last_name: this.closest('tr').children[2].textContent.trim(),
                phone: this.closest('tr').children[3].textContent.trim(),
                email: this.closest('tr').children[4].textContent.trim(),
                role_id: this.closest('tr').children[5].getAttribute('data-role-id')
            };

            document.getElementById('edit_original_rut').value = userToEdit.rut;
            document.getElementById('edit_rut').value = userToEdit.rut;
            document.getElementById('edit_first_name').value = userToEdit.first_name;
            document.getElementById('edit_last_name').value = userToEdit.last_name;
            document.getElementById('edit_phone').value = userToEdit.phone;
            document.getElementById('edit_email').value = userToEdit.email;
            document.getElementById('edit_role_id').value = userToEdit.role_id;

            document.getElementById('editModal').classList.remove('hidden');
        });
    });

    if (document.getElementById('closeEditModal')) {
        document.getElementById('closeEditModal').addEventListener('click', function () {
            document.getElementById('editModal').classList.add('hidden');
        });
    }

    function closeEditModalOnSubmit() {
        document.getElementById('editModal').classList.add('hidden');
        return true;
    }

    let rutToDelete = null;
    userDeleteButtons.forEach(button => {
        button.addEventListener('click', function () {
            rutToDelete = this.getAttribute('data-rut');
            document.getElementById('confirmModal').classList.remove('hidden');
        });
    });

    document.getElementById('cancelDelete').addEventListener('click', function () {
        document.getElementById('confirmModal').classList.add('hidden');
    });

    document.getElementById('confirmDelete').addEventListener('click', function () {
        if (rutToDelete) {
            fetch(`/eliminar_usuario/${rutToDelete}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': '{{ csrf_token() }}'
                }
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        location.reload();
                    } else {
                        alert('Error al eliminar el usuario.');
                    }
                })
                .catch(error => console.error('Error:', error));
        }
        document.getElementById('confirmModal').classList.add('hidden');
    });

    // Para proyectos
    const openProjectModalButton = document.getElementById('openProjectModal');
    const closeProjectModalButton = document.getElementById('closeProjectModal');
    const projectEditButtons = document.querySelectorAll('.btn-edit-project');
    const projectDeleteButtons = document.querySelectorAll('.btn-delete-project');

    if (openProjectModalButton) {
        openProjectModalButton.addEventListener('click', function () {
            document.getElementById('projectModal').classList.remove('hidden');
        });
    }

    if (closeProjectModalButton) {
        closeProjectModalButton.addEventListener('click', function () {
            document.getElementById('projectModal').classList.add('hidden');
        });
    }

    function closeModalOnSubmit(modalId) {
        document.getElementById(modalId).classList.add('hidden');
        return true;
    }

    projectEditButtons.forEach(button => {
        button.addEventListener('click', function () {
            const id = this.getAttribute('data-id');
            const name = this.getAttribute('data-name');
            const fondo = this.getAttribute('data-fondo');

            document.getElementById('edit_project_id').value = id;
            document.getElementById('edit_project_name').value = name;
            document.getElementById('edit_project_fondo').value = fondo;

            document.getElementById('editProjectModal').classList.remove('hidden');
        });
    });

    if (document.getElementById('closeEditProjectModal')) {
        document.getElementById('closeEditProjectModal').addEventListener('click', function () {
            document.getElementById('editProjectModal').classList.add('hidden');
        });
    }

    let projectIdToDelete = null;
    projectDeleteButtons.forEach(button => {
        button.addEventListener('click', function () {
            projectIdToDelete = this.getAttribute('data-id');
            document.getElementById('confirmProjectModal').classList.remove('hidden');
        });
    });

    document.getElementById('cancelProjectDelete').addEventListener('click', function () {
        document.getElementById('confirmProjectModal').classList.add('hidden');
    });

    document.getElementById('confirmProjectDelete').addEventListener('click', function () {
        if (projectIdToDelete) {
            fetch(`/eliminar_proyecto/${projectIdToDelete}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': '{{ csrf_token() }}'
                }
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        location.reload();
                    } else {
                        alert('Error al eliminar el proyecto.');
                    }
                })
                .catch(error => console.error('Error:', error));
        }
        document.getElementById('confirmProjectModal').classList.add('hidden');
    });
    // Para máquinas
    document.getElementById('openMachineModal').addEventListener('click', function () {
        document.getElementById('machineModal').classList.remove('hidden');
    });

    document.getElementById('closeMachineModal').addEventListener('click', function () {
        document.getElementById('machineModal').classList.add('hidden');
    });

    function closeModalOnSubmit(modalId) {
        document.getElementById(modalId).classList.add('hidden');
        return true;
    }

    // Handle Edit Confirmation para máquinas
    document.querySelectorAll('.btn-edit-machine').forEach(button => {
        button.addEventListener('click', function () {
            const id = this.getAttribute('data-id');
            const name = this.getAttribute('data-name');

            document.getElementById('edit_machine_id').value = id;
            document.getElementById('edit_machine_name').value = name;

            document.getElementById('editMachineModal').classList.remove('hidden');
        });
    });

    document.getElementById('closeEditMachineModal').addEventListener('click', function () {
        document.getElementById('editMachineModal').classList.add('hidden');
    });

    // Handle Delete Confirmation para máquinas
    let machineIdToDelete = null;
    document.querySelectorAll('.btn-delete-machine').forEach(button => {
        button.addEventListener('click', function () {
            machineIdToDelete = this.getAttribute('data-id');
            document.getElementById('confirmModal').classList.remove('hidden');
        });
    });

    document.getElementById('cancelDelete').addEventListener('click', function () {
        document.getElementById('confirmModal').classList.add('hidden');
    });

    document.getElementById('confirmDelete').addEventListener('click', function () {
        if (machineIdToDelete) {
            fetch(`/eliminar_maquina/${machineIdToDelete}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': '{{ csrf_token() }}'
                }
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        location.reload();
                    } else {
                        alert('Error al eliminar la máquina.');
                    }
                })
                .catch(error => console.error('Error:', error));
        }
        document.getElementById('confirmModal').classList.add('hidden');
    });

});
