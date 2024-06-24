from flask import request
from flask_jwt_extended import jwt_required
from repository_anomaly_detection import AnomalyDetection

def router(app, jwt):
    @app.route('/anomaly-detection', methods=['GET'])
    @jwt_required()
    def get_anomaly_detection():
        return AnomalyDetection.get(request.args)