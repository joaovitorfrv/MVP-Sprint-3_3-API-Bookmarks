from flask_openapi3 import Tag
from flask import redirect

home_tag = Tag(name="Documentação", description="Seleciona de documentação: Swagger, Redoc ou RapiDoc")

def init_home_routes(app):
    @app.get('/', tags=[home_tag])
    def home():
        return redirect('/openapi')