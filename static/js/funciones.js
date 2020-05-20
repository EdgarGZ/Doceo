function crearTemplate(HTMLString){
    const html = document.implementation.createHTMLDocument();
    html.body.innerHTML = HTMLString;
    return html.body.children[0]
}

// modal principal bg
function modal(){
	document.querySelector('.bg').classList.toggle('ver-bg');
}

// modales para el registro del tutor
// despliega el modal a mostrar y después de 1 segundo, lo desaparece
function error(){
	modal();
	document.getElementById('error').classList.toggle('ver-molde');
	setTimeout(function(){
		document.querySelector('.bg').classList.remove('ver-bg');
		document.getElementById('error').classList.remove('ver-molde');
	}, 1200);
}

// borrar campos
function borrarCampos(){
	var x = document.querySelectorAll(".dato");
    var i;
    for (i = 0; i < x.length; i++) {
        x[i].value = "";
    }
}

// Administrador
// Área
function agregarArea(){
	modal();
	document.getElementById('addAreaS').classList.toggle('ver-molde');
	setTimeout(function(){
		document.getElementById('addAreaS').classList.remove('ver-molde');
		modal();
	}, 1000);
}
function eliminarArea(){
	modal();
	document.getElementById('eleArea').classList.toggle('ver-molde');
}
function eliminarAreaS(){
	document.getElementById('eleArea').classList.remove('ver-molde');
	document.getElementById('eleAreaS').classList.toggle('ver-molde');
	setTimeout(function(){
		document.getElementById('eleAreaS').classList.remove('ver-molde');
		modal();
	}, 1000);
}
function eliminarAreaSC(){
	document.querySelector('.bg').classList.remove('ver-bg');
	document.getElementById('eleArea').classList.remove('ver-molde');
}
// Administrador
// Profesor
function agregarProfesor(){
	modal();
	document.getElementById('addProfesor').classList.toggle('ver-molde');
	setTimeout(function(){
		document.getElementById('addProfesor').classList.remove('ver-molde');
		modal();
	}, 1000);
}
function eliminarUsuario(){
	modal();
	document.getElementById('eliminarUsuario').classList.toggle('ver-molde');
}
function eliminarUsuarioS(){
	document.getElementById('eliminarUsuario').classList.remove('ver-molde');
	document.getElementById('eliminarUsuarioS').classList.toggle('ver-molde');
	setTimeout(function(){
		document.getElementById('eliminarUsuarioS').classList.remove('ver-molde');
		modal();
	}, 1000);
}
function eliminarAreaSC(){
	document.querySelector('.bg').classList.remove('ver-bg');
	document.getElementById('eleArea').classList.remove('ver-molde');
}

// Profesor y Tutor para agregar, eliminar y modificar tutorías
function cambiosHechos(){
	modal();
	document.getElementById('cambios').classList.toggle('ver-molde');
	setTimeout(function(){
		document.getElementById('cambios').classList.remove('ver-molde');
		modal();
	}, 1000);
}

function cancelarCambios(){
	document.querySelector('.bg').classList.remove('ver-bg');
	document.getElementById('cambios').classList.remove('ver-molde');
}

function addArea(){
	modal();
	document.getElementById('addArea').classList.toggle('ver-molde');
}

function agregarAreaC(){
	document.getElementById('addArea').classList.remove('ver-molde');
	document.querySelector('.bg').classList.remove('ver-bg');
}

function agregarAreaS(){
	//document.getElementById('addArea').classList.remove('ver-molde');
	document.getElementById('addAreaCheck').classList.toggle('ver-molde');
	setTimeout(function(){
		document.getElementById('addAreaCheck').classList.remove('ver-molde');
		modal();
	}, 1000);
}

// Tutor para iniciar, cancelar y finalizar tutorías
// Eliminar horarios
function del(){
	document.querySelector('.bg').classList.toggle('ver-bg');
	document.getElementById('addAreaDel').classList.toggle('ver-molde');
}

function eliminarAreaC(){
	document.getElementById('addAreaDel').classList.remove('ver-molde');
	document.querySelector('.bg').classList.remove('ver-bg');
}

function eliminarArea(){
 	//document.getElementById('addAreaDel').classList.remove('ver-molde');
	document.getElementById('addAreaTrash').classList.toggle('ver-molde');
	setTimeout(function(){
		document.getElementById('addAreaTrash').classList.remove('ver-molde');
		modal();
	}, 1000);
}

