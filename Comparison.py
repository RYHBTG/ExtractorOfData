import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Carregar os dados
df = pd.read_csv('C:/Users/Aluno/Documents/pythonProject/DataScraping/livro-com-todas-as-informacoes.csv')


rate_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
df['Avaliacao_Numerica'] = df['Avaliação'].map(rate_map)


df['Preço'] = df['Preço'].str.replace('£', '').astype(float)


df = df.dropna(subset=['Preço', 'Avaliacao_Numerica'])


# Verificar se ainda há dados após a remoção de N/A
if df.empty:
    print("Não há dados suficientes com avaliações numéricas para treinar o modelo.")
    print("Verifique se a coluna 'Avaliação' no seu arquivo CSV contém valores como 'One', 'Two', etc., ou números.")
else:
    # Separar X e y
    X = df[['Preço']]
    y = df['Avaliacao_Numerica']

    # Dividir em treino e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Treinar modelo de regressão linear
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Fazer previsões
    y_pred = model.predict(X_test)

    # Avaliar o modelo
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"Erro quadrático médio (MSE): {mse:.2f}")
    print(f"Coeficiente de determinação (R²): {r2:.2f}")

    # Opcional: arredondar previsões e calcular taxa de acerto exata
    # Isso só faz sentido se as avaliações forem inteiras (ex: 1 a 5 estrelas)
    y_pred_round = y_pred.round().clip(1, 5).astype(int)
    acertos = (y_pred_round == y_test).sum()
    taxa_acerto = (acertos / len(y_test)) * 100
    print(f"Taxa de acerto exata após arredondar: {taxa_acerto:.0f}%")

    print(f"Coeficiente do modelo (inclinação): {model.coef_[0]:.5f}")
    print(f"Intercepto do modelo: {model.intercept_:.2f}")
