from flask_openapi3 import Tag
from flask import jsonify
from schemas import *
from services.bookmark_service import *

# Configuração do Swagger Tag
bookmark_tag = Tag(
    name="Bookmarks",
    description="Operações com Bookmarks - Adição, visualização, atualização e remoção de links úteis"
)

def init_bookmark_routes(app):
    @app.post('/api/bookmarks',
              tags=[bookmark_tag],
              responses={
                  "201": BookmarkViewSchema,
                  "400": ErrorSchema
              })
    def add_bookmark(body: BookmarkPostSchema):
        """
        POST: Adicionar um novo Bookmark à base de dados
        """
        response, status_code = add_bookmark_service(body.model_dump())
        return jsonify(response), status_code

    @app.get('/api/bookmarks',
             tags=[bookmark_tag],
             responses={
                 "200": BookmarksListSchema,
                 "400": ErrorSchema
             })
    def get_bookmarks():
        """
        GET: Retornar todos os bookmarks cadastrados
        """
        response, status_code = get_bookmarks_service()
        return jsonify(response), status_code

    @app.get('/api/bookmark',
             tags=[bookmark_tag],
             responses={
                 "200": BookmarkViewSchema,
                 "404": ErrorSchema,
                 "400": ErrorSchema
             })
    def get_bookmark(query: BookmarkSearchForIdSchema):
        """
        GET: Buscar um bookmark específico pelo ID
        """
        response, status_code = get_bookmark_service(query.id)
        return jsonify(response), status_code

    @app.put('/api/bookmark',
             tags=[bookmark_tag],
             responses={
                 "200": BookmarkViewSchema,
                 "404": ErrorSchema,
                 "400": ErrorSchema
             })
    def update_bookmark(query: BookmarkSearchForIdSchema, body: BookmarkPostSchema):
        """
        PUT: Atualizar um bookmark existente
        """
        data = body.model_dump()
        data['id'] = query.id
        response, status_code = update_bookmark_service(query.id, data)
        return jsonify(response), status_code

    @app.delete('/api/bookmark',
                tags=[bookmark_tag],
                responses={
                    "200": BookmarkDelSchema,
                    "404": ErrorSchema,
                    "400": ErrorSchema
                })
    def delete_bookmark(query: BookmarkSearchForIdSchema):
        """
        DELETE: Remover um bookmark da base de dados
        """
        response, status_code = delete_bookmark_service(query.id)
        return jsonify(response), status_code