
from flask import Flask, render_template, json, request, url_for
from flask_cors import CORS
from align_tool import AlignTool
from align_tool_bbc import AlignToolObjects
from flask import make_response
from functools import wraps, update_wrapper
from datetime import datetime
from UTIL.storage_mongo import StorageMongo
from UTIL import utils
import os
import shutil
import json


app = Flask(__name__)
CORS(app)


@app.route("/")
def main():
    return render_template('index_alinhamento_noticias_avaliacao.html')

@app.route("/objetos")
def main_objects():
    return render_template('index_alinhamento_noticias_avaliacao_objetos.html')


@app.route("/baseline")
def main_baseline():
    return render_template('index_alinhamento_noticias_avaliacao_baseline.html')


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.route('/avaliacao', methods=['POST'])
def salvar_avaliacao():

    _link = request.form['link']

    _avaliacao = json.loads(request.form['avaliacao'])
    _medida_similaridade = request.form['medida_similaridade']


    storage = StorageMongo()
   
    dic_avaliacao = dict(link=_link, avaliacao=_avaliacao)
   
    id = None
    #       Similaridade WUP
    if _medida_similaridade == "wup":
        id = storage.insert_one(dic_avaliacao, "avaliacoes_wup")
        
    #     Similaridade Word Embeddings
    elif _medida_similaridade == "we":
       id =storage.insert_one(dic_avaliacao, "avaliacoes_we")

   

    print(id)
    return '',200


@app.route('/alinhamento', methods=['POST'])
def alinhar():
    
    _link = request.form['link']

    _experimento_pessoa = int(request.form['pessoas']) + 1
    _experimento_objeto = int(request.form['objetos']) + 1

    alinhador = AlignTool()
    try:
        result_pessoas, result_objetos, img_url, titulo, legenda, texto, dic_avaliacao = alinhador.align_from_url(
            _link, _experimento_pessoa, _experimento_objeto)

        if img_url != '':
            shutil.copy2('static/alinhamento2.jpg', img_url)

        response = dict(result_pessoas=result_pessoas,
                        result_objetos=result_objetos,
                        img_alinhamento=img_url,
                        texto=texto,
                        legenda=legenda,
                        titulo=titulo,
                        dic_avaliacao=dic_avaliacao)
        print(response)
        return json.dumps(response)
    except Exception:
        return json.dumps({})


@app.route('/alinhamento_objetos', methods=['POST'])
def alinhar_objetos():
    
    _link = request.form['link']

    _experimento_pessoa = int(request.form['pessoas']) + 1
    _experimento_objeto = int(request.form['objetos']) + 1

    alinhador = AlignToolObjects()
    try:
        result_pessoas, result_objetos, img_url, titulo, legenda, texto, dic_avaliacao = alinhador.align_from_url(
            _link, _experimento_pessoa, _experimento_objeto)

        if img_url != '':
            shutil.copy2('static/alinhamento2.jpg', img_url)

        response = dict(result_pessoas=result_pessoas,
                        result_objetos=result_objetos,
                        img_alinhamento=img_url,
                        texto=texto,
                        legenda=legenda,
                        titulo=titulo,
                        dic_avaliacao=dic_avaliacao)
        # print(response)
        return json.dumps(response)
    except Exception:
        return json.dumps({})

    


@app.route('/upload', methods=['POST'])
def alinhamento_livre():
    file = request.files['choosed_file']
    file.save('urls.txt')
    urls = utils.file_to_List('urls.txt')
    print(urls)
    _urls = dict(urls=urls)
  
    return json.dumps(_urls)
    #return json.dumps({'html': "oi"})


if __name__ == "__main__":
    app.debug = True
    app.run(host='127.0.0.1',port=9444)
    #host='0.0.0.0'
