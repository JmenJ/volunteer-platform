document.getElementById('loginForm').addEventListener('submit', function (e) {
    e.preventDefault();
  
    const role = document.getElementById('userRole').value;
    const login = document.getElementById('login').value;
    const password = document.getElementById('password').value;
  
    if (!role) {
      alert('Пожалуйста, выберите роль');
      return;
    }
  
    console.log(`Попытка входа:
  Роль: ${role === 'volunteer' ? 'Волонтёр' : 'Партнёр'}
  Логин: ${login}
  Пароль: ${'*'.repeat(password.length)}`);
  
    alert(`Вход как ${role === 'volunteer' ? 'Волонтёр' : 'Партнёр'} выполнен`);
  });
  