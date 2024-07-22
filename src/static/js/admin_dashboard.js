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
    const openMachineModalButton = document.getElementById('openMachineModal');
    const closeMachineModalButton = document.getElementById('closeMachineModal');
    const machineEditButtons = document.querySelectorAll('.btn-edit-machine');
    const machineDeleteButtons = document.querySelectorAll('.btn-delete-machine');

    if (openMachineModalButton) {
        openMachineModalButton.addEventListener('click', function () {
            document.getElementById('machineModal').classList.remove('hidden');
        });
    }

    if (closeMachineModalButton) {
        closeMachineModalButton.addEventListener('click', function () {
            document.getElementById('machineModal').classList.add('hidden');
        });
    }

    machineEditButtons.forEach(button => {
        button.addEventListener('click', function () {
            const id = this.getAttribute('data-id');
            const name = this.getAttribute('data-name');

            document.getElementById('edit_machine_id').value = id;
            document.getElementById('edit_machine_name').value = name;

            document.getElementById('editMachineModal').classList.remove('hidden');
        });
    });

    if (document.getElementById('closeEditMachineModal')) {
        document.getElementById('closeEditMachineModal').addEventListener('click', function () {
            document.getElementById('editMachineModal').classList.add('hidden');
        });
    }

    let machineIdToDelete = null;
    machineDeleteButtons.forEach(button => {
        button.addEventListener('click', function () {
            machineIdToDelete = this.getAttribute('data-id');
            document.getElementById('confirmMachineModal').classList.remove('hidden');
        });
    });

    document.getElementById('cancelDeleteMachine').addEventListener('click', function () {
        document.getElementById('confirmMachineModal').classList.add('hidden');
    });

    document.getElementById('confirmDeleteMachine').addEventListener('click', function () {
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
        document.getElementById('confirmMachineModal').classList.add('hidden');
    });


    // Para solventes
    const openSolventModalButton = document.getElementById('openSolventModal');
    const closeSolventModalButton = document.getElementById('closeSolventModal');
    const solventEditButtons = document.querySelectorAll('.btn-edit-solvent');
    const solventDeleteButtons = document.querySelectorAll('.btn-delete-solvent');

    if (openSolventModalButton) {
        openSolventModalButton.addEventListener('click', function () {
            document.getElementById('solventModal').classList.remove('hidden');
        });
    }

    if (closeSolventModalButton) {
        closeSolventModalButton.addEventListener('click', function () {
            document.getElementById('solventModal').classList.add('hidden');
        });
    }

    solventEditButtons.forEach(button => {
        button.addEventListener('click', function () {
            const id = this.getAttribute('data-id');
            const name = this.getAttribute('data-name');

            document.getElementById('edit_solvent_id').value = id;
            document.getElementById('edit_solvent_name').value = name;

            document.getElementById('editSolventModal').classList.remove('hidden');
        });
    });

    if (document.getElementById('closeEditSolventModal')) {
        document.getElementById('closeEditSolventModal').addEventListener('click', function () {
            document.getElementById('editSolventModal').classList.add('hidden');
        });
    }

    let solventIdToDelete = null;
    solventDeleteButtons.forEach(button => {
        button.addEventListener('click', function () {
            solventIdToDelete = this.getAttribute('data-id');
            document.getElementById('confirmSolventModal').classList.remove('hidden');
        });
    });

    document.getElementById('cancelDeleteSolvent').addEventListener('click', function () {
        document.getElementById('confirmSolventModal').classList.add('hidden');
    });

    document.getElementById('confirmDeleteSolvent').addEventListener('click', function () {
        if (solventIdToDelete) {
            fetch(`/eliminar_solvente/${solventIdToDelete}`, {
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
                        alert('Error al eliminar el solvente.');
                    }
                })
                .catch(error => console.error('Error:', error));
        }
        document.getElementById('confirmSolventModal').classList.add('hidden');
    });


    // Para preparación muestras
    const openSamplePreparationModalButton = document.getElementById('openSamplePreparationModal');
    const closeSamplePreparationModalButton = document.getElementById('closeSamplePreparationModal');
    const samplePreparationEditButtons = document.querySelectorAll('.btn-edit-sample-preparation');
    const samplePreparationDeleteButtons = document.querySelectorAll('.btn-delete-sample-preparation');

    if (openSamplePreparationModalButton) {
        openSamplePreparationModalButton.addEventListener('click', function () {
            document.getElementById('samplePreparationModal').classList.remove('hidden');
        });
    }

    if (closeSamplePreparationModalButton) {
        closeSamplePreparationModalButton.addEventListener('click', function () {
            document.getElementById('samplePreparationModal').classList.add('hidden');
        });
    }

    samplePreparationEditButtons.forEach(button => {
        button.addEventListener('click', function () {
            const id = this.getAttribute('data-id');
            const name = this.getAttribute('data-name');

            document.getElementById('edit_sample_preparation_id').value = id;
            document.getElementById('edit_sample_preparation_name').value = name;

            document.getElementById('editSamplePreparationModal').classList.remove('hidden');
        });
    });

    if (document.getElementById('closeEditSamplePreparationModal')) {
        document.getElementById('closeEditSamplePreparationModal').addEventListener('click', function () {
            document.getElementById('editSamplePreparationModal').classList.add('hidden');
        });
    }

    let samplePreparationIdToDelete = null;
    samplePreparationDeleteButtons.forEach(button => {
        button.addEventListener('click', function () {
            samplePreparationIdToDelete = this.getAttribute('data-id');
            document.getElementById('confirmSamplePreparationModal').classList.remove('hidden');
        });
    });

    document.getElementById('cancelDeleteSamplePreparation').addEventListener('click', function () {
        document.getElementById('confirmSamplePreparationModal').classList.add('hidden');
    });

    document.getElementById('confirmDeleteSamplePreparation').addEventListener('click', function () {
        if (samplePreparationIdToDelete) {
            fetch(`/eliminar_preparacion/${samplePreparationIdToDelete}`, {
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
                        alert('Error al eliminar la preparación de muestra.');
                    }
                })
                .catch(error => console.error('Error:', error));
        }
        document.getElementById('confirmSamplePreparationModal').classList.add('hidden');
    });
    // Para muestras
    const openSampleModalButton = document.getElementById('openSampleModal');
    const closeSampleModalButton = document.getElementById('closeSampleModal');
    const sampleEditButtons = document.querySelectorAll('.btn-edit-sample');
    const sampleDeleteButtons = document.querySelectorAll('.btn-delete-sample');

    if (openSampleModalButton) {
        openSampleModalButton.addEventListener('click', function () {
            document.getElementById('sampleModal').classList.remove('hidden');
        });
    }

    if (closeSampleModalButton) {
        closeSampleModalButton.addEventListener('click', function () {
            document.getElementById('sampleModal').classList.add('hidden');
        });
    }

    sampleEditButtons.forEach(button => {
        button.addEventListener('click', function () {
            const id = this.getAttribute('data-id');
            const name = this.getAttribute('data-name');

            document.getElementById('edit_sample_id').value = id;
            document.getElementById('edit_sample_name').value = name;

            document.getElementById('editSampleModal').classList.remove('hidden');
        });
    });

    if (document.getElementById('closeEditSampleModal')) {
        document.getElementById('closeEditSampleModal').addEventListener('click', function () {
            document.getElementById('editSampleModal').classList.add('hidden');
        });
    }

    let sampleIdToDelete = null;
    sampleDeleteButtons.forEach(button => {
        button.addEventListener('click', function () {
            sampleIdToDelete = this.getAttribute('data-id');
            document.getElementById('confirmSampleModal').classList.remove('hidden');
        });
    });

    document.getElementById('cancelDeleteSample').addEventListener('click', function () {
        document.getElementById('confirmSampleModal').classList.add('hidden');
    });

    document.getElementById('confirmDeleteSample').addEventListener('click', function () {
        if (sampleIdToDelete) {
            fetch(`/eliminar_muestra/${sampleIdToDelete}`, {
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
                        alert('Error al eliminar la muestra.');
                    }
                })
                .catch(error => console.error('Error:', error));
        }
        document.getElementById('confirmSampleModal').classList.add('hidden');
    });


});
