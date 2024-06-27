const iconeTema = document.getElementById('icone-tema');
const iconeDownload = document.querySelectorAll('.fa-download');
let tema = 'light'; // Tema inicial
const temaSalvo = localStorage.getItem('tema');
if (temaSalvo) {
  tema = temaSalvo;
  document.body.dataset.bsTheme = tema;
}

// Função para aplicar o tema
function aplicarTema() {
    if (tema === 'light') {
        iconeTema.classList.remove('fa-moon');
        iconeTema.classList.add('fa-sun');
        iconeDownload.forEach(element => {
            element.classList.remove('text-light');  
            element.classList.add('text-dark');
        });
    } else {
        iconeTema.classList.remove('fa-sun');
        iconeTema.classList.add('fa-moon');
        iconeDownload.forEach(element => {
            element.classList.add('text-light');
            element.classList.remove('text-dark');
        });
    }
    localStorage.setItem('tema', tema);
    atualizarTemaGrafico(); // Chama a função para atualizar a cor dos rótulos
}

// Aplicar tema ao carregar a página
aplicarTema();

iconeTema.addEventListener('click', () => {
    tema = tema === 'light' ? 'dark' : 'light';
    document.body.dataset.bsTheme = tema;
    aplicarTema();
});

function atualizarTemaGrafico() {
  const temaAtual = document.body.dataset.bsTheme;
  const corTexto = temaAtual === 'light' ? 'black' : 'white';

  // Atualiza a cor dos rótulos de valor no gráfico
  d3.selectAll(".bar-value")
      .attr("fill", corTexto);
}
