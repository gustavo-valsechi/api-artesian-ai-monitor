from repository_motor import Motor
from flask import request, jsonify
import tools

def router(app):
    @app.route('/motor', methods=['GET'])
    def get_motor():
        return Motor.get()
    
    @app.route('/motor', methods=['POST'])
    def save_motor():
        return Motor.save(tools.requestFormatter(request)["body"])
    
    @app.route('/motor/<int:id_motor>', methods=['DELETE', 'OPTIONS'])
    def delete_motor(id_motor):
        if request.method == 'OPTIONS':
            response = jsonify({"mensagem": "Permitido"})
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
            response.headers.add('Access-Control-Allow-Methods', 'DELETE')
            return response
        elif request.method == 'DELETE':
            return Motor.delete(id_motor)