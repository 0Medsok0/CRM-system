// Проверяем на пустоту
const form = document.querySelector('form');
  const submitButton = document.querySelector('input[type="submit"]');
  const inputs = document.querySelectorAll('input[type="text"]');

  form.addEventListener('submit', (event) => {
    let isValid = true;

    inputs.forEach((input) => {
      if (input.value.trim() === '') {
        isValid = false;
        input.classList.add('error');
      } else {
        input.classList.remove('error');
      }

      // Защита от введения скриптов
      input.value = input.value.replace(/<[^>]*>?/gm, '');
    });

    if (!isValid) {
      event.preventDefault();
    }
  });

  inputs.forEach((input) => {
    input.addEventListener('input', () => {
      input.classList.remove('error');
    });
  });