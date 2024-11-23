document.querySelector('form').addEventListener('submit', function(event) {
  var name = document.getElementById('name').value;
  var email = document.getElementById('email').value;
  var phone = document.getElementById('phone').value;
  var region = document.getElementById('region').value;
  var industry = document.getElementById('industry').value;

  var scriptPattern = /<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi;

  if (name === '' || email === '' || phone === '' || region === '' || industry === '') {
    alert('All fields are required.');
    event.preventDefault();
  } else if (scriptPattern.test(name) || scriptPattern.test(email) || scriptPattern.test(phone) || scriptPattern.test(region) || scriptPattern.test(industry)) {
    alert('Script tags are not allowed.');
    event.preventDefault();
  }
});
