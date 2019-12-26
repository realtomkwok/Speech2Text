import azure.cognitiveservices.speech as speechsdk
import time
import re
import os

speech_key, service_region = "087b5e1ed1494f77b1631627157d2b8a", "westus"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)


def s2t_continous(source_lang):
    result = []

    speech_config.speech_recognition_language = source_lang
    audio_config = speechsdk.AudioConfig(filename=audio_filename)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    
    done = False

    def stop_cb(evt):
        print('CLOSING on {}'.format(evt))
        speech_recognizer.stop_continuous_recognition()
        nonlocal done
        done = True
    
    speech_recognizer.recognized.connect(lambda evt: result.append(re.search(r'"(.*?)"', str(evt)).group(1)))
    speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
    
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    speech_recognizer.start_continuous_recognition()
    while not done:
        time.sleep(.5)
    
    # write output.txt
    with open('output/output.txt', 'w') as f:
        for paragraph in result:
            f.write("%s\n" % paragraph)
    print("Transcribed successfully. Check the file in 'output' folder.")

#朗读模块


audio_filename = "materials/audio/eng/short_version.wav"
s2t_continous('en-US')  # en-US/GB zh-CN/HK/TW

output_dir = "output"
try:
    os.makedirs(output_dir)
    print('Output Directory has been successfully created.')
except FileExistsError:
    pass


