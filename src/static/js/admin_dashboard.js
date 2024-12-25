window.closeModalOnSubmit = function() {
    document.getElementById('modal').classList.add('hidden');
    return true;
}

window.closeEditModalOnSubmit = function() {
    document.getElementById('editModal').classList.add('hidden');
    return true;
}

document.addEventListener('DOMContentLoaded', function () {
    function getCsrfToken() {
        return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    }

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


    let userToEdit = null;
    userEditButtons.forEach(button => {
        button.addEventListener('click', function () {
            const row = this.closest('tr');
            userToEdit = {
                rut: row.children[0].textContent.trim(),
                first_name: row.children[1].textContent.trim(),
                last_name: row.children[2].textContent.trim(),
                phone: row.children[3].textContent.trim(),
                email: row.children[4].textContent.trim(),
                role_id: row.querySelector('td:nth-child(6)').getAttribute('data-role-id'), // Asegúrate de agregar este atributo en tu HTML
                type: row.children[6].textContent.trim()
            };

            document.getElementById('edit_original_rut').value = userToEdit.rut;
            document.getElementById('edit_rut').value = userToEdit.rut;
            document.getElementById('edit_first_name').value = userToEdit.first_name;
            document.getElementById('edit_last_name').value = userToEdit.last_name;
            document.getElementById('edit_phone').value = userToEdit.phone;
            document.getElementById('edit_email').value = userToEdit.email;
            document.getElementById('edit_role_id').value = userToEdit.role_id;

            // Convertir el tipo de usuario mostrado a los valores del enum
            const typeSelect = document.getElementById('edit_type');
            if (userToEdit.type.toLowerCase().includes('interno')) {
                typeSelect.value = 'INTERNAL';
            } else if (userToEdit.type.toLowerCase().includes('externo')) {
                typeSelect.value = 'EXTERNAL';
            }

            document.getElementById('editModal').classList.remove('hidden');
        });
    });

    if (document.getElementById('closeEditModal')) {
        document.getElementById('closeEditModal').addEventListener('click', function () {
            document.getElementById('editModal').classList.add('hidden');
        });
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
                    'X-CSRFToken': getCsrfToken()
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
                    'X-CSRFToken': getCsrfToken()
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
                    'X-CSRFToken': getCsrfToken()
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
                    'X-CSRFToken': getCsrfToken()
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
                    'X-CSRFToken': getCsrfToken()
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
            const precio_interno = this.getAttribute('data-precio_interno');
            const precio_externo = this.getAttribute('data-precio_externo');

            document.getElementById('edit_sample_id').value = id;
            document.getElementById('edit_sample_name').value = name;
            document.getElementById('edit_sample_precio_interno').value = precio_interno;
            document.getElementById('edit_sample_precio_externo').value = precio_externo;

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
                    'X-CSRFToken': getCsrfToken()
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

    // Para núcleos
    const openNucleoModalButton = document.getElementById('openNucleoModal');
    const closeNucleoModalButton = document.getElementById('closeNucleoModal');
    const nucleoEditButtons = document.querySelectorAll('.btn-edit-nucleo');
    const nucleoDeleteButtons = document.querySelectorAll('.btn-delete-nucleo');

    if (openNucleoModalButton) {
        openNucleoModalButton.addEventListener('click', function () {
            document.getElementById('nucleoModal').classList.remove('hidden');
        });
    }

    if (closeNucleoModalButton) {
        closeNucleoModalButton.addEventListener('click', function () {
            document.getElementById('nucleoModal').classList.add('hidden');
        });
    }

    nucleoEditButtons.forEach(button => {
        button.addEventListener('click', function () {
            const id = this.getAttribute('data-id');
            const nombre = this.getAttribute('data-nombre');
            const precio_interno = this.getAttribute('data-precio_interno');
            const precio_externo = this.getAttribute('data-precio_externo');

            document.getElementById('edit_nucleo_id').value = id;
            document.getElementById('edit_nucleo_nombre').value = nombre;
            document.getElementById('edit_nucleo_precio_interno').value = precio_interno;
            document.getElementById('edit_nucleo_precio_externo').value = precio_externo;

            document.getElementById('editNucleoModal').classList.remove('hidden');
        });
    });

    if (document.getElementById('closeEditNucleoModal')) {
        document.getElementById('closeEditNucleoModal').addEventListener('click', function () {
            document.getElementById('editNucleoModal').classList.add('hidden');
        });
    }

    let nucleoIdToDelete = null;
    nucleoDeleteButtons.forEach(button => {
        button.addEventListener('click', function () {
            nucleoIdToDelete = this.getAttribute('data-id');
            document.getElementById('confirmNucleoModal').classList.remove('hidden');
        });
    });

    document.getElementById('cancelNucleoDelete').addEventListener('click', function () {
        document.getElementById('confirmNucleoModal').classList.add('hidden');
    });

    document.getElementById('confirmNucleoDelete').addEventListener('click', function () {
        if (nucleoIdToDelete) {
            fetch(`/eliminar_nucleo/${nucleoIdToDelete}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken()
                }
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        location.reload();
                    } else {
                        alert('Error al eliminar el núcleo.');
                    }
                })
                .catch(error => console.error('Error:', error));
        }
        document.getElementById('confirmNucleoModal').classList.add('hidden');
    });

    // Función para inicializar el cambio de estado de solicitudes
    function initializeEstadoChange() {
        const updateButtons = document.querySelectorAll('.actualizar-estado-btn');

        updateButtons.forEach(button => {
            button.addEventListener('click', function () {
                const form = this.closest('.estado-form');
                const solicitudId = form.getAttribute('data-solicitud-id');
                const estadoSelect = form.querySelector('.estado-select');
                const nuevoEstado = estadoSelect.value;

                cambiarEstadoSolicitud(solicitudId, nuevoEstado);
            });
        });
    }

    // Función para manejar el cambio de estado de una solicitud
    function cambiarEstadoSolicitud(solicitudId, nuevoEstado) {
        fetch(`/cambiar_estado/${solicitudId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({
                estado: nuevoEstado
            })
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Estado actualizado con éxito');
                    location.reload(); // Recargar para mostrar el nuevo estado
                } else {
                    alert('Error al actualizar el estado.');
                }
            })
            .catch(error => console.error('Error:', error));
    }

    // Función para inicializar la eliminación de solicitudes
    // Función para inicializar la eliminación de solicitudes
    function initializeDeleteRequest() {
        const requestDeleteButtons = document.querySelectorAll('.delete-request-button');
        let requestIdToDelete = null;

        // Añadir evento de clic a cada botón de eliminación
        requestDeleteButtons.forEach(button => {
            button.addEventListener('click', function () {
                requestIdToDelete = this.getAttribute('data-id');
                document.getElementById('confirmRequestModal').classList.remove('hidden');
            });
        });

        // Cancelar eliminación y ocultar el modal
        document.getElementById('cancelDeleteRequest').addEventListener('click', function () {
            document.getElementById('confirmRequestModal').classList.add('hidden');
        });

        // Confirmar eliminación y enviar solicitud POST
        document.getElementById('confirmDeleteRequest').addEventListener('click', function () {
            if (requestIdToDelete) {
                fetch(`/eliminar_solicitud/${requestIdToDelete}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCsrfToken()
                    }
                })
                .then(response => {
                    if (response.ok) {
                        location.reload();
                    } else {
                        alert('Error al eliminar la solicitud.');
                    }
                })
                .catch(error => console.error('Error:', error));
            }
            document.getElementById('confirmRequestModal').classList.add('hidden');
        });
    }


    // Inicializar las funciones
    initializeEstadoChange();
    initializeDeleteRequest();

});
