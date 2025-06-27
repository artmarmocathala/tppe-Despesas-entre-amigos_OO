from flask import Flask, jsonify, request, abort
from flask_migrate import Migrate
from models import db
from datetime import datetime
from flask_swagger_ui import get_swaggerui_blueprint


def create_app(database_uri=None):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri or 'postgresql://tppe:escondidinho@db/db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    Migrate(app, db)

    from models import Grupo, Pessoa, Compra, Imovel

    # Rotas de Grupos
    @app.route('/grupos', methods=['POST'])
    def criar_grupo():
        data = request.get_json()
        
        novo_grupo = Grupo(
            nome=data['nome'],
            max_pessoas=data.get('max_pessoas')
        )
        
        db.session.add(novo_grupo)
        db.session.commit()
        
        return jsonify(novo_grupo.to_dict()), 201


    @app.route('/grupos', methods=['GET'])
    def listar_grupos():
        grupos = Grupo.query.all()
        return jsonify([grupo.to_dict() for grupo in grupos])


    @app.route('/grupos/<int:grupo_id>', methods=['PUT'])
    def atualizar_grupo(grupo_id):
        grupo = db.session.get(Grupo, grupo_id)
        if not grupo:
            abort(404)
        data = request.get_json()
        
        grupo.nome = data.get('nome', grupo.nome)
        grupo.max_pessoas = data.get('max_pessoas', grupo.max_pessoas)
        
        db.session.commit()
        
        return jsonify(grupo.to_dict())

    @app.route('/grupos/<int:grupo_id>', methods=['DELETE'])
    def deletar_grupo(grupo_id):
        grupo = db.session.get(Grupo, grupo_id)
        if not grupo:
            abort(404)
        for despesa in grupo.despesas:
            db.session.delete(despesa)
        for pessoa in grupo.pessoas:
            db.session.delete(pessoa)
        db.session.delete(grupo)
        db.session.commit()
        return jsonify({'message': 'Grupo deletado com sucesso.'}), 200


    # Rotas de Pessoas
    @app.route('/grupos/<int:grupo_id>/pessoas', methods=['POST'])
    def adicionar_pessoa(grupo_id):
        grupo = db.session.get(Grupo, grupo_id)
        if not grupo:
            abort(404)
        data = request.get_json()
        
        if grupo.max_pessoas and len(grupo.pessoas) >= grupo.max_pessoas:
            return jsonify({'error': 'Grupo já atingiu o número máximo de pessoas'}), 400
        
        nova_pessoa = Pessoa(
            nome=data['nome'],
            cpf=data['cpf'],
            grupo_id=grupo_id
        )
        
        db.session.add(nova_pessoa)
        db.session.commit()
        
        return jsonify(nova_pessoa.to_dict()), 201


    @app.route('/grupos/<int:grupo_id>/pessoas', methods=['GET'])
    def listar_pessoas(grupo_id):
        pessoas = Pessoa.query.filter_by(grupo_id=grupo_id).all()
        return jsonify([pessoa.to_dict() for pessoa in pessoas])


    @app.route('/pessoas/<int:pessoa_id>', methods=['PUT'])
    def atualizar_pessoa(pessoa_id):
        pessoa = db.session.get(Pessoa, pessoa_id)
        if not pessoa:
            abort(404)
        data = request.get_json()
        
        pessoa.nome = data.get('nome', pessoa.nome)
        pessoa.cpf = data.get('cpf', pessoa.cpf)
        
        db.session.commit()
        
        return jsonify(pessoa.to_dict())


    @app.route('/pessoas/<int:pessoa_id>', methods=['DELETE'])
    def deletar_pessoa(pessoa_id):
        pessoa = db.session.get(Pessoa, pessoa_id)
        if not pessoa:
            abort(404)
        db.session.delete(pessoa)
        db.session.commit()
        return jsonify({'message': 'Pessoa deletada com sucesso.'}), 200


    # Rotas de Despesas
    @app.route('/grupos/<int:grupo_id>/despesas/compras', methods=['POST'])
    def registrar_compra(grupo_id):
        data = request.get_json()
        data_str = data.get('data')
        data_dt = None
        if data_str:
            try:
                data_dt = datetime.fromisoformat(data_str)
            except ValueError:
                data_dt = datetime.strptime(data_str, '%Y-%m-%d')
        nova_compra = Compra(
            valor=data['valor'],
            data=data_dt,
            grupo_id=grupo_id,
            pagador_id=data['pagador_id'],
            nome_mercado=data.get('nome_mercado'),
            itens=data.get('itens')
        )
        
        db.session.add(nova_compra)
        db.session.commit()
        
        return jsonify(nova_compra.to_dict()), 201


    @app.route('/grupos/<int:grupo_id>/despesas/imoveis', methods=['POST'])
    def registrar_despesa_imovel(grupo_id):
        data = request.get_json()
        data_str = data.get('data')
        data_dt = None
        if data_str:
            try:
                data_dt = datetime.fromisoformat(data_str)
            except ValueError:
                data_dt = datetime.strptime(data_str, '%Y-%m-%d')
        nova_despesa = Imovel(
            valor=data['valor'],
            data=data_dt,
            grupo_id=grupo_id,
            pagador_id=data['pagador_id'],
            endereco=data.get('endereco')
        )
        
        db.session.add(nova_despesa)
        db.session.commit()
        
        return jsonify(nova_despesa.to_dict()), 201


    @app.route('/grupos/<int:grupo_id>/despesas', methods=['GET'])
    def listar_despesas(grupo_id):
        despesas = []
        compras = Compra.query.filter_by(grupo_id=grupo_id).all()
        imoveis = Imovel.query.filter_by(grupo_id=grupo_id).all()
        
        for despesa in compras + imoveis:
            despesas.append(despesa.to_dict())
        
        return jsonify(despesas)


    @app.route('/despesas/compras/<int:compra_id>', methods=['DELETE'])
    def deletar_compra(compra_id):
        compra = db.session.get(Compra, compra_id)
        if not compra:
            abort(404)
        db.session.delete(compra)
        db.session.commit()
        return jsonify({'message': 'Compra deletada com sucesso.'}), 200


    @app.route('/despesas/imoveis/<int:imovel_id>', methods=['DELETE'])
    def deletar_imovel(imovel_id):
        imovel = db.session.get(Imovel, imovel_id)
        if not imovel:
            abort(404)
        db.session.delete(imovel)
        db.session.commit()
        return jsonify({'message': 'Despesa de imóvel deletada com sucesso.'}), 200


    from flask_swagger_ui import get_swaggerui_blueprint
    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.yaml'
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={'app_name': "Despesas entre Amigos API"}
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)