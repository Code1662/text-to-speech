#事前にpip install経由で以下のsoftware packageをインストールする必要はあります。
#もしCSVの代わりにExceファイルを使いたい場合は、openpyxlもpip経由でインストールしてください。
#pip install ibm-watson
#pip install pandas
#pip install inquirer
#pip install openpyxl
from ast import Or
from asyncio.windows_events import NULL
import json, pandas as pd
from tkinter import N
from threading import activeCount
import inquirer
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

print('start')
# 認証情報
with open("./auth.json",'r') as auth:
    auth_info = json.load(auth)
    apikey= auth_info['apikey']
    url=auth_info['url']

#setup service
authenticator = IAMAuthenticator(apikey)
tts = TextToSpeechV1(authenticator=authenticator)
tts.set_service_url(url)

#Text-to-speech向けのCSVファイルの読み取り
#もしExcelファイルを使いたい場合は、事前にPip install openpyxlをインストールし、
#以下の「pd.read_csv」を「pd.read_excel」に切り替えて、Excelファイルの保存先を入力してください。
TTS_Dataset = pd.read_excel("TTSConversionDataFile.xlsx", header= 'infer')
#データセットの最初の５行の確認（ヘッダー付き）
print(TTS_Dataset.head())

#データセットの行数の確認
df = TTS_Dataset
length =len(TTS_Dataset)
TextDataList = df.Text
JapaneseMeaning = df.JapaneseMeaning
print(length)

#発音の選択
#選択する前にこのURLをアクセスして試して見る事ができます。
# URL：　https://cloud.ibm.com/docs/text-to-speech?topic=text-to-speech-voices
#利用される音声のバージョンによって速度やピッチ（声の高さ・低さ）を調整出来ないものはありますのでご了承ください。(V3がつく音声）
#もし音声の選択機能を使いたいのであれば、７３列目の　voice= 'en-US_OliviaV3Voice'　を　voice= answers["Accent"]　に変更してください。
#選択オプションはご利用IDEのTerminalに表示されます。矢印キーを使って選択し、Enterキーで決定してください。
questions = [
  inquirer.List('Accent',
                message="どんな発音で聞きたいですか？矢印キーを使って選択してください。",
                choices=['en-GB_CharlotteV3Voice', 'en-GB_JamesV3Voice', 'en-GB_KateVoice', 'en-GB_KateV3Voice',
                'en-US_AllisonVoice', 'en-US_AllisonV3Voice', 'en-US_EmilyV3Voice', 'en-US_HenryV3Voice',
                'en-US_KevinV3Voice', 'en-US_LisaVoice', 'en-US_LisaV3Voice', 'en-US_MichaelVoice',
                'en-US_MichaelV3Voice', 'en-US_OliviaV3Voice'],
            )
]
answers = inquirer.prompt(questions)
print("選択された発音は"+ answers["Accent"] + "です。")

# 音声ファイル作成とデータ確認
for x in range(length):
    print(df.Text[x])
    print(df.JapaneseMeaning[x])
    if df.AudioFileName[x] == NULL  or not df.AudioFileName[x].endswith(('.mp3')):
        print('ERROR:出力するオーディオファイル名が記載されていないか、「.mp3」フォーマットがファイル名に入っていません')
        break
    elif df.JapaneseMeaningAudio[x] == NULL  or not df.JapaneseMeaningAudio[x].endswith(('.mp3')):
        print('ERROR:出力する日本語のオーディオファイル名が記載されていないか、「.mp3」フォーマットがファイル名に入っていません')
        break

    # 英語の音声ファイル作成
    with open(df.AudioFileName[x], 'wb') as audio_file: 
        res = tts.synthesize(df.Text[x], accept='audio/mp3', voice= 'en-US_OliviaV3Voice').get_result()
        audio_file.write(res.content)
              
    #日本語の意味を音声ファイルとしての作成
    with open(df.JapaneseMeaningAudio[x], 'wb') as audio_file2: 
        res = tts.synthesize(df.JapaneseMeaning[x], accept='audio/mp3', voice='ja-JP_EmiV3Voice').get_result()
        audio_file2.write(res.content)
        print('オーディオファイルはワーキングフォルダーに保存されています。')

#完成してファイルはユーザーの~/text-to-speech-main/フォルダーに保存されます。
print('end')
