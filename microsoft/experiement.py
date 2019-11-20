# Import Microsoft Speech SDK and setup account key infomation

import azure.cognitiveservices.speech as speechsdk
import os

speech_key, service_region = "087b5e1ed1494f77b1631627157d2b8a", "westus"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

# Transcribe audio file to text and translate it into targeted language (Chinese as an example)
def translate_speech_to_text():
    translation_config = speechsdk.translation.SpeechTranslationConfig(subscription=speech_key, region=service_region)
    fromLanguage = 'en-US'
    toLanguage = 'yue'
    translation_config.speech_recognition_language = fromLanguage
    translation_config.add_target_language(toLanguage)

    speech_recognizer = speechsdk.translation.TranslationRecognizer(translation_config=translation_config, audio_config=audio_input)

    print("正在识别")
    result = speech_recognizer.recognize_once()

    # Checks result.
    if result.reason == speechsdk.ResultReason.TranslatedSpeech:
        print("识别结果 '{}': {}".format(fromLanguage, result.text))
        print("翻译结果 into {}: {}".format(toLanguage, result.translations['yue']))
    elif result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("识别结果: {} (文本未能翻译)".format(result.text))
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("NOMATCH: 语音文件无法识别: {}".format(
            result.no_match_details))
    elif result.reason == speechsdk.ResultReason.Canceled:
        print("CANCELED: Reason={}".format(result.cancellation_details.reason))
        if result.cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("CANCELED: ErrorDetails={}".format(
                result.cancellation_details.error_details))


# Open file from folder
audio_filename = "materials/Speech2Text-Material.wav"
audio_input = speechsdk.AudioConfig(filename=audio_filename)

translate_speech_to_text()
