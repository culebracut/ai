import os
import azure.cognitiveservices.speech as speechsdk

SPEECH_KEY = os.environ.get('SPEECH_KEY')
ENDPOINT = os.environ.get('ENDPOINT')

audio_file_path = '/data/audio/output.wav'  # Replace with your audio file path
save_to_file = True  # Set to True if you want to save the output to a file, False for default speaker

# This example requires environment variables named "SPEECH_KEY" and "ENDPOINT"
# Replace with your own subscription key and endpoint, the endpoint is like : "https://YourServiceRegion.api.cognitive.microsoft.com"
speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, endpoint=ENDPOINT)

if save_to_file:
    # If you want to use a file output, use filename='output.wav'
    audio_config = speechsdk.audio.AudioOutputConfig(filename=audio_file_path)
else:
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

# The neural multilingual voice can speak different languages based on the input text.
#speech_config.speech_synthesis_voice_name='en-US-AvaMultilingualNeural'
speech_config.speech_synthesis_voice_name='zh-CN-XiaoxiaoNeural'

# Create a speech synthesizer using the configured settings.
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

# Get text from the console and synthesize to the default speaker.
print("Enter some text that you want to speak >")
#text = input()
text = "Four score and seven years ago our fathers brought forth on this continent, a new nation, conceived in Liberty, and dedicated to the proposition that all men are created equal."

speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    print("Speech synthesized for text [{}]".format(text))
elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
    cancellation_details = speech_synthesis_result.cancellation_details
    print("Speech synthesis canceled: {}".format(cancellation_details.reason))
    if cancellation_details.reason == speechsdk.CancellationReason.Error:
        if cancellation_details.error_details:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and endpoint values?")