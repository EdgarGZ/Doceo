// CONSTANTS
const MONTHS = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Augosto", "Septiembre", "Octobre", "Noviembre", "Diciembre"]

// DOM Manipulation Variables
const USER = document.getElementById('userIdentifier').textContent;

// WEBSOCKET
const WEBSOCKETURL = `ws://127.0.0.1:8000/ws/tutored/notifications/${USER}/`; // Websocket URL, same as mentioned in the routing.py
let WEBSOCKETURLENDPOINT =  WEBSOCKETURL;

const SOCKET = new WebSocket(WEBSOCKETURLENDPOINT) // Creating a new Web Socket Connection

// Socket On receive message Functionality
SOCKET.onmessage = function(e){
    console.log('message', e)
    alert(e.data) // Access the notification data
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


const TUTORSHIPBUTTON = document.getElementById('tutorship');
TUTORSHIPBUTTON.addEventListener('click', async (e) => {
    // Prevents the default behavior of the html element.
    e.preventDefault();

    // Variables
    let splittedText = e.target.parentElement.parentElement.children[1].textContent.split(':');
    let splittedSchedule = splittedText[1] + ':' + splittedText[2] + ':' + splittedText[3];
    let date = splittedSchedule.split('de')[0];
    let time = splittedSchedule.split('de')[1];
    let month = MONTHS[new Date().getMonth()];
    let referenceTutorship = e.target.parentElement.parentElement.children[3].textContent;
    let hideButton = e.target.parentElement.parentElement.children[4].children[0];

    // Constants
    const MODALTUTORSHIP = `
        <p class="b" id="tutoship_area">${e.target.parentElement.parentElement.children[0].textContent}</p>
        <p class="b">${date} de ${month}</p>
        <p class="b">${time}</p>
        <p>Importante: Debe de estar al pendiente de la confirmación por parte del tutor.</p>
        <div class="flex botonera">
            <input class="cancelar" type="submit" name="" value="Cancelar" onclick="cancelarAgenda()">
            <input class="guardar" type="submit" name="" value="Aceptar" onclick="agendarTutoria(${referenceTutorship})">
        </div>
    `;

    // DOM manipulation
    document.getElementById('notificacion').innerHTML = MODALTUTORSHIP;
    document.getElementById('notificacion').classList.toggle('ver-molde');
	document.querySelector('.bg').classList.toggle('ver-bg');
});

async function agendarTutoria(referencia) {
    const response = await fetch(`schedule/tutorship/${referencia}/`, {
        method: 'POST',
    });
    const resp = await response.json();
    let tutoship_area = document.getElementById('tutoship_area').textContent;

    if(resp.data === 'success'){
        const data = {
            accion: 'notify_schedule_tutorship',
            user: USER,
            tutoship_area: tutoship_area,
            referencia: referencia
        };
    
        try {
            SOCKET.send(JSON.stringify({ ...data }));
        } catch (error) {
            console.error(error.message);
        }
        cancelarAgenda();
        aceptarTuto();
        document.querySelector('.bg').classList.toggle('ver-bg');
        setTimeout(() => {
            location.reload();
        }, 5000)
    }
}
