import os
import re
import logging
from datetime import datetime, timezone

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

# Set TELEGRAM_BOT_TOKEN in your Windows environment before starting the bot.
TOKEN = os.getenv("9101710106:AAG4eVANxzSmb5afq5CDNE2OMjS1oNflVeo")

logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8",
)
logger = logging.getLogger(__name__)


def normalize_phone(raw: str) -> str | None:
    """Accept Vietnamese mobile numbers; this bot only validates/simulates."""
    phone = re.sub(r"[\s().-]", "", raw)
    if phone.startswith("+84"):
        phone = "0" + phone[3:]
    elif phone.startswith("84") and len(phone) == 11:
        phone = "0" + phone[2:]

    if re.fullmatch(r"0\d{9}", phone):
        return phone
    return None


def mask_phone(phone: str) -> str:
    return phone[:3] + "****" + phone[-3:]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = (
        "🤖 BOT KIỂM TRA OTP (CHẾ ĐỘ MÔ PHỎNG)\n\n"
        "Bot không gửi SMS/OTP thật và không gọi API của bên thứ ba.\n\n"
        "Lệnh sử dụng:\n"
        "/check – Kiểm tra bot hoạt động\n"
        "/test 0987654321 – Kiểm tra định dạng số và mô phỏng\n"
        "/help – Xem hướng dẫn"
    )
    await update.effective_message.reply_text(message)


async def check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.effective_message.reply_text(
        "✅ Bot đang hoạt động.\n"
        f"Thời gian UTC: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}"
    )


async def test(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.effective_message.reply_text(
            "Cách dùng: /test 0987654321"
        )
        return

    phone = normalize_phone(context.args[0])
    if not phone:
        await update.effective_message.reply_text(
            "❌ Số điện thoại chưa đúng định dạng Việt Nam.\n"
            "Ví dụ hợp lệ: /test 0987654321"
        )
        return

    user = update.effective_user
    user_id = user.id if user else "unknown"
    logger.info("SIMULATION user_id=%s phone=%s", user_id, mask_phone(phone))

    await update.effective_message.reply_text(
        "🧪 MÔ PHỎNG THÀNH CÔNG\n\n"
        f"Số kiểm tra: {mask_phone(phone)}\n"
        "Định dạng: hợp lệ\n"
        "Gửi SMS/OTP thật: KHÔNG\n"
        "API bên thứ ba: KHÔNG được gọi\n\n"
        "Đây chỉ là kiểm tra định dạng, không tạo hoặc gửi mã OTP."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await start(update, context)


async def post_init(application: Application) -> None:
    logger.info("Telegram simulation bot started")


def main() -> None:
    if not TOKEN:
        raise SystemExit(
            "Thiếu TELEGRAM_BOT_TOKEN. Hãy tạo bot bằng @BotFather, "
            "sau đó đặt biến môi trường TELEGRAM_BOT_TOKEN."
        )

    app = Application.builder().token(TOKEN).post_init(post_init).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check))
    app.add_handler(CommandHandler("test", test))
    app.add_handler(CommandHandler("help", help_command))

    print("Bot đang chạy. Nhấn Ctrl+C để dừng.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
