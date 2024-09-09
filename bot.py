from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

# Initialize the bot with your token
bot_token = '7543719732:AAH8cIPr_xv9oaxtzw21EmnDd0LhJXVfCPs'


async def start(update, context: ContextTypes.DEFAULT_TYPE):
    product_id = 1  # Example product ID (this should be dynamic for each product)

    # Create the WebApp URL with the product_id as a query parameter
    webapp_url = f"https://apiorderbot.onrender.com/weapp/{product_id}/"

    # Create a button to launch the WebApp
    keyboard = [
        [InlineKeyboardButton("Order Now", web_app=WebAppInfo(url=webapp_url))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the message with the WebApp button
    await update.message.reply_text(
        text="Check out this amazing product! Click the button below to order.",
        reply_markup=reply_markup
    )


# Create the Application and add the command handler
application = Application.builder().token(bot_token).build()

application.add_handler(CommandHandler("start", start))

# Start the bot
application.run_polling()
