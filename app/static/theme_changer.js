const iconeTema = document.getElementById('icone-tema');
const iconeDownload = document.querySelectorAll('.fa-download');
const iconeTrash = document.querySelectorAll('.fa-trash');
const iconePencil = document.querySelectorAll('.fa-pencil');
const links = document.querySelectorAll('.links');
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
        iconeTrash.forEach(element => {
            element.classList.remove('text-light');  
            element.classList.add('text-dark');
        });
        iconePencil.forEach(element => {
            element.classList.remove('text-light');  
            element.classList.add('text-dark');
        });
        links.forEach(element => {
            element.classList.remove('link-light');  
            element.classList.add('link-dark');
        });
    } else {
        iconeTema.classList.remove('fa-sun');
        iconeTema.classList.add('fa-moon');
        iconeDownload.forEach(element => {
            element.classList.add('text-light');
            element.classList.remove('text-dark');
        });
        iconeTrash.forEach(element => {
            element.classList.add('text-light');
            element.classList.remove('text-dark');
        });
        iconePencil.forEach(element => {
            element.classList.add('text-light');
            element.classList.remove('text-dark');
        });
        links.forEach(element => {
            element.classList.add('link-light');
            element.classList.remove('link-dark');  
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
  const {
    host, hostname, href, origin, pathname, port, protocol, search
  } = window.location
  if(pathname == '/painel') {
    // Atualiza a cor dos rótulos de valor no gráfico
    d3.selectAll(".bar-value")
        .attr("fill", corTexto);
  }
}
