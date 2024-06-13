import os
from flask import Flask, redirect, render_template, request, send_from_directory, current_app, g, jsonify, send_file
import os
import configparser
from pymongo import MongoClient, InsertOne
<<<<<<< HEAD
import requests

app = Flask(__name__)
url_base = 'https://granto-desafio-api.onrender.com'

=======
from bson import ObjectId, Binary
import tempfile
from dotenv import load_dotenv

app = Flask(__name__)
# Atualizando para buscar a URI corretamente
database_url = os.getenv('DB_URI_PASS')
client = MongoClient(database_url)
db = client.mydata
collection = db.mytable
>>>>>>> 1fa22a6a8a8de5f5dec049559b2b42055c4d4189
@app.route("/")
def homePage():
    return "Servidor Ok"

<<<<<<< HEAD
@app.route("/insercao")
def insercao():
    return render_template("insercao.html")

from flask import render_template, redirect, url_for, request

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
=======
@app.route("/inserir")
def inserir():
    file = request.files['file']
    other_data = request.form.to_dict()
    id_objeto = ObjectId()
    if file:
        filename = file.filename
        file_data = Binary(file.read())
        # Insere o arquivo no MongoDB
        document = {'_id':id_objeto, 'filename': filename, 'file_data': file_data}
        # Adiciona outros dados ao documento
        document.update(other_data)
        collection.insert_one(document)
        return jsonify({'message': 'Arquivo e dados guardados'})
    else:
        return jsonify({'message': 'Arquivo não encontrado'}), 404

@app.route("/listar/<pagina>")
@app.route("/listar/")
@app.route("/listar")
def listar(pagina=1):
    total_documentos = collection.count_documents({})
    page = int(pagina) if pagina else 1
    page_size = 10
    start_index = (page - 1) * page_size
    num_pages = total_documentos // page_size + (1 if total_documentos % page_size > 0 else 0)
    final_index = (start_index+10) if ((start_index+10) < total_documentos) else total_documentos
    documentos = collection.find({}).skip(start_index).limit(page_size)
    try:
        result = []
        for data in documentos:
            data['_id'] = str(data['_id'])
            if ('file_data' in data):
                del data['file_data']
            result.append(data)
        return jsonify({'index_inicial':start_index, 'index_final':final_index,'total':total_documentos,'documentos': result, 'num_pages':num_pages})
    except:
        jsonify({"error":"Não foi possível encontrar nenhum dado"})

@app.route('/quantidade_documentos')
def quantidade_documentos():
    try:
        return jsonify({"Quantidade":collection.count_documents({})})
    except:
        return 404

@app.route("/buscar/<pagina>/<query>/", methods=['GET', 'POST'])
@app.route("/buscar/<pagina>/<query>", methods=['GET', 'POST'])
@app.route("/buscar/<pagina>/", methods=['GET', 'POST'])
@app.route("/buscar/<pagina>", methods=['GET', 'POST'])
@app.route("/buscar/", methods=['GET', 'POST'])
@app.route("/buscar", methods=['GET', 'POST'])
def busca(query = '', pagina = None):
    if request.method == "POST":
        all_list = [' ', '', '*']
        page = int(pagina) if pagina else 1
        page_size = 10
        start_index = (page - 1) * page_size
        if query not in all_list:
            index_config = {
                "$search": {
                    "index": "teste-search",
                    "text": {
                        "query": query,
                        "path": {
                            "wildcard": "*"
                        }
                    }
                }
            }
            results = collection.aggregate([index_config])
            formatted_results = []
            for result in results:
                result['_id'] = str(result['_id'])
                if ('file_data' in result):
                    del result['file_data']
                formatted_results.append(result)
            total_documentos = len(formatted_results)
            num_pages = total_documentos // page_size + (1 if total_documentos % page_size > 0 else 0)
            final_index = (start_index+10) if ((start_index+10) < total_documentos) else total_documentos
            return jsonify({'index_inicial':start_index, 'index_final':final_index,'total':total_documentos,'documentos': formatted_results, 'num_pages':num_pages})
>>>>>>> 1fa22a6a8a8de5f5dec049559b2b42055c4d4189

        elif query in all_list:
            total_documentos = collection.count_documents({})
            num_pages = total_documentos // page_size + (1 if total_documentos % page_size > 0 else 0)
            final_index = (start_index+10) if ((start_index+10) < total_documentos) else total_documentos
            documentos = collection.find({}).skip(start_index).limit(page_size)
            try:
                result = []
                for data in documentos:
                    data['_id'] = str(data['_id'])
                    if ('file_data' in data):
                        del data['file_data']
                    result.append(data)
                return jsonify({'index_inicial':start_index, 'index_final':final_index,'total':total_documentos,'documentos': result, 'num_pages':num_pages})
            except:
                jsonify({"error":"Não foi possível encontrar nenhum dado"}), 404
        else:
            return jsonify({"error": "Formulário Inválido"}), 400
    else:
        return jsonify({"error": "Método não permitido"}), 405

@app.route("/baixar", methods=["GET", "POST"])
def baixar():
    id_objeto = request.form.get("_id")
    file_data = collection.find_one({"_id": ObjectId(id_objeto)})
    if file_data:
        # Obter os dados binários
        binary_data = file_data.get('file_data')
        nome = file_data.get('filename')
        # Criar um novo arquivo PDF
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_pdf_file:
            temp_pdf_path = temp_pdf_file.name
            temp_pdf_file.write(binary_data)

        # Enviar o PDF como resposta
        return send_file(temp_pdf_path, as_attachment=True)
    else:
        return "Arquivo não encontrado", 404
        
if __name__ == '__main__':
    app.run(debug=True)
