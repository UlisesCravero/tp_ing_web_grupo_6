


document.addEventListener('DOMContentLoaded', function() {
    
    var calendarEl = document.getElementById('calendar');

    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'timeGridWeek',
        headerToolbar: {
        center: 'addEventButton'
        },
        customButtons: {
        addEventButton: {
            text: 'add event...',
            click: function() {
            var dateStr = prompt('Enter a date in YYYY-MM-DD format');
            var date = new Date(dateStr + 'T10:00:00'); // will be in local time

            if (!isNaN(date.valueOf())) { // valid?
                calendar.addEvent({
                title: 'dynamic event',
                start: date,
                allDay: false
                });
                alert('Great. Now, update your database...');
            } else {
                alert('Invalid date.');
            }
            }
        }
        }
    });
    
    var data = JSON.parse(document.querySelector("#jsonData").getAttribute('data-json'));     
    //console.log(data);
    for (let index = 0; index < data.length; index++) {
        calendar.addEvent({
            title: 'Ocupado',
            start: data[index].fields.fecha_inicio,
            end: data[index].fields.fecha_fin,
            allDay: false
            });  
    }
    /*var date = new Date('2021-10-06T10:00:00');
    var dateend = new Date('2021-10-06T12:00:00');
    console.log('addevent');
    calendar.addEvent({
        title: 'dynamic event',
        start: date,
        end: dateend,
        allDay: false
        });*/
    calendar.render();
});




/*var data = JSON.parse(document.querySelector("#jsonData").getAttribute('data-json'));     
console.log(data[0].fields.fecha_fin);

console.log(event)
calendar.addEvent({ // this object will be "parsed" into an Event Object
    title: 'The Title', // a property!
    start: '2021-11-01', // a property!
    end: '2021-11-02' // a property! ** see important note below about 'end' **
    });
calendar.render();
});*/
