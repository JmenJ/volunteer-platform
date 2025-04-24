document.addEventListener('DOMContentLoaded', () => {
  const userRole = document.getElementById('userRole');

  const volunteerLogin = document.getElementById('volunteerLogin');
  const volunteerPassword = document.getElementById('volunteerPassword');

  const partnerLogin = document.getElementById('partnerLogin');
  const partnerPassword = document.getElementById('partnerPassword');

  function toggleLoginFields(role) {
    if (role === 'volunteer') {
      volunteerLogin.style.display = 'block';
      volunteerPassword.style.display = 'block';
      volunteerLogin.required = true;
      volunteerPassword.required = true;

      partnerLogin.style.display = 'none';
      partnerPassword.style.display = 'none';
      partnerLogin.required = false;
      partnerPassword.required = false;
    } else if (role === 'partner') {
      partnerLogin.style.display = 'block';
      partnerPassword.style.display = 'block';
      partnerLogin.required = true;
      partnerPassword.required = true;

      volunteerLogin.style.display = 'none';
      volunteerPassword.style.display = 'none';
      volunteerLogin.required = false;
      volunteerPassword.required = false;
    } else {
      // Ничего не выбрано — скрываем всё
      volunteerLogin.style.display = 'none';
      volunteerPassword.style.display = 'none';
      partnerLogin.style.display = 'none';
      partnerPassword.style.display = 'none';

      volunteerLogin.required = false;
      volunteerPassword.required = false;
      partnerLogin.required = false;
      partnerPassword.required = false;
    }
  }

  userRole.addEventListener('change', () => {
    toggleLoginFields(userRole.value);
  });

  // Обработка при загрузке страницы
  toggleLoginFields(userRole.value);
});


document.getElementById('loginForm').addEventListener('submit', function (e) {
  e.preventDefault();

  const role = document.getElementById('userRole').value;

  if (!role) {
    alert('Пожалуйста, выберите роль');
    return;
  }

  let login = '';
  let password = '';

  if (role === 'volunteer') {
    login = document.getElementById('volunteerLogin').value.trim();
    password = document.getElementById('volunteerPassword').value;
  } else if (role === 'partner') {
    login = document.getElementById('partnerLogin').value.trim();
    password = document.getElementById('partnerPassword').value;
  }

  // Проверка на заполненность
  if (!login || !password) {
    alert('Пожалуйста, заполните все поля');
    return;
  }

  // Вывод в консоль (не показываем пароль явно)
  console.log(`Попытка входа:
Роль: ${role === 'volunteer' ? 'Волонтёр' : 'Партнёр'}
Логин: ${login}
Пароль: ${'*'.repeat(password.length)}`);

  // Уведомление и перенаправление
  alert(`Вход как ${role === 'volunteer' ? 'Волонтёр' : 'Партнёр'} выполнен`);

  if (role === 'volunteer') {
    window.location.replace("main_vol.html");
  } else {
    window.location.replace("main_par.html");
  }
});
