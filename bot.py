from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Updater, CommandHandler, CallbackContext, Update

# Initialize the bot with your token
bot_token = '7543719732:AAH8cIPr_xv9oaxtzw21EmnDd0LhJXVfCPs'
updater = Updater(token=bot_token, use_context=True)
bot = updater.bot


def start(update: Update, context: CallbackContext):
    product_id = 1  # Example product ID (this should be dynamic for each product)

    # Create the WebApp URL with the product_id as a query parameter
    webapp_url = f"https://apiorderbot.onrender.com/weapp/{product_id}/"

    # Create a button to launch the WebApp
    keyboard = [
        [InlineKeyboardButton("Order Now", web_app=WebAppInfo(url=webapp_url))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the message with the WebApp button
    update.message.reply_text(
        text="Check out this amazing product! Click the button below to order.",
        reply_markup=reply_markup
    )


# Command handler to post the product
updater.dispatcher.add_handler(CommandHandler('start', start))

# Start the bot
updater.start_polling()
updater.idle()
