from sqlalchemy import Column, Float, Integer, DateTime, func, String
from flask import jsonify
import db
    
class Motor(db.Base):
    __tablename__ = 'motor'

    id_motor = Column(Integer, primary_key=True, autoincrement=True)
    tag = Column(String)
    descricao = Column(String)
    frequencia = Column(Float)
    corrente = Column(Float)
    tensao = Column(Float)
    potencia = Column(Float)
    timestamp = Column(DateTime, server_default=func.now())

    def builder(self):
        return {
            'id_motor': self.id_motor,
            'tag': self.tag,
            'descricao': self.descricao,
            'frequencia': self.frequencia,
            'corrente': self.corrente,
            'tensao': self.tensao,
            'potencia': self.potencia,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }

    def get():
        session = db.Session()

        data = session.query(Motor).order_by(Motor.timestamp.desc()).limit(10).all()
        serialized_data = [row.builder() for row in data]
        session.close()

        response = jsonify({'content': serialized_data})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    
    def save(body):
        session = db.Session()
        id_motor = body.get("id_motor")

        if id_motor:
            motor = session.query(Motor).filter_by(id_motor=id_motor).first()

            if not motor:
                session.close()
                return jsonify({"mensagem": "Motor não encontrado"}), 404
        else:
            motor = Motor()

        motor.id_motor = body.get("id_motor", motor.id_motor)
        motor.tag = body.get("tag", motor.tag)
        motor.descricao = body.get("descricao", motor.descricao)
        motor.frequencia = body.get("frequencia", motor.frequencia)
        motor.corrente = body.get("corrente", motor.corrente)
        motor.tensao = body.get("tensao", motor.tensao)
        motor.potencia = body.get("potencia", motor.potencia)

        session.add(motor)
        session.commit()
        session.close()
        
        return jsonify({"mensagem": "Motor atualizado com sucesso"}), 200
    
    def create(body):
        session = db.Session()
        id_motor = body.get("id_motor")

        if id_motor:
            motor = session.query(Motor).filter_by(id_motor=id_motor).first()

            if motor:
                session.close()
                return jsonify({"mensagem": "Motor já existe"}), 200

        motor = Motor(
            id_motor=id_motor,
            tag=body.get("tag"),
            descricao=body.get("descricao"), 
            frequencia=body.get("frequencia"),
            corrente=body.get("corrente"),
            tensao=body.get("tensao"),
            potencia=body.get("potencia"),
        )

        session.add(motor)
        session.commit()
        session.close()
        
        return jsonify({"mensagem": "Motor atualizado com sucesso"}), 200
    
    def delete(id_motor):
        session = db.Session()

        motor = session.query(Motor).filter_by(id_motor=id_motor).first()

        if not motor:
            session.close()
            return jsonify({"mensagem": "Motor não encontrado"}), 404

        session.delete(motor)

        session.commit()
        session.close()

        return jsonify({"mensagem": "Motor removido com sucesso"}), 200