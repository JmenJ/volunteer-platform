document.getElementById('loginForm').addEventListener('submit', function (e) {
  e.preventDefault();

  const role = document.getElementById('userRole').value;
  const login = document.getElementById('login').value;
  const password = document.getElementById('password').value;

  if (!role) {
    alert('Пожалуйста, выберите роль');
    return;
  }
  
  fetch('http://127.0.0.1:30000/login.html_prov', { headers: { 'Content-Type': 'text/plain', 'MyType': role, 'MyLogin':login, 'MyPassword':password} }) 
  .then(response => {
    if (response.headers.get("MyState")==="False"){
      alert("Не верно ввидено значение!");
      return;
    };
  })

  
  console.log(`Попытка входа:
Роль: ${role === 'Volunteers' ? 'Волонтёр' : 'Партнёр'}
Логин: ${login}
Пароль: ${'*'.repeat(password.length)}`);

  alert(`Вход как ${role === 'Volunteers' ? 'Волонтёр' : 'Партнёр'} выполнен`);

  // Перенаправление в зависимости от роли
  if (role === 'Volunteers') {
    window.location.replace("/main_vol.html");
  } else {
    window.location.replace("/main_par.html");
  }
});
