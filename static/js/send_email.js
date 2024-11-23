document.querySelector('form').addEventListener('submit', function(event) {
  var contactId = document.getElementById('contact_id').value;
  var subject = document.getElementById('subject').value;
  var body = document.getElementById('body').value;

  if (contactId === '' || subject === '' || body === '') {
    alert('All fields must be filled out');
    event.preventDefault();
  }
});
