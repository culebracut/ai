import os
import azure.cognitiveservices.speech as speechsdk

SPEECH_KEY = os.environ.get('SPEECH_KEY')
ENDPOINT = os.environ.get('ENDPOINT')

audio_file_path = '/data/audio/James_Joyce_reads_from_Anna_Livia.wav'  # Replace with your audio file path

use_microphone = False  # Set to True if you want to use the microphone, False for file input

def recognize_from_microphone():
     # This example requires environment variables named "SPEECH_KEY" and "ENDPOINT"
     # Replace with your own subscription key and endpoint, the endpoint is like : "https://YourServiceRegion.api.cognitive.microsoft.com"
    speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, endpoint=ENDPOINT)
    speech_config.speech_recognition_language="en-US"

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("Speak into your microphone.")
    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(speech_recognition_result.text))
    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and endpoint values?")

def recognize_from_file(file_path):
    speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, endpoint=ENDPOINT)
    audio_config = speechsdk.audio.AudioConfig(filename=file_path)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("Recognizing from file: {}".format(file_path))
    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(speech_recognition_result.text))
    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized.")
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))


if use_microphone:
    recognize_from_microphone()
else:
    recognize_from_file(audio_file_path)  # Replace with your audio file path