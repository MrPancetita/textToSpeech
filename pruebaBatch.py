import uuid
import requests
import json

synthesis_id = uuid.uuid4()
print(f"Synthesis ID: {synthesis_id}")

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

subscription_key = config.get("SubscriptionKey")

# Leer el contenido de noticia.txt
with open('noticia.txt', 'r', encoding='utf-8') as noticia_file:
    noticia_content = noticia_file.read()

url = f"https://eastus2.api.cognitive.microsoft.com/texttospeech/batchsyntheses/{synthesis_id}?api-version=2024-04-01"
headers = {
    "Ocp-Apim-Subscription-Key": f"{subscription_key}",
    "Content-Type": "application/json"
}
data = {
    "description": "My first ssml test",
    "inputKind": "SSML",
    "inputs": [
        {
            "content": f"<speak version=\"1.0\" xml:lang=\"en-US\"><voice name=\"es-ES-TristanMultilingualNeural\">{noticia_content}</voice></speak>"
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

response = requests.put(url, headers=headers, data=json.dumps(data))

if response.status_code == 200 or response.status_code == 201:
    print("Synthesis created successfully!")
    print(f"Recupéralo aquí:\ncurl -v -X GET \"https://eastus2.api.cognitive.microsoft.com/texttospeech/batchsyntheses/{synthesis_id}?api-version=2024-04-01\" -H \"Ocp-Apim-Subscription-Key: {subscription_key}\"")
else:
    print(f"Failed to create synthesis. Status code: {response.status_code}")
