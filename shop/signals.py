# your_app/signals.py

import requests
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product

# Your bot token and channel ID
BOT_TOKEN = '7543719732:AAH8cIPr_xv9oaxtzw21EmnDd0LhJXVfCPs'
CHANNEL_ID = '-1002437698028'

@receiver(post_save, sender=Product)
def send_product_to_channel(sender, instance, created, **kwargs):
    if created:
        # Prepare the message with the product details
        message = f"New Product Added!\n\n" \
                  f"Name: {instance.name}\n" \
                  f"Description: {instance.description}\n" \
                  f"Price: ${instance.price}\n" \
                  f"Image: {instance.image}\n"

        # Direct link to open the Mini App
        direct_link = f"https://t.me/StoreNowBot/mystore?startapp=product-{instance.id}"

        # URL to send the message
        url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'

        # Data to be sent in the HTTP POST request
        data = {
            'chat_id': CHANNEL_ID,
            'text': message,
            'parse_mode': 'HTML',  # Use HTML mode to format the message (optional)
            'reply_markup': {
                'inline_keyboard': [
                    [
                        {
                            'text': 'Order Now',
                            'url': direct_link
                        }
                    ]
                ]
            }
        }

        # Send the HTTP POST request
        response = requests.post(url, json=data)

        # Print the response (optional)
        print(response.json())
