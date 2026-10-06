from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from google import genai
import asyncio

BOT_TOKEN = "BU_YERGA_TELEGRAM_TOKEN"
GEMINI_API_KEY = "BU_YERGA_GEMINI_API_KEY"

client = genai.Client(api_key=GEMINI_API_KEY)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salom! 🤖\n\n"
        "Men AI yordamchingizman.\n"
        "Istalgan savolingizni yozing."
    )


def ask_gemini(savol):
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=savol
    )
    return response.text


async def ai_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    savol = update.message.text

    await update.message.reply_text("⏳ O'ylayapman...")

    try:
        javob = await asyncio.to_thread(
            ask_gemini,
            savol
        )

        await update.message.reply_text(javob)

    except Exception as e:
        await update.message.reply_text(
            "❌ Xatolik yuz berdi:\n\n" + str(e)[:1000]
        )


app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        ai_answer
    )
)

print("🤖 AI BOT ISHLAYAPTI...")

app.run_polling()
