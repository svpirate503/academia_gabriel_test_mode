import torch
from transformers import pipeline
import matplotlib.pyplot as plt

# Lista de textos bíblicos a analizar
biblical_texts = [
    "Porque de tal manera amó Dios al mundo, que ha dado a su Hijo unigénito, para que todo aquel que en él cree, no se pierda, mas tenga vida eterna. - Juan 3:16",
    "Yo soy el camino, y la verdad, y la vida; nadie viene al Padre sino por mí. - Juan 14:6",
    "Todo lo puedo en Cristo que me fortalece. - Filipenses 4:13",
    # Agrega más textos aquí
]

# Inicializar el pipeline de análisis de sentimiento
sentiment_analysis = pipeline("sentiment-analysis")

# Función para evaluar los textos bíblicos
def evaluate_texts(texts):
    evaluations = []
    for text in texts:
        result = sentiment_analysis(text)
        score = result[0]['score']
        evaluations.append((text, score))
    return evaluations

# Evaluar los textos
evaluated_texts = evaluate_texts(biblical_texts)

# Ordenar los textos por la puntuación
evaluated_texts.sort(key=lambda x: x[1], reverse=True)

# Separar los textos y sus puntuaciones
texts, scores = zip(*evaluated_texts)

# Crear el gráfico
plt.figure(figsize=(10, 5))
bars = plt.barh(texts, scores, color='green')

# Etiquetar las barras
for bar in bars:
    plt.text(bar.get_width(), bar.get_y() + bar.get_height()/2, f'{bar.get_width():.2f}', ha='left', va='center')

plt.xlabel('Puntuación de Adecuación')
plt.title('Evaluación de Textos Bíblicos para Evangelización')
plt.gca().invert_yaxis()  # Invertir el eje Y para que el texto con la puntuación más alta esté arriba
plt.show()

