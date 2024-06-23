import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from db import engine
import joblib

def dataset():
    """
    Carrega os dados do banco de dados PostgreSQL usando uma consulta SQL.
    """
    query = "SELECT * FROM log_motor lm;"

    with engine.connect() as connection:
        data = pd.read_sql_query(query, connection)
    return data

def pre_processing_data(data):
    """
    Normaliza os dados e separa as características (features) do alvo (target).
    """
    # Remover colunas que não serão usadas no treinamento
    features = data.drop(columns=['timestamp', 'id_log_motor'])

    # Normalizar os dados
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)

    return features_scaled, scaler

def train(features_scaled, contamination, n_estimators, max_samples, max_features, bootstrap):
    """
    Treina o modelo Isolation Forest nos dados fornecidos.
    """
    model = IsolationForest(
        contamination=contamination,
        n_estimators=n_estimators,
        max_samples=max_samples,
        max_features=max_features,
        bootstrap=bootstrap,
        random_state=42
    )
    model.fit(features_scaled)
    return model

def main():
    model_path = './isolation_forest_model.pkl'
    scaler_path = './scaler.pkl'

    # Carregar os dados
    data = dataset()

    # Pré-processar os dados
    features_scaled, scaler = pre_processing_data(data)

    # Treinar o modelo com parâmetros ajustáveis
    model = train(features_scaled, contamination=0.1, n_estimators=200, max_samples=256, max_features=1.0, bootstrap=False)

    # Salvar o modelo treinado e o scaler
    joblib.dump(model, model_path)
    joblib.dump(scaler, scaler_path)
    
if __name__ == '__main__':
    main()
