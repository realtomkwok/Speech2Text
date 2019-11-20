# 使用 Experienment.py

##测试环境

* 操作系统：macOS 10.14.6
* Python 版本：Python 3.6.0 64-bit

## 使用准备

### 安装所需包

**微软 Speech SDK**

* 安装代码： `pip3 install --upgrade azure-cognitiveservices-speech `
* 用途：语音识别、文本转录与文本翻译。

**FFmpeg**

* 安装代码：`pip3 install ffmpy3`
* 用途：将视频转换成识别所需的`.wav`文件。

### 科学上网

由于使用了服务器位置于美西地区的国际版 Microsoft Azure 服务，需要进行科学上网才可正常使用。

**❓为何选择国际版 Microsoft Azure？**

由于国内版 Microsoft Azure 试用期仅为一个月，且需预付费，成本较高；而国际版 Microsoft Azure 提供学生使用优惠，免费试用12个月，相比较成本较低。唯一缺点是需要科学上网。

### 其他注意事项

* 请不要改动 `speech_key, service_region` 这两个变量。这两个变量是 Azure 与程序验证的密钥与服务器地区设置。