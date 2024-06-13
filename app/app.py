import os
from flask import Flask, redirect, render_template, request, send_from_directory, current_app, g, jsonify, send_file
import os
import configparser
from pymongo import MongoClient, InsertOne
import requests

app = Flask(__name__)
url_base = 'https://granto-desafio-api.onrender.com'

@app.route("/")
def homePage():
    return render_template("index.html")

@app.route("/insercao")
def insercao():
    return render_template("insercao.html")

@app.route("/listagem/<int:pagina>/")
@app.route("/listagem/<int:pagina>")
@app.route("/listagem/")
@app.route("/listagem")
def listagem(pagina=1):
    try:
        response = requests.get(f'{url_base}/listar/{pagina}', allow_redirects=True)
        data = response.json()
        
        # Captura dos dados necessários
        documents = data['documentos']
        qntd_docs = data['total']
        start_index = data['index_inicial']
        final_index = data['index_final']
        total_pages = data['num_pages']

        # Verificações adicionais de página atual
        previous_page = pagina - 1 if pagina > 1 else 1
        next_page = pagina + 1 if pagina < total_pages else total_pages

        # Renderiza o template com os dados obtidos
        return render_template("listagem.html", 
            documents=documents, 
            qntd_docs=qntd_docs, 
            start_index=start_index, 
            final_index=final_index, 
            previous_page=previous_page, 
            next_page=next_page, 
            current_page=pagina, 
            total_pages=total_pages
        )
    
    except Exception as e:
        print(f"Erro ao obter os dados da página {pagina}: {str(e)}")
        return 'Erro ao carregar a página'

@app.route("/busca/<int:pagina>/<query>/", methods=['GET', 'POST'])
@app.route("/busca/<int:pagina>/<query>", methods=['GET', 'POST'])
@app.route("/busca/<int:pagina>/", methods=['GET', 'POST'])
@app.route("/busca/<int:pagina>", methods=['GET', 'POST'])
@app.route("/busca/", methods=['GET', 'POST'])
@app.route("/busca", methods=['GET', 'POST'])
def busca(query = '', pagina = 1):
    if (request.method == "POST"):
        query = request.form.get("search_bar")
        response = requests.post(f'{url_base}/buscar/{pagina}/{query}')
        data = response.json()
        if (len(data['documentos']) == 0):
            return render_template("busca_avancada.html", 
                documents=[], 
                qntd_docs=-1, 
                start_index=0, 
                final_index=0, 
                previous_page=0, 
                next_page=0, 
                current_page=0, 
                total_pages=0,
                search=query
            )
        # Captura dos dados necessários
        documents = data['documentos']
        qntd_docs = data['total']
        start_index = data['index_inicial']
        final_index = data['index_final']
        total_pages = data['num_pages']

        # Verificações adicionais de página atual
        previous_page = pagina - 1 if pagina > 1 else 1
        next_page = pagina + 1 if pagina < total_pages else total_pages

        # Renderiza o template com os dados obtidos
        return render_template("busca_avancada.html", 
            documents=documents, 
            qntd_docs=qntd_docs, 
            start_index=start_index, 
            final_index=final_index, 
            previous_page=previous_page, 
            next_page=next_page, 
            current_page=pagina, 
            total_pages=total_pages,
            search=query
        )
    elif (request.method == "GET"):
        response = requests.post(f'{url_base}/buscar/{pagina}/{query}')
        data = response.json()
        if (len(data['documentos']) == 0):
            return render_template("busca_avancada.html", 
                documents=[], 
                qntd_docs=-1, 
                start_index=0, 
                final_index=0, 
                previous_page=0, 
                next_page=0, 
                current_page=0, 
                total_pages=0,
                search=query
            )
        # Captura dos dados necessários
        documents = data['documentos']
        qntd_docs = data['total']
        start_index = data['index_inicial']
        final_index = data['index_final']
        total_pages = data['num_pages']

        # Verificações adicionais de página atual
        previous_page = pagina - 1 if pagina > 1 else 1
        next_page = pagina + 1 if pagina < total_pages else total_pages

        # Renderiza o template com os dados obtidos
        return render_template("busca_avancada.html", 
            documents=documents, 
            qntd_docs=qntd_docs, 
            start_index=start_index, 
            final_index=final_index, 
            previous_page=previous_page, 
            next_page=next_page, 
            current_page=pagina, 
            total_pages=total_pages,
            search=query
        )
    else:
        return 405

@app.route("/baixar", methods=["GET", "POST"])
def baixar(documentos = [], row_number=0):
    return 404
        
if __name__ == '__main__':
    app.run(debug=True)
