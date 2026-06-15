import os
import yfinance as yf
import requests

# 1. LINE Messaging APIの設定
# ⚠️ ご自身のアクセストークンに書き換えてください
LINE_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
URL = "https://api.line.me/v2/bot/message/broadcast"

# 2. チェックしたい銘柄のリスト
MY_STOCKS = {
    "285A.T": "キオクシア",
    "8035.T": "東エレクトロン",
    "ARM": "ARM",
    "NVDA": "NVIDIA"
}

# 送信するメッセージの「タイトル」をまず用意
message_text = "====== 📊 登録銘柄の株価一覧 ======\n"

# 3. 各銘柄のデータを取得して、メッセージ文字列を組み立てる
for ticker, name in MY_STOCKS.items():
    try:
        stock = yf.Ticker(ticker)
        history = stock.history(period="2d")
        
        if len(history) >= 2:
            close_today = history['Close'].iloc[-1]
            close_yesterday = history['Close'].iloc[-2]
            
            diff = close_today - close_yesterday
            diff_pct = (diff / close_yesterday) * 100
            
            icon = "📈" if diff >= 0 else "📉"
            
            # 文字列をどんどん後ろに追加していく(\n は改行コードです)
            message_text += f"{icon} {name} ({ticker})\n"
            message_text += f"   価格: {close_today:,.1f} | 前日比: {diff:+.1f} ({diff_pct:+.2f}%)\n\n"
        else:
            message_text += f"⚠️ {name}: データ不足\n\n"
            
    except Exception as e:
        message_text += f"❌ {name}: エラー({e})\n\n"

message_text += "======================================="

# 4. LINE Messaging APIの仕様に合わせてデータ（ペイロード）を作る
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {LINE_TOKEN}"
}

payload = {
    "messages": [
        {
            "type": "text",
            "text": message_text # 組み立てた株価テキストをここにセット！
        }
    ]
}

# 5. LINEサーバーへ送信
response = requests.post(URL, headers=headers, json=payload)

if response.status_code == 200:
    print("【成功】株価一覧をLINEに送信しました！")
else:
    print(f"【エラー】送信失敗（ステータスコード: {response.status_code}）")
    print(response.text)
