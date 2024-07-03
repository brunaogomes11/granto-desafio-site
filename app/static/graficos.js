function grafico_mapa() {
    showLoadingModal();
    const screenWidth = window.screen.width;
    const screenHeight = window.screen.height;
    // Dimensões do SVG
    const width = 600;
    const height = 600;

    // Seleciona o contêiner e adiciona o SVG
    const container = document.getElementById('mapa-container');
    if (container.childNodes.length !== 0) {
        container.innerHTML = ''
    }
    const svg = d3.select("#mapa-container").append("svg")
            .attr("width", width)
            .attr("height", height)
            .attr("viewBox", [0, 0, width, height])
            .attr("style", "max-width: 100%; height: auto; font: 1rem sans-serif;");

    // Configura o grupo principal do SVG
    const g = svg.append("g");
    const proj_br = d3.geoMercator()
        .scale(700)
        .center([-55, -15])
        .translate([width / 2, height / 2]);

    const path = d3.geoPath()
        .projection(proj_br);

    // Tooltip para mostrar o valor ao passar o mouse
    const tooltip = d3.select("body").append("div")
        .attr("class", "tooltip card")
        .style("opacity", 0)
        .style("position", "fixed")
        .style("left", (screenWidth < 900) ? "10px" : "20vw")
        .style("top", "50vh")
        .style("pointer-events", "none");
    Promise.all([
        d3.json('https://raw.githubusercontent.com/fititnt/gis-dataset-brasil/master/uf/topojson/uf.json'),
        fetch('data_graficos/mapa')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro ao carregar o JSON');
                }
                return response.json(); // Carrega como JSON diretamente
            })
    ]).then(([data_map, stateData]) => {
        const states = topojson.feature(data_map, data_map.objects.uf);
        // Cria um mapa para facilitar a busca por número de cada estado
        const stateNumbers = {};
        stateData.states.forEach(state => {
            const sigla = Object.keys(state)[0];
            const info = state[sigla];
            stateNumbers[sigla] = info.number;
        });
        const maxNumber = Math.max(...Object.values(stateNumbers));
        const color = d3.scaleSequential(d3.interpolatePurples)
            .domain([0, maxNumber]);
        
        // Desenha os estados
        g.selectAll(".state")
            .data(states.features)
            .enter()
            .append("path")
            .attr("class", "state")
            .attr("d", path)
            .attr("fill", function (d) {
                const stateId = d.id; // ID do estado
                const value = stateNumbers[stateId] || 0;
                return color(value);
            })
            .attr("stroke", "#000000")
            .attr("stroke-width", 1)
            .on("mouseover", function (event, d) {
                const [x, y] = d3.mouse(this)
                const stateId = event.id; // Use d.id para acessar o ID do estado
                const stateName = (states.features[d].properties.name == 'DF' ? 'Distrito Federal' : states.features[d].properties.name) || 'Desconhecido';
                if (stateName == 'DF') {
                    stateName.set('Distrito Federal')
                }
                const stateNumber = stateNumbers[stateId] || 0;
                tooltip.transition()
                    .duration(200)
                    .style("opacity", .9);
                tooltip.html(`
                    <div class="card-header">Estado: Quantidade de Contratos lidos</div>
                    <div class="card-body">${stateName}: ${stateNumber}</div>
                `)
            })
            .on("mouseout", function () {
                tooltip.transition()
                    .duration(500)
                    .style("opacity", 0);
            });

        // Desenha os contornos dos estados
        g.append("path")
            .datum(topojson.mesh(data_map, data_map.objects.uf, (a, b) => a !== b))
            .attr("d", path)
            .attr("class", "state_contour")
            .attr("fill", "none")
            .attr("stroke", "black");
        hideLoadingModal();
    }).catch(error => {
        console.error('Erro ao carregar os dados:', error);
    });
}
function grafico_barras() {
    showLoadingModal();
    fetch('/data_graficos/grafico')
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao carregar o JSON');
            }
            return response.json();
        })
        .then(data => {
            createChart(data.data);
            hideLoadingModal();
        })
        .catch(error => {
            console.error('Erro ao carregar os dados:', error);
            hideLoadingModal();
        });

    function createChart(data) {
        // Dimensões do gráfico
        const marginTop = 50;
        const marginRight = 400; // Aumentado para caber os rótulos
        const marginBottom = 20;
        const marginLeft = 300; // Aumentado para caber os rótulos
        const width = 800;
        const height = 600;
        const ptBr = d3.formatLocale({
            decimal: ",",
            thousands: ".",
            grouping: [3],
            currency: ["R$", ""]
        });

        const x = d3.scaleLinear()
            .domain([0, d3.max(data, d => d.eixo_valores)])
            .range([0, width]);

        const y = d3.scaleBand()
            .domain(data.sort((a, b) => d3.ascending(a.eixo_categorias, b.eixo_categorias)).map(d => d.eixo_categorias))
            .rangeRound([0, height - marginTop - marginBottom])
            .padding(0.1);

        const innerWidth = width + marginLeft + marginRight;
        const innerHeight = height + marginTop + marginBottom;
        const container = document.getElementById('grafico-container');
        if (container.childNodes.length !== 0) {
            container.innerHTML = '';
        }

        const svg = d3.select("#grafico-container").append("svg")
            .attr("width", innerWidth)
            .attr("height", innerHeight)
            .attr("viewBox", `0 0 ${innerWidth} ${innerHeight}`)
            .attr("preserveAspectRatio", `xMidYMid meet`)
            .attr("style", "max-width: 90%; height: auto; font: 1rem sans-serif;");

        const g = svg.append("g")
            .attr("transform", `translate(${marginLeft}, ${marginTop})`);

        g.append("g")
            .attr("fill", "#4510a3")
            .selectAll("rect")
            .data(data)
            .join("rect")
            .attr("x", x(0))
            .attr("y", d => y(d.eixo_categorias))
            .attr("class", "bordered border-1")
            .attr("height", y.bandwidth())
            .attr("width", 0)
            .transition()
            .duration(1000)
            .attr("width", d => x(d.eixo_valores));

        g.append("g")
            .selectAll("text")
            .data(data)
            .join("text")
            .attr("class", "bar-value")
            .attr("x", d => x(d.eixo_valores) + 5)
            .attr("y", d => y(d.eixo_categorias) + y.bandwidth() / 2)
            .attr("dy", "0.35em")
            .attr("fill", "currentColor")
            .text(d => ptBr.format("$,.2f")(d.eixo_valores));

        g.append("g")
            .attr("transform", `translate(0,0)`)
            .call(d3.axisTop(x).ticks(4).tickFormat(ptBr.format("$,.2f")))
            .style("font-size", "1rem")
            .call(g => g.select(".domain").remove());

        g.append("g")
            .attr("transform", `translate(0,0)`)
            .style("font-size", "1rem")
            .call(d3.axisLeft(y).tickSizeOuter(0));
    }
}

function showLoadingModal() {
    const loadingModal = new bootstrap.Modal(document.getElementById('loadingModal'), {
        backdrop: 'static',
        keyboard: false
    });
    loadingModal.show();
}

function hideLoadingModal() {
    const loadingModal = bootstrap.Modal.getInstance(document.getElementById('loadingModal'));
    loadingModal.hide();
}

grafico_mapa()
document.getElementById('nav-home-tab').addEventListener('shown.bs.tab', function (event) {
    grafico_mapa()
});

document.getElementById('nav-profile-tab').addEventListener('shown.bs.tab', function (event) {
    grafico_barras()
});