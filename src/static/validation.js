const form = document.querySelector('form')
const username_input = document.querySelector('input[name="username"]')
const password_input = document.querySelector('input[name="password"]')
const error_message = document.getElementById('error-message')

function getFormErrors(username, password){
  let errors = []

  if(username === '' || username == null){
    errors.push('Username is required')
    if(username_input) username_input.parentElement.classList.add('incorrect')
  }
  if(password === '' || password == null){
    errors.push('Password is required')
    if(password_input) password_input.parentElement.classList.add('incorrect')
  }

  return errors;
}

if(form && username_input && password_input && error_message){
  form.addEventListener('submit', function(event){
    username_input.parentElement.classList.remove('incorrect')
    password_input.parentElement.classList.remove('incorrect')
    error_message.textContent = ''

    const errors = getFormErrors(username_input.value, password_input.value)
    if(errors.length > 0){
      event.preventDefault()
      error_message.textContent = errors.join(', ')
    }
  })
}