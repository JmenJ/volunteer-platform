document.addEventListener('DOMContentLoaded', () => {
    const regRole = document.getElementById('regRole');
    const volunteerFields = document.getElementById('volunteerFields');
    const partnerFields = document.getElementById('partnerFields');
    function toggleFields(role) {
        if (role === 'volunteer') {
          volunteerFields.style.display = 'block';
          partnerFields.style.display = 'none';
      
          document.getElementById('volunteerInn').required = true;
          document.getElementById('volunteerPassword').required = true;
      
          document.getElementById('partnerLogin').required = false;
          document.getElementById('partnerEmail').required = false;
          document.getElementById('partnerPassword').required = false;
      
        } else if (role === 'partner') {
          partnerFields.style.display = 'block';
          volunteerFields.style.display = 'none';
      
          document.getElementById('partnerLogin').required = true;
          document.getElementById('partnerEmail').required = true;
          document.getElementById('partnerPassword').required = true;
      
          document.getElementById('volunteerInn').required = false;
          document.getElementById('volunteerPassword').required = false;
      
        } else {
          partnerFields.style.display = 'none';
          volunteerFields.style.display = 'none';
      
          document.getElementById('volunteerInn').required = false;
          document.getElementById('volunteerPassword').required = false;
          document.getElementById('partnerLogin').required = false;
          document.getElementById('partnerEmail').required = false;
          document.getElementById('partnerPassword').required = false;
        }
      }
      
    const registerForm = document.getElementById('registerForm');
  
    const modal = document.getElementById('codeModal');
    const modalMsg = document.getElementById('codeModalMessage');
    const codeInput = document.getElementById('codeInput');
    const confirmBtn = document.getElementById('confirmCodeBtn');
  
    const timerText = document.getElementById('timerText');
    const timerSpan = document.getElementById('timer');
    const resendBtn = document.getElementById('resendBtn');
  
    let confirmationCode = '';
    let pendingUser = null;
    let countdown = null;
    let secondsLeft = 60;
  
    const volunteerDB = {
      '1234567890': 'volunteer@mail.ru',
      '9876543210': 'ivanov@example.com'
    };
  
    regRole.addEventListener('change', () => {
        toggleFields(regRole.value);
      });
      
    registerForm.addEventListener('submit', function (e) {
      e.preventDefault();
      const role = regRole.value;
  
      if (role === 'volunteer') {
        const inn = document.getElementById('volunteerInn').value;
        const password = document.getElementById('volunteerPassword').value;
        const email = volunteerDB[inn];
  
        if (!email) {
          alert('ИНН не найден в базе');
          return;
        }
  
        confirmationCode = Math.floor(100000 + Math.random() * 900000).toString();
        pendingUser = { role, inn, password, email };
        openModal(email);
      }
  
      else if (role === 'partner') {
        const login = document.getElementById('partnerLogin').value;
        const password = document.getElementById('partnerPassword').value;
        const email = document.getElementById('partnerEmail').value;
  
        confirmationCode = Math.floor(100000 + Math.random() * 900000).toString();
        pendingUser = { role, login, password, email };
        openModal(email);
      }
  
      else {
        alert('Пожалуйста, выберите роль');
      }
    });
  
    confirmBtn.addEventListener('click', () => {
      if (codeInput.value === confirmationCode && pendingUser) {
        if (pendingUser.role === 'volunteer') {
          console.log(`Волонтёр зарегистрирован:\nИНН: ${pendingUser.inn}\nПочта: ${pendingUser.email}`);
          alert('Волонтёр успешно зарегистрирован!');
        } else {
          console.log(`Партнёр зарегистрирован:\nЛогин: ${pendingUser.login}\nПочта: ${pendingUser.email}`);
          alert('Партнёр успешно зарегистрирован!');
          window.location.replace("par/reg_par.html");
        }
  
        modal.style.display = 'none';
        codeInput.value = '';
        pendingUser = null;
      } else {
        alert('Неверный код');
      }
    });
  
    function startTimer() {
      clearInterval(countdown);
      secondsLeft = 60;
      timerSpan.textContent = secondsLeft;
      resendBtn.style.display = 'none';
  
      countdown = setInterval(() => {
        secondsLeft--;
        timerSpan.textContent = secondsLeft;
  
        if (secondsLeft <= 0) {
          clearInterval(countdown);
          resendBtn.style.display = 'inline-block';
        }
      }, 1000);
    }
  
    function openModal(email) {
      modalMsg.textContent = `Код отправлен на почту: ${email} (на деле: ${confirmationCode})`;
      modal.style.display = 'flex';
      startTimer();
    }
  
    resendBtn.addEventListener('click', () => {
      if (!pendingUser) return;
  
      confirmationCode = Math.floor(100000 + Math.random() * 900000).toString();
      alert(`Новый код отправлен на почту: ${pendingUser.email} (на деле: ${confirmationCode})`);
      startTimer();
    });
  });
  