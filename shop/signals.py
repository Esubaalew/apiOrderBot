import requests
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product
from django.conf import settings

# Your bot token and channel ID
BOT_TOKEN = '7543719732:AAH8cIPr_xv9oaxtzw21EmnDd0LhJXVfCPs'
CHANNEL_ID = '-1002437698028'


@receiver(post_save, sender=Product)
def send_product_to_channel(sender, instance, created, **kwargs):
    URL = settings.SITE_URL
    if created:
        # Image URL
        image_url = URL + instance.image.url

        # Caption to be sent with the phot
        caption = (
            f"<b>{instance.name}</b>\n\n"  # Product name in bold
            f"<i>{instance.description}</i>\n\n"  # Product description in italic
            f"ðŸ’² <b>Price:</b> {instance.price}\n"  # Add an emoji before price and make the label bold
        )

        # Direct link to open the Mini App
        direct_link = f"https://t.me/StoreNowBot/mystore?startapp=product-{instance.id}"

        # URL for sending the photo with a caption
        url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto'

        # Data to be sent in the HTTP POST request
        data = {
            'chat_id': CHANNEL_ID,
            'photo': image_url,
            'caption': caption,
            'parse_mode': 'HTML',  # Using HTML mode for formatting
            'reply_markup': {
                'inline_keyboard': [
                    [
                        {
                            'text': 'Order Now',
                            'url': direct_link  # Link to the product mini app
                        }
                    ]
                ]
            }
        }

        # Send the HTTP POST request
        response = requests.post(url, json=data)

        # Print the response from Telegram for debugging
        print(response.json())
