import json
import os

import azure.cognitiveservices.speech as speechsdk

def synthesize_speech_from_file(file_path, output_audio_path):
    # Set up the subscription info for the Speech Service:

    with open('config.json', 'r') as config_file:
        config = json.load(config_file)

    subscription_key = config.get("SubscriptionKey")
    region = config.get("ServiceRegion")


    # Create an instance of a speech config with specified subscription key and service region.
    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)

    # Set the voice name, refer to https://aka.ms/speech/voices/neural for full list.
    speech_config.speech_synthesis_voice_name = "es-ES-ArabellaMultilingualNeural"

    # Create a speech synthesizer using the default speaker as audio output.
    audio_config = speechsdk.audio.AudioOutputConfig(filename=output_audio_path)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    # Read the text from the file
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # Synthesize the text to speech
    result = synthesizer.speak_text_async(text).get()

    # Check result
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for text from [{}] and saved to [{}]".format(file_path, output_audio_path))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))

if __name__ == "__main__":
    input_text_file = "noticia.txt"
    output_audio_file = "noticia_audio.wav"
    synthesize_speech_from_file(input_text_file, output_audio_file)