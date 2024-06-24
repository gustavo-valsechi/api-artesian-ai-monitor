from flask import request
from flask_jwt_extended import jwt_required
from repository_anomaly_detection import AnomalyDetection
import tools

def router(app, jwt):
    @app.route('/anomaly-detection', methods=['GET'])
    @jwt_required()
    def get_anomaly_detection():
        return AnomalyDetection.get(request.args)
    
    @app.route('/anomaly-detection', methods=['POST'])
    def create_anomaly_detection():
        return AnomalyDetection.create(tools.requestFormatter(request)["body"])