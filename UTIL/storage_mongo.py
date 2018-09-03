"""Bloco de Persistência"""

from pymongo import MongoClient, ReturnDocument
from bson import BSON, decode_all


class StorageMongo():
    """Persistencia baseada em MongoDB.

    Args:
        host (str): endereco do host. Default `'localhost'`.
        port (int): porta do host. Default `27017`.
        name (str): nome do banco de dados.
        collection (str): nome da collection.
        models (dict): Relacao entre nome de colecao e modelo.
    """

    def __init__(self,
                 host='localhost',
                 port=27017,
                 name='text_image_align_db',
                 collection='gryfo_col',
                 models=None):
        

        client = MongoClient(host, port)

        self.db = client[name]
        self.collection = collection

        if models is None:
            models = {}
        self.models = models

        # for collection in self.models:
            # self.db[collection].create_index(GRYFO_ID)

  

    def add(self, obj, collection=None):
        """Adiciona um objeto a uma colecao.

        Args:
            obj (models.Model): Objeto.
            collection (str): Nome da colecao.

        Returns:
            models.Model: Objeto adicionado.
        """
        if collection is None:
            collection = self.collection

       
        mongo_id = self.insert_one(obj, collection=collection)
        obj.mongo_id = mongo_id

        return obj

    def update(self, obj_id, patch, collection=None):
        """Atualiza um objeto de uma colecao.

        Args:
            obj_id (str): ID do objeto.
            patch (dict): Novos valores indexados por nome.
            collection (str): Nome da colecao.

        Returns:
            models.Model: Objeto atualizado.
        """
        if collection is None:
            collection = self.collection

        if '_id' in patch:
            del patch['_id']

        obj = self.db[collection].find_one_and_update(
            filter={GRYFO_ID: obj_id},
            update={'$set': patch},
            return_document=ReturnDocument.AFTER)

        return obj

    def delete(self, obj_id, collection=None):
        """Remove um objeto de uma colecao.

        Args:
            obj_id (str): ID do objeto.
            collection (str): Nome da colecao.

        Returns:
            models.Model: Objeto removido.
        """
        obj = self.get(obj_id, collection=collection)

        self.delete_one({GRYFO_ID: obj_id}, collection=collection)

        return obj

   

    def insert_one(self, document, collection=None):
        """Insere um documento no banco.

        Args:
            document(dict): dicionario com os campos do documento.
            collection(str)[opcional]: nome da collection onde vai operar.

        Returns:
            bson.ObjectId: ID do documento adicionado.
        """
        if collection is None:
            collection = self.collection

        result = self.db[collection].insert_one(document)

        return result.inserted_id

    def dump(self, save_path='teste.bson', collection=None):
        """Salva o dump de uma collection em um local especifico

        Args:
            save_path(str): Local especifico que o usuario deseja salvar
            collection(str)[opcional]: nome da collection onde vai operar.
        """
        if collection is None:
            collection = self.collection

        with open(save_path, 'wb+') as f:
            for doc in self.find(collection=collection):
                f.write(BSON.encode(doc))

    def restore(self, path_src='teste.bson', collection=None):
        """Restaura o dump de uma collection em um local especifico

        Args:
            path_src(str): Local especifico que esta o arquivo dump.
            collection(str)[opcional]: nome da collection onde vai operar.
        """
        if collection is None:
            collection = self.collection

        with open(path_src, 'rb') as f:
            documents = decode_all(f.read())
            for document in documents:
                self.insert_one(collection=collection,
                                document=document)

    def insert_many(self, documents, collection=None):
        """Insere varios documentos no banco.

        Args:
            documents(list): lista de dicionarios.
            collection(str)[opcional]: nome da collection onde vai operar.

        Returns:
            list: IDs dos documentos adicionado.
        """
        if collection is None:
            collection = self.collection

        result = self.db[collection].insert_many(documents)

        return result.inserted_ids

    def find(self, query=None, projection=None, collection=None):
        """Busca documentos no banco.

        Args:
            query(dict): parametros de busca.
            collection(str)[opcional]: nome da collection onde vai operar.
        Returns:
            Cursor de resultados.
        """
        if collection is None:
            collection = self.collection
        return self.db[collection].find(query, projection)

    def find_one(self, query=None, projection=None, collection=None):
        """Busca um unico documento no banco.

        Args:
            query(dict): parametros de busca.
            collection(str)[opcional]: nome da collection onde vai operar.
        Returns:
            Cursor de resultados
        """
        if collection is None:
            collection = self.collection
        return self.db[collection].find_one(query, projection)

    def update_one(self, query, update, collection=None, upsert=False):
        """Atualiza um unico documento no banco.

        Args:
            query(dict): Parametros de busca.
            update(dict): Modificacoes a aplicar.
            collection(str)[opcional]: Nome da collection onde vai operar.
            upsert(boolean)[opcional]: Caso nao ache uma entrada, fazer um insert.

        Returns:
            pymongo.UpdateResult
        """
        if collection is None:
            collection = self.collection
        return self.db[collection].update_one(query, {'$set': update}, upsert)

    def update_many(self, query, update, collection=None, upsert=False):
        """Atualiza varios documentos no banco.

        Args:
            query(dict): Parametros de busca.
            update(dict): Modificacoes a aplicar.
            collection(str)[opcional]: Nome da collection onde vai operar.
            upsert(boolean)[opcional]: Caso nao ache uma entrada, fazer um insert.
        Returns:
            pymongo.UpdateResult
        """
        if collection is None:
            collection = self.collection
        return self.db[collection].update_many(query, update, upsert)

    def delete_one(self, query, collection=None):
        """Apaga um unico documento do banco.

        Args:
            query(dict): Parametros de busca.
            collection(str)[opcional]: Nome da collection onde vai operar.
        Returns:
            pymongo.DeleteResult
        """
        if collection is None:
            collection = self.collection
        return self.db[collection].delete_one(query)

    def delete_many(self, query=None, collection=None):
        """Apaga varios documentos do banco

        Args:
            query(dict): Parametros de busca.
            collection(str)[opcional]: Nome da collection onde vai operar.
        Returns:
            pymongo.DeleteResult
        """
        if collection is None:
            collection = self.collection
        if query is None:
            # Apaga todos documentos na collection
            return self.db[collection].delete_many({})
        return self.db[collection].delete_many(query)

    def aggregate(self, pipeline, collection=None, **kwargs):
        """Agrega valores do banco de dados.

        Args:
            pipeline(list): Lista de parametros para agregacao.
            collection(str)[opcional]: Nome da collection onde vai operar.
        Returns:
            Cursor de resultados
        """
        if collection is None:
            collection = self.collection
        return self.db[collection].aggregate(pipeline, **kwargs)

    def clear_db(self, collection=None):
        """Apaga a collection do banco de dados.

        Args:
            collection(str)[opcional]: Nome da collection que vai ser dropada.
        """
        if collection is None:
            collection = self.collection
        return self.db.drop_collection(collection)
