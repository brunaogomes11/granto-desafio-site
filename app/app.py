import os
from flask import Flask, redirect, render_template, request, send_from_directory, current_app, g, jsonify, send_file
import os
import configparser
from pymongo import MongoClient, InsertOne
import requests
import json

app = Flask(__name__)
url_base = 'https://granto-desafio-api.onrender.com'
theme = 'light'
@app.route("/")
def homePage():
    return render_template("index.html")
@app.route("/painel/")
@app.route("/painel")
def painel():
    return render_template("painel.html")

@app.route("/insercao/", methods=['GET', 'POST'])
@app.route("/insercao", methods=['GET', 'POST'])
def insercao():
    try:
        if request.method == 'POST':
            if 'file' not in request.files:
                return redirect(request.url)
            file = request.files.get('file')
            if not file:
                return
            files = {'file': (file.filename, file.stream, file.mimetype)}
            response = requests.get(f'{url_base}/inserir', files=files)
            mensagem = response.json()['message']
            status_code = response.status_code
            return render_template('insercao.html', mensagem=mensagem, response_code=status_code)
        return render_template("insercao.html")
    except Exception as e:
        return render_template("erros.html", status_code=e)

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
        return render_template("erros.html", status_code=e)

@app.route("/busca/<int:pagina>/<query>/", methods=['GET', 'POST'])
@app.route("/busca/<int:pagina>/<query>", methods=['GET', 'POST'])
@app.route("/busca/<int:pagina>/", methods=['GET', 'POST'])
@app.route("/busca/<int:pagina>", methods=['GET', 'POST'])
@app.route("/busca/", methods=['GET', 'POST'])
@app.route("/busca", methods=['GET', 'POST'])
def busca(query = '', pagina = 1):
    try:
        if (request.method == "POST"):
            query = request.form.get("search_bar")
            response = requests.post(f'{url_base}/buscar?pagina={pagina}&query={query}')
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
            json_response = {"pagina":pagina, "query":query}
            response = requests.post(f'{url_base}/buscar', json=json_response)
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
            return render_template("erros.html", status_code=405)
    except Exception as e:
        return render_template("erros.html", status_code=e)

@app.route("/baixar/<id>")
def baixar(id=''):
    arquivo = f'{url_base}/baixar/{id}'
    return redirect(arquivo)

@app.route("/atualizar/", methods=['POST'])
def atualizar():
    if request.method == 'POST':
        id = request.form.get('inputID')
        empresa_contratante = request.form.get('inputEmpresaContratante')
        cnpj_empresa_contratante = request.form.get('inputCNPJContratante')
        empresa_contratada = request.form.get('inputEmpresaContratada')
        cnpj_empresa_contratada = request.form.get('inputCNPJContratada')
        vigencia_seguro = request.form.get('inputVigencia')
        valor_seguro = request.form.get('inputValor')
        dict_atualizar = {}
        if empresa_contratante:
            dict_atualizar["preambulo.contratante.razao_social"] = empresa_contratante
        if cnpj_empresa_contratante:
            dict_atualizar["preambulo.contratante.cnpj"] = cnpj_empresa_contratante
        if empresa_contratada:
            dict_atualizar["preambulo.contratada.razao_social"] = empresa_contratada
        if cnpj_empresa_contratada:
            dict_atualizar["preambulo.contratada.cnpj"] = cnpj_empresa_contratada
        if vigencia_seguro:
            dict_atualizar["preambulo.vigencia"] = vigencia_seguro
        if valor_seguro:
            dict_atualizar["preambulo.valor"] = valor_seguro
        response = requests.get(f'{url_base}/atualizar/{id}', json=dict_atualizar)
        return redirect(request.referrer)
    else:
        return render_template("erros.html", status_code=405)
    
@app.route("/deletar/<id>")
def deletar(id=''):
    response = requests.get(f'{url_base}/deletar/{id}')
    data = response.json()
    return redirect(request.referrer)

@app.route('/data_graficos/<grafico>')
def data_graficos(grafico):
    response = requests.get(f'{url_base}/data_graficos/{grafico}')
    data = response.json()
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
