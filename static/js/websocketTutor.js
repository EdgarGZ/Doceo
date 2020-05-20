// DOM Manipulation Variables
const USER = document.getElementById('userIdentifier').textContent;
const CONTENEDORNOTIFICACION = document.getElementById('insertarNotificacion');

// WEBSOCKET
const WEBSOCKETURL = `ws://127.0.0.1:8000/ws/tutor/notifications/${USER}/`; // Websocket URL, same as mentioned in the routing.py
let WEBSOCKETURLENDPOINT =  WEBSOCKETURL;

const SOCKET = new WebSocket(WEBSOCKETURLENDPOINT) // Creating a new Web Socket Connection

// Socket On receive message Functionality
SOCKET.onmessage = async function (e){
    console.log('message', e)
    // alert(e.data) // Access the notification data
    const MODALASKTUTORSHIP = `
        <p class="b"><strong>${e.data.split('"')[1].charAt(0).toUpperCase()}${e.data.split('"')[1].slice(1)}</strong></p>
        <input class="cancelar pull-right" style="background-color: red" type="submit" name="" value="Cerrar" onclick="cancelarAgenda()">
    `;
    document.getElementById('notificacion').innerHTML = MODALASKTUTORSHIP;
    document.getElementById('notificacion').classList.toggle('ver-molde');
    document.querySelector('.bg').classList.toggle('ver-bg');
    
    const response = await fetch(`get/last/notification/`, {
        method: 'POST',
    });
    const resp = await response.json();
    try {
        document.getElementById('noNotificacions').style.display = 'none';
    } catch (error) { }
    const MODALPERSISTENTE = `
        <div class="col-xs-12 col-md-12 notificaciones">
            <p class="" id="pendiente"><a href="">${resp.data.tutorado}</a> solicitó la tutoría ${resp.data.tutoria} | <a onclick="verNoti(${resp.data.id_notificacion})">Ver detalles</a></p>
        </div>
    `;
    const HTMLMODALPERSISTENTE = crearTemplate(MODALPERSISTENTE);
    CONTENEDORNOTIFICACION.append(HTMLMODALPERSISTENTE);
    const BADGE = document.getElementById('notificacionBadge');
    BADGE.innerHTML = `${parseInt(BADGE.innerText) + 1}`
    BADGE.style.background = 'red';
}

// Socket Connet Functionality
SOCKET.onopen = function(e){
    console.log('open', e)
}

// Socket Error Functionality
SOCKET.onerror = function(e){
    console.log('error', e)
}

// Socket close Functionality
SOCKET.onclose = function(e){
    console.log('closed', e)
}


function nuevaTutoria() {

	let area_especialidad = document.getElementById('area_especialidad').value;
	let subarea_especialidad = document.getElementById('subarea_especialidad').textContent;
    let dia = document.getElementById('dia').value;
    
    
    const data = {
        accion: 'notify_tutorship',
        user: USER,
        area_especialidad: area_especialidad,
        subarea_especialidad: subarea_especialidad,
        dia: dia
    };

    try {
        SOCKET.send(JSON.stringify({ ...data }));
    } catch (error) {
        console.error(error.message);
    }
}

function crearTemplate(HTMLString){
    const html = document.implementation.createHTMLDocument();
    html.body.innerHTML = HTMLString;
    return html.body.children[0]
}

async function aceptarTutoriaWS(tutorship, tutored) {
    const data = {
        accion: 'notify_tutored_accepted_tutorship',
        user: USER,
        tutorship: tutorship,
        tutored: tutored
    };

    try {
        SOCKET.send(JSON.stringify({ ...data }));
    } catch (error) {
        console.error(error.message);
    }
}
