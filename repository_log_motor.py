from sqlalchemy import Column, Float, Integer, DateTime, func, Boolean
from sqlalchemy.exc import IntegrityError
from flask import jsonify
from repository_motor import Motor
from IA import anomaly_detection
import db
import asyncio
    
class LogMotor(db.Base):
    __tablename__ = 'log_motor'

    id_log_motor = Column(Integer, primary_key=True, autoincrement=True)
    id_motor = Column(Integer)
    status = Column(Boolean)
    frequencia = Column(Float)
    corrente = Column(Float)
    tensao_entrada = Column(Float)
    timestamp = Column(DateTime, server_default=func.now())

    def builder(self):
        return {
            'id_log_motor': self.id_log_motor,
            'id_motor': self.id_motor,
            'status': self.status,
            'frequencia': self.frequencia,
            'corrente': self.corrente,
            'tensao_entrada': self.tensao_entrada,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }

    def get():
        session = db.Session()

        data = session.query(LogMotor).order_by(LogMotor.timestamp.desc()).limit(10).all()
        serialized_data = [row.builder() for row in data]
        session.close()

        response = jsonify({'content': serialized_data})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    
    def getAll():
        session = db.Session()

        data = session.query(LogMotor).all()
        serialized_data = [row.builder() for row in data]
        session.close()

        return jsonify(serialized_data)
    
    async def create(body):
        session = db.Session()

        id_motor = body.get("id_motor")

        motor = session.query(Motor).filter_by(id_motor=id_motor).first()

        if not motor:
            await Motor.create({
                "id_motor": id_motor,
                "tag": f"P0{id_motor}-BA01",
                "descricao": f"Motor {id_motor}",
                "frequencia": 60,
                "corrente": 9.3,
                "tensao": 380,
                "potencia": 3.7,
            })

        log_motor = LogMotor(
            id_motor=id_motor,
            status=body.get("status"),
            frequencia=body.get("frequencia"),
            corrente=body.get("corrente"),
            tensao_entrada=body.get("tensao"),
        )

        session.add(log_motor)
        await session.commit()
        await session.close()

        anomaly_detection()

        return jsonify({"mensagem": "Log do motor registrado com sucesso!"}), 200