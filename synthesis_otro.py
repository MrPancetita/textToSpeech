import json
import os
import uuid
import requests

def batch_synthesize_speech(input_text_file, output_audio_file):
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)

    synthesisId = uuid.uuid4()
    print(f"Synthesis ID: {synthesisId}")   
    subscription_key = config.get("SubscriptionKey")
    region = config.get("ServiceRegion")

    # Read the text from the file
    with open(input_text_file, 'r', encoding='utf-8') as file:
        text = file.read()

    # Create the batch synthesis request
    batch_synthesis_url = f"https://{region}.api.cognitive.microsoft.com/texttospeech/batchsyntheses/{synthesisId}?api-version=2024-04-01"
    headers = {
        "Ocp-Apim-Subscription-Key": subscription_key,
        "Content-Type": "application/json"
    }
    body = {
        "input": {
            "text": text
        },
        "voice": {
            "name": "es-ES-TristanMultilingualNeural"
        },
        "audioConfig": {
            "audioFormat": "riff-16khz-16bit-mono-pcm"
        }
    }

    response = requests.post(batch_synthesis_url, headers=headers, json=body)
    if response.status_code == 202:
        print("Batch synthesis request accepted.")
        # You will need to poll the status URL provided in the response to check when the synthesis is complete
    else:
        print(f"Error: {response.status_code}")
        print(response.json())

if __name__ == "__main__":
    input_text_file = "noticia.txt"
    output_audio_file = "noticia_audio.wav"
    batch_synthesize_speech(input_text_file, output_audio_file)