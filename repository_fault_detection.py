from sqlalchemy import Column, Float, Integer, DateTime, func
from sqlalchemy.sql import and_
from flask import jsonify
import tools
import db
import math

class FaultDetection(db.Base):
    __tablename__ = 'previsao'

    id_previsao = Column(Integer, primary_key=True, autoincrement=True)
    id_log_motor = Column(Integer)
    previsao_registrada = Column(Float)
    offset_tolerancia = Column(Float)
    timestamp = Column(DateTime, server_default=func.now())

    def builder(self):
        return {
            'id_previsao': self.id_previsao,
            'previsao_registrada': self.previsao_registrada,
            'offset_tolerancia': self.offset_tolerancia,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def insert(counter, fault_counter):
        session = db.Session()

        fault_detection = 0

        if counter == fault_counter:
            fault_detection = 1

        register = FaultDetection(
            previsao_registrada=fault_detection, 
            offset_tolerancia=24.35
        )

        session.add(register)
        session.commit()
        session.close()

    def get(params):
        session = db.Session()
        data = session.query(FaultDetection)

        params = tools.objectFormatter(params)

        filters = []  

        for key in params.get('filters') or {}:
            if hasattr(FaultDetection, key):
                attr = getattr(FaultDetection, key)
                filters.append(attr == params['filters'][key])
            else:
                print(f"Atributo {key} não encontrado na classe FaultDetection")

        if len(filters):
            data = data.filter(and_(*filters))

        total_query = data.statement.with_only_columns(func.count()).order_by(None)
        total_records = session.execute(total_query).scalar()

        data = data.order_by(FaultDetection.timestamp.desc())
        data = data.limit(int(params.get('limit') or 10))
        data = data.offset(int(params.get('limit') or 10) * int(params.get('offset') or 0))
        data = data.all()

        serialized_data = [row.builder() for row in data]
        session.close()

        response = jsonify({
            'content': serialized_data,
            'total': total_records,
            'totalPage': math.ceil(total_records / int(params.get('limit') or 10))
        })

        return response
    
    def create(body):
        session = db.Session()
        
        faultDetection = FaultDetection(
            id_log_motor=body.get("id_log_motor"),
            previsao_registrada=body.get("previsao"), 
            offset_tolerancia=body.get("offset_tolerancia", 0)
        )

        session.add(faultDetection)
        session.commit()
        session.close()
        
        return jsonify({"mensagem": "Previsão registrada com sucesso!"}), 200