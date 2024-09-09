from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Updater, CommandHandler

# Initialize the bot with your token
bot_token = 'YOUR_TELEGRAM_BOT_TOKEN'
bot = Bot(token=bot_token)


def post_product(update, context):
    product_id = 1  # Example product ID (this should be dynamic for each product)

    # Create the WebApp URL with the product_id as a query parameter
    webapp_url = f"https://yourdomain.com/api/webapp/?product_id={product_id}"

    # Create a button to launch the WebApp
    keyboard = [
        [InlineKeyboardButton("Order Now", web_app=WebAppInfo(url=webapp_url))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the message with the WebApp button
    bot.send_message(
        chat_id='YOUR_CHANNEL_ID',
        text="Check out this amazing product! Click the button below to order.",
        reply_markup=reply_markup
    )


# Command handler to post the product
updater = Updater(token=bot_token, use_context=True)
updater.dispatcher.add_handler(CommandHandler('post_product', post_product))

# Start the bot
updater.start_polling()
updater.idle()
