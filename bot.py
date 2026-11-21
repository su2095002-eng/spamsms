import os
import re
import logging
from datetime import datetime, timezone

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)


def normalize_phone(raw: str) -> str | None:
    phone = re.sub(r"[\s().-]", "", raw)
    if phone.startswith("+84"):
        phone = "0" + phone[3:]
    elif phone.startswith("84") and len(phone) == 11:
        phone = "0" + phone[2:]
    return phone if re.fullmatch(r"0\d{9}", phone) else None


def mask_phone(phone: str) -> str:
    return phone[:3] + "****" + phone[-3:]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.effective_message.reply_text(
        "🤖 TELEGRAM BOT\n\n"
        "Các lệnh:\n"
        "/start - Mở bot\n"
        "/check - Kiểm tra trạng thái\n"
        "/test 0987654321 - Kiểm tra định dạng số\n"
        "/help - Hướng dẫn\n\n"
        "Bot hiện chỉ kiểm tra định dạng và mô phỏng; "
        "không gửi OTP hàng loạt hoặc gọi API của dịch vụ khác."
    )


async def check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    await update.effective_message.reply_text(
        f"✅ Bot đang hoạt động.\nThời gian UTC: {now}"
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
            "❌ Số chưa đúng định dạng Việt Nam.\n"
            "Ví dụ: /test 0987654321"
        )
        return

    user = update.effective_user
    logger.info(
        "Phone format checked | user_id=%s | phone=%s",
        user.id if user else "unknown",
        mask_phone(phone),
    )
    await update.effective_message.reply_text(
        "🧪 KIỂM TRA THÀNH CÔNG\n\n"
        f"Số điện thoại: {mask_phone(phone)}\n"
        "Định dạng: hợp lệ\n"
        "SMS/OTP thật: không gửi\n"
        "API bên thứ ba: không gọi"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await start(update, context)


def main() -> None:
    if not TOKEN:
        raise SystemExit(
            "Thiếu TELEGRAM_BOT_TOKEN. Hãy thêm biến này trong Railway Variables "
            "hoặc đặt biến môi trường trên máy tính."
        )

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check))
    app.add_handler(CommandHandler("test", test))
    app.add_handler(CommandHandler("help", help_command))

    logger.info("Telegram bot is starting")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
