from flask import Flask, request, abort
import pandas as pd
import gspread
import requests

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('m7oF0Ii4/ufgqDT9V29TOBW1D5715GpgqEX8Ltia29qXY1OH5iLriTRo6IuNxG9q3zIqNjsofByRoWX2Sm9z7m6epPcanjbz4JJ+i75TCqEVff2jisPpnZllzRm6h9uuCY4q31ikDdjhnrtEVrZrSAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('cb15d13e97326a3349cb158e03846af1')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    token = 'AF5y90PW7vmJALond4SEGVBFwmt3Jhj7Ba7oclAeXL4'

    sa = gspread.service_account(filename='geprek-wani-c700b4b8002f.json')

    sheet = sa.open('Wani Spreadsheet')

    worksheet = sheet.worksheet('Pesanan')

    df = pd.DataFrame(worksheet.get_all_records())

    df.rename(columns={'Request cabe GEPREK': 'Cabe'}, inplace=True)

    df.head()

    # create a list containing 'Makanan Utama' and 'Nama'
    list = ['Makanan Utama', 'Cabe', 'Nama']

    # replace the empty string with 1
    df[list] = df[list].replace('', 1)

    df[list]

    # Custom geprek
    df_geprek = df[df['Makanan Utama'].str.contains('Geprek') & ~df['Makanan Utama'].str.contains('Indomie')]
    df_geprek

    # Dataframe non-geprek
    df_not_geprek = df[~df['Makanan Utama'].str.contains('Geprek')]

    # Dataframe geprek tanpa nasi
    df_geprek_tanpa_nasi = df_geprek[df_geprek['Makanan Utama'].str.contains('tanpa nasi')]

    # Dataframe geprek dengan nasi
    df_geprek_dengan_nasi = df_geprek[~df_geprek['Makanan Utama'].str.contains('tanpa nasi')]

    # Dataframe indomie geprek
    df_indomie_geprek = df[df['Makanan Utama'].str.contains('Indomie') & df['Makanan Utama'].str.contains('Geprek')]

    # Dataframe camilan
    df_camilan = df[['Camilan', 'Nama']]
    df_camilan = df_camilan[df_camilan['Camilan'] != '']

    # Dataframe minuman
    df_minuman = df[['Minuman', 'Nama']]
    df_minuman = df_minuman[df_minuman['Minuman'] != '']

    # Dataframe sambal
    df_sambal = df[['Sambal', 'Nama']]
    df_sambal = df_sambal[df_sambal['Sambal'] != '']

    combined_prints = []
    combined_prints.append(f"Pesanan Depot Wani: {pd.Timestamp.now()}")
    combined_prints.append("=====================================")
    combined_prints.extend([f"{sum(df_geprek_dengan_nasi['Cabe'] == i)} Nasi Ayam Geprek Cabe {i} ({', '.join(df_geprek_dengan_nasi[df_geprek_dengan_nasi['Cabe'] == i]['Nama'])})" for i in df_geprek_dengan_nasi['Cabe'].unique()])
    combined_prints.extend([f"{sum(df_geprek_tanpa_nasi['Cabe'] == i)} Ayam Geprek tanpa nasi Cabe {i} ({', '.join(df_geprek_tanpa_nasi[df_geprek_tanpa_nasi['Cabe'] == i]['Nama'])})" for i in df_geprek_tanpa_nasi['Cabe'].unique()])
    combined_prints.extend([f"{sum(df_not_geprek['Makanan Utama'] == i)} {i} ({', '.join(df_not_geprek[df_not_geprek['Makanan Utama'] == i]['Nama'])})" for i in df_not_geprek['Makanan Utama'].unique()])
    combined_prints.extend([f"{sum(df_indomie_geprek['Cabe'] == i)} {df_indomie_geprek[df_indomie_geprek['Cabe'] == i]['Makanan Utama'].iloc[0]} Cabe {i} ({', '.join(df_indomie_geprek[df_indomie_geprek['Cabe'] == i]['Nama'])})" for i in df_indomie_geprek['Cabe'].unique()])
    combined_prints.extend([f"{sum(df_camilan['Camilan'] == i)} {i} ({', '.join(df_camilan[df_camilan['Camilan'] == i]['Nama'])})" for i in df_camilan['Camilan'].unique()])
    combined_prints.extend([f"{sum(df_minuman['Minuman'] == i)} {i} ({', '.join(df_minuman[df_minuman['Minuman'] == i]['Nama'])})" for i in df_minuman['Minuman'].unique()])
    combined_prints.extend([f"{sum(df_sambal['Sambal'] == i)} {i} ({', '.join(df_sambal[df_sambal['Sambal'] == i]['Nama'])})" for i in df_sambal['Sambal'].unique()])

    print('\n'.join(combined_prints))

    # remove all text after '(' in combined_prints
    # combined_prints = [i.split('(')[0] for i in combined_prints]

    # print('\n'.join(combined_prints))

    # payload = {'message' : '\n'.join(combined_prints)}
    # r = requests.post('https://notify-api.line.me/api/notify'
    #                 , headers={'Authorization' : 'Bearer {}'.format(token)}
    #                 , params = payload)
    
    return 'Success'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
