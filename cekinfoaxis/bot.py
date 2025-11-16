import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# =============== YOUR TOKEN ===================
BOT_TOKEN = "8273797655:AAGFjB7px-1XprLNR_6QNUWuqIFW_qm2owM"
# ==============================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# ===================================================
# START COMMAND
# ===================================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.effective_user.first_name

    msg = (
        f"👋 Halo *{username}*!\n\n"
        "Selamat datang di *Axis Info Checker Bot*.\n"
        "Saya dapat membantu mengecek info kartu Axis secara lengkap.\n\n"
        "*Perintah yang tersedia:*\n"
        "• `/infoaxis 628xxxx` — cek detail kartu Axis\n"
        "• `/help` — bantuan\n\n"
        "Silakan pilih perintah dari menu atau ketik manual 😊"
    )

    await update.message.reply_text(msg, parse_mode="Markdown")


# ===================================================
# HELP COMMAND
# ===================================================
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "🆘 *Bantuan Bot*\n\n"
        "`/start` — mulai bot\n"
        "`/infoaxis 628xxxx` — cek info kartu Axis\n\n"
        "Pastikan nomor diawali *628* dan minimal 10 digit."
    )
    await update.message.reply_text(msg, parse_mode="Markdown")


# ===================================================
# INFOAXIS COMMAND
# ===================================================
async def infoaxis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if len(context.args) == 0:
            return await update.message.reply_text(
                "❌ Format salah!\nGunakan:\n`/infoaxis 628xxxx`",
                parse_mode="Markdown"
            )

        number = context.args[0].strip()

        if not number.startswith("628") or len(number) < 10:
            return await update.message.reply_text(
                "❌ Nomor tidak valid!\nHarus mulai dengan *628*.",
                parse_mode="Markdown"
            )

        await update.message.reply_text(
            f"⏳ Sedang memproses nomor `{number}`...",
            parse_mode="Markdown"
        )

        # CALL API
        url = f"https://alettarestapi.vestia.icu/alettaendpoint/cardinfo/axis?number={number}"
        response = requests.get(url)
        data = response.json()

        if not data.get("success"):
            return await update.message.reply_text(
                f"❌ Gagal mengambil data.\n{data.get('message', 'Unknown Error')}",
                parse_mode="Markdown"
            )

        d = data["data"]

        msg = (
            "📱 *AXIS CARD INFORMATION*\n"
            "--------------------------------\n"
            f"• *Nomor:* `{d.get('msisdn', 'N/A')}`\n"
            f"• *Provider:* `{d['prefix'].get('value','N/A')}`\n"
            f"• *Dukcapil:* `{d['dukcapil'].get('value','N/A')}`\n"
            f"• *4G:* `{d['status_4g'].get('value','N/A')}`\n"
            f"• *Masa Aktif:* `{d['active_card'].get('value','N/A')}`\n"
            f"• *Aktif Sampai:* `{d['active_period'].get('value','N/A')}`\n"
            f"• *Masa Tenggang:* `{d['grace_period'].get('value','N/A')}`\n\n"
            "📶 *VoLTE*\n"
            f"   • Device : `{ 'Yes' if d['volte']['value'].get('device') else 'No' }`\n"
            f"   • Area   : `{ 'Yes' if d['volte']['value'].get('area') else 'No' }`\n"
            f"   • SIM    : `{ 'Yes' if d['volte']['value'].get('simcard') else 'No' }`\n\n"
            "📦 *Kuota Aktif*\n"
            f"• `{ d['quotas']['value'] if d['quotas']['success'] else 'Tidak ada paket aktif' }`\n\n"
            "🛠 Developer: Purple | Iris"
        )

        await update.message.reply_text(msg, parse_mode="Markdown")

    except Exception as e:
        await update.message.reply_text(
            f"❌ Error internal: `{str(e)}`",
            parse_mode="Markdown"
        )


# ===================================================
# BOT MAIN
# ===================================================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("infoaxis", infoaxis))

    print("BOT RUNNING…")
    app.run_polling()


if __name__ == "__main__":
    main()
