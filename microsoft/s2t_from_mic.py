import os
import time
import re
import datetime
import azure.cognitiveservices.speech as speechsdk

speech_key, service_region = "087b5e1ed1494f77b1631627157d2b8a", "westus"
speech_config = speechsdk.SpeechConfig(
    subscription=speech_key, region=service_region)

def s2t_from_mic():
   #识别结果暂存于列表
    result = []

    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config)

    done = False

    def stop_cb(evt):
        print('CLOSING on {}'.format(evt))
        speech_recognizer.stop_continuous_recognition()
        nonlocal done
        done = True

    speech_recognizer.recognized.connect(
        lambda evt: result.append(re.search(r'"(.*?)"', str(evt)).group(1)))
    speech_recognizer.session_started.connect(
        lambda evt: print('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(
        lambda evt: print('SESSION STOPPED {}'.format(evt)))
    speech_recognizer.canceled.connect(
        lambda evt: print('CANCELED {}'.format(evt)))

    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    speech_recognizer.start_continuous_recognition()
    while not done:
        time.sleep(.5)

    # write output text file named by current date and time.
    with open('output/from_file_{}.txt'.format(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")), 'w') as f:
        for paragraph in result:
            f.write("%s\n" % paragraph)
    print("Transcribed successfully. Check the file in 'output' folder.")


s2t_from_mic(

)
