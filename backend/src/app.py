import os
from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
from database import db
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
from flask_jwt_extended import JWTManager


load_dotenv()


def create_app(database_uri=None):
    app = Flask(__name__)
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri or \
        'postgresql://tppe:escondidinho@db/db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

    jwt = JWTManager(app)

    db.init_app(app)
    Migrate(app, db)

    from routes.grupos import grupos_bp
    from routes.pessoas import pessoas_bp
    from routes.despesas import despesas_bp
    from routes.usuarios import usuarios_bp
    from routes.auth import auth_bp
    from routes.stats import stats_bp
    app.register_blueprint(grupos_bp, url_prefix='/grupos')
    app.register_blueprint(pessoas_bp)
    app.register_blueprint(despesas_bp)
    app.register_blueprint(usuarios_bp, url_prefix='/usuarios')
    app.register_blueprint(auth_bp)
    app.register_blueprint(stats_bp)

    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.yaml'
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={'app_name': "Despesas entre Amigos API"}
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000)
