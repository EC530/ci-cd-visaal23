const startDate = new Date();
const daysOfWeek = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
const monthNames = ["January", "February", "March", "April", "May", "June", 
                    "July", "August", "September", "October", "November", "December"];

let appointments = [
    { day: 0, time: "9:30 AM - 10:00 AM", user: "Gracie Morris", type: "Blood analysis", class: "green" },
    { day: 0, time: "10:00 AM - 10:30 AM", user: "Adam King", type: "General examination", class: "blue" },
    { day: 0, time: "11:00 AM - 11:30 AM", user: "Sienna Butler", type: "Prenatal testing", class: "red" },
    { day: 2, time: "9:30 AM - 10:00 AM", user: "Gracie Morris", type: "Blood analysis", class: "green" },
    { day: 1, time: "10:00 AM - 10:30 AM", user: "Adam King", type: "General examination", class: "blue" },
    { day: 1, time: "11:00 AM - 11:30 AM", user: "Sienna Butler", type: "Prenatal testing", class: "red" }
];

let content = document.querySelector('.timeline__content');

function generateSlide(dayIndex) {
    let currentDate = new Date(startDate.getTime() + dayIndex * 24 * 60 * 60 * 1000);
    let day = currentDate.getDate();
    let month = monthNames[currentDate.getMonth()];
    let dayOfWeek = daysOfWeek[currentDate.getDay()];
    let isToday = dayIndex === 0;

    let dayAppointments = appointments.filter(appointment => appointment.day === dayIndex);

    let appointmentsHTML = dayAppointments.map(appointment =>
        `<div class="timeline__row">
            <div class="timeline__hour">${appointment.time.split('-')[0]}</div>
            <div class="timeline__details timeline__details--${appointment.class}">
                <h3 class="timeline__user">${appointment.user}</h3>
                <div class="timeline__time">${appointment.time}</div>
                <div class="timeline__info timeline__info--${appointment.class}">${appointment.type}</div>
            </div>
        </div>`).join('');

    return `<div class="timeline__slide swiper-slide">
        <div class="timeline__header">
            <span class="timeline__header-day">${day}</span>
            <span class="timeline__header-month">${dayOfWeek}, ${month}</span>
            ${isToday ? '<div class="timeline__header-todaybg"></div><div class="timeline__header-today">TODAY</div>' : ''}
        </div>
        
        <div class="timeline__grid scrollbar-macosx">
            ${appointmentsHTML}
        </div>
    </div>`;
}

// Initial page load: fill the timeline
for (let i = 0; i < 7; i++) {
    let slideHTML = generateSlide(i);
    content.innerHTML += slideHTML;
}

function addAppointment(patientName, dateTime, type, color) {
    const appointmentDate = new Date(dateTime);
    const appointmentDay = appointmentDate.getDay();
    const time = `${appointmentDate.getHours()}:${appointmentDate.getMinutes()} AM - ${appointmentDate.getHours()+1}:${appointmentDate.getMinutes()} AM`; // Adjust time format as needed

    const newAppointment = { day: appointmentDay, time, user: patientName, type, class: color };
    appointments.push(newAppointment);

    // Re-render the updated day
    const updatedSlideHTML = generateSlide(appointmentDay);
    const slides = Array.from(content.querySelectorAll('.timeline__slide'));
    slides[appointmentDay].outerHTML = updatedSlideHTML;
}

function submitAppointmentForm() {
    const patientName = document.querySelector('[name="appname"]').value;
    const dateTime = document.querySelector('[name="timepicker"]').value;
    const type = document.querySelector('[name="apptype"]').value;
    const color = 'green'; // Determine the color logic based on conditions or input

    addAppointment(patientName, dateTime, type, color);

    console.log('Appointment added:', { patientName, dateTime, type });
    // Potentially clear the form here or close the modal
}

document.addEventListener('DOMContentLoaded', function() {
    const submitBtn = document.getElementById('submitAppointment');
    if (submitBtn) {
        submitBtn.addEventListener('click', submitAppointmentForm);
    } else {
        console.error('Submit button not found.');
    }
});
