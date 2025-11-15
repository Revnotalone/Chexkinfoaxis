import os
import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

# ==========================
# TOKEN FROM RENDER ENV VAR
# ==========================
BOT_TOKEN = os.getenv("BOT_TOKEN")


# ==========================
#  /start COMMAND
# ==========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name

    msg = (
        f"👋 Halo *{user}*!\n\n"
        "Selamat datang di *Axis Checker Bot*.\n"
        "Saya bisa mengecek informasi kartu Axis dengan lengkap.\n\n"
        "📝 *Perintah yang tersedia:*\n"
        "• `/infoaxis 628xxxxxx` — cek kartu Axis\n"
        "• `/help` — lihat bantuan\n\n"
        "Silakan pilih command dari menu atau ketik manual."
    )

    await update.message.reply_text(msg, parse_mode="Markdown")


# ==========================
#  /help COMMAND
# ==========================
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "🆘 *Bantuan Bot*\n\n"
        "`/start` — mulai bot\n"
        "`/infoaxis 628xxxxxx` — cek informasi kartu Axis\n\n"
        "Pastikan nomor formatnya benar, mulai dengan *628*."
    )
    await update.message.reply_text(msg, parse_mode="Markdown")


# ==========================
#  /infoaxis COMMAND
# ==========================
async def infoaxis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # CEK PARAMETER
        if len(context.args) == 0:
            return await update.message.reply_text(
                "❌ Format salah!\nGunakan: `/infoaxis 628xxxxxx`",
                parse_mode="Markdown"
            )

        number = context.args[0].strip()

        # VALIDASI NOMOR
        if not number.startswith("628") or len(number) < 10:
            return await update.message.reply_text(
                "❌ Nomor tidak valid!\nHarus mulai dengan *628* dan minimal 10 digit.",
                parse_mode="Markdown"
            )

        await update.message.reply_text(
            f"⏳ Sedang memproses nomor `{number}`...",
            parse_mode="Markdown"
        )

        # API REQUEST
        url = f"https://alettarestapi.vestia.icu/alettaendpoint/cardinfo/axis?number={number}"
        response = requests.get(url)
        data = response.json()

        # HANDLE GAGAL
        if not data.get("success"):
            return await update.message.reply_text(
                f"❌ Gagal mengambil data.\n{data.get('message','Unknown Error')}",
                parse_mode="Markdown"
            )

        d = data["data"]

        # FORMAT PESAN
        msg = (
            "📱 *AXIS CARD INFORMATION*\n"
            "--------------------------------\n"
            f"• *Nomor:* `{d.get('msisdn','N/A')}`\n"
            f"• *Provider:* `{d['prefix'].get('value','N/A')}`\n"
            f"• *Dukcapil:* `{d['dukcapil'].get('value','N/A')}`\n"
            f"• *Status 4G:* `{d['status_4g'].get('value','N/A')}`\n"
            f"• *Masa Aktif:* `{d['active_card'].get('value','N/A')}`\n"
            f"• *Aktif Sampai:* `{d['active_period'].get('value','N/A')}`\n"
            f"• *Masa Tenggang:* `{d['grace_period'].get('value','N/A')}`\n\n"

            "📶 *VoLTE Status*\n"
            f"   • Device: `{ 'Yes' if d['volte']['value'].get('device') else 'No' }`\n"
            f"   • Area: `{ 'Yes' if d['volte']['value'].get('area') else 'No' }`\n"
            f"   • SIM: `{ 'Yes' if d['volte']['value'].get('simcard') else 'No' }`\n\n"

            "📦 *Paket Data*\n"
            f"• `{ d['quotas']['value'] if d['quotas']['success'] else 'Tidak ada paket aktif' }`\n\n"

            "🛠 Developer: Purple | Iris"
        )

        await update.message.reply_text(msg, parse_mode="Markdown")

    except Exception as e:
        await update.message.reply_text(
            f"❌ Error internal: `{str(e)}`",
            parse_mode="Markdown"
        )


# ==========================
#  MAIN BOT
# ==========================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("infoaxis", infoaxis))

    print("BOT RUNNING ON RENDER 🔥")
    app.run_polling()


if __name__ == "__main__":
    main()