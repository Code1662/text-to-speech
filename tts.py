#事前にpip install経由で以下のsoftware packageをインストールする必要はあります。
#pip install ibm-watson
import json
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

print('start')
# 認証情報
with open("auth.json",'r') as auth:
    auth_info = json.load(auth)
    apikey= auth_info['apikey']
    url=auth_info['url']
# 音声に変換したい文章
text='ちなみに、先ほど探していたのは、こちらの資料でしょう。'

# setup service
authenticator = IAMAuthenticator(apikey)
tts = TextToSpeechV1(authenticator=authenticator)
tts.set_service_url(url)

# 音声ファイル作成
with open('./audio.mp3', 'wb') as audio_file:
    res = tts.synthesize(text, accept='audio/mp3', voice='ja-JP_EmiV3Voice').get_result()
    audio_file.write(res.content)
