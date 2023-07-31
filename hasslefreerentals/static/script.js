// SEND OTP JS CODE BEGIN
let countdownTimer;
let remainingSeconds = 80;
let isCountdownActive = false;

function startTimer() {
  countdownTimer = setInterval(updateTimer, 1000);
  updateTimer();
}

function updateTimer() {
  const otpLink = document.querySelector('.otpsend');

  if (remainingSeconds > 0) {
    otpLink.textContent = `Resend Code in (${remainingSeconds} sec)`;
    remainingSeconds--;
  } else {
    otpLink.textContent = 'Resend Code';
    otpLink.classList.add('active');
    clearInterval(countdownTimer);
    isCountdownActive = false;
  }
}

function sendotp() {
  const otpLink = document.querySelector('.otpsend');

  if (!isCountdownActive) {
    // Code to send the OTP goes here
    // You can add your logic to send the OTP
    // For example, you can make an API call to send the OTP
    var value = document.getElementById('phoneno').value;
    $.ajax({
      url: '/auth/sendotp',
      type: 'POST',
      data: { 'data': value }
    });
    console.log('Sending OTP...');
    // Once the OTP is sent, start the timer
    startTimer();
    isCountdownActive = true;
  }
}
// SEND OTP JS CODE ENDS


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
