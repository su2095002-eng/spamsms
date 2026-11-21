CAI DAT VA CHAY BOT

1. Cai Python 3.12+.
2. Mo PowerShell tai thu muc nay.
3. Chay: py -m venv .venv
4. Chay: .\.venv\Scripts\Activate.ps1
5. Chay: pip install -r requirements.txt
6. Dat token:
   $env:TELEGRAM_BOT_TOKEN="TOKEN_MOI_CUA_BAN"
7. Chay: python bot.py

RAILWAY
1. Upload/push cac file nay len repository.
2. Them Variable TELEGRAM_BOT_TOKEN trong Railway.
3. Start command: python bot.py (hoac dung Procfile worker).
4. Chi chay mot instance polling.

Bao mat: Token cu da tung duoc gui trong chat. Hay revoke token cu qua @BotFather va chi dung token moi trong bien moi truong.
