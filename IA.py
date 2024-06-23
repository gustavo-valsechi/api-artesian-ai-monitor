import pandas as pd
import joblib
from sqlalchemy import text
from db import engine

def dataset():
    """
    Carrega os dados do banco de dados PostgreSQL usando uma consulta SQL.
    """
    query = "SELECT * FROM log_motor lm WHERE NOT EXISTS (SELECT 1 FROM previsao p WHERE p.id_log_motor = lm.id_log_motor);"

    with engine.connect() as connection:
        data = pd.read_sql_query(query, connection)
    return data

def pre_processing_data(data, scaler, feature_columns):
    """
    Normaliza os dados usando o scaler fornecido.
    """
    # Selecionar apenas as colunas necessárias para previsão
    features = data[feature_columns]

    # Normalizar os dados com o scaler fornecido
    features_scaled = scaler.transform(features)

    return features_scaled

def predicts(model, features_scaled):
    """
    Faz previsões de anomalias com o modelo treinado.
    """
    predicoes = model.predict(features_scaled)
    # Converter -1 para 1 (anomalia) e 1 para 0 (normal)
    predicoes = [1 if p == -1 else 0 for p in predicoes]
    return predicoes

def response(engine, data, predicoes):
    """
    Insere os resultados de volta na tabela do banco de dados.
    """
    with engine.begin() as connection:
        for i, pred in enumerate(predicoes):
            result = connection.execute(text("""
                INSERT INTO previsao (id_log_motor, previsao_registrada)
                VALUES (:id_log_motor, :previsao);
            """), {
                'previsao': int(pred), 
                'id_log_motor': int(data['id_log_motor'].iloc[i])
                }
            )

            # Log para verificar se a atualização foi realizada
            print(f"Atualização {i + 1}/{len(predicoes)}: Linhas afetadas = {result.rowcount}")

# cria um arquivo CSV para com os dados e as previsões de anomalias (PODE REMOVER DEPOIS)
def salvar_resultados(data, predicoes, output_path):
    """
    Salva os dados com as previsões de anomalias em um arquivo CSV.
    """
    # Adicionar a coluna de anomalias aos dados originais
    data['anomalia'] = predicoes
    data.to_csv(output_path, index=False, encoding='utf-8', sep=',')

def anomaly_detection():
    # Carregar os dados do banco de dados
    data = dataset()

    # Carregar o modelo treinado e o scaler
    model = joblib.load('./isolation_forest_model.pkl')
    scaler = joblib.load('./scaler.pkl')

    # Definir os nomes das colunas usadas para o treinamento do modelo
    feature_columns = ['id_motor', 'status', 'frequencia', 'corrente', 'tensao_entrada']

    # Pré-processar os dados
    features_scaled = pre_processing_data(data, scaler, feature_columns)

    # Fazer previsões de anomalias
    predicoes = predicts(model, features_scaled)

    # Inserir os resultados de volta na tabela do banco de dados
    response(engine, data, predicoes)
