#导入 Microsoft Speech SDK
import re
import os
import time
import datetime
import azure.cognitiveservices.speech as speechsdk

#Azure订阅密钥和区域设置
speech_key, service_region = "087b5e1ed1494f77b1631627157d2b8a", "westus"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

#语音识别模块（现已支持超过15秒的音频）
def s2t_from_file(source_lang):
    #识别结果暂存于列表
    result = []

    speech_config.speech_recognition_language = source_lang
    audio_config = speechsdk.AudioConfig(filename=audio_filename)
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config)

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

#麦克风识别模块
def s2t_from_mic():
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    print("Speak now...")

    result = speech_recognizer.recognize_once()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(result.text))
        #创建输出目录
        output_dir = "output"
        try:
            os.makedirs(output_dir)
            print('Output Directory has been successfully created.')
        except FileExistsError:
            pass
        #写入文件
        with open('output/from_mic_{}.txt'.format(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")), 'w') as f:
            f.write(result.text)
            print("Transcribed successfully. Check the file in 'output' folder.")

    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(result.no_match_details))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech Recognition canceled: {}".format(
            cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(
                cancellation_details.error_details))

print('select the source of your speech.')
selection = int(input('1: from an audio file \n2: from microphone input\n'))
if selection == 1:
    #用户输入文件路径
    print("type the path of your audio file here...")
    time.sleep(.5)
    print("e.g. materials/lang/filename.wav")
    print("IMPORTANT: don't forget to put the file into the 'materials' folder first!")
    audio_filename = input()

    #用户输入识别源语言
    print("type the code of the source language of your file")
    time.sleep(.5)
    print("e.g. en-US, zh-CN")
    time.sleep(.5)
    print("refer to https://docs.microsoft.com/zh-cn/azure/cognitive-services/speech-service/language-support#speech-to-text for the code of language")
    s2t_from_file(input())  # en-US/GB zh-CN/HK/TW
elif selection == 2:
    s2t_from_mic()
else:
    print('wrong input.')


#创建输出文件夹
output_dir = "output"
try:
    os.makedirs(output_dir)
    print('Output Directory has been successfully created.')
except FileExistsError:
    pass
