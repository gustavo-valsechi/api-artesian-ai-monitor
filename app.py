from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from waitress import serve

import router_auth
import router_fault_detection
import router_log_motor
import router_motor
import router_flow

if __name__ == '__main__':
    app = Flask(__name__)

    app.config['JWT_SECRET_KEY'] = 'artesian-ai-monitor'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 43200

    jwt = JWTManager(app)

    CORS(
        app, 
        origins="*", 
        supports_credentials=True,
    )

    router_auth.router(app, jwt)
    router_fault_detection.router(app, jwt)
    router_log_motor.router(app, jwt)
    router_motor.router(app, jwt)
    router_flow.router(app, jwt)

    # app.run(debug=True)
    serve(app, host='0.0.0.0', port=5000)