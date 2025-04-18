import uuid
import requests
import json
import re

# Este es el que hay que usar para, a partir del texto de texto_input.txt generar el archivo de audio por batch synthesis

synthesis_id = uuid.uuid4()
print(f"Synthesis ID: {synthesis_id}")

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

subscription_key = config.get("SubscriptionKey")

# Leer el contenido de texto_input.txt
with open('texto_input.txt', 'r', encoding='utf-8') as texto_input_file:
    texto_input_content = texto_input_file.read()

# Limpiar el texto para SSML
def clean_text_for_ssml(text):
    # Eliminar caracteres no válidos como espacios extra o caracteres especiales
    text = re.sub(r'[^\w\s.,;!?-]', '', text)  # Permitir solo caracteres alfanuméricos y puntuación básica
    text = re.sub(r'\s+', ' ', text).strip()   # Reemplazar múltiples espacios por uno solo
    return text

texto_input_content = clean_text_for_ssml(texto_input_content)

url = f"https://eastus2.api.cognitive.microsoft.com/texttospeech/batchsyntheses/{synthesis_id}?api-version=2024-04-01"
headers = {
    "Ocp-Apim-Subscription-Key": f"{subscription_key}",
    "Content-Type": "application/json"
}
data = {
    "description": "My first ssml conversor",
    "inputKind": "SSML",
    "inputs": [
        {
            "content": f"<speak version=\"1.0\" xml:lang=\"es-ES\"><voice name=\"es-ES-ArabellaMultilingualNeural\">{texto_input_content}</voice></speak>"
        }
    ],
    "properties": {
        "outputFormat": "riff-24khz-16bit-mono-pcm",
        "wordBoundaryEnabled": False,
        "sentenceBoundaryEnabled": False,
        "concatenateResult": False,
        "decompressOutputFiles": False
    }
}

response = requests.put(url, headers=headers, json=data)

if response.status_code == 200 or response.status_code == 201:
    print("Synthesis created successfully!")
    print(f"Recupéralo aquí:\ncurl -v -X GET \"https://eastus2.api.cognitive.microsoft.com/texttospeech/batchsyntheses/{synthesis_id}?api-version=2024-04-01\" -H \"Ocp-Apim-Subscription-Key: {subscription_key}\"")
else:
    print(f"Failed to create synthesis. Status code: {response.status_code}")
    print("Response content:")
    try:
        print(response.json())
    except:
        print(response.text)
