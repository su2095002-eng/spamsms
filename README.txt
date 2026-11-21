BOT TELEGRAM KIỂM TRA OTP - CHẾ ĐỘ MÔ PHỎNG

1. Cài Python 3.10 trở lên.
2. Mở PowerShell tại thư mục chứa bot.py.
3. Cài thư viện:
   py -m pip install -r requirements.txt

4. Tạo bot Telegram:
   - Mở Telegram, tìm @BotFather.
   - Gửi /newbot và làm theo hướng dẫn.
   - Sao chép token BotFather cấp.

5. Đặt token trong PowerShell (thay TOKEN_CUA_BAN bằng token thật):
   $env:TELEGRAM_BOT_TOKEN="TOKEN_CUA_BAN"

6. Chạy:
   py bot.py

7. Mở bot Telegram và gửi:
   /start
   /check
   /test 0987654321

LƯU Ý:
- Bot chỉ kiểm tra định dạng số và mô phỏng.
- Không gửi SMS/OTP thật, không gọi các API từ spamsms1_1.py.
- Không chia sẻ token BotFather cho người khác.
- Dừng bot bằng Ctrl+C.