function iniciarTuto(){
	modal();
	document.getElementById('tutoIniciada').classList.toggle('ver-molde');
	setTimeout(function(){
		document.querySelector('.bg').classList.remove('ver-bg');
		document.getElementById('tutoIniciada').classList.remove('ver-molde');
	}, 1000);
	document.getElementById('iniciar').style.display="none";
}

function cancelarTuto(){
	modal();
	document.getElementById('tutoCancelada').classList.toggle('ver-molde');
}

function finalizarTuto(){
	modal();
	document.getElementById('tutoFinalizada').classList.toggle('ver-molde');
}

async function aceptarTutoria(tutoria, notificacion) {
	const response = await fetch(`accept/tutorship/${tutoria}/${notificacion}/`, {
        method: 'POST',
    });
	const resp = await response.json();
	if(resp.data == "success"){
		cancelarAgenda();
		aceptarTuto();
		document.querySelector('.bg').classList.toggle('ver-bg');
		setTimeout(() => {
			location.reload();
		}, 5000)
	}
}

function aceptarTuto(){
	document.getElementById('tutoCheck').classList.toggle('ver-molde');
	document.getElementById('notificacion').classList.remove('ver-molde');
	setTimeout(function(){
		document.getElementById('tutoCheck').classList.remove('ver-molde');
		modal();
	}, 5000);
}

function denegarTutoria(){
	document.getElementById('notificacionPersistida').classList.remove('ver-molde');
	document.querySelector('.bg').classList.remove('ver-bg');
	document.getElementById('notificacionModalPersistida').remove();
}

function cancelarTutoriaC(){
	document.getElementById('tutoCancelada').classList.remove('ver-molde');
	document.querySelector('.bg').classList.remove('ver-bg');
}

function finalizarTutoria(){
	document.getElementById('tutoFinalizada').classList.remove('ver-molde');
	document.querySelector('.bg').classList.remove('ver-bg');
}

function finalizarTutoriaC(){
	document.getElementById('tutoFinalizada').classList.remove('ver-molde');
	document.querySelector('.bg').classList.remove('ver-bg');
}

// notificacion
async function verNoti(tutoriaId){
	const NOTIFICACION_CONTAINER = document.getElementById('notificacionPersistida');
	const response = await fetch(`get/tutorship/notification/${tutoriaId}/`, {
        method: 'POST',
    });
	const resp = await response.json();
	const TUTORSHIP_DATA = resp.data;
	const MODAL_TUTORSHIP = `
		<div id="notificacionModalPersistida">
			<p>${TUTORSHIP_DATA.tutorado} solicitó una de tus tutorías:</p>
			<p class="b">${TUTORSHIP_DATA.tutoria}</p>
			<p class="b">Este ${TUTORSHIP_DATA.dia} de este mes</p>
			<p class="b">${TUTORSHIP_DATA.hora_inicio} - ${TUTORSHIP_DATA.hora_fin}</p>
			<div class="flex botonera">
				<input class="cancelar" type="submit" name="" value="Denegar" onclick="denegarTutoria()">
				<input class="guardar" type="submit" name="" value="Aceptar" onclick="aceptarTutoria(${TUTORSHIP_DATA.id_tutoria}, ${TUTORSHIP_DATA.id_notificacion});aceptarTutoriaWS(${TUTORSHIP_DATA.tutoria}, ${TUTORSHIP_DATA.tutorado_username})">
			</div>
		</div>
    `;
    const HTML_MODAL_PERSISTENTE = crearTemplate(MODAL_TUTORSHIP);
    NOTIFICACION_CONTAINER.append(HTML_MODAL_PERSISTENTE);
	modal();
	document.getElementById('notificacionPersistida').classList.toggle('ver-molde');
}

// borrar horario finalizarTutoria
function borrarHorario(){
	modal();
	document.getElementById('eleHorario').classList.toggle('ver-molde');
}

function borrarHorarioS(){
	document.getElementById('eleHorario').classList.remove('ver-molde');
	document.getElementById('eleHorarioS').classList.toggle('ver-molde');
	setTimeout(function(){
		document.getElementById('eleHorarioS').classList.remove('ver-molde');
		modal();
	}, 1000);
}

function borrarHorarioSC(){
	document.getElementById('eleHorario').classList.remove('ver-molde');
	document.querySelector('.bg').classList.remove('ver-bg');
}

// Tutorado

function agendarTutoria(){
	modal();
	document.getElementById('notificacion').classList.toggle('ver-molde');
}

function cancelarAgenda(){
	document.getElementById('notificacion').classList.remove('ver-molde');
	document.querySelector('.bg').classList.remove('ver-bg');
}