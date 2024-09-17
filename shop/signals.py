import requests
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
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
                  f"Price: ${instance.price}\n"

        # Direct link to open the Mini App
        direct_link = f"https://t.me/StoreNowBot/mystore?startapp=product-{instance.id}"

        # Get the absolute URL for the image
        image_url = instance.image.url
        full_image_url = settings.SITE_URL + image_url  # Ensure SITE_URL is properly set in settings.py

        # URL to send the photo
        photo_url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto'

        # Prepare the photo data (use 'photo' field for the image URL)
        photo_data = {
            'chat_id': CHANNEL_ID,
            'caption': message,
            'photo': full_image_url,  # Send the image URL directly in 'photo'
            'parse_mode': 'HTML'  # Use HTML mode to format the message (optional)
        }

        # Send the HTTP POST request for the photo
        response = requests.post(photo_url, data=photo_data)

        # Check if the photo message is sent successfully
        if response.status_code == 200:
            # Send the inline keyboard as a follow-up message
            message_url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
            message_data = {
                'chat_id': CHANNEL_ID,
                'text': 'Click below to order now!',
                'parse_mode': 'HTML',
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
            # Send the HTTP POST request for the message
            requests.post(message_url, json=message_data)
        else:
            # Print the error if the request failed
            print(f"Error: {response.status_code} - {response.text}")
