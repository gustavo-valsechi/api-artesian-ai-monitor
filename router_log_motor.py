from repository_log_motor import LogMotor
from flask_jwt_extended import jwt_required
from flask import request, jsonify
import tools

def router(app, jwt):
    @app.route('/log-motor', methods=['GET'])
    @jwt_required()
    def get_log_motor():
        return LogMotor.get()
    
    @app.route('/log-motor', methods=['POST'])
    def create_log_motor():
        return LogMotor.create(tools.requestFormatter(request)["body"])