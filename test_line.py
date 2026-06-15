import requests

# LINE Messaging APIの設定
# ⚠️ 下の "" の中に、ステップ1でコピーした長いアクセストークンを貼り付けてください
LINE_TOKEN ="MY_ACCESS_TOKEN_HERE"
URL = "https://api.line.me/v2/bot/message/broadcast"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {LINE_TOKEN}"
}

# 送信するメッセージ内容
payload = {
    "messages": [
        {
            "type": "text",
            "text": "Hello World! Linuxからの送信に成功しました！"
        }
    ]
}

# LINEのサーバーへリクエストを送信
response = requests.post(URL, headers=headers, json=payload)

if response.status_code == 200:
    print("【成功】LINEにメッセージを送信しました！")
else:
    print(f"【エラー】送信失敗（ステータスコード: {response.status_code}）")
    print(response.text)
