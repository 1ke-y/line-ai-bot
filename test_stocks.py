import yfinance as yf

# 1. あなたがチェックしたい銘柄のリスト（日本株は末尾に .T が必要です）
MY_STOCKS = {
    "285A.T": "Kioxia",
    "8035.T": "TEL",
    "ARM": "ARM",
    "NVDA": "NVIDIA"
}

print("====== 📊 登録銘柄の最新株価一覧 ======")

# 2. 銘柄データを1つずつループ処理して取得
for ticker, name in MY_STOCKS.items():
    try:
        # yfinanceで株価情報を引っ張る
        stock = yf.Ticker(ticker)
        
        # 直近2日分のデータを取得（前日比を計算するため）
        history = stock.history(period="2d")
        
        if len(history) >= 2:
            close_today = history['Close'].iloc[-1]      # 本日の終値（または現在値）
            close_yesterday = history['Close'].iloc[-2]  # 前日の終値
            
            # 前日比（プラスマイナス）を計算
            diff = close_today - close_yesterday
            diff_pct = (diff / close_yesterday) * 100
            
            # 上がったか下がったかで絵文字を分ける
            icon = "📈" if diff >= 0 else "📉"
            
            # 綺麗に整形してターミナルに表示
            print(f"{icon} {name} ({ticker})")
            print(f"   価格: {close_today:,.1f} | 前日比: {diff:+.1f} ({diff_pct:+.2f}%)")
        else:
            print(f"⚠️ {name}: データが不足しています")
            
    except Exception as e:
        print(f"❌ {name} のデータ取得でエラーが発生しました: {e}")

print("=======================================")
