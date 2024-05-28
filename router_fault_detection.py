from flask import request
from repository_fault_detection import FaultDetection

def router(app):
    @app.route('/fault-detection', methods=['GET'])
    def get_fault_detection():
        return FaultDetection.get(request.args)