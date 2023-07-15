function sendotp() {
    var value = document.getElementById('phoneno').value;
    $.ajax({
        url: '/auth/sendotp',
        type: 'POST',
        data: { 'data': value }
    });
}

window.addEventListener('DOMContentLoaded', (event) => {
    console.log('DOM fully loaded and parsed');
    let queryterm = document.getElementById('search');
        if (queryterm) {
            queryterm.addEventListener('input', async function() {
                let response = await fetch('/searchequipments?q=' + queryterm.value);
                let results = await response.text();
                console.log('Inside Second JS');
                console.log(results);
                document.getElementById('searchresults').innerHTML = results;    
            });
        }    
});

function submit() {
    document.getElementById('form-element').submit()
}