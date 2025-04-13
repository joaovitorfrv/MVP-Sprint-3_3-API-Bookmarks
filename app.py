from flask_openapi3 import OpenAPI, Info
from flask_cors import CORS
from routes import init_routes
from model import Base, engine

# Configuração básica do app
info = Info(title='Microsserviço de Bookmark', version='1.0.0')
app = OpenAPI(__name__, info=info)
CORS(app)

app.config['FLASK_APP'] = 'app.py'  # Adicione esta linha

# Cria tabelas
Base.metadata.create_all(bind=engine)

# Inicializa todas as rotas
init_routes(app)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)