document.getElementById('botao-fechar').addEventListener('click', function() {
  // Lógica para fechar o app
  document.getElementById('app').style.display = 'none';
});

document.getElementById('botao-minimizar').addEventListener('click', function() {
  // Lógica para minimizar o app
  const app = document.getElementById('app');
  if (app.style.height === '30px') {
    app.style.height = 'auto';
    this.innerHTML = '&#8211;'; // Símbolo de menos
  } else {
    app.style.height = '30px';
    app.style.overflow = 'hidden';
    this.innerHTML = '&#9633;'; // Símbolo de quadrado (restaurar)
  }
});